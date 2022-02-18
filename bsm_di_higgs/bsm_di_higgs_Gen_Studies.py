from __future__ import print_function
from optparse import OptionParser
from math import *
import os
import sys

usage = "Usage: %prog [options] input_file.root\n"
parser = OptionParser(usage=usage)

parser.add_option("-m" ,"--massDirectories",action="store_true", dest="massDir", default=False,
    help="directories of all different mass points")
parser.add_option("-o","--outDir",dest="outDir",default= False,
    help = "path to output directory for plots. If a relative path is given the path is interpreted relative to 'path'")

parser.add_option("--maxevents", action="store", dest="maxevents", help="maximum number of events to loop over", default="10000")

(opts, args) = parser.parse_args()

# # manage parser options
# if not os.path.isabs(opts.massDir):
#     opts.massDir = os.path.abspath(opts.massDir)
# if not os.path.exists(opts.massDir):
#     sys.exit("input directory {} does not exist".format(opts.massDir))


outpath=opts.outDir
for n in range(50):
    if not os.path.exists(outpath):
        os.makedirs(outpath+"/")
        print ("made dir: ", outpath)
        break
    else:
        outpath = outpath + "_{}".format(n)

import ROOT
from DataFormats.FWLite import Events, Handle
import Utilities.General.cmssw_das_client as das_client

ROOT.gStyle.SetOptStat(0)

def FindAllMothers(particle):
    mother_ids = []
    # print ("particle id ", particle.pdgId())
    # print ("# mothers ", particle.numberOfMothers())
    for i in range(particle.numberOfMothers()):
        # print ("mother id ", particle.mother(i).pdgId())
        mother_ids.append(particle.mother(i).pdgId())
        next_mothers_ids = FindAllMothers(particle.mother(i))
        for next_mother_id in next_mothers_ids:
            mother_ids.append(next_mother_id)
    return mother_ids

# find a mother
def FindSpecificMothers(mothers, truemother):
    for potentialmother in mothers:
        if int(potentialmother) == int(truemother):
            # print(truemother," found")
            return True
    return False
    
def find_masses(dataset_name):
    index_2 = dataset_name.find("_h2_M")
    #print(index_1,index_2)
    number_1 = ""
    number_2 = ""
    for char in dataset_name[1:]:
        #print(char)
        if not char.isdigit(): break
        number_1+=char
    for char in dataset_name[index_2+5:]:
        #print(char)
        if not char.isdigit(): break
        number_2+=char
    # print("MH="+number_1+" Mh="+number_2)
    return number_1,number_2

max_events = int(opts.maxevents)

infos = [] 
for (dirpath, dirnames, filenames) in os.walk(args[0]):
    for dir in dirnames:
        files=[]
        for (subdirpath, subdirnames, subfilenames) in os.walk(args[0]+"/"+dir):
            for fil in subfilenames:
                if fil.find(".root") >= 0:
                    files.append(fil)
            infos.append([args[0]+dir+"/",find_masses(dir),files]) #save array with directory to trees, masses and trees

# # 2D and 3D Histogramms over all mass points
# dr_median_hsm_h_MH = ROOT.TH3F("Median_DeltaR_b_q_qbar_Top_Pt","",20,0,2000,20,0,6)
# dr_median_hsm_h_MH.GetXaxis().SetTitle("Median #Delta R(h_{SM}h)")
# dr_median_hsm_h_MH.GetYaxis().SetTitle("Heavy Higgs Mass")
# dr_median_hsm_h_MH.GetZaxis().SetTitle("Arbitrary units")

# dr_max_b_q_qbar_top_pt = ROOT.TH2F("Max_DeltaR_b_q_qbar_Top_Pt","",20,0,2000,20,0,6)
# dr_max_b_q_qbar_top_pt.GetXaxis().SetTitle("Top Quark/Antiquark p_{T}[GeV]")
# dr_max_b_q_qbar_top_pt.GetYaxis().SetTitle("Maximum #Delta R(b/#bar{b},q,#bar{q'})")
# dr_max_b_q_qbar_top_pt.GetZaxis().SetTitle("Arbitrary units")

for masspoints in infos:
    directoryName = masspoints[0]
    mH = masspoints[1][0]
    mh = masspoints[1][1]
    fullfilelist = masspoints[2]

    reducedfilelist = []
    n_events = 0 
    for file in fullfilelist:
        if n_events < max_events:
            reducedfilelist.append(str(file))
            root_file=ROOT.TFile.Open(directoryName+file,"READ")
            n_events+=root_file.Get("Events").GetEntries()
            root_file.Close()
        else:
            break
    print("")
    print("Heavy higgs mass: "+ mH +", light higgs mass: "+mh)
    print("list of used files: ", reducedfilelist)
    print("number of events: ", n_events)

    # product labels and handles
    handlePruned = Handle("std::vector<reco::GenParticle>")
    handlePacked = Handle("std::vector<pat::PackedGenParticle>")
    eventinfo = Handle("GenEventInfoProduct")
    #lheinfo = Handle("LHEEventProduct")
    labelPruned = "prunedGenParticles"
    labelPacked = "packedGenParticles"
    labelWeight = "generator"
    #labelLHE = "externalLHEProducer"

    # Histogramms for each seperate mass point
    heavyHiggs_pt = ROOT.TH1F("HeavyHiggs_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,20,0,2000)
    heavyHiggs_pt.GetXaxis().SetTitle("Heavy Higgs p_{T}[GeV]")

    lightHiggs_pt = ROOT.TH1F("LightHiggs_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,20,0,2000)
    lightHiggs_pt.GetXaxis().SetTitle("Light Higgs p_{T}[GeV]")

    smHiggs_pt = ROOT.TH1F("SMHiggs_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,20,0,2000)
    smHiggs_pt.GetXaxis().SetTitle("SM Higgs p_{T}[GeV]")

    antitau_pt = ROOT.TH1F("antitau_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,20,0,2000)
    antitau_pt.GetXaxis().SetTitle("antitau p_{T}[GeV]")

    tau_pt = ROOT.TH1F("tau_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,20,0,2000)
    tau_pt.GetXaxis().SetTitle("Tau p_{T}[GeV]")

    antibquark_pt =ROOT.TH1F("antibquark_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,20,0,2000)
    antibquark_pt.GetXaxis().SetTitle("Anti Bottom Quark  p_{T}[GeV]")

    bquark_pt =ROOT.TH1F("bquark_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,20,0,2000)
    bquark_pt.GetXaxis().SetTitle("Bottom Quark p_{T}[GeV]")

    higgs_dR =ROOT.TH1F("higgs_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,20,0,6)
    higgs_dR.GetXaxis().SetTitle("#Delta R(h_{SM}h)")

    tau_dR =ROOT.TH1F("tau_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,20,0,6)
    tau_dR.GetXaxis().SetTitle("#Delta R(tau tau)")

    bquark_dR =ROOT.TH1F("bquark_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,20,0,6)
    bquark_dR.GetXaxis().SetTitle("#Delta R(b/#bar{b})")

    count = 0
    # loop over files
    for filename in reducedfilelist:
        # loop over events in file
        events = Events(directoryName+filename)
        for event in events:
            count += 1
            # if count ==2:
            #     break
            if count % 1000 == 0:
                print (count)
            event.getByLabel(labelPruned, handlePruned)
            event.getByLabel(labelWeight, eventinfo)
            #event.getByLabel(labelLHE, lheinfo)
            # get the products (prunedGenParticles collection, GenEventInfoProduct and LHEEventProduct)
            pruned = handlePruned.product()
            weight = eventinfo.product().weight()
            #lhe_weight = lheinfo.product().originalXWGTUP()
            
            everything_found = False
            bottom_p4=None
            antibottom_p4=None
            tau_p4=None
            antitau_p4=None
            HeavyHiggs_p4=None
            SMHiggs_p4=None
            LightHiggs_p4=None 

            bottom_found=False
            antibottom_found=False
            tau_found=False
            antitau_found=False
            HeavyHiggs_found=False
            SMHiggs_found=False
            LightHiggs_found=False

            bottom_id = 5
            antibottom_id = -5
            tau_id = 15
            antitau_id = -15
            HeavyHiggs_id = 45
            SMHiggs_id = 25
            LightHiggs_id = 35
            
            mothers = []
            for p in pruned:
                #print (p.pdgId())
                if everything_found: break
                mothers = FindAllMothers(p)
                if p.pdgId()==bottom_id and p.isLastCopy() and FindSpecificMothers(mothers, LightHiggs_id):
                    bottom_found = True
                    bottom_p4 = p.p4()
                if p.pdgId()==antibottom_id and p.isLastCopy() and FindSpecificMothers(mothers, LightHiggs_id):
                    antibottom_found = True
                    antibottom_p4 = p.p4()
                if p.pdgId()==tau_id and p.isLastCopy() and FindSpecificMothers(mothers, SMHiggs_id):
                    tau_found = True
                    tau_p4 = p.p4()
                if p.pdgId()==antitau_id and p.isLastCopy() and FindSpecificMothers(mothers, SMHiggs_id):
                    antitau_found = True
                    antitau_p4 = p.p4()
                if abs(p.pdgId())==SMHiggs_id and p.isLastCopy() and FindSpecificMothers(mothers, HeavyHiggs_id):
                    SMHiggs_found = True
                    SMHiggs_p4 = p.p4()
                if abs(p.pdgId())==LightHiggs_id and p.isLastCopy() and FindSpecificMothers(mothers, HeavyHiggs_id):
                    LightHiggs_found = True
                    LightHiggs_p4 = p.p4()
                if abs(p.pdgId())==HeavyHiggs_id and p.isLastCopy():
                    HeavyHiggs_found = True
                    HeavyHiggs_p4 = p.p4()
                # print("b:", bottom_found, "ab:", antibottom_found, "t:", tau_found,"at:", antitau_found,"HH:", HeavyHiggs_found,"SMH:", SMHiggs_found,"LH:", LightHiggs_found) 
                everything_found = bottom_found and antibottom_found and tau_found and antitau_found and HeavyHiggs_found and SMHiggs_found and LightHiggs_found

            if everything_found:
                bquark_pt.Fill(bottom_p4.pt(),weight)
                antibquark_pt.Fill(antibottom_p4.pt(),weight)
                Tau_pt.Fill(tau_p4.pt(),weight)
                antiTau_pt.Fill(antitau_p4.pt(),weight)
                heavyHiggs_pt.Fill(HeavyHiggs_p4.pt(),weight)
                lightHiggs_pt.Fill(LightHiggs_p4.pt(),weight)
                smHiggs_pt.Fill(SMHiggs_p4.pt(),weight)
            
                dR_b_b = sqrt(ROOT.Math.VectorUtil.DeltaR2(bottom_p4, antibottom_p4))
                bquark_dR.Fill(dR_b_b,weight)
                dR_tau_tau = sqrt(ROOT.Math.VectorUtil.DeltaR2(tau_p4, antitau_p4))
                tau_dR.Fill(dR_tau_tau,weight)
                dR_hsm_h = sqrt(ROOT.Math.VectorUtil.DeltaR2(SMHiggs_p4, LightHiggs_p4))
                higgs_dR.Fill(dR_hsm_h,weight)
            else:
                continue

    bquark_pt.Scale(1./bquark_pt.Integral())
    antibquark_pt.Scale(1./antibquark_pt.Integral())
    tau_pt.Scale(1./tau_pt.Integral())
    antitau_pt.Scale(1./antitau_pt.Integral())
    heavyHiggs_pt.Scale(1./heavyHiggs_pt.Integral())
    lightHiggs_pt.Scale(1./lightHiggs_pt.Integral())
    smHiggs_pt.Scale(1./smHiggs_pt.Integral())
    higgs_dR.Scale(1./higgs_dR.Integral())
    tau_dR.Scale(1./tau_dR.Integral())
    bquark_dR.Scale(1./bquark_dR.Integral())

    output_file = ROOT.TFile.Open(outpath+"/"+"GenStudies_"+"MH_"+mH+"_Mh_"+mh+".root","RECREATE")
    output_file.WriteTObject(bquark_pt)
    output_file.WriteTObject(antibquark_pt)
    output_file.WriteTObject(tau_pt)
    output_file.WriteTObject(antitau_pt)
    output_file.WriteTObject(heavyHiggs_pt)
    output_file.WriteTObject(lightHiggs_pt)
    output_file.WriteTObject(smHiggs_pt)
    output_file.WriteTObject(higgs_dR)
    output_file.WriteTObject(tau_dR)
    output_file.WriteTObject(bquark_dR)
    output_file.Close()
