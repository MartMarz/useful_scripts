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

def filename(folder):
    return (folder+"_3D")

def ratios(histo1,histo2,leg, outPath, tau=False, single=False):
    ROOT.gStyle.SetPadRightMargin(0.05)

    canvas = ROOT.TCanvas("canvas","canvas",980,720)
    canvas.cd()

    #style settings 
    if tau:
        histo2.SetLineColor(ROOT.kBlue)
    else:
        histo2.SetLineColor(ROOT.kGreen)

    histo2.SetLineWidth(2)
    histo1.SetLineWidth(2)
    histo2.SetTitle("")
    histo1.SetTitle("")

    if not single: 
        histo2.GetYaxis().SetTitle("Efficiency")
        histo2.Divide(histo1)
        histo2.Draw("hist")
        tmp = histo2.Clone()
        tmp.SetLineColor(ROOT.kBlack)
        tmp.SetLineWidth(1)
        tmp.Draw("same, E0")

        legend = ROOT.TLegend(0.5,0.9,0.95,0.95)
        legend.AddEntry(histo2, leg, "l")
        legend.Draw()
        legend.SetTextSize(0.03)

        max=histo2.GetBinContent(histo2.GetMaximumBin())
        histo2.SetMaximum(max+0.2)
    else:
        histo1.Draw("same, hist")
        histo2.Draw("same, hist")
        histo1.SetLineColor(ROOT.kBlack)
        histo2.SetLineColor(ROOT.kRed)
        legend = ROOT.TLegend(0.5,0.9,0.95,0.99)
        legend.AddEntry(histo2, "post "+leg, "l")
        legend.AddEntry(histo1, "pre "+leg, "l")
        legend.Draw()
        legend.SetTextSize(0.03)

    # tt_bla = ROOT.TText()
    # tt_bla.SetTextFont(63)
    # tt_bla.SetTextSizePixels(40)
    # tt_bla.DrawTextNDC(0.1, 0.95, "CMS simulation")
    # tt_wip = ROOT.TText()
    # tt_wip.SetTextFont(63)
    # tt_wip.SetTextSizePixels(30)
    # tt_wip = tt_wip.DrawTextNDC(0.1, 0.91, "work in progress")

    canvas.Update()
    canvas.SaveAs(outPath+".pdf")

files=[]
for (dirpath, dirnames, filenames) in os.walk(args[0]):
    for file in filenames:
        if file.find("_3D_") >= 0:
            files.append([file,"3D"])

for file in files:
    if(file[0].find("_3D_")) >= 0:
        histFile_3D = ROOT.TFile.Open(args[0]+file[0],"READ")
        prematch_tau_dR = histFile_3D.Get("prematch_tau_dR")
        postmatch_tau_dR = histFile_3D.Get("postmatch_tau_dR")
        prematch_jet_dR = histFile_3D.Get("prematch_jet_dR")
        postmatch_jet_dR = histFile_3D.Get("postmatch_jet_dR")
        prematch_b_dR = histFile_3D.Get("prematch_b_dR")
        postmatch_b_dR = histFile_3D.Get("postmatch_b_dR")
        prematch_fullhad_dR = histFile_3D.Get("prematch_fullhad_dR")
        postmatch_fullhad_dR = histFile_3D.Get("postmatch_fullhad_dR")
        prematch_semiele_dR = histFile_3D.Get("prematch_semiele_dR")
        postmatch_semiele_dR = histFile_3D.Get("postmatch_semiele_dR")
        prematch_semimu_dR = histFile_3D.Get("prematch_semimu_dR")
        postmatch_semimu_dR = histFile_3D.Get("postmatch_semimu_dR")
        precuts_jet_dR = histFile_3D.Get("precuts_jet_dR")
        precuts_tau_dR = histFile_3D.Get("precuts_tau_dR")
        
        prematch_tau_dR.SetDirectory(0)
        postmatch_tau_dR.SetDirectory(0)
        prematch_jet_dR.SetDirectory(0)
        postmatch_jet_dR.SetDirectory(0)
        prematch_b_dR.SetDirectory(0)
        postmatch_b_dR.SetDirectory(0)
        prematch_fullhad_dR.SetDirectory(0)
        postmatch_fullhad_dR.SetDirectory(0)
        prematch_semiele_dR.SetDirectory(0)
        postmatch_semiele_dR.SetDirectory(0)
        prematch_semimu_dR.SetDirectory(0)
        postmatch_semimu_dR.SetDirectory(0)
        precuts_jet_dR.SetDirectory(0)
        precuts_tau_dR.SetDirectory(0)

        histFile_3D.Close()

outpath=opts.outDir
name=filename(outpath)
check = name
for n in range(50):
    if not os.path.exists(check):
        os.makedirs(check+"/")
        print ("made dir: ", check)
        break
    else:
        check = name + "_{}".format(n)

#compare plots
#precuts to prematch 
ratios(precuts_tau_dR,prematch_tau_dR,"all RECO cuts",check+"/precuts_prematch_tau",single=True)
ratios(precuts_jet_dR,prematch_jet_dR,"all RECO cuts",check+"/precuts_prematch_b",single=True)
#precuts to dR matching
ratios(precuts_tau_dR,postmatch_tau_dR,"all RECO cuts and matched",check+"/precuts_postmatch_tau",single=True)
ratios(precuts_jet_dR,postmatch_jet_dR,"all RECO cuts and matched",check+"/precuts_postmatch_b",single=True)
#prematch to dR matching 
ratios(prematch_tau_dR,postmatch_tau_dR,"tau and b matched",check+"/prematch_postmatch_tau",single=True)
ratios(prematch_jet_dR,postmatch_jet_dR,"tau and b matched",check+"/prematch_postmatch_b",single=True)
#splitted
ratios(prematch_b_dR,postmatch_b_dR,"b matched",check+"/prematch_postmatch_bquarks",single=True)
ratios(prematch_semimu_dR,postmatch_semimu_dR,"tau and mu matched",check+"/prematch_postmatch_taumu",single=True)
ratios(prematch_semiele_dR,postmatch_semiele_dR,"tau and e matched",check+"/prematch_postmatch_tauele",single=True)
ratios(prematch_fullhad_dR,postmatch_fullhad_dR,"tau matched",check+"/prematch_postmatch_tauhad",single=True)

#efficiency
#precuts to prematch
ratios(precuts_tau_dR,prematch_tau_dR,"all RECO cuts",check+"/eff_precuts_prematch_tau",tau=True)
ratios(precuts_jet_dR,prematch_jet_dR,"all RECO cuts",check+"/eff_precuts_prematch_b")
#precuts to dR matching
ratios(precuts_tau_dR,postmatch_tau_dR,"all RECO cuts and matched",check+"/eff_precuts_postmatch_tau",tau=True)
ratios(precuts_jet_dR,postmatch_jet_dR,"all RECO cuts and matched",check+"/eff_precuts_postmatch_b")
#prematch to dR matching 
ratios(prematch_tau_dR,postmatch_tau_dR,"tau and b matched",check+"/eff_prematch_postmatch_tau",tau=True)
ratios(prematch_jet_dR,postmatch_jet_dR,"tau and b matched",check+"/eff_prematch_postmatch_b")
#splitted
ratios(prematch_b_dR,postmatch_b_dR,"b matched",check+"/eff_prematch_postmatch_bquarks")
ratios(prematch_semimu_dR,postmatch_semimu_dR,"tau and mu matched",check+"/eff_prematch_postmatch_taumu",tau=True)
ratios(prematch_semiele_dR,postmatch_semiele_dR,"tau and e matched",check+"/eff_prematch_postmatch_tauele",tau=True)
ratios(prematch_fullhad_dR,postmatch_fullhad_dR,"tau matched",check+"/eff_prematch_postmatch_tauhad",tau=True)
