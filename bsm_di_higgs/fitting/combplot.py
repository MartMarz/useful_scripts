from matplotlib import pyplot as plt
import numpy as np
from matplotlib import gridspec
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec


mH= [600,700,800,900,1000,1200]

baselimit = [0.0308,0.0269,0.0239,0.0200,0.0151,0.0112]

nodR_0AK_normalVarslimit= [0.0308,0.0269,0.0239,0.0200,0.0151,0.0112]

nodR_0AK_boostedVarslimit= [0.0239,0.0200,0.0161,0.0142,0.0103,0.007]

nodR_1AK_normalVarslimit= [0.0239,0.0210,0.0190,0.0181,0.0142,0.0112]

nodR_1AK_boostedVarslimit= [0.0200,0.0161,0.0146,0.0122,0.0093,0.0073]

yesdR_1AK_normalVarslimit= [0.0220,0.0190,0.0151,0.0122,0.0093,0.0073]

yesdR_1AK_boostedVarslimit= [0.0190,0.0146,0.0112,0.0093,0.0063,0.0054]

yesdR_0AK_normalVarslimit= [0.0278,0.0220,0.0171,0.0132,0.0103,0.0073]

yesdR_0AK_boostedVarslimit= [0.0210,0.0171,0.0112,0.0093,0.0063,0.0054]


ratio_nodR_0AK_boostedVarslimit= []
ratio_nodR_1AK_normalVarslimit= []
ratio_nodR_1AK_boostedVarslimit= []
ratio_yesdR_1AK_normalVarslimit= []
ratio_yesdR_1AK_boostedVarslimit= []
ratio_yesdR_0AK_normalVarslimit= []
ratio_yesdR_0AK_boostedVarslimit= []
for n in range(len(mH)):
    ratio_nodR_0AK_boostedVarslimit.append((nodR_0AK_boostedVarslimit[n])/baselimit[n])
    ratio_nodR_1AK_normalVarslimit.append((nodR_1AK_normalVarslimit[n])/baselimit[n])
    ratio_nodR_1AK_boostedVarslimit.append((nodR_1AK_boostedVarslimit[n])/baselimit[n])
    ratio_yesdR_1AK_normalVarslimit.append((yesdR_1AK_normalVarslimit[n])/baselimit[n])
    ratio_yesdR_1AK_boostedVarslimit.append((yesdR_1AK_boostedVarslimit[n])/baselimit[n])
    ratio_yesdR_0AK_normalVarslimit.append((yesdR_0AK_normalVarslimit[n])/baselimit[n])
    ratio_yesdR_0AK_boostedVarslimit.append((yesdR_0AK_boostedVarslimit[n])/baselimit[n])


fig, (ax,ax1)= plt.subplots(2, 1, gridspec_kw={'height_ratios': [3,1], 'hspace':0.1}, sharex=True)
fig.subplots_adjust(top=0.85)
ax1.set_xlabel("$m_{H}$ (GeV)")
ax.set_ylabel(r"95% CL limit on $\sigma$B(H$\rightarrow$hh$_{S}\rightarrow\tau\tau$bb) (pb)")
ax1.set_ylabel(r"$\frac{approach}{baseline}$")

ax.text(550, 0.045, 'CMS simulation', fontdict=None,size=20,weight='bold',color='black')
ax.text(575, 0.0425, 'work in progress', fontdict=None,size=10,weight='bold')
ax.text(1100, 0.0425, '$m_{h_{S}}$ = 60 GeV', fontdict=None,size=14)

ax.plot(mH, nodR_0AK_normalVarslimit, 'x-', color='red',label="baseline")
# ax.plot(mH, nodR_0AK_boostedVarslimit, 'x-', color='black',label="Feat.")
# ax.plot(mH, nodR_1AK_normalVarslimit, 'x--', color='red',label=r"N$_{AK8}$")
ax.plot(mH, nodR_1AK_boostedVarslimit, 'x--', color='black',label=r"Feat.+N$_{AK8}$")
# ax.plot(mH, yesdR_0AK_normalVarslimit, '^-', color='red',label="Split.")
ax.plot(mH, yesdR_0AK_boostedVarslimit, '^-', color='black',label="Feat.+Split.")
ax.plot(mH, yesdR_1AK_normalVarslimit, '^--', color='red',label=r"Split.+N$_{AK8}$")
ax.plot(mH, yesdR_1AK_boostedVarslimit, '^--', color='black',label=r"Feat.+Split.+N$_{AK8}$")

# ax1.plot(mH, ratio_nodR_0AK_boostedVarslimit, 'x-', color='black')
# ax1.plot(mH, ratio_nodR_1AK_normalVarslimit, 'x--', color='red')
ax1.plot(mH, ratio_nodR_1AK_boostedVarslimit, 'x--', color='black')
# ax1.plot(mH, ratio_yesdR_0AK_normalVarslimit, '^-', color='red')
ax1.plot(mH, ratio_yesdR_0AK_boostedVarslimit, '^-', color='black')
ax1.plot(mH, ratio_yesdR_1AK_normalVarslimit, '^--', color='red')
ax1.plot(mH, ratio_yesdR_1AK_boostedVarslimit, '^--', color='black')
ax1.hlines(1,550,1250,'black')

ax.legend(loc="upper right")

ax.set_ylim([0.002, 0.04])
ax1.set_ylim([0.2, 1.05])
ax1.set_xlim([550, 1250])


plt.savefig('on_their_own_ratio.pdf')