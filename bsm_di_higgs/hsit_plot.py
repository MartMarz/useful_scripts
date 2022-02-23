from __future__ import print_function
from optparse import OptionParser
from math import *
import os
import sys
import numpy as np



usage = "Usage: %prog [options] input_file.root\n"
parser = OptionParser(usage=usage)

parser.add_option("-i" ,"--input",action="store_true", dest="input", default=False,
    help="directories of all different mass points")
parser.add_option("-o","--outDir",dest="outDir",default= "plots",
    help = "path to output directory for plots. If a relative path is given the path is interpreted relative to 'path'")

(opts, args) = parser.parse_args()  

import ROOT
from DataFormats.FWLite import Events, Handle
import Utilities.General.cmssw_das_client as das_client

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadLeftMargin(0.11)
ROOT.gStyle.SetPadBottomMargin(0.12)
ROOT.gStyle.SetPalette(ROOT.kBird)

def find_masses(dataset_name):
    index_1 = dataset_name.find("_MH_")
    index_2 = dataset_name.find("_Mh_")
    #print(index_1,index_2)
    number_1 = ""
    number_2 = ""
    for char in dataset_name[index_1+4:]:
        if not char.isdigit(): break
        number_1+=char

    for char in dataset_name[index_2+4:]:
        if not char.isdigit(): break
        number_2+=char
    # print("MH="+number_1+" Mh="+number_2)
    return number_1,number_2

def filename(MH1,mh1,MH2,mh2,MH3,mh3,folder):
    return (folder+"_H1_"+MH1+"_"+"h1_"+mh1+"_"+"H2_"+MH2+"_"+"h2_"+mh2+"_"+"H3_"+MH3+"_"+"h3_"+mh3)

def plottHisto(hist1,hist2,hist3,file,mass):
    ROOT.gStyle.SetPadRightMargin(0.05)

    canvas = ROOT.TCanvas("canvas","canvas",980,720)
    canvas.cd()

    hist1.SetTitle("")
    hist2.SetTitle("")
    hist3.SetTitle("")

    maxy1=hist1.GetBinContent(hist1.GetMaximumBin())
    maxy2=hist2.GetBinContent(hist2.GetMaximumBin())
    maxy3=hist3.GetBinContent(hist3.GetMaximumBin())
    maximum=max(maxy1,maxy2,maxy3)

    hist1.SetMaximum(maximum+0.1)

    hist1.SetTitleOffset(1.25,"X")   

    hist1.SetLineColor(ROOT.kRed)
    hist1.SetLineWidth(3)
    hist1.GetYaxis().SetTitle("Arbitrary Units")
    hist2.SetLineColor(ROOT.kBlue)
    hist2.SetLineWidth(3)
    hist3.SetLineColor(ROOT.kGreen+2)
    hist3.SetLineWidth(3)

    hist1.Draw("hist")
    hist2.Draw("hist,same")
    hist3.Draw("hist,same")

    canvas.RedrawAxis("g")

    tt_bla = ROOT.TText()
    tt_bla.SetTextFont(63)
    tt_bla.SetTextSizePixels(40)
    tt_bla.DrawTextNDC(0.1, 0.95, "CMS simulation")
    tt_wip = ROOT.TText()
    tt_wip.SetTextFont(63)
    tt_wip.SetTextSizePixels(30)
    tt_wip = tt_wip.DrawTextNDC(0.1, 0.91, "work in progress")

    legend = ROOT.TLegend (0.65 ,0.65 ,0.95 ,0.9)
    legend.AddEntry(hist3,"M_{H}="+mass[2][0]+"GeV"+", m_{h}="+mass[2][1]+"GeV")
    legend.AddEntry(hist2,"M_{H}="+mass[1][0]+"GeV"+", m_{h}="+mass[1][1]+"GeV")
    legend.AddEntry(hist1,"M_{H}="+mass[0][0]+"GeV"+", m_{h}="+mass[0][1]+"GeV")
    legend.SetLineWidth (2)
    legend.Draw("same")

    canvas.Print(file)
    canvas.Clear()

def plot3DHisto(hist,file):
    ROOT.gStyle.SetPadRightMargin(0.15)
    ROOT.gStyle.SetPadLeftMargin(0.13)

    canvas = ROOT.TCanvas("canvas","canvas",980,720)
    canvas.cd()

    hist.SetTitle("")
    
    hist.SetMinimum(0.2)

    hist.Draw("BOX2 Z")
    hist.SetTitleOffset(1.75,"X") 
    hist.SetTitleOffset(2.25,"Y")
    hist.SetTitleOffset(1.75,"Z")
    hist.SetXTitle("Light Higgs Mass [GeV]")
    hist.SetYTitle("Heavy Higgs Mass [GeV]")
    ROOT.gPad.Modified()
    ROOT.gPad.Update()

    palette=hist.GetListOfFunctions().FindObject("palette")
    palette.SetX1NDC(0.89)
    palette.SetX2NDC(0.93)
    palette.SetY1NDC(0.1)
    palette.SetY2NDC(0.9)
    palette.GetAxis().SetTitle("Arbitrary Units")
    palette.GetAxis().SetTitleOffset(-1)
    canvas.Modified()
    canvas.Update()
    
   
    tt_bla = ROOT.TText()
    tt_bla.SetTextFont(63)
    tt_bla.SetTextSizePixels(40)
    tt_bla.DrawTextNDC(0.1, 0.95, "CMS simulation")
    tt_wip = ROOT.TText()
    tt_wip.SetTextFont(63)
    tt_wip.SetTextSizePixels(30)
    tt_wip = tt_wip.DrawTextNDC(0.1, 0.91, "work in progress")

    canvas.Print(file)
    canvas.Clear()

files=[]
for (dirpath, dirnames, filenames) in os.walk(args[0]):
    for file in filenames:
        if file.find("_MH_") >= 0:
            files.append([file,find_masses(file)])
        else:
            files.append([file,"3D"])

masspoint1=["500","120"]
masspoint2=["1200","120"]
masspoint3=["3000","120"]
masspoints=[masspoint1,masspoint2,masspoint3]

for file in files:
    if (file[0].find("_MH_"+masspoint1[0]+"_Mh_") >= 0 and file[0].find("_Mh_"+masspoint1[1]+".root") >=0):
        histFile_1 = ROOT.TFile.Open(args[0]+file[0],"READ")
        bquark_pt_Histo_1 = histFile_1.Get("bquark_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        antibquark_pt_Histo_1 = histFile_1.Get("antibquark_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        tau_pt_Histo_1 = histFile_1.Get("tau_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        antitau_pt_Histo_1 = histFile_1.Get("antitau_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        HHpT_Histo_1 = histFile_1.Get("HeavyHiggs_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        LHpt_Histo_1 = histFile_1.Get("LightHiggs_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        SMpt_Histo_1 = histFile_1.Get("SMHiggs_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        HdR_Histo_1 = histFile_1.Get("higgs_dR_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        tdR_Histo_1 = histFile_1.Get("tau_dR_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        bdR_Histo_1 = histFile_1.Get("bquark_dR_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])

        bquark_pt_Histo_1.SetDirectory(0)
        antibquark_pt_Histo_1.SetDirectory(0)
        tau_pt_Histo_1.SetDirectory(0)
        antitau_pt_Histo_1.SetDirectory(0)
        HHpT_Histo_1.SetDirectory(0)
        LHpt_Histo_1.SetDirectory(0)
        SMpt_Histo_1.SetDirectory(0)
        HdR_Histo_1.SetDirectory(0)
        tdR_Histo_1.SetDirectory(0)
        bdR_Histo_1.SetDirectory(0)
        histFile_1.Close()

    elif(file[0].find("_MH_"+masspoint2[0]+"_Mh_") >= 0 and file[0].find("_Mh_"+masspoint2[1]+".root") >=0):
        histFile_2 = ROOT.TFile.Open(args[0]+file[0],"READ")
        bquark_pt_Histo_2 = histFile_2.Get("bquark_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        antibquark_pt_Histo_2 = histFile_2.Get("antibquark_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        tau_pt_Histo_2 = histFile_2.Get("tau_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        antitau_pt_Histo_2 = histFile_2.Get("antitau_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        HHpT_Histo_2 = histFile_2.Get("HeavyHiggs_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        LHpt_Histo_2 = histFile_2.Get("LightHiggs_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        SMpt_Histo_2 = histFile_2.Get("SMHiggs_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        HdR_Histo_2 = histFile_2.Get("higgs_dR_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        tdR_Histo_2 = histFile_2.Get("tau_dR_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        bdR_Histo_2 = histFile_2.Get("bquark_dR_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])

        bquark_pt_Histo_2.SetDirectory(0)
        antibquark_pt_Histo_2.SetDirectory(0)
        tau_pt_Histo_2.SetDirectory(0)
        antitau_pt_Histo_2.SetDirectory(0)
        HHpT_Histo_2.SetDirectory(0)
        LHpt_Histo_2.SetDirectory(0)
        SMpt_Histo_2.SetDirectory(0)
        HdR_Histo_2.SetDirectory(0)
        tdR_Histo_2.SetDirectory(0)
        bdR_Histo_2.SetDirectory(0)
        histFile_2.Close()
    
    elif(file[0].find("_MH_"+masspoint3[0]+"_Mh_") >= 0 and file[0].find("_Mh_"+masspoint3[1]+".root") >=0):
        histFile_3 = ROOT.TFile.Open(args[0]+file[0],"READ")
        bquark_pt_Histo_3 = histFile_3.Get("bquark_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        antibquark_pt_Histo_3 = histFile_3.Get("antibquark_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        tau_pt_Histo_3 = histFile_3.Get("tau_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        antitau_pt_Histo_3 = histFile_3.Get("antitau_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        HHpT_Histo_3 = histFile_3.Get("HeavyHiggs_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        LHpt_Histo_3 = histFile_3.Get("LightHiggs_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        SMpt_Histo_3 = histFile_3.Get("SMHiggs_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        HdR_Histo_3 = histFile_3.Get("higgs_dR_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        tdR_Histo_3 = histFile_3.Get("tau_dR_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        bdR_Histo_3 = histFile_3.Get("bquark_dR_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])

        bquark_pt_Histo_3.SetDirectory(0)
        antibquark_pt_Histo_3.SetDirectory(0)
        tau_pt_Histo_3.SetDirectory(0)
        antitau_pt_Histo_3.SetDirectory(0)
        HHpT_Histo_3.SetDirectory(0)
        LHpt_Histo_3.SetDirectory(0)
        SMpt_Histo_3.SetDirectory(0)
        HdR_Histo_3.SetDirectory(0)
        tdR_Histo_3.SetDirectory(0)
        bdR_Histo_3.SetDirectory(0)
        histFile_3.Close()
    
    elif(file[0].find("_3D_")) >= 0:
        histFile_3D = ROOT.TFile.Open(args[0]+file[0],"READ")
        dRbb_Histo_3D = histFile_3D.Get("DeltaR_b_bbar")
        dRtautau_Histo_3D = histFile_3D.Get("DeltaR_tau_tau")
        dRhhSM_Histo_3D = histFile_3D.Get("DeltaR_h_hSM")
        pTHH_Histo_3D = histFile_3D.Get("HeavyHiggs_pt")
        pTLH_Histo_3D = histFile_3D.Get("LightHiggs_pt")
        pTSMH_Histo_3D = histFile_3D.Get("SMHiggs_pt")

        dRbb_Histo_3D.SetDirectory(0)
        dRtautau_Histo_3D.SetDirectory(0)
        dRhhSM_Histo_3D.SetDirectory(0)
        pTHH_Histo_3D.SetDirectory(0)
        pTLH_Histo_3D.SetDirectory(0)
        pTSMH_Histo_3D.SetDirectory(0)
        histFile_3D.Close()

outpath=opts.outDir
name=filename(masspoint1[0],masspoint1[1],masspoint2[0],masspoint2[1],masspoint3[0],masspoint3[1],outpath)
check = name
for n in range(50):
    if not os.path.exists(check):
        os.makedirs(check+"/")
        print ("made dir: ", check)
        break
    else:
        check = name + "_{}".format(n)


plottHisto(bquark_pt_Histo_1,bquark_pt_Histo_2,bquark_pt_Histo_3,check+"/bquark_pt.png",masspoints)
plottHisto(antibquark_pt_Histo_1,antibquark_pt_Histo_2,antibquark_pt_Histo_3,check+"/antibquark_pt.png",masspoints)
plottHisto(tau_pt_Histo_1,tau_pt_Histo_2,tau_pt_Histo_3,check+"/tau_pt.png",masspoints)
plottHisto(antitau_pt_Histo_1,antitau_pt_Histo_2,antitau_pt_Histo_3,check+"/antitau_pt.png",masspoints)

plottHisto(HHpT_Histo_1,HHpT_Histo_2,HHpT_Histo_3,check+"/HHpT.png",masspoints)
plottHisto(LHpt_Histo_1,LHpt_Histo_2,LHpt_Histo_3,check+"/LHpt.png",masspoints)
plottHisto(SMpt_Histo_1,SMpt_Histo_2,tau_pt_Histo_3,check+"/SMpt.png",masspoints)

plottHisto(HdR_Histo_1,HdR_Histo_2,HdR_Histo_3,check+"/hSM_h_dR.png",masspoints)
plottHisto(tdR_Histo_1,tdR_Histo_2,tdR_Histo_3,check+"/tau_dau_dR.png",masspoints)
plottHisto(bdR_Histo_1,bdR_Histo_2,bdR_Histo_3,check+"/b_b_dR.png",masspoints)
 
plot3DHisto(dRbb_Histo_3D,check+"/dRbb_3D.png")
plot3DHisto(dRtautau_Histo_3D,check+"/dRtt_3D.png")
plot3DHisto(dRhhSM_Histo_3D,check+"/dRhhSM_3D.png")
plot3DHisto(pTHH_Histo_3D,check+"/pTHH_3D.png")
plot3DHisto(pTLH_Histo_3D,check+"/pTLH_3D.png")
plot3DHisto(pTSMH_Histo_3D,check+"/pTSHM_3D.png")

