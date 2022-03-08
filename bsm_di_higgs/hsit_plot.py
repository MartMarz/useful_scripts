from __future__ import print_function
from optparse import OptionParser
from math import *
import os
# from signal import pthread_kill
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

def plottHisto(hist1,hist2,hist3,file,mass,line=False,axis=False,ptTitle=None):
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

    # hist1.SetMaximum(1)
    hist1.SetMaximum(maximum+0.1)

    hist1.SetTitleOffset(1.25,"X")   

    hist1.SetLineColor(ROOT.kBlack)
    hist1.SetLineWidth(3)
    hist1.GetYaxis().SetTitle("Arbitrary Units")
    
    hist2.SetLineColor(ROOT.kMagenta-4)
    hist2.SetLineWidth(3)
    hist3.SetLineColor(ROOT.kGreen+1)
    hist3.SetLineWidth(3)

    XTitle = hist1.GetXaxis().GetTitle()
    if not ptTitle is None:
        hist1.SetXTitle(ptTitle)
    elif axis:
        hist1.SetXTitle("#Delta R(h_{SM}h_{S})")
    else:
        hist1.SetXTitle(XTitle)

    hist1.Draw("hist")
    hist2.Draw("hist,same")
    hist3.Draw("hist,same")
    if line:
        ak4line = ROOT.TLine(0.4,0.,0.4,maximum+0.1)
        ak8line = ROOT.TLine(0.8,0.,0.8,maximum+0.1)#0.005
        ak15line = ROOT.TLine(1.5,0.,1.5,maximum+0.1)

        ak4line.SetLineColor(ROOT.kRed)
        ak4line.SetLineWidth(3)
        ak4line.SetLineStyle(2)

        ak8line.SetLineColor(ROOT.kRed)
        ak8line.SetLineWidth(3)
        ak8line.SetLineStyle(2)

        ak15line.SetLineColor(ROOT.kRed)
        ak15line.SetLineWidth(3)
        ak15line.SetLineStyle(2)

        ak4text = ROOT.TText()
        ak4text.SetTextFont(63)
        ak4text.SetTextSizePixels(30)
        ak4text.SetTextColor(ROOT.kRed)
        ak4text.DrawTextNDC(0.125, 0.05, "0.4")

        ak8text = ROOT.TText()
        ak8text.SetTextFont(63)
        ak8text.SetTextSizePixels(30)
        ak8text.SetTextColor(ROOT.kRed)
        ak8text.DrawTextNDC(0.205, 0.05, "0.8")#0.82

        ak15text = ROOT.TText()
        ak15text.SetTextFont(63)
        ak15text.SetTextSizePixels(30)
        ak15text.SetTextColor(ROOT.kRed)
        ak15text.DrawTextNDC(0.3, 0.05, "1.5")

        ak4line.Draw()
        ak8line.Draw()
        ak15line.Draw()

    # canvas.RedrawAxis("g")

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

def getbins(histo3D):
    n_LH_bins = histo3D.GetNbinsX()
    n_HH_bins = histo3D.GetNbinsY()
    n_value_bins = histo3D.GetNbinsZ()

    LHedges = np.array(float(histo3D.GetXaxis().GetBinLowEdge(1)))
    HHedges = np.array(float(histo3D.GetYaxis().GetBinLowEdge(1)))
    Valueedges = np.array(float(histo3D.GetZaxis().GetBinLowEdge(1)))

    for mLH in range(2,n_LH_bins+2):
        LHedges=np.append(LHedges, float(histo3D.GetXaxis().GetBinLowEdge(mLH)))
    for mHH in range(2,n_HH_bins+2):
        HHedges=np.append(HHedges, float(histo3D.GetYaxis().GetBinLowEdge(mHH)))
    for val in range(2,n_value_bins+2):
        Valueedges=np.append(Valueedges, float(histo3D.GetZaxis().GetBinLowEdge(val)))
    infos=[[n_LH_bins,LHedges],[n_HH_bins,HHedges],[n_value_bins,Valueedges]]
    return(infos)

def make2Dhist(mLH,Hist_3D,infos):
    hist2D = ROOT.TH2F("","",infos[1][0],infos[1][1],infos[2][0],infos[2][1])
    hist2D.GetXaxis().SetTitle(Hist_3D.GetYaxis().GetTitle())
    hist2D.GetYaxis().SetTitle(Hist_3D.GetZaxis().GetTitle())

    LHbin=0
    # print(infos)
    for LH in infos[0][1]:
        if LH == (mLH+1):
            for mHHbin in range(1,infos[1][0]+1):
                for valuebin in range(1,infos[2][0]+1):
                    binnumber_3D = Hist_3D.GetBin(LHbin,mHHbin,valuebin)
                    bincontent = Hist_3D.GetBinContent(binnumber_3D)
                    binnumber_2D = hist2D.GetBin(mHHbin,valuebin)
                    hist2D.SetBinContent(binnumber_2D,bincontent)
                    # print(LHbin, mHHbin, valuebin)
        LHbin+=1
    # Hist_3D.Print("range")
    # hist2D.Print("range")
    return(hist2D)
                

def plot2DHisto(hist,file,mLH,line=False,axis=False,ptTitle=None,bottom=False):
    ROOT.gStyle.SetPadRightMargin(0.15)
    ROOT.gStyle.SetPadLeftMargin(0.13)

    canvas = ROOT.TCanvas("canvas","canvas",980,720)
    canvas.cd()

    hist.SetMinimum(0.)
    hist.SetMaximum(1.)

    hist.SetTitle("m_{h_{S}}"+"={}GeV".format(mLH))
    hist.Draw("COLZ1")
    hist.SetTitleOffset(1.25,"Y")
    # hist.SetTitleColor(ROOT.kGreen)
    hist.SetTitleOffset(1.75,"Z")
    hist.SetXTitle("m_{H} (GeV)")
    YTitle = hist.GetYaxis().GetTitle()
    if axis:
        hist.SetYTitle("#Delta R(h_{SM}h_{S})")
    elif not ptTitle is None:
        hist.SetYTitle(ptTitle)
    else:
        hist.SetYTitle(YTitle)

    if line:
        if bottom:
            ak4line = ROOT.TLine(200.,0.4,3000,0.4)
            ak8line = ROOT.TLine(200.,0.8,3000,0.8)#0.005
            ak15line = ROOT.TLine(200.,1.5,3000,1.5)

            ak4line.SetLineColor(ROOT.kRed)
            ak4line.SetLineWidth(2)
            ak4line.SetLineStyle(2)

            ak8line.SetLineColor(ROOT.kRed)
            ak8line.SetLineWidth(2)
            ak8line.SetLineStyle(2)

            ak15line.SetLineColor(ROOT.kRed)
            ak15line.SetLineWidth(2)
            ak15line.SetLineStyle(2)

            ak4text = ROOT.TText()
            ak4text.SetTextFont(63)
            ak4text.SetTextSizePixels(30)
            ak4text.SetTextColor(ROOT.kRed)
            ak4text.DrawTextNDC(0.075, 0.155, "0.4")

            ak8text = ROOT.TText()
            ak8text.SetTextFont(63)
            ak8text.SetTextSizePixels(30)
            ak8text.SetTextColor(ROOT.kRed)
            ak8text.DrawTextNDC(0.075, 0.2125, "0.8")#0.82

            ak15text = ROOT.TText()
            ak15text.SetTextFont(63)
            ak15text.SetTextSizePixels(30)
            ak15text.SetTextColor(ROOT.kRed)
            ak15text.DrawTextNDC(0.075, 0.3, "1.5")

            ak4line.Draw()
            ak8line.Draw()
            ak15line.Draw()
            hist.GetYaxis().SetTitleColor(ROOT.kGreen)
        else:
            ak5line = ROOT.TLine(200.,0.5,3000,0.5)
            ak5line.SetLineColor(ROOT.kRed)
            ak5line.SetLineWidth(2)
            ak5line.SetLineStyle(2)
            ak5text = ROOT.TText()
            ak5text.SetTextFont(63)
            ak5text.SetTextSizePixels(30)
            ak5text.SetTextColor(ROOT.kRed)
            ak5text.DrawTextNDC(0.075, 0.165, "0.5")
            ak5line.Draw()
            hist.GetYaxis().SetTitleColor(ROOT.kBlue)

    ROOT.gPad.Modified()
    ROOT.gPad.Update()
    palette=hist.GetListOfFunctions().FindObject("palette")
    palette.GetAxis().SetTitle("Arbitrary Units")
    palette.Draw("same")
    palette.GetAxis().SetTitleOffset(1)
    canvas.Modified()
    canvas.Update()
    title=ROOT.gPad.FindObject("title")
    title.SetX1NDC(0.6)
    title.SetX2NDC(0.8)
    title.SetY1NDC(0.92)
    title.SetY2NDC(0.98)
    canvas.Modified()
    canvas.Update()

    tt_bla = ROOT.TText()
    tt_bla.SetTextFont(63)
    tt_bla.SetTextSizePixels(40)
    tt_bla.DrawTextNDC(0.15, 0.95, "CMS simulation")
    tt_wip = ROOT.TText()
    tt_wip.SetTextFont(63)
    tt_wip.SetTextSizePixels(30)
    tt_wip.DrawTextNDC(0.15, 0.91, "work in progress")

    canvas.Print(file)
    canvas.Clear()

def plot3DHisto(hist,file,nbins,axis=False,ptTitle=None):
    ROOT.gStyle.SetPadRightMargin(0.15)
    ROOT.gStyle.SetPadLeftMargin(0.13)

    canvas = ROOT.TCanvas("canvas","canvas",980,720)
    canvas.cd()

    hist.SetTitle("")

    # if nbins==40:
    #     hist.SetMinimum(0.1)
    # elif nbins==20:
    #     hist.SetMinimum(0.2)
    # elif nbins==10:
    #     hist.SetMinimum(0.35)
    hist.SetMaximum(1.)
    hist.SetMinimum(0.)


    hist.Draw("BOX2 Z")
    hist.SetTitleOffset(1.75,"X") 
    hist.SetTitleOffset(2.25,"Y")
    hist.SetTitleOffset(1.75,"Z")
    hist.SetXTitle("Light Higgs Mass (GeV)")
    hist.SetYTitle("Heavy Higgs Mass (GeV)")
    ZTitle=hist.GetZaxis().GetTitle()
    if axis:
        hist.SetZTitle("#Delta R(h_{SM}h_{S})")
    elif not ptTitle is None:
        hist.SetZTitle(ptTitle)
    else:
        hist.SetZTitle(ZTitle)

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
    tt_wip.DrawTextNDC(0.1, 0.91, "work in progress")

    canvas.Print(file)
    canvas.Clear()

files=[]
for (dirpath, dirnames, filenames) in os.walk(args[0]):
    for file in filenames:
        if file.find("_MH_") >= 0:
            files.append([file,find_masses(file)])
        else:
            files.append([file,"3D"])

masspoint1=["2000","500"]
masspoint2=["2000","120"]
masspoint3=["2000","1000"]
masspoints=[masspoint1,masspoint2,masspoint3]

for file in files:
    if (file[0].find("_MH_"+masspoint1[0]+"_Mh_") >= 0 and file[0].find("_Mh_"+masspoint1[1]+".root") >=0):
        histFile_1 = ROOT.TFile.Open(args[0]+file[0],"READ")
        bquark_pt_Histo_1 = histFile_1.Get("bquark_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        # antibquark_pt_Histo_1 = histFile_1.Get("antibquark_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        tau_pt_Histo_1 = histFile_1.Get("tau_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        # antitau_pt_Histo_1 = histFile_1.Get("antitau_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        HHpT_Histo_1 = histFile_1.Get("HeavyHiggs_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        LHpt_Histo_1 = histFile_1.Get("LightHiggs_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        SMpt_Histo_1 = histFile_1.Get("SMHiggs_pt_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        HdR_Histo_1 = histFile_1.Get("higgs_dR_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        tdR_Histo_1 = histFile_1.Get("tau_dR_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])
        bdR_Histo_1 = histFile_1.Get("bquark_dR_MH_"+masspoint1[0]+"_mh_"+masspoint1[1])

        bquark_pt_Histo_1.SetDirectory(0)
        # antibquark_pt_Histo_1.SetDirectory(0)
        tau_pt_Histo_1.SetDirectory(0)
        # antitau_pt_Histo_1.SetDirectory(0)
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
        # antibquark_pt_Histo_2 = histFile_2.Get("antibquark_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        tau_pt_Histo_2 = histFile_2.Get("tau_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        # antitau_pt_Histo_2 = histFile_2.Get("antitau_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        HHpT_Histo_2 = histFile_2.Get("HeavyHiggs_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        LHpt_Histo_2 = histFile_2.Get("LightHiggs_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        SMpt_Histo_2 = histFile_2.Get("SMHiggs_pt_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        HdR_Histo_2 = histFile_2.Get("higgs_dR_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        tdR_Histo_2 = histFile_2.Get("tau_dR_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])
        bdR_Histo_2 = histFile_2.Get("bquark_dR_MH_"+masspoint2[0]+"_mh_"+masspoint2[1])

        bquark_pt_Histo_2.SetDirectory(0)
        # antibquark_pt_Histo_2.SetDirectory(0)
        tau_pt_Histo_2.SetDirectory(0)
        # antitau_pt_Histo_2.SetDirectory(0)
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
        # antibquark_pt_Histo_3 = histFile_3.Get("antibquark_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        tau_pt_Histo_3 = histFile_3.Get("tau_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        # antitau_pt_Histo_3 = histFile_3.Get("antitau_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        HHpT_Histo_3 = histFile_3.Get("HeavyHiggs_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        LHpt_Histo_3 = histFile_3.Get("LightHiggs_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        SMpt_Histo_3 = histFile_3.Get("SMHiggs_pt_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        HdR_Histo_3 = histFile_3.Get("higgs_dR_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        tdR_Histo_3 = histFile_3.Get("tau_dR_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])
        bdR_Histo_3 = histFile_3.Get("bquark_dR_MH_"+masspoint3[0]+"_mh_"+masspoint3[1])

        bquark_pt_Histo_3.SetDirectory(0)
        # antibquark_pt_Histo_3.SetDirectory(0)
        tau_pt_Histo_3.SetDirectory(0)
        # antitau_pt_Histo_3.SetDirectory(0)
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


infosdR=getbins(dRbb_Histo_3D)#infos=[[n_LH_bins,LHedges],[n_HH_bins,HHedges],[n_value_bins,Valueedges]]
infospT=getbins(pTHH_Histo_3D)

# plottHisto(bquark_pt_Histo_1,bquark_pt_Histo_2,bquark_pt_Histo_3,check+"/bquark_pt.pdf",masspoints,ptTitle="Bottom Quark p_{T}(GeV)")
# plottHisto(antibquark_pt_Histo_1,antibquark_pt_Histo_2,antibquark_pt_Histo_3,check+"/antibquark_pt.pdf",masspoints,ptTitle="Anti Bottom Quark p_{T}(GeV)")
# plottHisto(tau_pt_Histo_1,tau_pt_Histo_2,tau_pt_Histo_3,check+"/tau_pt.pdf",masspoints,ptTitle="Tau p_{T}(GeV)")
# plottHisto(antitau_pt_Histo_1,antitau_pt_Histo_2,antitau_pt_Histo_3,check+"/antitau_pt.pdf",masspoints,ptTitle="Anti Tau Quark p_{T}(GeV)")

# plottHisto(HHpT_Histo_1,HHpT_Histo_2,HHpT_Histo_3,check+"/HHpt.pdf",masspoints,ptTitle="Heavy Higgs p_{T}(GeV)")
# plottHisto(LHpt_Histo_1,LHpt_Histo_2,LHpt_Histo_3,check+"/LHpt.pdf",masspoints,ptTitle="Light Higgs p_{T}(GeV)")
# plottHisto(SMpt_Histo_1,SMpt_Histo_2,SMpt_Histo_3,check+"/SMpt.pdf",masspoints,ptTitle="SM Higgs p_{T}(GeV)")

# plottHisto(HdR_Histo_1,HdR_Histo_2,HdR_Histo_3,check+"/hSM_h_dR.pdf",masspoints,axis=True)
# plottHisto(tdR_Histo_1,tdR_Histo_2,tdR_Histo_3,check+"/tau_tau_dR.pdf",masspoints,True)
# plottHisto(bdR_Histo_1,bdR_Histo_2,bdR_Histo_3,check+"/b_b_dR.pdf",masspoints,True)
 
# plot3DHisto(dRbb_Histo_3D,check+"/dRbb_3D.pdf",infosdR[2][0])
# plot3DHisto(dRtautau_Histo_3D,check+"/dRtt_3D.pdf",infosdR[2][0])
# plot3DHisto(dRhhSM_Histo_3D,check+"/dRhhSM_3D.pdf",infosdR[2][0],axis=True)
# plot3DHisto(pTHH_Histo_3D,check+"/pTHH_3D.pdf",infospT[2][0],ptTitle="Heavy Higgs p_{T}(GeV)")
# plot3DHisto(pTLH_Histo_3D,check+"/pTLH_3D.pdf",infospT[2][0],ptTitle="Light Higgs p_{T}(GeV)")
# plot3DHisto(pTSMH_Histo_3D,check+"/pTHSM_3D.pdf",infospT[2][0],ptTitle="SM Higgs p_{T}(GeV)")

mLH=[120]#,500,1000]
for mL in mLH:
    plot2DHisto(make2Dhist(mL,dRbb_Histo_3D,infosdR),check+"/"+"{}".format(mL)+"_dRbb_2D.pdf",mL,True,bottom=True)
    plot2DHisto(make2Dhist(mL,dRtautau_Histo_3D,infosdR),check+"/"+"{}".format(mL)+"_dRtt_2D.pdf",mL,True,bottom=False)
    # plot2DHisto(make2Dhist(mL,dRhhSM_Histo_3D,infosdR),check+"/"+"{}".format(mL)+"_dRhhSM_2D.pdf",mL,False,axis=True)

    # plot2DHisto(make2Dhist(mL,pTSMH_Histo_3D,infospT),check+"/"+"{}".format(mL)+"_pTSMH_2D.pdf",mL,False,ptTitle="SM Higgs p_{T}(GeV)")
    # plot2DHisto(make2Dhist(mL,pTLH_Histo_3D,infospT),check+"/"+"{}".format(mL)+"_pTLH_2D.pdf",mL,False,ptTitle="Light Higgs p_{T}(GeV)")
    plot2DHisto(make2Dhist(mL,pTHH_Histo_3D,infospT),check+"/"+"{}".format(mL)+"_pTHH_2D.pdf",mL,False,ptTitle="p_{T}(H)(GeV)")