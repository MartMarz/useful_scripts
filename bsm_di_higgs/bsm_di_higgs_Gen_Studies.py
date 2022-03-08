from __future__ import print_function
from optparse import OptionParser
from math import *
import os
import sys
import numpy as np

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
        outpath = opts.outDir + "_{}".format(n)

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

def Scale3DHisto(histname,nxbins,nybins,nzbins):
    for x in range(1,nxbins+1):
        for y in range(1,nybins+1):
            integral=0
            for z in range(1,nzbins+1):
                integral+= histname.GetBinContent(x,y,z)
            for newz in range(1,nzbins+1):
                if integral !=0:
                    histname.SetBinContent(x,y,newz,(histname.GetBinContent(x,y,newz)/integral))

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

HHedges =np.array([200.])
LHedges = np.array([35.])
HHbins = 0
LHbins = 0
for masses in infos:
    mH = float(masses[1][0])+1.
    mh = float(masses[1][1])+1.

    HHalreadysafed=False
    for safedHH in HHedges:
        if mH==safedHH:
            HHalreadysafed=True
            break

    LHalreadysafed=False
    for safedLH in LHedges:
        if mh==safedLH:
            LHalreadysafed=True
            break
    
    if not HHalreadysafed:
        HHedges=np.append(HHedges, mH)
        HHbins+=1
    if not LHalreadysafed:
        LHedges=np.append(LHedges, mh)
        LHbins+=1
        
dRbins=100
dRmax=6
dRedges=np.array([0.])
for n in range(1, dRbins+1):
    dRedges=np.append(dRedges, n*(float(dRmax)/float(dRbins)))

pTbins=100
pTmax=2000
pTedges=np.array([0.])
for n in range(1, pTbins+1):
    pTedges = np.append(pTedges, n*(float(pTmax)/float(pTbins)))


HHedges=np.sort(HHedges)
LHedges=np.sort(LHedges)
print(HHedges, HHbins, LHedges, LHbins, dRedges, dRbins, pTedges, pTbins)

# 3D Histogramms over all mass points
drbb_mh_MH = ROOT.TH3F("DeltaR_b_bbar","#Delta R(b/#bar{b})",LHbins,LHedges,HHbins,HHedges,dRbins,dRedges)
drbb_mh_MH.GetYaxis().SetTitle("m_{H} (GeV)")
drbb_mh_MH.GetXaxis().SetTitle("m_{h_{S}} (GeV)")
drbb_mh_MH.GetZaxis().SetTitle("#Delta R(b/#bar{b})")
# drbb_mh_MH.GetWaxis().SetTitle("Arbitrary units")

drtt_mh_MH = ROOT.TH3F("DeltaR_tau_tau","#Delta R(tau tau)",LHbins,LHedges,HHbins,HHedges,dRbins,dRedges)
drtt_mh_MH.GetYaxis().SetTitle("m_{H} (GeV)")
drtt_mh_MH.GetXaxis().SetTitle("m_{h_{S}} (GeV)")
drtt_mh_MH.GetZaxis().SetTitle("#Delta R(tau tau)")
# drbb_mh_MH.GetWaxis().SetTitle("Arbitrary units")

drhh_mh_MH = ROOT.TH3F("DeltaR_h_hSM","#Delta R(h_{S}h)",LHbins,LHedges,HHbins,HHedges,dRbins,dRedges)
drhh_mh_MH.GetYaxis().SetTitle("m_{H} (GeV)")
drhh_mh_MH.GetXaxis().SetTitle("m_{h_{S}} (GeV)")
drhh_mh_MH.GetZaxis().SetTitle("#Delta R(h_{SM}h)")
# drbb_mh_MH.GetWaxis().SetTitle("Arbitrary units")

ptHH_mh_MH = ROOT.TH3F("HeavyHiggs_pt","Heavy Higgs p_{T}",LHbins,LHedges,HHbins,HHedges,pTbins,pTedges)
ptHH_mh_MH.GetYaxis().SetTitle("m_{H} (GeV)")
ptHH_mh_MH.GetXaxis().SetTitle("m_{h_{S}} (GeV)")
ptHH_mh_MH.GetZaxis().SetTitle("H p_{T}(GeV)")
# drbb_mh_MH.GetWaxis().SetTitle("Arbitrary units")

ptLH_mh_MH = ROOT.TH3F("LightHiggs_pt","Light Higgs p_{T}",LHbins,LHedges,HHbins,HHedges,pTbins,pTedges)
ptLH_mh_MH.GetYaxis().SetTitle("m_{H} (GeV)")
ptLH_mh_MH.GetXaxis().SetTitle("m_{h_{S}} (GeV)")
ptLH_mh_MH.GetZaxis().SetTitle("h_{S} p_{T}(GeV)")
# drbb_mh_MH.GetWaxis().SetTitle("Arbitrary units")

ptSMH_mh_MH = ROOT.TH3F("SMHiggs_pt","SM Higgs p_{T}",LHbins,LHedges,HHbins,HHedges,pTbins,pTedges)
ptSMH_mh_MH.GetYaxis().SetTitle("m_{H} (GeV)")
ptSMH_mh_MH.GetXaxis().SetTitle("m_{h_{S}} (GeV)")
ptSMH_mh_MH.GetZaxis().SetTitle("h p_{T}(GeV)")
# drbb_mh_MH.GetWaxis().SetTitle("Arbitrary units")

masspointcounter=0
for masspoints in infos:

    # if masspointcounter==7:
    #     break
    # masspointcounter+=1

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
    print("m_H: "+ mH +", m_h_S: "+mh)
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
    heavyHiggs_pt = ROOT.TH1F("HeavyHiggs_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,pTbins,0,2000)
    heavyHiggs_pt.GetXaxis().SetTitle("H p_{T}(GeV)")

    lightHiggs_pt = ROOT.TH1F("LightHiggs_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,pTbins,0,2000)
    lightHiggs_pt.GetXaxis().SetTitle("h_{S} p_{T}(GeV)")

    smHiggs_pt = ROOT.TH1F("SMHiggs_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,pTbins,0,2000)
    smHiggs_pt.GetXaxis().SetTitle("h p_{T}(GeV)")

    # antitau_pt = ROOT.TH1F("antitau_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,pTbins,0,2000)
    # antitau_pt.GetXaxis().SetTitle("Anti Tau p_{T}(GeV)")

    tau_pt = ROOT.TH1F("tau_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,pTbins,0,2000)
    tau_pt.GetXaxis().SetTitle("tau p_{T}(GeV)")

    # antibquark_pt =ROOT.TH1F("antibquark_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,pTbins,0,2000)
    # antibquark_pt.GetXaxis().SetTitle("Anti Bottom Quark p_{T}(GeV)")

    bquark_pt =ROOT.TH1F("bquark_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,pTbins,0,2000)
    bquark_pt.GetXaxis().SetTitle("b p_{T}(GeV)")

    higgs_dR =ROOT.TH1F("higgs_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,0,6)
    higgs_dR.GetXaxis().SetTitle("#Delta R(h_{S}h)")

    tau_dR =ROOT.TH1F("tau_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,0,6)
    tau_dR.GetXaxis().SetTitle("#Delta R(tau tau)")

    bquark_dR =ROOT.TH1F("bquark_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,0,6)
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
                bquark_pt.Fill(antibottom_p4.pt(),weight)
                # antibquark_pt.Fill(antibottom_p4.pt(),weight)
                tau_pt.Fill(tau_p4.pt(),weight)
                tau_pt.Fill(antitau_p4.pt(),weight)
                # antitau_pt.Fill(antitau_p4.pt(),weight)
                heavyHiggs_pt.Fill(HeavyHiggs_p4.pt(),weight)
                lightHiggs_pt.Fill(LightHiggs_p4.pt(),weight)
                smHiggs_pt.Fill(SMHiggs_p4.pt(),weight)
            
                dR_b_b = sqrt(ROOT.Math.VectorUtil.DeltaR2(bottom_p4, antibottom_p4))
                bquark_dR.Fill(dR_b_b,weight)
                dR_tau_tau = sqrt(ROOT.Math.VectorUtil.DeltaR2(tau_p4, antitau_p4))
                tau_dR.Fill(dR_tau_tau,weight)
                dR_hsm_h = sqrt(ROOT.Math.VectorUtil.DeltaR2(SMHiggs_p4, LightHiggs_p4))
                higgs_dR.Fill(dR_hsm_h,weight)

                drbb_mh_MH.Fill(int(mh),int(mH),dR_b_b,weight)
                drtt_mh_MH.Fill(int(mh),int(mH),dR_tau_tau,weight)
                drhh_mh_MH.Fill(int(mh),int(mH),dR_hsm_h,weight)
                ptHH_mh_MH.Fill(int(mh),int(mH),HeavyHiggs_p4.pt(),weight)
                ptLH_mh_MH.Fill(int(mh),int(mH),LightHiggs_p4.pt(),weight)
                ptSMH_mh_MH.Fill(int(mh),int(mH),SMHiggs_p4.pt(),weight)
            else:
                continue

    bquark_pt.Scale(1./bquark_pt.Integral())
    # antibquark_pt.Scale(1./antibquark_pt.Integral())
    tau_pt.Scale(1./tau_pt.Integral())
    # antitau_pt.Scale(1./antitau_pt.Integral())
    heavyHiggs_pt.Scale(1./heavyHiggs_pt.Integral())
    lightHiggs_pt.Scale(1./lightHiggs_pt.Integral())
    smHiggs_pt.Scale(1./smHiggs_pt.Integral())
    higgs_dR.Scale(1./higgs_dR.Integral())
    tau_dR.Scale(1./tau_dR.Integral())
    bquark_dR.Scale(1./bquark_dR.Integral())

    output_file = ROOT.TFile.Open(outpath+"/"+"GenStudies_"+"MH_"+mH+"_Mh_"+mh+".root","RECREATE")
    output_file.WriteTObject(bquark_pt)
    # output_file.WriteTObject(antibquark_pt)
    output_file.WriteTObject(tau_pt)
    # output_file.WriteTObject(antitau_pt)
    output_file.WriteTObject(heavyHiggs_pt)
    output_file.WriteTObject(lightHiggs_pt)
    output_file.WriteTObject(smHiggs_pt)
    output_file.WriteTObject(higgs_dR)
    output_file.WriteTObject(tau_dR)
    output_file.WriteTObject(bquark_dR)
    output_file.Close()

Scale3DHisto(drbb_mh_MH,LHbins,HHbins,dRbins)
Scale3DHisto(drtt_mh_MH,LHbins,HHbins,dRbins)  
Scale3DHisto(drhh_mh_MH,LHbins,HHbins,dRbins)  
Scale3DHisto(ptHH_mh_MH,LHbins,HHbins,pTbins)  
Scale3DHisto(ptLH_mh_MH,LHbins,HHbins,pTbins)  
Scale3DHisto(ptSMH_mh_MH,LHbins,HHbins,pTbins)        
output_file = ROOT.TFile.Open(outpath+"/"+"GenStudies_"+"3D_histo.root","RECREATE")
output_file.WriteTObject(drbb_mh_MH)
output_file.WriteTObject(drtt_mh_MH)
output_file.WriteTObject(drhh_mh_MH)
output_file.WriteTObject(ptHH_mh_MH)
output_file.WriteTObject(ptLH_mh_MH)
output_file.WriteTObject(ptSMH_mh_MH)
output_file.Close()

