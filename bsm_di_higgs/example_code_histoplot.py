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

# Use data in the form of arrays inside an array:
# plots[point,point,point,....]
# 
# point =  [wan_mhS,MH_arr,    #0
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

#2D mass
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from matplotlib.patches import Polygon
# canvas properties
width = 30.
height = 25.
ratio = width/height
fig = plt.figure(figsize=(width,height))

# seperate canvas for use of colour bars (depends how many different variables one wants to plot)
gs  = gridspec.GridSpec(1, 2, width_ratios=[width, 1] ,wspace=0.02)
gs1 = GridSpecFromSubplotSpec(1, 1, subplot_spec=gs[0])
# gs2 = GridSpecFromSubplotSpec(3, 1, height_ratios=[1,1,1], subplot_spec=gs[1],hspace=0.125)
gs2 = GridSpecFromSubplotSpec(1, 1, subplot_spec=gs[1])
# plt.subplots_adjust(wspace=0.02)
ax = fig.add_subplot(gs1[0])
ax1 = fig.add_subplot(gs2[0])
# ax2 = fig.add_subplot(gs2[2])
# ax3 = fig.add_subplot(gs2[1])
# ax2 = fig.add_subplot(gs2[1])
# ax3 = fig.add_subplot(gs2[0])

plt.figtext(0.025, 0.95, 'CMS simulation', fontdict=None,size=60,weight='bold')
plt.figtext(0.025, 0.92, 'work in progress', fontdict=None,size=50,weight='bold')

# axis max and min values
maxMH=3225
maxmhS=3225
minMH=225
minmhS=25

# define arrays for values of different hypotheses (mean and median)
mean_quadruplets=[]
median_quadruplets=[]
counter_tuple = []

# fill arrays with needed values (point is defined at the end of script) structure = plots[point,point,...]
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

# color and size options
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

# build my own x&y-axis with given masspoints
xtix=[0]
for mH in plots[0][1]:
    xtix.append(str(format(mH, ".0f")))
ytix=[0]
for mh in wanted_mhS_2D:
    ytix.append(mh)

# maximum value of the colour bar here acceptence
maxval=1.
# Draw the Histogramm and fill with the acceptence if wanted
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

# fill the dR Values of the two pairs
maxvaltau=0.5
maxvalb=0.4
for quad in median_quadruplets:
    MHindex=plots[0][1].index(quad[1])
    MHposition=MHindex+1
    mhindex=np.where(wanted_mhS_2D==str(quad[0]))[0][0]
    mhposition=mhindex+1
    ax.text(MHposition-0.25, mhposition+0.05, "{}".format(format(quad[2], ".2f")), style='italic',color=dRtcolor)
    ax.text(MHposition-0.25, mhposition-0.35, "{}".format(format(quad[3], ".2f")), style='italic',color=dRbcolor)
    if quad[2] <= 0.5 and quad[3] > 0.4:
        ax.add_patch(Rectangle((MHposition-0.5, mhposition-0.5), 1, 1, linewidth=1, edgecolor='black', facecolor=cmap_tau(quad[2]/maxvaltau),alpha=1))
    elif quad[3] <= 0.4 and quad[2] > 0.5:
        ax.add_patch(Rectangle((MHposition-0.5, mhposition-0.5), 1, 1, linewidth=1, edgecolor='black', facecolor=cmap_b(quad[3]/maxvalb),alpha=1))
    elif quad[2] <= 0.5 and quad[3] <= 0.4:
        ax.add_patch(Polygon([[MHposition-0.5,mhposition-0.5],[MHposition-0.5,mhposition+0.5],[MHposition+0.5,mhposition+0.5]], closed=True, linewidth=1, edgecolor='black', facecolor=cmap_tau(quad[2]/0.5),alpha=1))
        ax.add_patch(Polygon([[MHposition-0.5,mhposition-0.5],[MHposition+0.5,mhposition-0.5],[MHposition+0.5,mhposition+0.5]], closed=True, linewidth=1, edgecolor='black', facecolor=cmap_b(quad[3]/0.4),alpha=1))

# draw the axis

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

# legend

# ax.text(0.5,len(wanted_mhS_2D)-3, 'median $\Delta$R(ττ)$< 0.5$', style='italic', fontsize=fontsize, color='black',
#         bbox={'facecolor': cmap_tau(0.5), 'alpha': 0.5, 'pad': 10})
# ax.text(0.5,len(wanted_mhS_2D)-1, 'median $\Delta$R(bb)$< 0.4$', style='italic', fontsize=fontsize, color='black',
#         bbox={'facecolor': cmap_b(0.5), 'alpha': 0.5, 'pad': 10})
# ax.text(0.5,len(wanted_mhS_2D)-1, '$\epsilon_{cuts}$< 0.2', style='italic', fontsize=fontsize, color='black',
#         bbox={'facecolor': cmap_eff(0.5), 'alpha': 0.5, 'pad': 10})

# plot the colourbars
ax.yaxis.label.set_fontsize(fontsize+10)
ax.xaxis.label.set_fontsize(fontsize+10)

norm_eff = mpl.colors.Normalize(vmin=0, vmax=maxval)
cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap_eff,
                                norm=norm_eff,
                                orientation='vertical')
cb1.set_label('acceptance', rotation='vertical', fontsize=fontsize+10, position=(0,0.5))
cb1.ax.tick_params(labelsize=fontsize)
cb1.ax.locator_params(nbins=2)

# norm_tau = mpl.colors.Normalize(vmin=0, vmax=maxvaltau)
# cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap_tau,
#                                 norm=norm_tau,
#                                 orientation='vertical')
# cb2.set_label('$\Delta$R(h to ττ)', rotation='vertical', fontsize=fontsize+5, position=(0,0.5))
# cb2.ax.tick_params(labelsize=fontsize)
# cb2.ax.locator_params(nbins=2)

# norm_b = mpl.colors.Normalize(vmin=0, vmax=maxvalb)
# cb3 = mpl.colorbar.ColorbarBase(ax3, cmap=cmap_b,
#                                 norm=norm_b,
#                                 orientation='vertical')
# cb3.set_label('$\Delta$R(h$_S$ to bb)', rotation='vertical', fontsize=fontsize+5, position=(0,0.5))
# cb3.ax.tick_params(labelsize=fontsize)
# cb3.ax.locator_params(nbins=2)

# plt.show()
# fig.tight_layout()

# save plot (check for overwrite)
plt.savefig(check+'/2D_combined_plot.pdf')
