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

def FindAllDaughters(particle):
    daughter_ids = []
    # print ("particle id ", particle.pdgId())
    # print ("# mothers ", particle.numberOfMothers())
    for i in range(particle.numberOfDaughters()):
        # print ("mother id ", particle.mother(i).pdgId())
        daughter_ids.append(particle.daughter(i).pdgId())
        next_daughter_ids = FindAllDaughters(particle.daughter(i))
        for next_daughter_id in next_daughter_ids:
            daughter_ids.append(next_daughter_id)
    return daughter_ids

def FindNextDaughters(particle):
    daughter_ids = []
    # print ("particle id ", particle.pdgId())
    # print ("# mothers ", particle.numberOfMothers())
    for i in range(particle.numberOfDaughters()):
        # print ("mother id ", particle.mother(i).pdgId())
        daughter_ids.append(particle.daughter(i).pdgId())
    return daughter_ids

# find a mother
def FindSpecificParticle(mothers, truemother):
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

prematch_RECO_fullhad = ROOT.TH1F("prematch_fullhad_dR","prematch_fullhad_dR",dRbins,0,6)
prematch_RECO_fullhad.GetXaxis().SetTitle("#Delta R(tau tau)")
prematch_RECO_semimu = ROOT.TH1F("prematch_semimu_dR","prematch_semimu_dR",dRbins,0,6)
prematch_RECO_semimu.GetXaxis().SetTitle("#Delta R(tau mu)")
prematch_RECO_semiele = ROOT.TH1F("prematch_semiele_dR","prematch_semiele_dR",dRbins,0,6)
prematch_RECO_semiele.GetXaxis().SetTitle("#Delta R(tau e)")
prematch_RECO_bs = ROOT.TH1F("prematch_b_dR","prematch_b_dR",dRbins,0,6)
prematch_RECO_bs.GetXaxis().SetTitle("#Delta R(bb)")

postmatch_RECO_fullhad = ROOT.TH1F("postmatch_fullhad_dR","postmatch_fullhad_dR",dRbins,0,6)
postmatch_RECO_fullhad.GetXaxis().SetTitle("#Delta R(tau tau)")
postmatch_RECO_semimu = ROOT.TH1F("postmatch_semimu_dR","postmatch_semimu_dR",dRbins,0,6)
postmatch_RECO_semimu.GetXaxis().SetTitle("#Delta R(tau mu)")
postmatch_RECO_semiele = ROOT.TH1F("postmatch_semiele_dR","postmatch_semiele_dR",dRbins,0,6)
postmatch_RECO_semiele.GetXaxis().SetTitle("#Delta R(tau e)")
postmatch_RECO_bs = ROOT.TH1F("postmatch_b_dR","postmatch_b_dR",dRbins,0,6)
postmatch_RECO_bs.GetXaxis().SetTitle("#Delta R(bb)")

prematch_RECO_tau = ROOT.TH1F("prematch_tau_dR","prematch_tau_dR",dRbins,0,6)
prematch_RECO_tau.GetXaxis().SetTitle("#Delta R(tau tau)")
postmatch_RECO_tau = ROOT.TH1F("postmatch_tau_dR","postmatch_tau_dR",dRbins,0,6)
postmatch_RECO_tau.GetXaxis().SetTitle("#Delta R(tau tau)")
prematch_RECO_jet = ROOT.TH1F("prematch_jet_dR","prematch_jet_dR",dRbins,0,6)
prematch_RECO_jet.GetXaxis().SetTitle("#Delta R(bb)")
postmatch_RECO_jet = ROOT.TH1F("postmatch_jet_dR","postmatch_jet_dR",dRbins,0,6)
postmatch_RECO_jet.GetXaxis().SetTitle("#Delta R(bb)")

precuts_RECO_jet = ROOT.TH1F("precuts_jet_dR","precuts_jet_dR",dRbins,0,6)
precuts_RECO_jet.GetXaxis().SetTitle("#Delta R(bb)")
precuts_RECO_tau = ROOT.TH1F("precuts_tau_dR","precuts_tau_dR",dRbins,0,6)
precuts_RECO_tau.GetXaxis().SetTitle("#Delta R(tau tau)")


masspointcounter=0
for masspoints in infos:

    # if masspointcounter==3:
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
    handleJets = Handle("std::vector<pat::Jet>")
    handleTaus = Handle("std::vector<pat::Tau>")
    handleMuons = Handle("std::vector<pat::Muon>")
    handleElectrons = Handle("std::vector<pat::Electron>")
    handleFat = Handle("std::vector<pat::Jet>")
    eventinfo = Handle("GenEventInfoProduct")
    #lheinfo = Handle("LHEEventProduct")
    labelJets = "slimmedJets"
    labelTaus = "slimmedTaus"
    labelElectrons = "slimmedElectrons"
    labelMuons = "slimmedMuons"
    labelPruned = "prunedGenParticles"
    labelPacked = "packedGenParticles"
    labelWeight = "generator"
    labelFat = "slimmedJetsAK8"
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
    tau_pt.GetXaxis().SetTitle("vis tau p_{T}(GeV)")

    # antibquark_pt =ROOT.TH1F("antibquark_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,pTbins,0,2000)
    # antibquark_pt.GetXaxis().SetTitle("Anti Bottom Quark p_{T}(GeV)")

    bquark_pt =ROOT.TH1F("bquark_pt"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,pTbins,0,2000)
    bquark_pt.GetXaxis().SetTitle("b p_{T}(GeV)")

    higgs_dR =ROOT.TH1F("higgs_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,0,6)
    higgs_dR.GetXaxis().SetTitle("#Delta R(h_{S}h)")

    tau_dR =ROOT.TH1F("tau_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,0,6)
    tau_dR.GetXaxis().SetTitle("#Delta R(vistau vistau)")

    bquark_dR =ROOT.TH1F("bquark_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,0,6)
    bquark_dR.GetXaxis().SetTitle("#Delta R(b/#bar{b})")

    bquark_eta =ROOT.TH1F("bquark_eta"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,-3,3)
    bquark_eta.GetXaxis().SetTitle("b eta")
    tau_eta =ROOT.TH1F("tau_eta"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,-3,3)
    tau_eta.GetXaxis().SetTitle("vis tau eta")
    HH_eta =ROOT.TH1F("HeavyHiggs_eta"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,-3,3)
    HH_eta.GetXaxis().SetTitle("H eta")
    LH_eta =ROOT.TH1F("LightHiggs_eta"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,-3,3)
    LH_eta.GetXaxis().SetTitle("h_{S} eta")
    SM_eta =ROOT.TH1F("SMHiggs_eta"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,-3,3)
    SM_eta.GetXaxis().SetTitle("h eta")

    #counter
    b_cut_counter = ROOT.TH1F("b_cut_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    b_cut_counter.GetXaxis().SetTitle("N_{bcuts}")

    had_tau_cut_counter = ROOT.TH1F("had_tau_cut_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    had_tau_cut_counter.GetXaxis().SetTitle("N_{hadtcuts}")
    had_found_counter = ROOT.TH1F("had_found_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    had_found_counter.GetXaxis().SetTitle("N_{hadfound}")

    semiele_tau_cut_counter = ROOT.TH1F("semiele_tau_cut_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    semiele_tau_cut_counter.GetXaxis().SetTitle("N_{semieletcuts}")
    semiele_found_counter = ROOT.TH1F("semiele_found_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    semiele_found_counter.GetXaxis().SetTitle("N_{semielefound}")

    semimu_tau_cut_counter = ROOT.TH1F("semimu_tau_cut_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    semimu_tau_cut_counter.GetXaxis().SetTitle("N_{semimutcuts}")
    semimu_found_counter = ROOT.TH1F("semimu_found_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    semimu_found_counter.GetXaxis().SetTitle("N_{semimufound}")

    fulllep_found_counter = ROOT.TH1F("fulllep_found_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    fulllep_found_counter.GetXaxis().SetTitle("N_{fulllepfound}")

    found_counter = ROOT.TH1F("found_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    found_counter.GetXaxis().SetTitle("N_{found}")

    event_counter = ROOT.TH1F("event_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    event_counter.GetXaxis().SetTitle("N_{event}")

    combined_tau_cut_counter = ROOT.TH1F("combined_tau_cut_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    combined_tau_cut_counter.GetXaxis().SetTitle("N_{combinedtaucut}")

    combined_cut_counter = ROOT.TH1F("combined_cut_counter"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,2,0,2)
    combined_cut_counter.GetXaxis().SetTitle("N_{combinedcut}")

    # Reco_Tau_dR = ROOT.TH1F("Reco_tau_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,0,6)
    # Reco_Tau_dR.GetXaxis().SetTitle("#Delta R(vistau recotau)")

    # Reco_Mu_dR = ROOT.TH1F("Reco_mu_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,0,6)
    # Reco_Mu_dR.GetXaxis().SetTitle("#Delta R(vistau recomu)")

    # Reco_Ele_dR = ROOT.TH1F("Reco_ele_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,0,6)
    # Reco_Ele_dR.GetXaxis().SetTitle("#Delta R(vistau recoele)")

    # Reco_Bottom_dR = ROOT.TH1F("Reco_b_dR"+"_MH_"+mH+"_mh_"+mh,"Di Higgs M_{H}="+mH+" m_{h}="+mh,dRbins,0,6)
    # Reco_Bottom_dR.GetXaxis().SetTitle("#Delta R(b recojet)")

    count = 0
    # loop over files
    for filename in reducedfilelist:
        # loop over events in file
        events = Events(directoryName+filename)
        # if count >= 1:
        #     break
        for event in events:
            # print("run:", event.eventAuxiliary().run(),"lumi: ",event.eventAuxiliary().luminosityBlock(),"eventID: " ,event.eventAuxiliary().event())
            count += 1
            # if count % 100 == 0:
            #     print (count)
            if count % 1000 == 0:
                print (count)
            # if count == 1000:
            #     break
            
            event.getByLabel(labelJets, handleJets)
            event.getByLabel(labelTaus, handleTaus)
            event.getByLabel(labelMuons, handleMuons)
            event.getByLabel(labelElectrons, handleElectrons)
            event.getByLabel(labelPruned, handlePruned)
            event.getByLabel(labelFat, handleFat)
            event.getByLabel(labelWeight, eventinfo)
            #event.getByLabel(labelLHE, lheinfo)
            # get the products (prunedGenParticles collection, GenEventInfoProduct and LHEEventProduct)
            pruned = handlePruned.product()
            weight = eventinfo.product().weight()
            Jets = handleJets.product()
            Taus = handleTaus.product()
            Muons = handleMuons.product()
            Fats = handleFat.product()
            Electrons = handleElectrons.product()
            #lhe_weight = lheinfo.product().originalXWGTUP()

            #DeepTau vs jets name = by[WP]DeepTau2017v2p1VSjet; WP=VVVLoose,VVLoose,VLoose,Loose,Medium,Tight,VTight,VVTight
            #DeepTau vs e name = by[WP]DeepTau2017v2p1VSe; WP=VVVLoose,VVLoose,VLoose,Loose,Medium,Tight,VTight,VVTight
            #DeepTau vs mu name = by[WP]DeepTau2017v2p1VSmu; WP=VLoose,Loose,Medium,Tight
            #function = tau.tauID(name)
            # for tau in Taus:
            #     print(tau.tauID("byVVVLooseDeepTau2017v2p1VSjet"))
            # for jet in Jets:
            #     if count==1:
            #         print(jet.getPairDiscri())
            
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
            
            cuts_appl=True
            bottom_cut=False
            antibottom_cut=False
            tau_cut=False
            antitau_cut=False

            fullhad_tau_cut_val=40.
            ele_tau_cut_val=33.
            mu_tau_cut_val=25.
            semihad_tau_cut_val=30.

            fullhad_tau_eta_val=2.1
            ele_tau_eta_val=2.1
            mu_tau_eta_val=2.1
            semihad_tau_eta_val=2.3

            b_cut_val=20.
            b_eta_val=2.5

            HeavyHiggs_id = 45
            SMHiggs_id = 25
            LightHiggs_id = 35

            bottom_id = 5
            antibottom_id = -5

            ele_id=11
            antiele_id=-11
            ele_neut_id=12
            antiele_neut_id=-12
            mu_id=13
            antimu_id=-13
            mu_neut_id=14
            antimu_neut_id=-14
            tau_id = 15
            antitau_id = -15
            tau_neut_id=16
            antitau_neut_id=-16
            
            mothers = []
            nextdaughters = []
            tau_decay_mode = None
            antitau_decay_mode = None
            event_decay = None

            #find all particles in event
            for p in pruned:
                #print (p.pdgId())
                if everything_found: break
                mothers = FindAllMothers(p)
                if p.pdgId()==bottom_id and p.isLastCopy() and FindSpecificParticle(mothers, LightHiggs_id):
                    bottom_found = True
                    bottom_p4 = p.p4()
                    if bottom_p4.pt() > b_cut_val and abs(bottom_p4.eta()) <= b_eta_val:
                        bottom_cut = True
                if p.pdgId()==antibottom_id and p.isLastCopy() and FindSpecificParticle(mothers, LightHiggs_id):
                    antibottom_found = True
                    antibottom_p4 = p.p4()
                    if antibottom_p4.pt() > b_cut_val and abs(antibottom_p4.eta()) <= b_eta_val:
                        antibottom_cut = True

                if p.pdgId()==tau_id and p.isLastCopy() and FindSpecificParticle(mothers, SMHiggs_id):
                    tau_found = True
                    tau_p4 = p.p4()
                    nextdaughters = FindNextDaughters(p)

                    #identifie decay mode
                    for daughter in nextdaughters:
                        if abs(daughter) == ele_id:
                            tau_decay_mode = "Ele"
                        elif abs(daughter) == mu_id:
                            tau_decay_mode = "Mu"
                    if tau_decay_mode == None:
                        tau_decay_mode = "Had"

                if p.pdgId()==antitau_id and p.isLastCopy() and FindSpecificParticle(mothers, SMHiggs_id):
                    antitau_found = True
                    antitau_p4 = p.p4()
                    nextdaughters = FindNextDaughters(p)

                    #identifie decay mode
                    for daughter in nextdaughters:
                        if abs(daughter) == ele_id:
                            antitau_decay_mode = "Ele"
                        elif abs(daughter) == mu_id:
                            antitau_decay_mode = "Mu"
                    if antitau_decay_mode == None:
                        antitau_decay_mode = "Had"


                if abs(p.pdgId())==SMHiggs_id and p.isLastCopy() and FindSpecificParticle(mothers, HeavyHiggs_id):
                    SMHiggs_found = True
                    SMHiggs_p4 = p.p4()
                if abs(p.pdgId())==LightHiggs_id and p.isLastCopy() and FindSpecificParticle(mothers, HeavyHiggs_id):
                    LightHiggs_found = True
                    LightHiggs_p4 = p.p4()
                if abs(p.pdgId())==HeavyHiggs_id and p.isLastCopy():
                    HeavyHiggs_found = True
                    HeavyHiggs_p4 = p.p4()
                # print("b:", bottom_found, "ab:", antibottom_found, "t:", tau_found,"at:", antitau_found,"HH:", HeavyHiggs_found,"SMH:", SMHiggs_found,"LH:", LightHiggs_found) 
                everything_found = bottom_found and antibottom_found and tau_found and antitau_found and HeavyHiggs_found and SMHiggs_found and LightHiggs_found
            
            event_counter.Fill(1)
            #calculate visable tau pT
            if everything_found:
                vis_tau_p4 = tau_p4
                vis_antitau_p4 = antitau_p4
                for p in pruned:
                    mothers = FindAllMothers(p)
                    if (abs(p.pdgId())==tau_neut_id or abs(p.pdgId())==ele_neut_id or abs(p.pdgId())==mu_neut_id) and p.isLastCopy() and FindSpecificParticle(mothers, tau_id):
                        vis_tau_p4 = vis_tau_p4 - p.p4()
                    if (abs(p.pdgId())==tau_neut_id or abs(p.pdgId())==ele_neut_id or abs(p.pdgId())==mu_neut_id) and p.isLastCopy() and FindSpecificParticle(mothers, antitau_id):
                        vis_antitau_p4 = vis_antitau_p4 - p.p4()

                #check tau cuts
                if tau_decay_mode == "Had" and antitau_decay_mode == "Had":
                    event_decay = "fullhad"
                    if vis_tau_p4.pt() > fullhad_tau_cut_val and vis_antitau_p4.pt() > fullhad_tau_cut_val and abs(vis_tau_p4.eta()) <= fullhad_tau_eta_val and abs(vis_antitau_p4.eta()) <= fullhad_tau_eta_val:
                        tau_cut = True
                        antitau_cut = True
                elif (tau_decay_mode == "Had" and antitau_decay_mode == "Mu"):
                    event_decay = "semimu"
                    if vis_tau_p4.pt() > semihad_tau_cut_val and abs(vis_tau_p4.eta()) <= semihad_tau_eta_val and vis_antitau_p4.pt() > mu_tau_cut_val and abs(vis_antitau_p4.eta()) <= mu_tau_eta_val:
                        tau_cut = True
                        antitau_cut = True
                elif (tau_decay_mode == "Mu" and antitau_decay_mode == "Had"):
                    event_decay = "semimu"
                    if vis_tau_p4.pt() > mu_tau_cut_val and abs(vis_tau_p4.eta()) <= mu_tau_eta_val and vis_antitau_p4.pt() > semihad_tau_cut_val and abs(vis_antitau_p4.eta()) <= semihad_tau_eta_val:
                        tau_cut = True
                        antitau_cut = True
                elif (tau_decay_mode == "Had" and antitau_decay_mode == "Ele"):
                    event_decay = "semiele"
                    if vis_tau_p4.pt() > semihad_tau_cut_val and abs(vis_tau_p4.eta()) <= semihad_tau_eta_val and vis_antitau_p4.pt() > ele_tau_cut_val and abs(vis_antitau_p4.eta()) <= ele_tau_eta_val:
                        tau_cut = True
                        antitau_cut = True
                elif (tau_decay_mode == "Ele" and antitau_decay_mode == "Had"):
                    event_decay = "semiele"
                    if vis_tau_p4.pt() > ele_tau_cut_val and abs(vis_tau_p4.eta()) <= ele_tau_eta_val and vis_antitau_p4.pt() > semihad_tau_cut_val and abs(vis_antitau_p4.eta()) <= semihad_tau_eta_val:
                        tau_cut = True
                        antitau_cut = True
                else:
                    event_decay = "fulllep"
                
                #fill number of events Gen Level
                found_counter.Fill(1)
                if tau_cut and antitau_cut:
                    combined_tau_cut_counter.Fill(1)
                if event_decay == "fullhad":
                    had_found_counter.Fill(1)
                    if tau_cut and antitau_cut:
                        had_tau_cut_counter.Fill(1)
                elif event_decay == "semimu":
                    semimu_found_counter.Fill(1)
                    if tau_cut and antitau_cut:
                        semimu_tau_cut_counter.Fill(1)
                elif event_decay == "semiele":
                    semiele_found_counter.Fill(1)
                    if tau_cut and antitau_cut:
                        semiele_tau_cut_counter.Fill(1)
                elif event_decay == "fulllep":
                    fulllep_found_counter.Fill(1)

                if bottom_cut and antibottom_cut:
                    b_cut_counter.Fill(1)

                if tau_cut and antitau_cut and bottom_cut and antibottom_cut:
                    combined_cut_counter.Fill(1)

                #Reco counter and matching
                RecoFlag_tau_number = False
                RecoFlag_jet_number = False
                RecoFlag_dR = False
                RecoFlag_dis = False

                Reco_tau_dR_err = 0.1
                Reco_mu_dR_err = 0.04
                Reco_ele_dR_err = 0.04
                Reco_jet_dR_err = 0.1

                nMu=0
                for muons in Muons:
                    if muons.p4().pt() > mu_tau_cut_val and abs(muons.p4().eta()) <= mu_tau_eta_val:
                        nMu+=1
                nEle=0
                for ele in Electrons:
                    if ele.p4().pt() > ele_tau_cut_val and abs(ele.p4().eta()) <= ele_tau_eta_val:
                        nEle+=1
                nJet=0
                for jets in Jets:
                    if jets.p4().pt() > b_cut_val and abs(jets.p4().eta()) <= b_eta_val:
                        nJet+=1

                if event_decay == "fullhad":
                    tau_cut_val = fullhad_tau_cut_val
                    tau_eta_val = fullhad_tau_eta_val
                elif event_decay == "semimu" or event_decay == "semiele":
                    tau_cut_val = semihad_tau_cut_val
                    tau_eta_val = semihad_tau_eta_val

                nTau=0
                tauindexlist=[]
                for taus in Taus:
                    if taus.p4().pt() > tau_cut_val and abs(taus.p4().eta()) <= tau_eta_val:
                        nTau+=1

                # decay categorization
                if event_decay == "fullhad":
                    RecoTaus_dR=[]
                    RecoAntiTaus_dR=[]
                    if nTau>=2:
                        RecoFlag_tau_number = True
                        index=0
                        for taus in Taus:
                            if taus.p4().pt() > tau_cut_val and abs(taus.p4().eta()) <= tau_eta_val:
                                RecoTaus_dR_val=(sqrt(ROOT.Math.VectorUtil.DeltaR2(taus.p4(), vis_tau_p4)))
                                RecoAntiTaus_dR_val=(sqrt(ROOT.Math.VectorUtil.DeltaR2(taus.p4(), vis_antitau_p4)))
                                RecoTaus_dR.append([RecoTaus_dR_val,index])
                                RecoAntiTaus_dR.append([RecoAntiTaus_dR_val,index])
                                index+=1
                        RecoTaus_dR.sort(key=lambda RecoTaus_dR:RecoTaus_dR[0])
                        RecoAntiTaus_dR.sort(key=lambda RecoAntiTaus_dR:RecoAntiTaus_dR[0])
                        #distinct taus for both particles
                        if RecoAntiTaus_dR[0][1] == RecoTaus_dR[0][1]:
                            if RecoAntiTaus_dR[0][0] < RecoTaus_dR[0][0]:
                                tauindex = 1
                                antitauindex = 0
                            elif RecoAntiTaus_dR[0][0] > RecoTaus_dR[0][0]:
                                tauindex = 0
                                antitauindex = 1
                            elif RecoAntiTaus_dR[0][0] == RecoTaus_dR[0][0]:
                                if RecoAntiTaus_dR[1][0] < RecoTaus_dR[1][0]:
                                    antitauindex = 1
                                    tauindex = 0
                                elif RecoAntiTaus_dR[1][0] > RecoTaus_dR[1][0]:
                                    antitauindex = 0
                                    tauindex = 1
                                elif RecoAntiTaus_dR[1][0] == RecoTaus_dR[1][0]:
                                    antitauindex = 0
                                    tauindex = 1
                        else:       
                            tauindex = 0 
                            antitauindex = 0

                if event_decay == "semimu":
                    RecoTaus_dR=[]
                    RecoMuon_dR=[]
                    #number check
                    if nTau>=1 and nMu>=1:
                        RecoFlag_tau_number = True
                        #match dR
                        if tau_decay_mode == "Had" and antitau_decay_mode == "Mu":
                            for taus in Taus:
                                if taus.p4().pt() > tau_cut_val and abs(taus.p4().eta()) <= tau_eta_val:
                                    RecoTaus_dR.append(sqrt(ROOT.Math.VectorUtil.DeltaR2(taus.p4(), vis_tau_p4)))
                            for muons in Muons:
                                if muons.p4().pt() > mu_tau_cut_val and abs(muons.p4().eta()) <= mu_tau_eta_val:
                                    RecoMuon_dR.append(sqrt(ROOT.Math.VectorUtil.DeltaR2(muons.p4(), vis_antitau_p4)))
                            RecoTaus_dR.sort()
                            RecoMuon_dR.sort()
                        elif tau_decay_mode == "Mu" and antitau_decay_mode == "Had":
                            for taus in Taus:
                                if taus.p4().pt() > tau_cut_val and abs(taus.p4().eta()) <= tau_eta_val:
                                    RecoTaus_dR.append(sqrt(ROOT.Math.VectorUtil.DeltaR2(taus.p4(), vis_antitau_p4)))
                            for muons in Muons:
                                if muons.p4().pt() > mu_tau_cut_val and abs(muons.p4().eta()) <= mu_tau_eta_val:
                                    RecoMuon_dR.append(sqrt(ROOT.Math.VectorUtil.DeltaR2(muons.p4(), vis_tau_p4)))
                            RecoTaus_dR.sort()
                            RecoMuon_dR.sort()

                elif event_decay == "semiele":
                    RecoTaus_dR=[]
                    RecoEle_dR=[]
                    #number check
                    if nTau>=1 and nEle>=1:
                        RecoFlag_tau_number = True
                        #match dR
                        if tau_decay_mode == "Had" and antitau_decay_mode == "Ele":
                            for taus in Taus:
                                if taus.p4().pt() > tau_cut_val and abs(taus.p4().eta()) <= tau_eta_val:
                                    RecoTaus_dR.append(sqrt(ROOT.Math.VectorUtil.DeltaR2(taus.p4(), vis_tau_p4)))
                            for ele in Electrons:
                                if ele.p4().pt() > ele_tau_cut_val and abs(ele.p4().eta()) <= ele_tau_eta_val:
                                    RecoEle_dR.append(sqrt(ROOT.Math.VectorUtil.DeltaR2(ele.p4(), vis_antitau_p4)))
                            RecoTaus_dR.sort()
                            RecoEle_dR.sort()
                        elif tau_decay_mode == "Ele" and antitau_decay_mode == "Had":
                            for taus in Taus:
                                if taus.p4().pt() > tau_cut_val and abs(taus.p4().eta()) <= tau_eta_val:
                                    RecoTaus_dR.append(sqrt(ROOT.Math.VectorUtil.DeltaR2(taus.p4(), vis_antitau_p4)))
                            for ele in Electrons:
                                if ele.p4().pt() > ele_tau_cut_val and abs(ele.p4().eta()) <= ele_tau_eta_val:
                                    RecoEle_dR.append(sqrt(ROOT.Math.VectorUtil.DeltaR2(ele.p4(), vis_tau_p4)))
                            RecoTaus_dR.sort()
                            RecoEle_dR.sort()
                    
                if nJet >= 2:
                    RecoBottom_dR=[]
                    RecoAntibottom_dR=[]
                    RecoFlag_jet_number = True
                    index=0
                    for jets in Jets:
                        if jets.p4().pt() > b_cut_val and abs(jets.p4().eta()) <= b_eta_val:
                            RecoBottom_dR_val=(sqrt(ROOT.Math.VectorUtil.DeltaR2(jets.p4(), bottom_p4)))
                            RecoAntibottom_dR_val=(sqrt(ROOT.Math.VectorUtil.DeltaR2(jets.p4(), antibottom_p4)))
                            RecoBottom_dR.append([RecoBottom_dR_val,index])
                            RecoAntibottom_dR.append([RecoAntibottom_dR_val,index])
                            index+=1
                    RecoBottom_dR.sort(key=lambda RecoBottom_dR:RecoBottom_dR[0])
                    RecoAntibottom_dR.sort(key=lambda RecoAntibottom_dR:RecoAntibottom_dR[0])
                    #distinct bs for both particles
                    if RecoAntibottom_dR[0][1] == RecoBottom_dR[0][1]:
                        if RecoAntibottom_dR[0][0] < RecoBottom_dR[0][0]:
                            bindex = 1
                            antibindex = 0
                        elif RecoAntibottom_dR[0][0] > RecoBottom_dR[0][0]:
                            bindex = 0
                            antibindex = 1
                        elif RecoAntibottom_dR[0][0] == RecoBottom_dR[0][0]:
                            if RecoAntibottom_dR[1][0] < RecoBottom_dR[1][0]:
                                antibindex = 1
                                bindex = 0
                            elif RecoAntibottom_dR[1][0] > RecoBottom_dR[1][0]:
                                antibindex = 0
                                bindex = 1
                            elif RecoAntibottom_dR[1][0] == RecoBottom_dR[1][0]:
                                antibindex = 0
                                bindex = 1
                    else:       
                        bindex = 0 
                        antibindex = 0
                
            if everything_found and tau_cut and antitau_cut and bottom_cut and antibottom_cut:
                # print("event made cuts")
                dRtautau=sqrt(ROOT.Math.VectorUtil.DeltaR2(vis_tau_p4, vis_antitau_p4))
                dRbb=sqrt(ROOT.Math.VectorUtil.DeltaR2(bottom_p4, antibottom_p4))

                precuts_RECO_jet.Fill(dRbb,weight)
                precuts_RECO_tau.Fill(dRtautau,weight)

                if RecoFlag_tau_number:
                    if event_decay == "semimu":
                        prematch_RECO_semimu.Fill(dRtautau,weight)
                        if RecoMuon_dR[0] <= Reco_mu_dR_err and RecoTaus_dR[0] <= Reco_tau_dR_err:
                            postmatch_RECO_semimu.Fill(dRtautau,weight) 
                    elif event_decay == "semiele":
                        prematch_RECO_semiele.Fill(dRtautau,weight)
                        if RecoEle_dR[0] <= Reco_ele_dR_err and RecoTaus_dR[0] <= Reco_tau_dR_err:
                            postmatch_RECO_semiele.Fill(dRtautau,weight)
                    elif event_decay == "fullhad":
                        prematch_RECO_fullhad.Fill(dRtautau,weight)
                        if RecoAntiTaus_dR[antitauindex][0] <= Reco_tau_dR_err and RecoTaus_dR[tauindex][0] <= Reco_tau_dR_err:
                            postmatch_RECO_fullhad.Fill(dRtautau,weight)
                if RecoFlag_jet_number:
                    prematch_RECO_bs.Fill(dRbb,weight)
                    if RecoBottom_dR[bindex][0] <= Reco_jet_dR_err and RecoAntibottom_dR[antibindex][0] <= Reco_jet_dR_err:
                        postmatch_RECO_bs.Fill(dRbb,weight)
                
                if RecoFlag_tau_number and RecoFlag_jet_number:
                    prematch_RECO_tau.Fill(dRtautau,weight)
                    prematch_RECO_jet.Fill(dRbb,weight)
                    if RecoBottom_dR[bindex][0] <= Reco_jet_dR_err and RecoAntibottom_dR[antibindex][0] <= Reco_jet_dR_err:
                        if event_decay == "semimu":
                            if RecoMuon_dR[0] <= Reco_mu_dR_err and RecoTaus_dR[0] <= Reco_tau_dR_err:
                                postmatch_RECO_tau.Fill(dRtautau,weight)
                                postmatch_RECO_jet.Fill(dRbb,weight)
                        elif event_decay == "semiele":
                            if RecoEle_dR[0] <= Reco_ele_dR_err and RecoTaus_dR[0] <= Reco_tau_dR_err:
                                postmatch_RECO_tau.Fill(dRtautau,weight)
                                postmatch_RECO_jet.Fill(dRbb,weight)
                        elif event_decay == "fullhad":
                            if RecoAntiTaus_dR[antitauindex][0] <= Reco_tau_dR_err and RecoTaus_dR[tauindex][0] <= Reco_tau_dR_err:
                                postmatch_RECO_tau.Fill(dRtautau,weight)
                                postmatch_RECO_jet.Fill(dRbb,weight)

                tau_pt.Fill(vis_tau_p4.pt(),weight)
                tau_pt.Fill(vis_antitau_p4.pt(),weight)
                tau_eta.Fill(vis_tau_p4.eta(),weight)
                tau_eta.Fill(vis_antitau_p4.eta(),weight)

                bquark_pt.Fill(bottom_p4.pt(),weight)
                bquark_pt.Fill(antibottom_p4.pt(),weight)
                bquark_eta.Fill(bottom_p4.eta(),weight)
                bquark_eta.Fill(antibottom_p4.eta(),weight)
                # antibquark_pt.Fill(antibottom_p4.pt(),weight)
                # antitau_pt.Fill(antitau_p4.pt(),weight)
                heavyHiggs_pt.Fill(HeavyHiggs_p4.pt(),weight)
                lightHiggs_pt.Fill(LightHiggs_p4.pt(),weight)
                smHiggs_pt.Fill(SMHiggs_p4.pt(),weight)

                HH_eta.Fill(HeavyHiggs_p4.eta(),weight)
                LH_eta.Fill(LightHiggs_p4.eta(),weight)
                SM_eta.Fill(SMHiggs_p4.eta(),weight)
            
                dR_b_b = dRbb
                bquark_dR.Fill(dR_b_b,weight)
                dR_tau_tau = dRtautau
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
    bquark_eta.Scale(1./bquark_eta.Integral())
    # antibquark_pt.Scale(1./antibquark_pt.Integral())
    tau_pt.Scale(1./tau_pt.Integral())
    tau_eta.Scale(1./tau_eta.Integral())
    # antitau_pt.Scale(1./antitau_pt.Integral())
    heavyHiggs_pt.Scale(1./heavyHiggs_pt.Integral())
    lightHiggs_pt.Scale(1./lightHiggs_pt.Integral())
    smHiggs_pt.Scale(1./smHiggs_pt.Integral())

    HH_eta.Scale(1./HH_eta.Integral())
    LH_eta.Scale(1./LH_eta.Integral())
    SM_eta.Scale(1./SM_eta.Integral())

    higgs_dR.Scale(1./higgs_dR.Integral())
    tau_dR.Scale(1./tau_dR.Integral())
    bquark_dR.Scale(1./bquark_dR.Integral())

    output_file = ROOT.TFile.Open(outpath+"/"+"GenStudies_"+"MH_"+mH+"_Mh_"+mh+".root","RECREATE")

    # output_file.WriteTObject(Reco_Tau_dR)
    # output_file.WriteTObject(Reco_Mu_dR)
    # output_file.WriteTObject(Reco_Ele_dR)
    # output_file.WriteTObject(Reco_Bottom_dR)

    output_file.WriteTObject(event_counter)
    output_file.WriteTObject(found_counter)
    output_file.WriteTObject(combined_cut_counter)
    output_file.WriteTObject(combined_tau_cut_counter)
    output_file.WriteTObject(had_tau_cut_counter)
    output_file.WriteTObject(had_found_counter)
    output_file.WriteTObject(semimu_tau_cut_counter)
    output_file.WriteTObject(semimu_found_counter)
    output_file.WriteTObject(semiele_tau_cut_counter)
    output_file.WriteTObject(semiele_found_counter)
    output_file.WriteTObject(fulllep_found_counter)
    output_file.WriteTObject(b_cut_counter)

    output_file.WriteTObject(bquark_pt)
    output_file.WriteTObject(bquark_eta)
    # output_file.WriteTObject(antibquark_pt)
    output_file.WriteTObject(tau_pt)
    output_file.WriteTObject(tau_eta)
    # output_file.WriteTObject(antitau_pt)
    output_file.WriteTObject(heavyHiggs_pt)
    output_file.WriteTObject(lightHiggs_pt)
    output_file.WriteTObject(smHiggs_pt)

    output_file.WriteTObject(HH_eta)
    output_file.WriteTObject(LH_eta)
    output_file.WriteTObject(SM_eta)

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

output_file.WriteTObject(prematch_RECO_tau)
output_file.WriteTObject(postmatch_RECO_tau)
output_file.WriteTObject(prematch_RECO_jet)
output_file.WriteTObject(postmatch_RECO_jet)
output_file.WriteTObject(prematch_RECO_bs)
output_file.WriteTObject(postmatch_RECO_bs)
output_file.WriteTObject(prematch_RECO_fullhad)
output_file.WriteTObject(postmatch_RECO_fullhad)
output_file.WriteTObject(prematch_RECO_semiele)
output_file.WriteTObject(postmatch_RECO_semiele)
output_file.WriteTObject(prematch_RECO_semimu)
output_file.WriteTObject(postmatch_RECO_semimu)

output_file.WriteTObject(precuts_RECO_jet)
output_file.WriteTObject(precuts_RECO_tau)

output_file.Close()

