import ROOT
import sys
import os
import optparse
ROOT.gROOT.SetBatch(True)

parser = optparse.OptionParser()
parser.add_option("-w","-i","--inputDir",dest="inputDir",
    help = "absolute path to working directory of plotscript where 'inoput.root' file is stored")
parser.add_option("-c","--compareDir",dest="compareDir",
    help = "absolute path to working directory of plotscript where 'compare.root' file is stored")
parser.add_option("-o","--outDir",dest="outDir",default="shiftPlots",
    help = "path to output directory for plots. If a relative path is given the path is interpreted relative to 'inputDir'")
parser.add_option("-p","--processes",dest="processes",default=None,
    help = "considered processes as a comma separated list. If none is given the five ttbar processes are used as default")
parser.add_option("-l","--proclabel",dest="proclabel",default=None,
    help = "label for process combination printed on plots. If none is given the default is this file is used")
parser.add_option("-n","--procname",dest="procname",default=None,
    help = "name for process combination for naming the plots. If none is given the default in this file is used")
#parser.add_option("-s","--systs",dest="systematics",default=None,
#    help = "considered systematics as a comma separated list. If none is given the defaults in this file are used")
parser.add_option("-v","--variables",dest="variables",default=None,
    help = "considered variables as a comma sepatated list. If none is given the defaults in this file are used")
(opts, args) = parser.parse_args()

# manage parser options
if not os.path.isabs(opts.inputDir):
    opts.inputDir = os.path.abspath(opts.inputDir)
if not os.path.exists(opts.inputDir):
    sys.exit("input directory {} does not exist".format(opts.inputDir))
filePath = opts.inputDir+"/DYJetsToLLM50_RunIIAutumn18MiniAOD_102X_13TeV_MINIAOD_madgraph-pythia8_v1.root"
if not os.path.exists(filePath):
    sys.exit("root file {} does not exist".format(filePath))

if not os.path.isabs(opts.compareDir):
    opts.compareDir = os.path.abspath(opts.compareDir)
if not os.path.exists(opts.compareDir):
    sys.exit("compare directory {} does not exist".format(opts.inputDir))
secfilePath = opts.compareDir+"/tree_1.root"
if not os.path.exists(secfilePath):
    sys.exit("root file {} does not exist".format(secfilePath))


if not os.path.isabs(opts.outDir):
    opts.outDir = opts.inputDir+"/"+opts.outDir
if not os.path.exists(opts.outDir):
    os.makedirs(opts.outDir)

if opts.processes:
    opts.processes = opts.processes.split(",")
else:
    print("using default processes:")
    opts.processes = [
        "DYinc"
        ]
    print("\n".join(opts.processes))

if not opts.proclabel:
    print("using default process label:")
    opts.proclabel = "DYinc"
    print(opts.proclabel)

if not opts.procname:
    print("using default process name:")
    opts.procname = "DYinc"
    print(opts.procname)



#if opts.systematics:
#    opts.systematics = opts.systematics.split(",")
#else:
#    print("using default systematics:")
#    opts.systematics = [
#        "CMS_res_j_2018",
#        "CMS_scale_j_2018",
#        "CMS_HDAMP_2018",
#        "CMS_UE_2018",
#        "CMS_PDF_2018",
#        "CMS_PU_2018",
#        "CMS_scaleMuF_2018",
#        "CMS_scaleMuR_2018",
#        "CMS_ISR_2018",
#        "CMS_FSR_2018",
#        "CMS_eff_e_2018",
#        "CMS_eff_m_2018",
#        "CMS_trig_e_2018",
#        "CMS_trig_m_2018",
#        "CMS_btag_lf_2018",
#        "CMS_btag_lfstats1_2018",
#        "CMS_btag_lfstats2_2018",
#        "CMS_btag_hf_2018",
#        "CMS_btag_hfstats1_2018",
#        "CMS_btag_hfstats2_2018",
#        "CMS_btag_cferr1_2018",
#        "CMS_btag_cferr2_2018",
#        ]
#    print("\n".join(opts.systematics))

if opts.variables:
    opts.variables = opts.variables.split(",")
else:
    print("using default variables:")
    opts.variables =    [["Pair_Tau_Pt","pt_2"],
                         ["Pair_Mu_Pt","pt_1"], 
                         ["nJets_nom", "njets"],
                         ["Pair_Tau_Eta", "eta_2"],
                         ["Pair_Tau_Phi", "phi_2"],
                         ["Pair_Mu_Eta", "eta_1"],
                         ["Pair_Mu_Phi", "phi_1"],
                         ["Jet_Pt_nom", "jpt_1"],
                         ["taggedJet_Pt_nom", "bpt_1"],                      
                         ["Jet_Eta_nom", "jeta_1"],
                         ["Jet_Phi_nom", "jphi_1"],
                         ["nTagsM_nom", "nbtag"],
                         ["taggedJet_Eta_nom", "beta_1"],
                         ["taggedJet_Phi_nom", "bphi_1"]]          


def getCanvas(name):
    c = ROOT.TCanvas(name, name, 1024, 1024)
    c.Divide(1, 2)
    c.cd(1).SetPad(0., 0.3, 1.0, 1.0)
    c.cd(1).SetBottomMargin(0.0)
    c.cd(2).SetPad(0., 0.0, 1.0, 0.3)
    c.cd(2).SetTopMargin(0.0)
    c.cd(1).SetTopMargin(0.07)
    c.cd(2).SetBottomMargin(0.4)
    c.cd(1).SetRightMargin(0.05)
    c.cd(1).SetLeftMargin(0.15)
    c.cd(2).SetRightMargin(0.05)
    c.cd(2).SetLeftMargin(0.15)
    c.cd(2).SetTicks(1, 1)
    c.cd(1).SetTicks(1, 1)
    return c

def drawshifts(ogfile, secfile, outdir, processes, variable, variable_og, procLabel = "", procName = ""):
    if procName == "":
        procName = "_".join(processes)

    ROOT.gStyle.SetOptStat(0)
    c = getCanvas(procName+"_"+variable)
    c.cd(1)
    ROOT.gPad.SetLogy()

    nom     = None
    comp      = None

    for proc in processes:
        nomName = proc+"_"+variable
        channel = proc
        cutsArtus = "abs(beta_1)<=2.4 && abs(jeta_1)<=2.4 && njets>=2 && nbtag>=1 && extraelec_veto<0.5 && extramuon_veto<0.5 && pt_2>=30 && pt_1>=24 && abs(eta_1)<=2.1 && abs(eta_2)<=2.3"
        cutsSnape = "nMu == 1 && nMu==nVetoMu"
        print("adding {}".format(nomName))
        if (variable == "Pair_Tau_Pt" or variable == "Pair_Mu_Pt" or variable == "taggedJet_Pt_nom" or variable =="Jet_Pt_nom"):
            tree_nom = ogfile.Get("mt_nominal/ntuple")
            tmp_nom = ROOT.TH1D("tmp_nom",variable,100,0,400)
            tree_nom.Draw(variable_og+">>tmp_nom", cutsArtus)

            tree_comp = secfile.Get("Events")
            tmp_comp = ROOT.TH1D("tmp_comp",variable,100,0,400)
            tree_comp.Draw(variable+">>tmp_comp", cutsSnape)

        elif (variable == "nJets_nom" or variable == "nTagsM_nom"):
            tree_nom = ogfile.Get("mt_nominal/ntuple")
            tmp_nom = ROOT.TH1D("tmp_nom",variable,10,0,10)
            tree_nom.Draw(variable_og+">>tmp_nom", cutsArtus)

            tree_comp = secfile.Get("Events")
            tmp_comp = ROOT.TH1D("tmp_comp",variable,10,0,10)
            tree_comp.Draw(variable+">>tmp_comp", cutsSnape)

        elif (variable == "Pair_Tau_Phi" or variable == "Pair_Mu_Phi" or variable == "Jet_Phi_nom" or variable=="taggedJet_Phi_nom"):
            tree_nom = ogfile.Get("mt_nominal/ntuple")
            tmp_nom = ROOT.TH1D("tmp_nom",variable,50,-4,4)
            tree_nom.Draw(variable_og+">>tmp_nom", cutsArtus)

            tree_comp = secfile.Get("Events")
            tmp_comp = ROOT.TH1D("tmp_comp",variable,50,-4,4)
            tree_comp.Draw(variable+">>tmp_comp", cutsSnape)

        elif (variable == "Pair_Tau_Eta" or variable == "Pair_Mu_Eta" or variable == "Jet_Eta_nom" or variable=="taggedJet_Eta_nom"):
            tree_nom = ogfile.Get("mt_nominal/ntuple")
            tmp_nom = ROOT.TH1D("tmp_nom",variable,50,-3,3)
            tree_nom.Draw(variable_og+">>tmp_nom", cutsArtus)

            tree_comp = secfile.Get("Events")
            tmp_comp = ROOT.TH1D("tmp_comp",variable,50,-3,3)
            tree_comp.Draw(variable+">>tmp_comp", cutsSnape)

        title = variable
        if nom is None:
            nom     = tmp_nom.Clone()
            nom.Reset()
        if comp is None:
            comp      = tmp_comp.Clone()
            comp.Reset()
        nom.Add(tmp_nom)
        comp.Add(tmp_comp)

    # style settings
#    nom.SetMarkerSize(1.3)
#    nom.SetMarkerStyle(20)
#    nom.SetMarkerColor(1)

    nom.SetFillColor(0)
    nom.SetTitle("")
    nom.GetXaxis().SetTitle(title)
    nom.GetXaxis().SetTitleSize(0.04)
    # nom.GetXaxis().SetTitleOffset(0.8)
    nom.GetYaxis().SetTitle("Events")
    nom.GetYaxis().SetTitleSize(0.07)
    nom.GetYaxis().SetTitleOffset(0.6)
    nom.GetYaxis().SetLabelSize(0.04)


    cms = ROOT.TLatex(0.15, 0.94, 'CMS #it{private work}'  )
    cms.SetNDC()
    cms.SetTextSize(0.07)
    ROOT.gStyle.SetPalette(1)

    lumi = ROOT.TLatex(0.7, 0.94, '59.7 fb^{-1} (13 TeV)'  )
    lumi.SetNDC()
    lumi.SetTextSize(0.05)

    processlabel = ROOT.TLatex(0.17, 0.86, procLabel )
    processlabel.SetNDC()
    processlabel.SetTextSize(0.05)

    nom.Draw("")
    cms.Draw()
    lumi.Draw()
    processlabel.Draw()

    comp.Print()
    
    comp.Draw("samehist")
    comp.SetFillColor(0)
    comp.SetLineColor(2)
#    comp.SetLineWidth(2)
#    nom.SetMarkerSize(1.3)
#    nom.SetMarkerStyle(20)
#    nom.SetMarkerColor(2)
 
    legend = ROOT.TLegend(0.6, 0.8, 0.9, 0.9)
    legend.AddEntry(nom, "Artus", "l")
    legend.AddEntry(comp, "Snape", "l")
    legend.Draw("")
    legend.SetBorderSize(0)
    legend.SetLineStyle(0)
    legend.SetTextSize(0.03)

    c.cd(2)
    ratioComp = nom.Clone()
    ratioComp.Divide(comp)
    ratioComp.SetLineColor(comp.GetLineColor())
    ratioComp.Draw("E0")
    ratioComp.SetMarkerSize(0)
    ratioComp.GetYaxis().SetTitle("#frac{Artus}{Snape}")
    ratioComp.GetYaxis().CenterTitle()
    ratioComp.GetYaxis().SetRangeUser(-3, 3)
    # ratioUp.GetXaxis().SetLabelSize(nom.GetXaxis().GetLabelSize() * 3.5)
    # ratioUp.GetYaxis().SetLabelSize(nom.GetYaxis().GetLabelSize() * 3.5)
    # ratioUp.GetXaxis().SetTitleSize(nom.GetXaxis().GetTitleSize() * 3.5)
    # ratioUp.GetYaxis().SetTitleSize(nom.GetYaxis().GetTitleSize() * 2.0)
    ratioComp.GetYaxis().SetLabelSize(0.15)
    ratioComp.GetYaxis().SetTitleSize(0.12)
    ratioComp.GetYaxis().SetTitleOffset(0.6)

    ratioComp.GetXaxis().SetLabelSize(0.15)
    ratioComp.GetXaxis().SetTitleSize(0.15)

    ratioComp.SetTitle("")
    ratioComp.GetYaxis().SetNdivisions(505)

    c.Update()
    lineratio = ROOT.TLine(c.cd(2).GetUxmin(), 1.0, c.cd(2).GetUxmax(), 1.0)
    lineratio.SetLineColor(ROOT.kBlack)
    lineratio.Draw()
    c.Update()

    outPath = outdir+"/compare_"+variable+"_"+procName
    c.SaveAs(outPath+".pdf")
    c.SaveAs(outPath+".png")

    print("plot saved at {}.pdf".format(outPath))
    c.Clear()

    del nom
    del comp



ROOT.gStyle.SetOptStat(0)

rfile = ROOT.TFile.Open(filePath)
cfile = ROOT.TFile.Open(secfilePath)

for var in opts.variables:
    drawshifts(rfile, cfile, opts.outDir, opts.processes, variable=var[0], variable_og=var[1], procLabel = opts.proclabel, procName = opts.procname)
 
