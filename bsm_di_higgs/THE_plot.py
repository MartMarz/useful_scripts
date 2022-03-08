from __future__ import print_function
from optparse import OptionParser
from math import *
import os
from sqlite3 import Row
from telnetlib import TELNET_PORT
import matplotlib.pyplot as plt
# from signal import pthread_kill
import sys
from tokenize import Double
import numpy as np
import ROOT
from DataFormats.FWLite import Events, Handle
import Utilities.General.cmssw_das_client as das_client

usage = "Usage: %prog [options] input_file.root\n"
parser = OptionParser(usage=usage)

parser.add_option("-i" ,"--input",action="store_true", dest="input", default=False,
    help="directories of all different mass points")
parser.add_option("-o","--outDir",dest="outDir",default= "plots",
    help = "path to output directory for plots. If a relative path is given the path is interpreted relative to 'path'")

(opts, args) = parser.parse_args()  

def find_masses(dataset_name):
    index_1 = dataset_name.find("_MH_")
    index_2 = dataset_name.find("_Mh_")
    number_1 = ""
    number_2 = ""
    for char in dataset_name[index_1+4:]:
        if not char.isdigit(): break
        number_1+=char

    for char in dataset_name[index_2+4:]:
        if not char.isdigit(): break
        number_2+=char
    return number_1,number_2

def calculate(filename,histname):
    quantile_05=np.array([0.5])
    median=np.array([0.])

    histfile = ROOT.TFile.Open(filename,"READ")
    histo = histfile.Get(histname)
    mean_val = histo.GetMean() 
    histo.GetQuantiles(1,median,quantile_05)
    median_val = median[0]
    std_dev=histo.GetStdDev()
    return mean_val, median_val, std_dev

files=[]
for (dirpath, dirnames, filenames) in os.walk(args[0]):
    for file in filenames:
        if file.find("_MH_") >= 0:
            files.append([file,find_masses(file)])

histos=["bquark_pt","tau_pt","HeavyHiggs_pt","LightHiggs_pt","SMHiggs_pt","higgs_dR","tau_dR","bquark_dR"]
wanted_mhS=np.array(["60","120","500"])
# "60","70","75","80","85","90","95","100","110","120","130","150","170","190","250","300","350","400","450","500","550","600","650","700","800"
# "900","1000","1200","1300","1400","1600","1800","2000","2200","2400","2600","2800"


infos=[]
for file in files:
    mhS=file[1][1]
    MH=file[1][0]
    for wan_mhS in wanted_mhS:
        if wan_mhS==mhS:
            for hist in histos:
                mean, median, std_dev=calculate(args[0]+file[0],hist+"_MH_"+MH+"_mh_"+mhS)
                infos.append([mhS,float(MH),hist,mean,median,std_dev])
infos=sorted(infos)

plots=[]
for wan_mhS in wanted_mhS:
    MH_arr=[]
    b_pt_mean=[]
    b_pt_median=[]
    b_pt_std_dev=[]
    t_pt_mean=[]
    t_pt_median=[]
    t_pt_std_dev=[]
    HH_pt_mean=[]
    HH_pt_median=[]
    HH_pt_std_dev=[]
    LH_pt_mean=[]
    LH_pt_median=[]
    LH_pt_std_dev=[]
    SM_pt_mean=[]
    SM_pt_median=[]
    SM_pt_std_dev=[]
    b_dR_mean=[]
    b_dR_median=[]
    b_dR_std_dev=[]
    t_dR_mean=[]
    t_dR_median=[]
    t_dR_std_dev=[]
    h_dR_mean=[]
    h_dR_median=[]
    h_dR_std_dev=[]
    for point in infos:
        mhS=point[0]
        MH_val=point[1]
        name=point[2]
        mean=point[3]
        median=point[4]
        std_dev=point[5]
        if mhS==wan_mhS:
            if name=="bquark_pt":
                MH_arr.append(MH_val)
                b_pt_mean.append(mean)
                b_pt_median.append(median)
                b_pt_std_dev.append(std_dev) 
            elif name=="tau_pt":
                t_pt_mean.append(mean)
                t_pt_median.append(median)
                t_pt_std_dev.append(std_dev)
            elif name=="HeavyHiggs_pt":
                HH_pt_mean.append(mean)
                HH_pt_median.append(median)
                HH_pt_std_dev.append(std_dev)
            elif name=="LightHiggs_pt":
                LH_pt_mean.append(mean)
                LH_pt_median.append(median)
                LH_pt_std_dev.append(std_dev)
            elif name=="SMHiggs_pt":
                SM_pt_mean.append(mean)
                SM_pt_median.append(median)
                SM_pt_std_dev.append(std_dev)
            elif name=="higgs_dR":
                h_dR_mean.append(mean)
                h_dR_median.append(median)
                h_dR_std_dev.append(std_dev)
            elif name=="tau_dR":
                t_dR_mean.append(mean)
                t_dR_median.append(median)
                t_dR_std_dev.append(std_dev)
            elif name=="bquark_dR":
                b_dR_mean.append(mean)
                b_dR_median.append(median)
                b_dR_std_dev.append(std_dev)
    plots.append(
        [wan_mhS,MH_arr,    #0
        b_pt_mean,b_pt_median,b_pt_std_dev, #2
        t_pt_mean,t_pt_median,t_pt_std_dev, #5
        HH_pt_mean,HH_pt_median,HH_pt_std_dev,  #8
        LH_pt_mean,LH_pt_median,LH_pt_std_dev,  #11
        SM_pt_mean,SM_pt_median,SM_pt_std_dev,  #14
        b_dR_mean,b_dR_median,b_dR_std_dev, #17
        t_dR_mean,t_dR_median,t_dR_std_dev, #20
        h_dR_mean,h_dR_median,h_dR_std_dev]) #23


# More versatile wrapper
# fig, hosts = plt.subplots(2,3,figsize=(20,10)) # (width, height) in inches
# (see https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.subplots.html)
# mean
fig = plt.figure(figsize=(20,10))
gs = fig.add_gridspec(2, len(wanted_mhS), hspace=0, wspace=0)
hosts = gs.subplots(sharex='col', sharey='row') 

maxMH=3225
maxpT=1225
minMH=225
minpT=25
maxdR=0
mindR=5.75

a=[None]*len(wanted_mhS)
b=[None]*len(wanted_mhS)
dR_arr =[a,b]
for j in range(2):
    for i in range(len(hosts[0])):
        dR_arr[j][i]=(hosts[j][i].twinx())

for ax in hosts:
    for a in ax:
        a.set_xlim(minMH, maxMH)
        a.set_ylim(minpT,maxpT)
        a.set_xlabel("$m_{H}$ (GeV)")
        a.set_ylabel("mean $p_{T}$ (GeV)")
        a.label_outer()

for Rx in dR_arr:
    for R in Rx:
        R.set_ylabel("mean $\Delta$R")
        R.set_ylim(0, 5.75)
        lastrow = R.is_last_row()
        lastcol = R.is_last_col()
        if not lastrow:
            for label in R.get_xticklabels(which="both"):
                label.set_visible(False)
            R.get_xaxis().get_offset_text().set_visible(False)
            R.set_xlabel("")
        if not lastcol:
            for label in R.get_yticklabels(which="both"):
                label.set_visible(False)
            R.get_yaxis().get_offset_text().set_visible(False)
            R.set_ylabel("")

dRbcolor='limegreen'
pTbcolor='limegreen'
dRtcolor='deepskyblue'
pTtcolor='deepskyblue'
dRhcolor='k'
pThcolor='k'
linecolor='r'
fontsize=20
legendsize=15
linewidth=3
gridcolor='lightgray'
transperancy=0.25
areacolor='mistyrose'

particle=["bottom","tau"]
collum=-1
for mhS in wanted_mhS:
    collum+=1   
    for part in particle:
        if part == "bottom":
            row = 0
        elif part == "tau":
            row = 1

        host=hosts[row][collum]
        dR = dR_arr[row][collum]

        if part == "tau":
            tindex=0
            tcut=False
            cutindex=len(plots[collum][1])-1
            for value in plots[collum][20]:
                if value <= 0.5:
                    cutindex=tindex
                    tcut=True
                    break
                else:
                    tindex+=1
            if tcut:
                host.axvspan(plots[collum][1][cutindex]-250, maxMH, facecolor=pTtcolor, alpha=0.15)
                host.text(plots[collum][1][cutindex]-200,maxpT/2,'boosted region',color=pTtcolor, fontsize=15,alpha=0.9,rotation=-90)
            host.grid(color=gridcolor, linestyle='--', linewidth=1,alpha=transperancy+0.25)
            dR.axhline(0.5,c=linecolor,label="0,5")
            # H_pT, = host.plot(plots[collum][1], plots[collum][8], color=pThcolor,ls='-.', label="p$_{T}$(H)",linewidth=linewidth,alpha=transperancy)
            LH_pT, = host.plot(plots[collum][1], plots[collum][14], color=pThcolor, ls=':',label="p$_{T}$(h to tau tau)",linewidth=linewidth,alpha=transperancy)
            tau_pT, = host.plot(plots[collum][1], plots[collum][5], color=pTtcolor,ls='--', label="p$_{T}$(tau)",linewidth=linewidth,alpha=transperancy)
            # h_dR, = dR.plot(plots[collum][1], plots[collum][23], color=dRhcolor , label="$\Delta$R(hh$_{S}$)",linewidth=linewidth)
            t_dR, = dR.plot(plots[collum][1], plots[collum][20], color=dRtcolor , label="$\Delta$R(tautau)",linewidth=linewidth)

            lnshost= [LH_pT,tau_pT]
            lnsdR=[t_dR]
            if dR.is_last_col():
                dR.legend(handles=lnsdR, loc='upper right',prop={'size': legendsize})
                dR.text(maxMH-225,0.6,'0.5',color=linecolor, fontsize=15)
            if host.is_first_col():
                host.legend(handles=lnshost, loc='upper left',prop={'size': legendsize})

            # dR.yaxis.label.set_color(t_dR.get_color())
            dR.yaxis.label.set_fontsize(fontsize)
            host.yaxis.label.set_fontsize(fontsize)
            host.xaxis.label.set_fontsize(fontsize)


        elif part == "bottom":
            bindex=0
            bcut=False
            cutindex=len(plots[collum][1])-1
            for value in plots[collum][17]:
                if value <= 0.4:
                    cutindex=bindex
                    bcut=True
                    break
                else:
                    bindex+=1
            if bcut:
                host.axvspan(plots[collum][1][cutindex-1], maxMH, facecolor=pTbcolor, alpha=0.15)
                host.text(plots[collum][1][cutindex-1]+50,maxpT/2,'boosted region',color=pTbcolor, fontsize=15,alpha=0.9,rotation=-90)
            host.grid(color=gridcolor, linestyle='--', linewidth=1,alpha=transperancy+0.25)
            dR.axhline(0.4,c=linecolor,label="0,4")
            dR.axhline(0.8,c=linecolor,label="0,8")
            host.set_title("$m_{h_{S}}$ =" +mhS+ " GeV",fontsize=fontsize,color=pTbcolor)
            H_pT, = host.plot(plots[collum][1], plots[collum][8], color=pThcolor,ls='-.', label="p$_{T}$(H)",linewidth=linewidth,alpha=transperancy)
            SM_pT, = host.plot(plots[collum][1], plots[collum][11], color=pThcolor,ls=':', label="p$_{T}$(h$_{S}$ to bb)",linewidth=linewidth,alpha=transperancy)
            b_pT, = host.plot(plots[collum][1], plots[collum][2], color=pTbcolor,ls='--', label="p$_{T}$(b)",linewidth=linewidth,alpha=transperancy)
            h_dR, = dR.plot(plots[collum][1], plots[collum][23], color=dRhcolor , label="$\Delta$R(hh$_{S}$)",linewidth=linewidth)
            b_dR, = dR.plot(plots[collum][1], plots[collum][17], color=dRbcolor , label="$\Delta$R(bb)",linewidth=linewidth)
            # dR.axhline(1.5,c=linecolor)

            lnshost= [H_pT,SM_pT,b_pT]
            lnsdR=[b_dR,h_dR]
            if dR.is_last_col():
                dR.legend(handles=lnsdR, loc='upper right',prop={'size': legendsize})
                dR.text(maxMH-225,0.5,'0.4',color=linecolor, fontsize=15)
                dR.text(maxMH-225,0.9,'0.8',color=linecolor, fontsize=15)

            if host.is_first_col():
                host.legend(handles=lnshost, loc='upper left',prop={'size': legendsize})
            
            # dR.yaxis.label.set_color(b_dR.get_color())
            dR.yaxis.label.set_fontsize(fontsize)
            host.yaxis.label.set_fontsize(fontsize)
            host.xaxis.label.set_fontsize(fontsize)

outpath=opts.outDir
name = outpath
for mhS in wanted_mhS:
    name=name+"_"+mhS
check = name
for n in range(50):
    if not os.path.exists(check):
        os.makedirs(check+"/")
        print ("made dir: ", check)
        break
    else:
        check = name + "_{}".format(n)
fig.tight_layout()
plt.savefig(check+'/mean.pdf')

#median
fig = plt.figure(figsize=(20,10))
gs = fig.add_gridspec(2, len(wanted_mhS), hspace=0, wspace=0)
hosts = gs.subplots(sharex='col', sharey='row') 

maxMH=3225
maxpT=1225
minMH=225
minpT=25
maxdR=0
mindR=5.75

a=[None]*len(wanted_mhS)
b=[None]*len(wanted_mhS)
dR_arr =[a,b]
for j in range(2):
    for i in range(len(hosts[0])):
        dR_arr[j][i]=(hosts[j][i].twinx())

for ax in hosts:
    for a in ax:
        a.set_xlim(minMH, maxMH)
        a.set_ylim(minpT,maxpT)
        a.set_xlabel("$m_{H}$ (GeV)")
        a.set_ylabel("median $p_{T}$ (GeV)")
        a.label_outer()

for Rx in dR_arr:
    for R in Rx:
        R.set_ylabel("median $\Delta$R")
        R.set_ylim(0, 5.75)
        lastrow = R.is_last_row()
        lastcol = R.is_last_col()
        if not lastrow:
            for label in R.get_xticklabels(which="both"):
                label.set_visible(False)
            R.get_xaxis().get_offset_text().set_visible(False)
            R.set_xlabel("")
        if not lastcol:
            for label in R.get_yticklabels(which="both"):
                label.set_visible(False)
            R.get_yaxis().get_offset_text().set_visible(False)
            R.set_ylabel("")

dRbcolor='limegreen'
pTbcolor='limegreen'
dRtcolor='deepskyblue'
pTtcolor='deepskyblue'
dRhcolor='k'
pThcolor='k'
linecolor='r'
fontsize=20
legendsize=15
linewidth=3
gridcolor='lightgray'
transperancy=0.25
areacolor='mistyrose'

particle=["bottom","tau"]
collum=-1
for mhS in wanted_mhS:
    collum+=1   
    for part in particle:
        if part == "bottom":
            row = 0
        elif part == "tau":
            row = 1

        host=hosts[row][collum]
        dR = dR_arr[row][collum]

        if part == "tau":
            tindex=0
            tcut=False
            cutindex=len(plots[collum][1])-1
            for value in plots[collum][21]:
                if value <= 0.5:
                    cutindex=tindex
                    tcut=True
                    break
                else:
                    tindex+=1
            if tcut:
                host.axvspan(plots[collum][1][cutindex], maxMH, facecolor=pTtcolor, alpha=0.15)
                host.text(plots[collum][1][cutindex]+50,maxpT/2,'boosted region',color=pTtcolor, fontsize=15,alpha=0.9,rotation=-90)
            host.grid(color=gridcolor, linestyle='--', linewidth=1,alpha=transperancy+0.25)
            dR.axhline(0.5,c=linecolor,label="0,5")
            # H_pT, = host.plot(plots[collum][1], plots[collum][9], color=pThcolor,ls='-.', label="p$_{T}$(H)",linewidth=linewidth,alpha=transperancy)
            LH_pT, = host.plot(plots[collum][1], plots[collum][15], color=pThcolor, ls=':',label="p$_{T}$(h to tau tau)",linewidth=linewidth,alpha=transperancy)
            tau_pT, = host.plot(plots[collum][1], plots[collum][6], color=pTtcolor,ls='--', label="p$_{T}$(tau)",linewidth=linewidth,alpha=transperancy)
            # h_dR, = dR.plot(plots[collum][1], plots[collum][24], color=dRhcolor , label="$\Delta$R(hh$_{S}$)",linewidth=linewidth)
            t_dR, = dR.plot(plots[collum][1], plots[collum][21], color=dRtcolor , label="$\Delta$R(tautau)",linewidth=linewidth)

            lnshost= [LH_pT,tau_pT]
            lnsdR=[t_dR]
            if dR.is_last_col():
                dR.legend(handles=lnsdR, loc='upper right',prop={'size': legendsize})
                dR.text(maxMH-225,0.6,'0.5',color=linecolor, fontsize=15)
            if host.is_first_col():
                host.legend(handles=lnshost, loc='upper left',prop={'size': legendsize})

            # dR.yaxis.label.set_color(t_dR.get_color())
            dR.yaxis.label.set_fontsize(fontsize)
            host.yaxis.label.set_fontsize(fontsize)
            host.xaxis.label.set_fontsize(fontsize)


        elif part == "bottom":
            bindex=0
            bcut=False
            cutindex=len(plots[collum][1])-1
            for value in plots[collum][18]:
                if value <= 0.4:
                    cutindex=bindex
                    bcut=True
                    break
                else:
                    bindex+=1
            if bcut:
                host.axvspan(plots[collum][1][cutindex-1], maxMH, facecolor=pTbcolor, alpha=0.15)
                host.text(plots[collum][1][cutindex-1]+50,maxpT/2,'boosted region',color=pTbcolor, fontsize=15,alpha=0.9,rotation=-90)
            host.grid(color=gridcolor, linestyle='--', linewidth=1,alpha=transperancy+0.25)
            dR.axhline(0.4,c=linecolor,label="0,4")
            dR.axhline(0.8,c=linecolor,label="0,8")
            host.set_title("$m_{h_{S}}$ =" +mhS+ " GeV",fontsize=fontsize,color=pTbcolor)
            H_pT, = host.plot(plots[collum][1], plots[collum][9], color=pThcolor,ls='-.', label="p$_{T}$(H)",linewidth=linewidth,alpha=transperancy)
            SM_pT, = host.plot(plots[collum][1], plots[collum][12], color=pThcolor,ls=':', label="p$_{T}$(h$_{S}$ to bb)",linewidth=linewidth,alpha=transperancy)
            b_pT, = host.plot(plots[collum][1], plots[collum][3], color=pTbcolor,ls='--', label="p$_{T}$(b)",linewidth=linewidth,alpha=transperancy)
            h_dR, = dR.plot(plots[collum][1], plots[collum][24], color=dRhcolor , label="$\Delta$R(hh$_{S}$)",linewidth=linewidth)
            b_dR, = dR.plot(plots[collum][1], plots[collum][18], color=dRbcolor , label="$\Delta$R(bb)",linewidth=linewidth)
            # dR.axhline(1.5,c=linecolor)

            lnshost= [H_pT,SM_pT,b_pT]
            lnsdR=[b_dR,h_dR]
            if dR.is_last_col():
                dR.legend(handles=lnsdR, loc='upper right',prop={'size': legendsize})
                dR.text(maxMH-225,0.5,'0.4',color=linecolor, fontsize=15)
                dR.text(maxMH-225,0.9,'0.8',color=linecolor, fontsize=15)

            if host.is_first_col():
                host.legend(handles=lnshost, loc='upper left',prop={'size': legendsize})
            
            # dR.yaxis.label.set_color(b_dR.get_color())
            dR.yaxis.label.set_fontsize(fontsize)
            host.yaxis.label.set_fontsize(fontsize)
            host.xaxis.label.set_fontsize(fontsize)

fig.tight_layout()
plt.savefig(check+'/median.pdf')