import ROOT
import sys
import os
import optparse
ROOT.gROOT.SetBatch(True)

parser = optparse.OptionParser()
parser.add_option("-w","-i","--inputDir",dest="inputDir",
    help = "absolute path to working directory of plotscript where 'inoput.root' file is stored")
parser.add_option("-o","--outDir",dest="outDir",default="shiftPlots",
    help = "path to output directory for plots. If a relative path is given the path is interpreted relative to 'inputDir'")
(opts, args) = parser.parse_args()

# manage parser options
if not os.path.isabs(opts.inputDir):
    opts.inputDir = os.path.abspath(opts.inputDir)
if not os.path.exists(opts.inputDir):
    sys.exit("input directory {} does not exist".format(opts.inputDir))

filePath = opts.inputDir+"combine.root"
if not os.path.exists(filePath):
    sys.exit("root file {} does not exist".format(filePath))

if not os.path.isabs(opts.outDir):
    opts.outDir = opts.inputDir+"/"+opts.outDir
if not os.path.exists(opts.outDir):
    os.makedirs(opts.outDir)

def getCanvas(name):
    c = ROOT.TCanvas(name, name, 1024, 1024)
    c.Divide(1, 2)
    c.cd(1).SetPad(0., 0.7, 1.0, 1.0)
    c.cd(1).SetBottomMargin(0.0)
    c.cd(2).SetPad(0., 0.0, 1.0, 0.7)
    c.cd(2).SetTopMargin(0.0)
    c.cd(1).SetTopMargin(0.3)
    c.cd(2).SetBottomMargin(0.15)
    c.cd(1).SetRightMargin(0.05)
    c.cd(1).SetLeftMargin(0.15)
    c.cd(2).SetRightMargin(0.05)
    c.cd(2).SetLeftMargin(0.15)
    c.cd(2).SetTicks(1, 1)
    c.cd(1).SetTicks(1, 1)
    return c

def sanity(ogfile, outdir,variable,cuts,legend=None,XAxisLabel=None,suffix=""):
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas(variable, variable, 1024, 1024)
    c.cd(1).SetPad(0., 0.0, 1.0, 1.0)
    c.cd(1).SetBottomMargin(0.1)
    c.cd(1).SetTopMargin(0.07)
    c.cd(1).SetRightMargin(0.05)
    c.cd(1).SetLeftMargin(0.15)
    c.cd(1).SetTicks(1, 1)
    ROOT.gPad.SetLogy()

    nom     = None
    tree_nom = ogfile.Get("Events")
    tmp_nom = ROOT.TH1D("tmp_nom",variable,40,0,4)
    tree_nom.Draw(variable+">>tmp_nom", cuts)
    title = variable
    if nom is None:
        nom     = tmp_nom.Clone()
        nom.Reset()
    nom.Add(tmp_nom)

    nom.SetFillColor(0)
    nom.SetTitle("")
    nom.GetXaxis().SetTitle(title)
    nom.GetXaxis().SetTitleSize(0.05)
    # nom.GetXaxis().SetTitleOffset(0.8)
    nom.GetYaxis().SetTitle("Events")
    nom.GetYaxis().SetTitleSize(0.05)
    nom.GetYaxis().SetTitleOffset(1)
    nom.GetYaxis().SetLabelSize(0.04)
    nom.GetXaxis().SetLabelSize(0.04)
    nom.GetXaxis().SetTitle(XAxisLabel)

    cms = ROOT.TLatex(0.15, 0.94, 'CMS #it{private work}'  )
    cms.SetNDC()
    cms.SetTextSize(0.05)
    ROOT.gStyle.SetPalette(1)

    lumi = ROOT.TLatex(0.65, 0.94, '13 TeV'  )
    lumi.SetNDC()
    lumi.SetTextSize(0.03)

    year = ROOT.TLatex(0.9, 0.94, '2018'  )
    year.SetNDC()
    year.SetTextSize(0.03)

    nom.Draw("histe")
    cms.Draw()
    lumi.Draw()
    year.Draw()

    leg = ROOT.TLegend(0.6, 0.8, 0.9, 0.9)
    leg.AddEntry(nom, legend, "l")
    leg.Draw("")
    leg.SetBorderSize(0)
    leg.SetLineStyle(0)
    leg.SetTextSize(0.03)

    c.Update()

    outPath = outdir+"/sanity_"+variable+"_"+suffix
    c.SaveAs(outPath+".pdf")
    c.SaveAs(outPath+".png")

    print("plot saved at {}.pdf".format(outPath))
    c.Clear()

    del nom

def drawshifts(ogfile, outdir,variable1=None,variable2=None,cuts1=None,cuts2=None,cuts3=None,mode=None,legend1=None,legend2=None,legend3=None,YAxisLabel=None,XAxisLabel=None,efficiency=False,min=0,max=4,nbin=40,suffix=""):

    ROOT.gStyle.SetOptStat(0)
    c = getCanvas(variable1)
    c.cd(1)
    ROOT.gPad.SetLogy()

    nom     = None
    comp    = None
    comp1   = None

    nomName =variable1

    print("adding {}".format(nomName))
    if mode == "compare cuts":

        tree_nom = ogfile.Get("Events")
        tmp_nom = ROOT.TH1D("tmp_nom",variable1,nbin,min,max)
        tree_nom.Draw(variable1+">>tmp_nom", cuts1)

        tree_comp = ogfile.Get("Events")
        tmp_comp = ROOT.TH1D("tmp_comp",variable1,nbin,min,max)
        tree_comp.Draw(variable1+">>tmp_comp", cuts2)   

        outPath = outdir+"/compare_cuts_"+variable1+"_"+suffix


    if mode == "compare variables":

        tree_nom = ogfile.Get("Events")
        tmp_nom = ROOT.TH1D("tmp_nom",variable1,nbin,min,max)
        tree_nom.Draw(variable1+">>tmp_nom", cuts1)
        
        tree_comp = ogfile.Get("Events")
        tmp_comp = ROOT.TH1D("tmp_comp",variable1,nbin,min,max)
        tree_comp.Draw(variable2+">>tmp_comp", cuts1)   

        outPath = outdir+"/compare_variables_"+variable1+"_"+variable2+"_"+suffix

    if mode == "compare three":

        tree_nom = ogfile.Get("Events")
        tmp_nom = ROOT.TH1D("tmp_nom",variable1,nbin,min,max)
        tree_nom.Draw(variable1+">>tmp_nom", cuts1)

        tree_comp = ogfile.Get("Events")
        tmp_comp = ROOT.TH1D("tmp_comp",variable1,nbin,min,max)
        tree_comp.Draw(variable1+">>tmp_comp", cuts2)   
        
        tree_comp1 = ogfile.Get("Events")
        tmp_comp1 = ROOT.TH1D("tmp_comp1",variable1,nbin,min,max)
        tree_comp1.Draw(variable1+">>tmp_comp1", cuts3)

        outPath = outdir+"/compare_cuts_"+variable1+"_"+suffix

    if comp is None:
        comp      = tmp_comp.Clone()
        comp.Reset()
    if nom is None:
        nom     = tmp_nom.Clone()
        nom.Reset()
    if mode=="compare three":
        if comp1 is None:
            comp1      = tmp_comp1.Clone()
            comp1.Reset()
        comp1.Add(tmp_comp1)
    comp.Add(tmp_comp)
    nom.Add(tmp_nom)
    

    # style settings
#    nom.SetMarkerSize(1.3)
#    nom.SetMarkerStyle(20)
#    nom.SetMarkerColor(1)

    nom.SetFillColor(0)
    if not XAxisLabel==None:
        nom.SetTitle("")
        nom.GetXaxis().SetTitle(XAxisLabel)
    else:
        nom.SetTitle("")
        nom.GetXaxis().SetTitle("BLANK")

    nom.GetXaxis().SetTitleSize(0.04)
    # nom.GetXaxis().SetTitleOffset(0.8)
    nom.GetYaxis().SetTitle("Events")
    nom.GetYaxis().SetTitleSize(0.15)
    nom.GetYaxis().SetTitleOffset(0.4)
    nom.GetYaxis().SetLabelSize(0.12)


    cms = ROOT.TLatex(0.15, 0.8, 'CMS #it{private work}'  )
    cms.SetNDC()
    cms.SetTextSize(0.15)
    ROOT.gStyle.SetPalette(1)

    lumi = ROOT.TLatex(0.65, 0.8, '13 TeV'  )
    lumi.SetNDC()
    lumi.SetTextSize(0.13)

    year = ROOT.TLatex(0.9, 0.8, '2018'  )
    year.SetNDC()
    year.SetTextSize(0.13)

    nom.Draw("histe")
    cms.Draw()
    lumi.Draw()
    year.Draw()

    comp.Print()    
    comp.Draw("samehiste")
    comp.SetFillColor(0)
    comp.SetLineColor(2)
    if mode=="compare three":
        comp1.Print()    
        comp1.Draw("samehiste")
        comp1.SetFillColor(0)
        comp1.SetLineColor(ROOT.kBlack)
#    comp.SetLineWidth(2)
#    nom.SetMarkerSize(1.3)
#    nom.SetMarkerStyle(20)
#    nom.SetMarkerColor(2)

    legend = ROOT.TLegend(0.65, 0.45, 0.96, 0.75)

    if mode == "compare three":
        if legend1!=None and legend2!=None and legend3!=None:
            legend.AddEntry(nom, legend1, "l")
            legend.AddEntry(comp, legend2, "l")
            legend.AddEntry(comp1, legend3, "l")
    else:
        if legend1!=None and legend2!=None:
            legend.AddEntry(nom, legend1, "l")
            legend.AddEntry(comp, legend2, "l")
        else:
            legend.AddEntry(nom, "variable1", "l")
            legend.AddEntry(comp, "variable2", "l")
    
    legend.Draw("")
    legend.SetBorderSize(3)
    legend.SetLineStyle(1)
    legend.SetTextSize(0.09)

    c.cd(2)
    if efficiency:
        if mode == "compare three":

            ratioComp = ROOT.TGraphAsymmErrors(comp,nom,option = "cp")
            ratioComp.SetLineColor(comp.GetLineColor())
            ratioComp.Draw("AP")

            ratioComp1 = ROOT.TGraphAsymmErrors(comp1,nom,option = "cp")
            ratioComp1.SetLineColor(comp1.GetLineColor())
            ratioComp1.Draw("SAME ")

            ratioComp1.SetMarkerSize(0)
        else:
            ratioComp = ROOT.TGraphAsymmErrors(comp,nom,option = "cp")
            ratioComp.SetLineColor(comp.GetLineColor())
            ratioComp.Draw("AP")
    else:
        ratioComp = comp.Clone()
        ratioComp.Sumw2()
        ratioComp.Divide(nom)
        ratioComp.SetLineColor(comp.GetLineColor())
        ratioComp.Draw("E0")

    ratioComp.SetMarkerSize(0)
    if YAxisLabel==None:
        ratioComp.GetYaxis().SetTitle("#frac{RECO}{GEN}")
    else:
        ratioComp.GetYaxis().SetTitle(YAxisLabel)

    ratioComp.GetXaxis().SetTitle(nom.GetXaxis().GetTitle())
    ratioComp.GetYaxis().CenterTitle()
    if mode == "compare cuts":
        ratioComp.GetYaxis().SetRangeUser(0., 1.05)
    if mode == "compare variables":
        ratioComp.GetYaxis().SetRangeUser(0.7, 1.3)
    if mode == "compare three":
        ratioComp.GetYaxis().SetRangeUser(0., 1.05)
    ratioComp.GetXaxis().SetLabelSize(nom.GetXaxis().GetLabelSize() * 1.4)
    ratioComp.GetYaxis().SetLabelSize(nom.GetYaxis().GetLabelSize() * 0.41)
    ratioComp.GetXaxis().SetTitleSize(nom.GetXaxis().GetTitleSize() * 1.4)
    ratioComp.GetYaxis().SetTitleSize(nom.GetYaxis().GetTitleSize() * 0.38)
    # ratioComp.GetYaxis().SetLabelSize(0.15)
    # ratioComp.GetYaxis().SetTitleSize(0.12)
    ratioComp.GetYaxis().SetTitleOffset(1)

    # ratioComp.GetXaxis().SetLabelSize(0.15)
    # ratioComp.GetXaxis().SetTitleSize(0.15)

    ratioComp.SetTitle("")
    ratioComp.GetYaxis().SetNdivisions(7)

    c.Update()
    lineratio1 = ROOT.TLine(c.cd(2).GetUxmin(), 0., c.cd(2).GetUxmax(), 0.)
    lineratio1.SetLineColor(ROOT.kBlack)
    lineratio1.Draw()

    lineratio = ROOT.TLine(c.cd(2).GetUxmin(), 1.0, c.cd(2).GetUxmax(), 1.0)
    lineratio.SetLineColor(ROOT.kBlack)
    lineratio.Draw()
    c.Update()

    c.SaveAs(outPath+".pdf")
    c.SaveAs(outPath+".png")

    print("plot saved at {}.pdf".format(outPath))
    c.Clear()

    del nom
    del comp
    del comp1

ROOT.gStyle.SetOptStat(0)

rfile = ROOT.TFile.Open(filePath)

variables =    ["GEN_VisTau_Pt",
                "Pair_Tau_Pt_corr",
                "GEN_Muon_Pt",
                "Pair_Mu_Pt_corr",
                "GEN_bPair_dR",
                "bJetPair_bTagDisSorted_dR_corr_nom",
                "bJetPair_PtSorted_dR_corr_nom",
                "bJetPair_massSorted_dR_corr_nom",
                "GEN_TauPair_dR",
                "Pair_dR_corr",
                "GEN_System_dR",
                "System_bTagDisSorted_dR_corr_nom",
                "System_PtSorted_dR_corr_nom",
                "System_massSorted_dR_corr_nom",
                "GEN_RECO_dR_b1",
                "GEN_RECO_dR_b2",
                "GEN_RECO_dR_tau",
                "GEN_RECO_dR_muon",
                ]
# templatecuts =  "Flag_bPair_corr_nom" +"&&"+"nPairs_corr"+"&&"+"SystemFlag_corr_nom"+"&&"+"singleTrigMatch_corr"+"&&"+"crossTrigMatch_corr"+"&&"+"muTrig"
        # +"&&"+"tauTrig"+"&&"+"Flag_decay_channel"+"&&"+"Flag_lepTau_genCuts"+"&&"+"Flag_bQuark_genCuts"+"&&"+"Flag_hadTau_genCuts"
        # +"&&"+"Pair_Charge_Valid_corr"+"&&"+"Pair_dR_Valid_corr"
noCuts=""
channelCuts = "Flag_decay_channel==1"
allGenCuts = "Flag_decay_channel==1"+"&&"+"Flag_lepTau_genCuts==1"+"&&"+"Flag_hadTau_genCuts==1"+"&&"+"Flag_bQuark_genCuts==1"
tauGenCuts = "Flag_decay_channel==1"+"&&"+"Flag_lepTau_genCuts==1"+"&&"+"Flag_hadTau_genCuts==1"
bGenCuts = "Flag_decay_channel==1"+"&&"+"Flag_bQuark_genCuts==1"

tauRecoCuts = "nPairs_corr==1"
tauRecoValid = "Pair_Charge_Valid_corr==1"+"&&"+"Pair_dR_Valid_corr==1"
bRecoCuts = "Flag_bPair_corr_nom==1"
allRecoCuts = "SystemFlag_corr_nom==1"

allmissIdCuts = "Flag_decay_channel==0"+"&&"+"SystemFlag_corr_nom==1"
taumissIdCuts = "Flag_decay_channel==0"+"&&"+"nPairs_corr==1"
bmissIdCuts = "Flag_decay_channel==0"+"&&"+"Flag_bPair_corr_nom==1"

bmatching = "GEN_RECO_dR_b1<0.3"+"&&"+"GEN_RECO_dR_b2<0.3"
notbmatching = "GEN_RECO_dR_b2>2.5"
taumatching = "GEN_RECO_dR_muon<0.3"+"&&"+"GEN_RECO_dR_tau<0.3"
ptcut1="taggedJet_Pt_corr_nom[0] > 30. &&nTagsM_corr_nom==1"
ptcut2="taggedJet_Pt_corr_nom[0] > 30. &&taggedJet_Pt_corr_nom[1]&&nTagsM_corr_nom==2"
ptcut3="taggedJet_Pt_corr_nom[0] > 30. &&taggedJet_Pt_corr_nom[1]&&taggedJet_Pt_corr_nom[2]&&nTagsM_corr_nom==3"
ptcut4="taggedJet_Pt_corr_nom[0] > 30. &&taggedJet_Pt_corr_nom[1]&&taggedJet_Pt_corr_nom[2]&&taggedJet_Pt_corr_nom[3]&&nTagsM_corr_nom==4"

# sanity(rfile, opts.outDir,variable="GEN_RECO_dR_b1",cuts=bGenCuts+"&&"+bRecoCuts,legend="RECO cuts",XAxisLabel="min #DeltaR(GEN b, RECO Jet)")
# sanity(rfile, opts.outDir,variable="GEN_RECO_dR_b2",cuts=bGenCuts+"&&"+bRecoCuts,legend="RECO cuts",XAxisLabel="remaining #DeltaR(GEN b, RECO Jet)")
# sanity(rfile, opts.outDir,variable="GEN_RECO_dR_tau",cuts=tauGenCuts+"&&"+tauRecoCuts+"&&"+"Pair_Charge_Valid_corr==1",legend="RECO cuts",XAxisLabel="#DeltaR(GEN;RECO #tau_{h})")
# sanity(rfile, opts.outDir,variable="GEN_RECO_dR_muon",cuts=tauGenCuts+"&&"+tauRecoCuts+"&&"+"Pair_Charge_Valid_corr==1",legend="RECO cuts",XAxisLabel="#DeltaR(GEN;RECO #mu)")

# sanity(rfile, opts.outDir,variable="GEN_TauPair_dR",cuts=allRecoCuts+"&&"+allGenCuts+"&&"+"bJetPair_bTagDisSorted_dR_corr_nom>2"+"&&"+"Pair_Charge_Valid_corr==1",legend="#DeltaR(JetJet)>2",XAxisLabel="#DeltaR(#mu#tau_{h})")
# sanity(rfile, opts.outDir,variable="GEN_System_dR",cuts=allRecoCuts+"&&"+allGenCuts+"&&"+"bJetPair_bTagDisSorted_dR_corr_nom>2"+"&&"+"Pair_Charge_Valid_corr==1",legend="#DeltaR(JetJet)>2",XAxisLabel="#DeltaR(jets taus)")
# sanity(rfile, opts.outDir,variable="GEN_bPair_dR",cuts=allRecoCuts+"&&"+allGenCuts+"&&"+"bJetPair_bTagDisSorted_dR_corr_nom>2"+"&&"+"Pair_Charge_Valid_corr==1",legend="#DeltaR(JetJet)>2",XAxisLabel="#DeltaR(jets taus)")

# drawshifts(rfile, opts.outDir,variable1="GEN_TauPair_dR",cuts1=tauGenCuts,cuts2=tauGenCuts+"&&"+tauRecoCuts+"&&"+"Pair_Charge_Valid_corr==1",mode="compare cuts",legend1="GEN cuts",legend2="RECO cuts",XAxisLabel="GEN #DeltaR(#mu#tau_{h})")
# drawshifts(rfile, opts.outDir,variable1="GEN_TauPair_dR",variable2="Pair_dR_corr",cuts1=tauGenCuts+"&&"+tauRecoCuts+"&&"+"Pair_Charge_Valid_corr==1",mode="compare variables",legend1="GEN #DeltaR",legend2="RECO #DeltaR",XAxisLabel="#DeltaR(#mu#tau_{h})",efficiency=False,min=0.3,max=0.5,nbin=30,suffix="test")

# drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",cuts1=bGenCuts+"&&"+bRecoCuts+"&&nTagsM_corr_nom==4",cuts2=bGenCuts+"&&"+bRecoCuts+"&&"+ptcut4,mode="compare cuts",legend1="four bJets",legend2="bJet p_{T}>30 GeV",XAxisLabel="GEN #DeltaR(bb)")
# drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",variable2="bJetPair_bTagDisSorted_dR_corr_nom",cuts1=bGenCuts+"&&"+allRecoCuts,mode="compare variables",legend1="GEN #DeltaR",legend2="RECO #DeltaR",XAxisLabel="#DeltaR(bb)")
# drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",variable2="bJetPair_PtSorted_dR_corr_nom",cuts1=bGenCuts+"&&"+bRecoCuts,mode="compare variables",legend1="GEN #DeltaR",legend2="RECO #DeltaR",XAxisLabel="#DeltaR(bb)")
# drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",variable2="bJetPair_massSorted_dR_corr_nom",cuts1=bGenCuts+"&&"+bRecoCuts,mode="compare variables",legend1="GEN #DeltaR",legend2="RECO #DeltaR",XAxisLabel="#DeltaR(bb)")

# drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",cuts1=bGenCuts+"&&"+bRecoCuts,cuts2=bGenCuts+"&&"+bRecoCuts+"&&"+"GEN_RECO_dR_b2>0.3",mode="compare cuts",legend1="GEN cuts",legend2="#DeltaR(gen;RECO) > 0.3",XAxisLabel="GEN #DeltaR(bb)",efficiency=True,min=0,max=0.8,nbin=40,suffix="test")
# drawshifts(rfile, opts.outDir,variable1="GEN_TauPair_dR",cuts1=tauGenCuts+"&&"+tauRecoCuts,cuts2=tauGenCuts+"&&"+tauRecoCuts+"&&"+"(GEN_RECO_dR_tau>0.1 || GEN_RECO_dR_tau>0.1)",mode="compare cuts",legend1="GEN cuts",legend2="#DeltaR(gen;RECO) > 0.1",XAxisLabel="GEN #DeltaR(bb)",efficiency=True,min=0,max=0.8,nbin=40,suffix="test")

# drawshifts(rfile, opts.outDir,variable1="GEN_RECO_dR_b1",cuts1=bGenCuts+"&&"+bRecoCuts,cuts2=bGenCuts+"&&"+bRecoCuts+"&&"+"GEN_bPair_dR<0.5",mode="compare cuts",legend1="RECO cuts",legend2="GEN #DeltaR(bb) < 0.5",XAxisLabel="min #DeltaR(GEN;RECO bb)",efficiency=True,min=0,max=0.8,nbin=40,suffix="one")
# drawshifts(rfile, opts.outDir,variable1="GEN_RECO_dR_b2",cuts1=bGenCuts+"&&"+bRecoCuts,cuts2=bGenCuts+"&&"+bRecoCuts+"&&"+"GEN_bPair_dR<0.5",mode="compare cuts",legend1="RECO cuts",legend2="GEN #DeltaR(bb) < 0.5",XAxisLabel="remaining pair #DeltaR(GEN;RECO bb)",efficiency=True,min=0,max=0.8,nbin=40,suffix="two")
# drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",cuts1=bGenCuts,cuts2=bGenCuts+"&&"+bRecoCuts,mode="compare cuts",legend1="GEN cuts",legend2="RECO cuts",XAxisLabel="GEN #DeltaR(bb)",efficiency=True,min=0,max=0.8,nbin=40,suffix="efficiency")
# drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",cuts1=bGenCuts+"&&"+bRecoCuts,cuts2=bGenCuts+"&&"+bRecoCuts+"&&"+"GEN_RECO_dR_b2>0.5",mode="compare cuts",legend1="RECO cuts",legend2="#DeltaR(gen;RECO) > 0.5",XAxisLabel="GEN #DeltaR(bb)",efficiency=True,min=0,max=0.8,nbin=40,suffix="matching")

drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",cuts1=bGenCuts,cuts2=bGenCuts+"&&"+bRecoCuts,mode="compare cuts",legend1="GEN cuts",legend2="RECO cuts",XAxisLabel="GEN #DeltaR(bb)",efficiency=True,min=0,max=0.8,nbin=40,suffix="efficiency")
drawshifts(rfile, opts.outDir,variable1="GEN_TauPair_dR",cuts1=tauGenCuts,cuts2=tauGenCuts+"&&"+tauRecoCuts,mode="compare cuts",legend1="GEN cuts",legend2="RECO cuts",XAxisLabel="GEN #DeltaR(#tau#tau)",efficiency=True,min=0,max=0.8,nbin=40,suffix="efficiency")

sanity(rfile, opts.outDir,variable="GEN_RECO_dR_b1",cuts=bGenCuts+"&&"+bRecoCuts,legend="RECO cuts",XAxisLabel="min #DeltaR(GEN b, RECO Jet)",suffix="")
sanity(rfile, opts.outDir,variable="GEN_RECO_dR_b2",cuts=bGenCuts+"&&"+bRecoCuts,legend="RECO cuts",XAxisLabel="remaining pair #DeltaR(GEN b, RECO Jet)",suffix="")
sanity(rfile, opts.outDir,variable="GEN_RECO_dR_tau",cuts=tauGenCuts+"&&"+tauRecoCuts+"&&"+"Pair_Charge_Valid_corr==1",legend="RECO cuts",XAxisLabel="#DeltaR(GEN;RECO #tau_{h})",suffix="")
sanity(rfile, opts.outDir,variable="GEN_RECO_dR_muon",cuts=tauGenCuts+"&&"+tauRecoCuts+"&&"+"Pair_Charge_Valid_corr==1",legend="RECO cuts",XAxisLabel="#DeltaR(GEN;RECO #mu)",suffix="")

drawshifts(rfile, opts.outDir,variable1="GEN_RECO_dR_b1",cuts1=bGenCuts+"&&"+bRecoCuts,cuts2=bGenCuts+"&&"+bRecoCuts+"&&"+"nTagsM_corr_nom>1",mode="compare cuts",legend1="nbJets #geq 1",legend2="nJets #geq 2",XAxisLabel="min #DeltaR(GEN b, RECO Jet)",efficiency=True,min=0,max=4,nbin=80,suffix="2tags")
drawshifts(rfile, opts.outDir,variable1="GEN_RECO_dR_b2",cuts1=bGenCuts+"&&"+bRecoCuts,cuts2=bGenCuts+"&&"+bRecoCuts+"&&"+"nTagsM_corr_nom>1",mode="compare cuts",legend1="nbJets #geq 1",legend2="nJets #geq 2",XAxisLabel="remaining pair #DeltaR(GEN b, RECO Jet)",efficiency=True,min=0,max=4,nbin=80,suffix="2tags")

drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",cuts1=bGenCuts+"&&"+bRecoCuts,cuts2=bGenCuts+"&&"+bRecoCuts+"&&"+"(GEN_RECO_dR_b1>0.3 || GEN_RECO_dR_b2>0.3)",mode="compare cuts",legend1="RECO cuts",legend2="#DeltaR(matching) > 0.3",XAxisLabel="GEN #DeltaR(bb)",efficiency=True,min=0,max=4,nbin=80,suffix="find")
drawshifts(rfile, opts.outDir,variable1="GEN_TauPair_dR",cuts1=tauGenCuts+"&&"+tauRecoCuts,cuts2=tauGenCuts+"&&"+tauRecoCuts+"&&"+"(GEN_RECO_dR_tau>0.3 || GEN_RECO_dR_muon>0.3)",mode="compare cuts",legend1="RECO cuts",legend2="#DeltaR(matching) > 0.3",XAxisLabel="GEN #DeltaR(#tau#tau)",efficiency=True,min=0,max=4,nbin=80,suffix="find")

drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",cuts1=bGenCuts,cuts2=bGenCuts+"&&"+bRecoCuts,cuts3=bGenCuts+"&&"+bRecoCuts+"&&"+"(GEN_RECO_dR_b1<0.3 && GEN_RECO_dR_b2<0.3)",mode="compare three",legend1="GEN cuts",legend2="RECO cuts",legend3="#DeltaR(matching) < 0.3",YAxisLabel="#frac{RECO}{GEN} / #frac{#DeltaR(matching)}{GEN}",XAxisLabel="GEN #DeltaR(bb)",efficiency=True,min=0,max=0.8,nbin=40,suffix="three")
drawshifts(rfile, opts.outDir,variable1="GEN_TauPair_dR",cuts1=tauGenCuts,cuts2=tauGenCuts+"&&"+tauRecoCuts,cuts3=tauGenCuts+"&&"+tauRecoCuts+"&&"+"(GEN_RECO_dR_tau<0.3 && GEN_RECO_dR_muon<0.3)",mode="compare three",legend1="GEN cuts",legend2="RECO cuts",legend3="#DeltaR(matching) < 0.3",YAxisLabel="#frac{RECO}{GEN} / #frac{#DeltaR(matching)}{GEN}",XAxisLabel="GEN #DeltaR(#tau#tau)",efficiency=True,min=0,max=0.8,nbin=40,suffix="three")
drawshifts(rfile, opts.outDir,variable1="GEN_bPair_dR",cuts1=bGenCuts,cuts2=bGenCuts+"&&"+bRecoCuts+"&&"+"nTagsM_corr_nom>1",cuts3=bGenCuts+"&&"+bRecoCuts+"&&"+"nTagsM_corr_nom>1"+"&&"+"(GEN_RECO_dR_b1<0.3 && GEN_RECO_dR_b2<0.3)",mode="compare three",legend1="GEN cuts",legend2="RECO cuts &  nbJets#geq2",legend3="#DeltaR(matching) < 0.3",YAxisLabel="#frac{RECO}{GEN} / #frac{#DeltaR(matching)}{GEN}",XAxisLabel="GEN #DeltaR(bb)",efficiency=True,min=0,max=0.8,nbin=40,suffix="three_2tags")