import ROOT
import sys
import os
import optparse
ROOT.gROOT.SetBatch(True)

parser = optparse.OptionParser()
parser.add_option("-w","-i","--inputDir",dest="inputDir",
    help = "absolute path to working directory of plotscript where 'output_limitInput.root' file is stored")
parser.add_option("-o","--outDir",dest="outDir",default="shiftPlots",
    help = "path to output directory for plots. If a relative path is given the path is interpreted relative to 'inputDir'")
parser.add_option("-p","--processes",dest="processes",default=None,
    help = "considered processes as a comma separated list. If none is given the five ttbar processes are used as default")
parser.add_option("-l","--proclabel",dest="proclabel",default=None,
    help = "label for process combination printed on plots. If none is given the default is this file is used")
parser.add_option("-n","--procname",dest="procname",default=None,
    help = "name for process combination for naming the plots. If none is given the default in this file is used")
parser.add_option("-s","--systs",dest="systematics",default=None,
    help = "considered systematics as a comma separated list. If none is given the defaults in this file are used")
parser.add_option("-v","--variables",dest="variables",default=None,
    help = "considered variables as a comma sepatated list. If none is given the defaults in this file are used")
(opts, args) = parser.parse_args()

# manage parser options
if not os.path.isabs(opts.inputDir):
    opts.inputDir = os.path.abspath(opts.inputDir)
if not os.path.exists(opts.inputDir):
    sys.exit("input directory {} does not exist".format(opts.inputDir))
filePath = opts.inputDir+"/NMSSMM500h1M125tautauh2M100_RunIIAutumn18MiniAOD_102X_13TeV_MINIAOD_madgraph-pythia8_v1.root"
if not os.path.exists(filePath):
    sys.exit("root file {} does not exist".format(filePath))


if not os.path.isabs(opts.outDir):
    opts.outDir = opts.inputDir+"/"+opts.outDir
if not os.path.exists(opts.outDir):
    os.makedirs(opts.outDir)

if opts.processes:
    opts.processes = opts.processes.split(",")
else:
    print("using default processes:")
    opts.processes = [
        "tthf", "ttlf", "ttcc"
        ]
    print("\n".join(opts.processes))

if not opts.proclabel:
    print("using default process label:")
    opts.proclabel = "t#bar{t}"
    print(opts.proclabel)

if not opts.procname:
    print("using default process name:")
    opts.procname = "ttbar"
    print(opts.procname)



if opts.systematics:
    opts.systematics = opts.systematics.split(",")
else:
    print("using default systematics:")
    opts.systematics = [
        "CMS_res_j_2018",
        "CMS_scale_j_2018",
        "CMS_HDAMP_2018",
        "CMS_UE_2018",
        "CMS_PDF_2018",
        "CMS_PU_2018",
        "CMS_scaleMuF_2018",
        "CMS_scaleMuR_2018",
        "CMS_ISR_2018",
        "CMS_FSR_2018",
        "CMS_eff_e_2018",
        "CMS_eff_m_2018",
        "CMS_trig_e_2018",
        "CMS_trig_m_2018",
        "CMS_btag_lf_2018",
        "CMS_btag_lfstats1_2018",
        "CMS_btag_lfstats2_2018",
        "CMS_btag_hf_2018",
        "CMS_btag_hfstats1_2018",
        "CMS_btag_hfstats2_2018",
        "CMS_btag_cferr1_2018",
        "CMS_btag_cferr2_2018",
        ]
    print("\n".join(opts.systematics))

if opts.variables:
    opts.variables = opts.variables.split(",")
else:
    print("using default variables:")
    #opts.variables = [
    #    #"finaldiscr_ljets_ge6j_ge3t_ttcc_node",
    #    #"finaldiscr_ljets_ge6j_ge3t_ttZ_node",
    #    #"finaldiscr_ljets_ge6j_ge3t_tthf_node",
    #    #"finaldiscr_ljets_ge6j_ge3t_ttlf_node",
    #    "inclusive_CSV_0",
    #    "inclusive_JetCSV_0",
    #    "inclusive_Jet_Pt_0",
    #    "inclusive_N_BTagsM",
    #    "inclusive_N_Jets"
    #    #"ge6j_ge3t_RecoTTZ_Z_M",
    #    ]
    opts.variables = [
        #"finaldiscr_ljets_ge4j_3t_ttZ_node",
        #"finaldiscr_ljets_ge4j_3t_tthf_node",

        #"finaldiscr_ljets_ge4j_ge4t_ttZ_node",
        #"finaldiscr_ljets_ge4j_ge4t_tthf_node",

        #"finaldiscr_ljets_ge4j_ge3t_ttZ_node",
        #"finaldiscr_ljets_ge4j_ge3t_tthf_node",

        "finaldiscr_ljets_ge6j_ge3t_ttHNodeDNN_ttZ_node",
        "finaldiscr_ljets_ge6j_ge3t_ttHNodeDNN_ttH_node",
        "finaldiscr_ljets_ge6j_ge3t_ttHNodeDNN_tthf_node",
        "finaldiscr_ljets_ge6j_ge3t_ttHNodeDNN_ttcc_node",
        "finaldiscr_ljets_ge6j_ge3t_ttHNodeDNN_ttlf_node",

        #"finaldiscr_ljets_le5j_ge3t_ttZ_node",
        #"finaldiscr_ljets_le5j_ge3t_tthf_node",
        "finaldiscr_ljets_5j_ge3t_ttHNodeDNN_ttZ_node",
        "finaldiscr_ljets_5j_ge3t_ttHNodeDNN_ttZ_node",
        "finaldiscr_ljets_5j_ge3t_ttHNodeDNN_ttH_node",
        "finaldiscr_ljets_5j_ge3t_ttHNodeDNN_tthf_node",
        "finaldiscr_ljets_5j_ge3t_ttHNodeDNN_ttcc_node",

        "finaldiscr_ljets_4j_ge3t_ttHNodeDNN_ttlf_node",
        "finaldiscr_ljets_4j_ge3t_ttHNodeDNN_ttH_node",
        "finaldiscr_ljets_4j_ge3t_ttHNodeDNN_tthf_node",
        "finaldiscr_ljets_4j_ge3t_ttHNodeDNN_ttcc_node",
        "finaldiscr_ljets_4j_ge3t_ttHNodeDNN_ttlf_node",
        ]

    print("\n".join(opts.variables))






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


def drawshifts(file, outdir, processes, variable, syst, procLabel = "", procName = ""):
    if procName == "":
        procName = "_".join(processes)

    ROOT.gStyle.SetOptStat(0)
    c = getCanvas(procName+"_"+variable+"_"+syst)
    c.cd(1)
    ROOT.gPad.SetLogy()

    nom     = None
    up      = None
    down    = None
    for proc in processes:
        nomName = proc+"_"+variable
        channel = proc
        print("adding {}".format(nomName))
        tree_nom = file.Get(channel+"_"+"nominal/"+"ntuple")
        tmp_nom = ROOT.TH1D("tmp_nom",variable,10,0,10)
        tree_nom.Draw(variable+"*btagSF"+">>tmp_nom")

        tree_up = file.Get(channel+"_"+syst+"Up/"+"ntuple")
        tmp_up = ROOT.TH1D("tmp_up",variable,10,0,10)
        tree_up.Draw(variable+"*btagSF"+">>tmp_up")

        tree_down = file.Get(channel+"_"+syst+"Down/"+"ntuple")
        tmp_down = ROOT.TH1D("tmp_down",variable,10,0,10)
        tree_down.Draw(variable+"*btagSF"+">>tmp_down")
        #tmp_nom     = file.Get(channel+"_"+"nominal/"+variable)
        #tmp_up      = file.Get(channel+"_"+syst+"Up/"+variable)
        #tmp_down    = file.Get(channel+"_"+syst+"Down/"+variable)
        #title       = tmp_nom.GetTitle()
        title = variable
        if nom is None:
            nom     = tmp_nom.Clone()
            nom.Reset()
        if up is None:
            up      = tmp_up.Clone()
            up.Reset()
        if down is None:
            down    = tmp_down.Clone()
            down.Reset()
        nom.Add(tmp_nom)
        up.Add(tmp_up)
        down.Add(tmp_down)


    # style settings
    nom.SetMarkerSize(1.3)
    nom.SetMarkerStyle(20)
    nom.SetMarkerColor(1)

    nom.SetFillColor(1)
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

    nom.Draw("PE0")
    cms.Draw()
    lumi.Draw()
    processlabel.Draw()

    up.Print()
    down.Print()

    up.Draw("samehist")
    up.SetFillColor(0)
    up.SetLineColor(2)
    up.SetLineWidth(2)

    down.Draw("samehist")
    down.SetFillColor(0)
    down.SetLineColor(4)
    down.SetLineWidth(2)

    legend = ROOT.TLegend(0.6, 0.8, 0.9, 0.9)
    legend.AddEntry(nom, "nominal", "P")
    legend.AddEntry(up, syst+" up", "l")
    legend.AddEntry(down, syst+" down", "l")
    legend.Draw()
    legend.SetBorderSize(0)
    legend.SetLineStyle(0)
    legend.SetTextSize(0.03)

    c.cd(2)
    ratioUp = nom.Clone()
    ratioUp.Divide(up)
    ratioUp.SetLineColor(up.GetLineColor())
    ratioUp.Draw("E0")
    ratioUp.SetMarkerSize(0)
    ratioUp.GetYaxis().SetTitle("#frac{nominal}{variation}")
    ratioUp.GetYaxis().CenterTitle()
    ratioUp.GetYaxis().SetRangeUser(0.58, 1.42)
    # ratioUp.GetXaxis().SetLabelSize(nom.GetXaxis().GetLabelSize() * 3.5)
    # ratioUp.GetYaxis().SetLabelSize(nom.GetYaxis().GetLabelSize() * 3.5)
    # ratioUp.GetXaxis().SetTitleSize(nom.GetXaxis().GetTitleSize() * 3.5)
    # ratioUp.GetYaxis().SetTitleSize(nom.GetYaxis().GetTitleSize() * 2.0)
    ratioUp.GetYaxis().SetLabelSize(0.15)
    ratioUp.GetYaxis().SetTitleSize(0.12)
    ratioUp.GetYaxis().SetTitleOffset(0.6)

    ratioUp.GetXaxis().SetLabelSize(0.15)
    ratioUp.GetXaxis().SetTitleSize(0.15)

    ratioUp.SetTitle("")
    ratioUp.GetYaxis().SetNdivisions(505)

    ratioDown = nom.Clone()
    ratioDown.Divide(down)
    ratioDown.SetLineColor(down.GetLineColor())
    ratioDown.Draw("E0same")
    ratioDown.SetMarkerSize(0)

    # ratioDown.SetTitle("");
    # ratioDown.GetYaxis().SetTitle("nominal/variation");

    c.Update()
    lineratio = ROOT.TLine(c.cd(2).GetUxmin(), 1.0, c.cd(2).GetUxmax(), 1.0)
    lineratio.SetLineColor(ROOT.kBlack)
    lineratio.Draw()
    c.Update()

    outPath = outdir+"/shifts_"+syst+"_"+variable+"_"+procName
    c.SaveAs(outPath+".pdf")
    c.SaveAs(outPath+".png")

    print("plot saved at {}.pdf".format(outPath))
    c.Clear()

    del nom
    del up
    del down





ROOT.gStyle.SetOptStat(0)

rfile = ROOT.TFile.Open(filePath)

for var in opts.variables:
    for syst in opts.systematics:
        drawshifts(rfile, opts.outDir, opts.processes, var, syst, procLabel = opts.proclabel, procName = opts.procname)
