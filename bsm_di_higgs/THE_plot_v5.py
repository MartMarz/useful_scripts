from __future__ import print_function
from optparse import OptionParser
from math import *
import os
from sqlite3 import Row
from telnetlib import TELNET_PORT
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import gridspec
from matplotlib.ticker import FormatStrFormatter
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
    number= histo.Integral()
    return mean_val, median_val, std_dev, number

files=[]
for (dirpath, dirnames, filenames) in os.walk(args[0]):
    for file in filenames:
        if file.find("_MH_") >= 0:
            files.append([file,find_masses(file)])

histos=["bquark_pt","tau_pt","HeavyHiggs_pt","LightHiggs_pt","SMHiggs_pt","higgs_dR","tau_dR","bquark_dR",
        "combined_cut_counter","combined_tau_cut_counter","event_counter","found_counter","b_cut_counter",
        "fulllep_found_counter","semimu_found_counter","semiele_found_counter","had_found_counter",
        "semimu_tau_cut_counter","semiele_tau_cut_counter","had_tau_cut_counter"]
        
wanted_mhS=np.array(["100","170","1400"])
wanted_mhS_2D=np.array(["60","70","80","90","100","120","150","170","190","250","300","350","400","450","500","550","600","650","700","800"
,"900","1000","1200","1300","1400","1600","1800","2000","2200","2400","2600","2800"])


infos=[]
for file in files:
    mhS=file[1][1]
    MH=file[1][0]
    for wan_mhS in wanted_mhS_2D:
        if wan_mhS==mhS:
            for hist in histos:
                mean, median, std_dev, number=calculate(args[0]+file[0],hist+"_MH_"+MH+"_mh_"+mhS)
                infos.append([mhS,float(MH),hist,mean,median,std_dev,number])
infos=sorted(infos)

plots=[]
for wan_mhS in wanted_mhS_2D:
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
    com_counter=[]
    com_tau_counter=[]
    event_counter=[]
    found_counter=[]
    b_cut_counter=[]
    fulllep_counter=[]
    semimu_found_counter=[]
    semiele_found_counter=[]
    had_found_counter=[]
    semimu_cut_counter=[]
    semiele_cut_counter=[]
    had_cut_counter=[]
    for point in infos:
        mhS=point[0]
        MH_val=point[1]
        name=point[2]
        mean=point[3]
        median=point[4]
        std_dev=point[5]
        number=point[6]
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
            elif name=="combined_cut_counter":
                com_counter.append(number)
            elif name=="combined_tau_cut_counter":
                com_tau_counter.append(number)
            elif name=="event_counter":
                event_counter.append(number)
            elif name=="found_counter":
                found_counter.append(number)
            elif name=="b_cut_counter":
                b_cut_counter.append(number)
            elif name=="fulllep_found_counter":
                fulllep_counter.append(number)
            elif name=="semimu_found_counter":
                semimu_found_counter.append(number)
            elif name=="semiele_found_counter":
                semiele_found_counter.append(number)
            elif name=="had_found_counter":
                had_found_counter.append(number)
            elif name=="semimu_tau_cut_counter":
                semimu_cut_counter.append(number)
            elif name=="semiele_tau_cut_counter":
                semiele_cut_counter.append(number)
            elif name=="had_tau_cut_counter":
                had_cut_counter.append(number)

    plots.append(
        [wan_mhS,MH_arr,    #0
        b_pt_mean,b_pt_median,b_pt_std_dev, #2
        t_pt_mean,t_pt_median,t_pt_std_dev, #5
        HH_pt_mean,HH_pt_median,HH_pt_std_dev,  #8
        LH_pt_mean,LH_pt_median,LH_pt_std_dev,  #11
        SM_pt_mean,SM_pt_median,SM_pt_std_dev,  #14
        b_dR_mean,b_dR_median,b_dR_std_dev, #17
        t_dR_mean,t_dR_median,t_dR_std_dev, #20
        h_dR_mean,h_dR_median,h_dR_std_dev, #23
        com_counter,com_tau_counter,event_counter, #26
        found_counter,b_cut_counter,fulllep_counter, #29
        semimu_found_counter,semiele_found_counter,had_found_counter, #32
        semimu_cut_counter,semiele_cut_counter,had_cut_counter]) #35

# print(plots[0])
# print(plots[1])

# More versatile wrapper
# fig, hosts = plt.subplots(2,3,figsize=(20,10)) # (width, height) in inches
# (see https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.subplots.html)
# mean
if len(wanted_mhS)>1:
    fig = plt.figure(figsize=(20,10))
else:
    fig = plt.figure(figsize=(7.3,10))

plt.figtext(0.025, 0.95, 'CMS simulation', fontdict=None,size=30,weight='bold')
plt.figtext(0.025, 0.92, 'work in progress', fontdict=None,size=25,weight='bold')
gs = fig.add_gridspec(2, len(wanted_mhS), hspace=0, wspace=0)
hosts = gs.subplots(sharex='col', sharey='row') 

maxMH=3225
maxpT=1225
minMH=225
minpT=25
maxdR=0
mindR=5.75

if len(wanted_mhS)>1:
    a=[None]*len(wanted_mhS)
    b=[None]*len(wanted_mhS)
    dR_arr =[a,b]
    for j in range(2):
        for i in range(len(hosts[0])):
            dR_arr[j][i]=(hosts[j][i].twinx())
else:
    a=[None]*2
    dR_arr = a
    for j in range(2):
        dR_arr[j]=(hosts[j].twinx())

for ax in hosts:
    if len(wanted_mhS)>1:
        for a in ax:
            a.set_xlim(minMH, maxMH)
            a.set_ylim(minpT,maxpT)
            a.set_xlabel("$m_{H}$ (GeV)")
            a.set_ylabel("mean $p_{T}$ (GeV)")
            a.label_outer()
    else:
        ax.set_xlim(minMH, maxMH)
        ax.set_ylim(minpT,maxpT)
        ax.set_xlabel("$m_{H}$ (GeV)")
        ax.set_ylabel("mean $p_{T}$ (GeV)")
        ax.label_outer()

for Rx in dR_arr:
    if len(wanted_mhS)>1:
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
    else:
        Rx.set_ylabel("mean $\Delta$R")
        Rx.set_ylim(0, 5.75)
        lastrow = Rx.is_last_row()
        lastcol = Rx.is_last_col()
        if not lastrow:
            for label in Rx.get_xticklabels(which="both"):
                label.set_visible(False)
            Rx.get_xaxis().get_offset_text().set_visible(False)
            Rx.set_xlabel("")
        if not lastcol:
            for label in Rx.get_yticklabels(which="both"):
                label.set_visible(False)
            Rx.get_yaxis().get_offset_text().set_visible(False)
            Rx.set_ylabel("")

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
plotsindex=-1
for mhS2D in wanted_mhS_2D:
    plotsindex+=1
    for mhs in wanted_mhS:
        if mhs==mhS2D:
            collum+=1  
            for part in particle:
                if part == "bottom":
                    row = 0
                elif part == "tau":
                    row = 1

                if len(wanted_mhS)>1:
                    host=hosts[row][collum]
                    dR = dR_arr[row][collum]
                else:
                    host=hosts[row]
                    dR = dR_arr[row]

                if part == "tau":
                    tindex=0
                    tcut=False
                    cutindex=len(plots[plotsindex][1])-1
                    for value in plots[plotsindex][20]:
                        if value <= 0.5:
                            cutindex=tindex
                            tcut=True
                            break
                        else:
                            tindex+=1
                    if tcut:
                        host.axvspan(plots[plotsindex][1][cutindex]-250, maxMH, facecolor=pTtcolor, alpha=0.15)
                        host.text(plots[plotsindex][1][cutindex]-200,maxpT/3,'boosted region',color=pTtcolor, fontsize=15,alpha=0.9,rotation=-90)
                    host.grid(color=gridcolor, linestyle='--', linewidth=1,alpha=transperancy+0.25)
                    dR.axhline(0.5,c=linecolor,label="0,5")
                    # H_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][8], color=pThcolor,ls='-.', label="p$_{T}$(H)",linewidth=linewidth,alpha=transperancy)
                    LH_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][14], color=pThcolor, ls=':',label="p$_{T}$(h to tau tau)",linewidth=linewidth,alpha=transperancy)
                    tau_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][5], color=pTtcolor,ls='--', label="p$_{T}$(tau)",linewidth=linewidth,alpha=transperancy)
                    # h_dR, = dR.plot(plots[plotsindex][1], plots[plotsindex][23], color=dRhcolor , label="$\Delta$R(hh$_{S}$)",linewidth=linewidth)
                    t_dR, = dR.plot(plots[plotsindex][1], plots[plotsindex][20], color=dRtcolor , label="$\Delta$R(tautau)",linewidth=linewidth)

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
                    cutindex=len(plots[plotsindex][1])-1
                    for value in plots[plotsindex][17]:
                        if value <= 0.4:
                            cutindex=bindex
                            bcut=True
                            break
                        else:
                            bindex+=1
                    if bcut:
                        host.axvspan(plots[plotsindex][1][cutindex-1], maxMH, facecolor=pTbcolor, alpha=0.15)
                        host.text(plots[plotsindex][1][cutindex-1]+50,maxpT/3,'boosted region',color=pTbcolor, fontsize=15,alpha=0.9,rotation=-90)
                    host.grid(color=gridcolor, linestyle='--', linewidth=1,alpha=transperancy+0.25)
                    dR.axhline(0.4,c=linecolor,label="0,4")
                    dR.axhline(0.8,c=linecolor,label="0,8")
                    host.set_title("$m_{h_{S}}$ =" +mhs+ " GeV",fontsize=fontsize,color=pTbcolor)
                    H_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][8], color=pThcolor,ls='-.', label="p$_{T}$(H)",linewidth=linewidth,alpha=transperancy)
                    SM_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][11], color=pThcolor,ls=':', label="p$_{T}$(h$_{S}$ to bb)",linewidth=linewidth,alpha=transperancy)
                    b_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][2], color=pTbcolor,ls='--', label="p$_{T}$(b)",linewidth=linewidth,alpha=transperancy)
                    h_dR, = dR.plot(plots[plotsindex][1], plots[plotsindex][23], color=dRhcolor , label="$\Delta$R(hh$_{S}$)",linewidth=linewidth)
                    b_dR, = dR.plot(plots[plotsindex][1], plots[plotsindex][17], color=dRbcolor , label="$\Delta$R(bb)",linewidth=linewidth)
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
# fig.tight_layout()
plt.savefig(check+'/mean.pdf')

#median
if len(wanted_mhS)>1:
    fig = plt.figure(figsize=(20,10))
else:
    fig = plt.figure(figsize=(7.3,10))

plt.figtext(0.025, 0.95, 'CMS simulation', fontdict=None,size=30,weight='bold')
plt.figtext(0.025, 0.92, 'work in progress', fontdict=None,size=25,weight='bold')
gs = fig.add_gridspec(2, len(wanted_mhS), hspace=0, wspace=0)
hosts = gs.subplots(sharex='col', sharey='row') 

maxMH=3225
maxpT=1225
minMH=225
minpT=25
maxdR=0
mindR=5.75

if len(wanted_mhS)>1:
    a=[None]*len(wanted_mhS)
    b=[None]*len(wanted_mhS)
    dR_arr =[a,b]
    for j in range(2):
        for i in range(len(hosts[0])):
            dR_arr[j][i]=(hosts[j][i].twinx())
else:
    a=[None]*2
    dR_arr = a
    for j in range(2):
        dR_arr[j]=(hosts[j].twinx())

for ax in hosts:
    if len(wanted_mhS)>1:
        for a in ax:
            a.set_xlim(minMH, maxMH)
            a.set_ylim(minpT,maxpT)
            a.set_xlabel("$m_{H}$ (GeV)")
            a.set_ylabel("median $p_{T}$ (GeV)")
            a.label_outer()
    else:
        ax.set_xlim(minMH, maxMH)
        ax.set_ylim(minpT,maxpT)
        ax.set_xlabel("$m_{H}$ (GeV)")
        ax.set_ylabel("median $p_{T}$ (GeV)")
        ax.label_outer()

for Rx in dR_arr:
    if len(wanted_mhS)>1:
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
    else:
        Rx.set_ylabel("median $\Delta$R")
        Rx.set_ylim(0, 5.75)
        lastrow = Rx.is_last_row()
        lastcol = Rx.is_last_col()
        if not lastrow:
            for label in Rx.get_xticklabels(which="both"):
                label.set_visible(False)
            Rx.get_xaxis().get_offset_text().set_visible(False)
            Rx.set_xlabel("")
        if not lastcol:
            for label in Rx.get_yticklabels(which="both"):
                label.set_visible(False)
            Rx.get_yaxis().get_offset_text().set_visible(False)
            Rx.set_ylabel("")

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
plotsindex=-1
for mhS2D in wanted_mhS_2D:
    plotsindex+=1
    for mhs in wanted_mhS:
        if mhs==mhS2D:
            collum+=1   
            for part in particle:
                if part == "bottom":
                    row = 0
                elif part == "tau":
                    row = 1
                
                if len(wanted_mhS)>1:
                    host=hosts[row][collum]
                    dR = dR_arr[row][collum]
                else:
                    host=hosts[row]
                    dR = dR_arr[row]

                if part == "tau":
                    tindex=0
                    tcut=False
                    cutindex=len(plots[plotsindex][1])-1
                    for value in plots[plotsindex][21]:
                        if value <= 0.5:
                            cutindex=tindex
                            tcut=True
                            break
                        else:
                            tindex+=1
                    if tcut:
                        host.axvspan(plots[plotsindex][1][cutindex], maxMH, facecolor=pTtcolor, alpha=0.15)
                        host.text(plots[plotsindex][1][cutindex]+50,maxpT/3,'boosted region',color=pTtcolor, fontsize=15,alpha=0.9,rotation=-90)
                    host.grid(color=gridcolor, linestyle='--', linewidth=1,alpha=transperancy+0.25)
                    dR.axhline(0.5,c=linecolor,label="0,5")
                    # H_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][9], color=pThcolor,ls='-.', label="p$_{T}$(H)",linewidth=linewidth,alpha=transperancy)
                    LH_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][15], color=pThcolor, ls=':',label="p$_{T}$(h to tau tau)",linewidth=linewidth,alpha=transperancy)
                    tau_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][6], color=pTtcolor,ls='--', label="p$_{T}$(tau)",linewidth=linewidth,alpha=transperancy)
                    # h_dR, = dR.plot(plots[plotsindex][1], plots[plotsindex][24], color=dRhcolor , label="$\Delta$R(hh$_{S}$)",linewidth=linewidth)
                    t_dR, = dR.plot(plots[plotsindex][1], plots[plotsindex][21], color=dRtcolor , label="$\Delta$R(tautau)",linewidth=linewidth)

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
                    cutindex=len(plots[plotsindex][1])-1
                    for value in plots[plotsindex][18]:
                        if value <= 0.4:
                            cutindex=bindex
                            bcut=True
                            break
                        else:
                            bindex+=1
                    if bcut:
                        host.axvspan(plots[plotsindex][1][cutindex-1], maxMH, facecolor=pTbcolor, alpha=0.15)
                        host.text(plots[plotsindex][1][cutindex-1]+50,maxpT/3,'boosted region',color=pTbcolor, fontsize=15,alpha=0.9,rotation=-90)
                    host.grid(color=gridcolor, linestyle='--', linewidth=1,alpha=transperancy+0.25)
                    dR.axhline(0.4,c=linecolor,label="0,4")
                    dR.axhline(0.8,c=linecolor,label="0,8")
                    host.set_title("$m_{h_{S}}$ =" +mhs+ " GeV",fontsize=fontsize,color=pTbcolor)
                    H_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][9], color=pThcolor,ls='-.', label="p$_{T}$(H)",linewidth=linewidth,alpha=transperancy)
                    SM_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][12], color=pThcolor,ls=':', label="p$_{T}$(h$_{S}$ to bb)",linewidth=linewidth,alpha=transperancy)
                    b_pT, = host.plot(plots[plotsindex][1], plots[plotsindex][3], color=pTbcolor,ls='--', label="p$_{T}$(b)",linewidth=linewidth,alpha=transperancy)
                    h_dR, = dR.plot(plots[plotsindex][1], plots[plotsindex][24], color=dRhcolor , label="$\Delta$R(hh$_{S}$)",linewidth=linewidth)
                    b_dR, = dR.plot(plots[plotsindex][1], plots[plotsindex][18], color=dRbcolor , label="$\Delta$R(bb)",linewidth=linewidth)
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

# fig.tight_layout()
plt.savefig(check+'/median.pdf')

#2D mass
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.patches import Polygon
width = 30.
height = 25.
ratio = width/height
fig = plt.figure(figsize=(width,height))
gs  = gridspec.GridSpec(1, 2, width_ratios=[width, 1] ,wspace=0.02)
gs1 = GridSpecFromSubplotSpec(1, 1, subplot_spec=gs[0])
gs2 = GridSpecFromSubplotSpec(3, 1, height_ratios=[1,1,1], subplot_spec=gs[1],hspace=0.125)
# plt.subplots_adjust(wspace=0.02)
ax = fig.add_subplot(gs1[0])
ax1 = fig.add_subplot(gs2[0])
ax2 = fig.add_subplot(gs2[2])
ax3 = fig.add_subplot(gs2[1])

plt.figtext(0.025, 0.95, 'CMS simulation', fontdict=None,size=60,weight='bold')
plt.figtext(0.025, 0.92, 'work in progress', fontdict=None,size=50,weight='bold')

maxMH=3225
maxmhS=3225
minMH=225
minmhS=25
mean_quadruplets=[]
median_quadruplets=[]
counter_tuple = []

for point in plots:
    dRt_mean=point[20]
    dRb_mean=point[17]

    dRt_median=point[21]
    dRb_median=point[18]

    event_counter = point[28]
    found = point[29]
    b_counter = point[30]
    tau_counter = point[27]
    comb_cut_counter = point[26]
    fulllep_found = point[31]

    for mH in point[1]:
        mean_quad=[int(point[0]),mH,dRt_mean[point[1].index(mH)],dRb_mean[point[1].index(mH)]]
        mean_quadruplets.append(mean_quad)
        median_quad=[int(point[0]),mH,dRt_median[point[1].index(mH)],dRb_median[point[1].index(mH)]]
        median_quadruplets.append(median_quad)
        counter_list=[int(point[0]),mH,event_counter[point[1].index(mH)],found[point[1].index(mH)],b_counter[point[1].index(mH)],
                        tau_counter[point[1].index(mH)],comb_cut_counter[point[1].index(mH)],fulllep_found[point[1].index(mH)]]
        counter_tuple.append(counter_list)

mhlist,MHlist,tlist,blist=zip(*mean_quadruplets)

dRbcolor='forestgreen'
pTbcolor='limegreen'
dRtcolor='royalblue'
pTtcolor='deepskyblue'
dRhcolor='k'
pThcolor='k'
linecolor='r'
fontsize=40
legendsize=15
linewidth=3
gridcolor='lightgray'
transperancy=0.25
areacolor='mistyrose'
cmap_eff = mpl.cm.Reds_r
cmap_tau = mpl.cm.Blues_r
cmap_b = mpl.cm.Greens_r

ax.set_xlim(0, len(plots[0][1])+1)
ax.set_ylim(0, len(wanted_mhS_2D)+1)
ax.set_xlabel("$m_{H}$ (GeV)")
ax.set_ylabel("$m_{h_{S}}$ (GeV)")

xtix=[0]
for mH in plots[0][1]:
    xtix.append(str(format(mH, ".0f")))
ytix=[0]
for mh in wanted_mhS_2D:
    ytix.append(mh)

maxval=0.2
for quad in counter_tuple:
    MHindex=plots[0][1].index(quad[1])
    MHposition=MHindex+1
    mhindex=np.where(wanted_mhS_2D==str(quad[0]))[0][0]
    mhposition=mhindex+1

    event_counter = quad[2]
    found = quad[3]
    b_counter = quad[4]
    tau_counter = quad[5]
    comb_cut_counter = quad[6]
    fulllep_found = quad[7]

    b_eff = b_counter/found
    t_eff = tau_counter/(found-fulllep_found)
    com_eff = comb_cut_counter/(found-fulllep_found)
    number_events = found-fulllep_found

    # ax.text(MHposition-0.25, mhposition+0.05, "{}".format(format(com_eff, ".2f")), style='italic',color='black')
    # ax.text(MHposition-0.4, mhposition-0.35, "{equa}".format(nFound=format( found,".0f") , nLep = format(fulllep_found ,".0f"), equa =format(number_events ,".0f")), style='italic',color=dRtcolor,)
    ax.add_patch(Rectangle((MHposition-0.5, mhposition-0.5), 1, 1, linewidth=1, edgecolor='black', facecolor='white',alpha=1))
    if com_eff <= maxval:
        ax.add_patch(Rectangle((MHposition-0.5, mhposition-0.5), 1, 1, linewidth=1, edgecolor='black', facecolor=cmap_eff(com_eff/maxval),alpha=1))

for quad in median_quadruplets:
    MHindex=plots[0][1].index(quad[1])
    MHposition=MHindex+1
    mhindex=np.where(wanted_mhS_2D==str(quad[0]))[0][0]
    mhposition=mhindex+1
    # ax.text(MHposition-0.25, mhposition+0.05, "{}".format(format(quad[2], ".2f")), style='italic',color=dRtcolor)
    # ax.text(MHposition-0.25, mhposition-0.35, "{}".format(format(quad[3], ".2f")), style='italic',color=dRbcolor)
    if quad[2] <= 0.5 and quad[3] > 0.4:
        ax.add_patch(Rectangle((MHposition-0.5, mhposition-0.5), 1, 1, linewidth=1, edgecolor='black', facecolor=cmap_tau(quad[2]/0.5),alpha=1))
    elif quad[3] <= 0.4 and quad[2] > 0.5:
        ax.add_patch(Rectangle((MHposition-0.5, mhposition-0.5), 1, 1, linewidth=1, edgecolor='black', facecolor=cmap_b(quad[3]/0.4),alpha=1))
    elif quad[2] <= 0.5 and quad[3] <= 0.4:
        ax.add_patch(Polygon([[MHposition-0.5,mhposition-0.5],[MHposition-0.5,mhposition+0.5],[MHposition+0.5,mhposition+0.5]], closed=True, linewidth=1, edgecolor='black', facecolor=cmap_tau(quad[2]/0.5),alpha=1))
        ax.add_patch(Polygon([[MHposition-0.5,mhposition-0.5],[MHposition+0.5,mhposition-0.5],[MHposition+0.5,mhposition+0.5]], closed=True, linewidth=1, edgecolor='black', facecolor=cmap_b(quad[3]/0.4),alpha=1))
        
# ax.axhline(4.5,c='red')
# ax.axhline(9.5,c='red')
# ax.axvline(15.5,c='red')
# # ax.set_zlabel("$\Delta$R (tau tau)")
ax.set_xticks(range(len(plots[0][1])+1))
# ax.set_xticks(np.arange(0.5,len(plots[0][1])+1.5,1), minor=True)
ax.set_xticklabels(xtix,fontsize=fontsize, rotation=45)
ax.set_yticks(range(len(wanted_mhS_2D)+1))
# ax.set_yticks(np.arange(0.5,len(wanted_mhS_2D)+1.5,1), minor=True)
ax.set_yticklabels(ytix,fontsize=fontsize)
# ax.grid(which='minor', alpha=0.5,linestyle='--')

ax.text(0.5,len(wanted_mhS_2D)-5, 'median $\Delta$R(ττ)$< 0.5$', style='italic', fontsize=fontsize, color='black',
        bbox={'facecolor': cmap_tau(0.5), 'alpha': 0.5, 'pad': 10})
ax.text(0.5,len(wanted_mhS_2D)-3, 'median $\Delta$R(bb)$< 0.4$', style='italic', fontsize=fontsize, color='black',
        bbox={'facecolor': cmap_b(0.5), 'alpha': 0.5, 'pad': 10})
ax.text(0.5,len(wanted_mhS_2D)-1, '$\epsilon_{cuts}$< 0.2', style='italic', fontsize=fontsize, color='black',
        bbox={'facecolor': cmap_eff(0.5), 'alpha': 0.5, 'pad': 10})

ax.yaxis.label.set_fontsize(fontsize+10)
ax.xaxis.label.set_fontsize(fontsize+10)

norm_eff = mpl.colors.Normalize(vmin=0, vmax=maxval)
cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap_eff,
                                norm=norm_eff,
                                orientation='vertical')
cb1.set_label('$\epsilon_{cuts}$', rotation='vertical', fontsize=fontsize+10, position=(0,0.5))
cb1.ax.tick_params(labelsize=fontsize)
cb1.ax.locator_params(nbins=2)

norm_tau = mpl.colors.Normalize(vmin=0, vmax=0.5)
cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap_tau,
                                norm=norm_tau,
                                orientation='vertical')
cb2.set_label('$\Delta$R(h to ττ)', rotation='vertical', fontsize=fontsize+5, position=(0,0.5))
cb2.ax.tick_params(labelsize=fontsize)
cb2.ax.locator_params(nbins=2)

norm_b = mpl.colors.Normalize(vmin=0, vmax=0.4)
cb3 = mpl.colorbar.ColorbarBase(ax3, cmap=cmap_b,
                                norm=norm_b,
                                orientation='vertical')
cb3.set_label('$\Delta$R(h$_S$ to bb)', rotation='vertical', fontsize=fontsize+5, position=(0,0.5))
cb3.ax.tick_params(labelsize=fontsize)
cb3.ax.locator_params(nbins=2)

# plt.show()
# fig.tight_layout()
plt.savefig(check+'/2D_combined_plot.pdf')

#         [wan_mhS,MH_arr,    #0
#         b_pt_mean,b_pt_median,b_pt_std_dev, #2
#         t_pt_mean,t_pt_median,t_pt_std_dev, #5
#         HH_pt_mean,HH_pt_median,HH_pt_std_dev,  #8
#         LH_pt_mean,LH_pt_median,LH_pt_std_dev,  #11
#         SM_pt_mean,SM_pt_median,SM_pt_std_dev,  #14
#         b_dR_mean,b_dR_median,b_dR_std_dev, #17
#         t_dR_mean,t_dR_median,t_dR_std_dev, #20
#         h_dR_mean,h_dR_median,h_dR_std_dev, #23
#         com_counter,com_tau_counter,event_counter, #26
#         found_counter,b_cut_counter,fulllep_counter, #29
#         semimu_found_counter,semiele_found_counter,had_found_counter, #32
#         semimu_cut_counter,semiele_cut_counter,had_cut_counter]) #35