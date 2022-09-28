from matplotlib import pyplot as plt
import numpy as np
from matplotlib import gridspec
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec


mH= [600,700,800,900,1000,1200]

baselimit_bb= [0.0396,0.0303,0.0249, 0.0200,0.0151,0.0112]
baselimit_tautau=[0.0513,0.0581,0.0781,0.1030, 0.1147,0.1890]

yesdR_0AK_normalVarslimit_bb= [0.0327,0.0239,0.0171, 0.0132,0.0103,0.0073]
yesdR_0AK_normalVarslimit_tautau=[0.0522,0.0586,0.0845,0.1147, 0.1118,0.2012]

nodR_1AK_normalVarslimit_bb= [0.0308,0.0259,0.0210, 0.0190,0.0142,0.0112]
nodR_1AK_normalVarslimit_tautau=[0.0366,0.0361,0.0439,0.0542, 0.0688,0.1147]

nodR_0AK_boostedVarslimit_bb= [0.0317,0.0239,0.0171, 0.0142,0.0103,0.0073]
nodR_0AK_boostedVarslimit_tautau=[0.0376,0.0396,0.0513,0.0679, 0.0669,0.1030]

baselimit=baselimit_tautau
nodR_0AK_boostedVarslimit = nodR_0AK_boostedVarslimit_tautau
nodR_1AK_normalVarslimit = nodR_1AK_normalVarslimit_tautau
yesdR_0AK_normalVarslimit = yesdR_0AK_normalVarslimit_tautau

ratio_nodR_0AK_boostedVarslimit= []
ratio_nodR_1AK_normalVarslimit= []
ratio_yesdR_0AK_normalVarslimit= []

for n in range(len(mH)):
    ratio_nodR_0AK_boostedVarslimit.append((nodR_0AK_boostedVarslimit[n])/baselimit[n])
    ratio_nodR_1AK_normalVarslimit.append((nodR_1AK_normalVarslimit[n])/baselimit[n])
    ratio_yesdR_0AK_normalVarslimit.append((yesdR_0AK_normalVarslimit[n])/baselimit[n])


fig, (ax,ax1)= plt.subplots(2, 1, gridspec_kw={'height_ratios': [3,1], 'hspace':0.1}, sharex=True)
fig.subplots_adjust(top=0.85)
ax1.set_xlabel("$m_{H}$ (GeV)")
ax.set_ylabel(r"95% CL limit on $\sigma$B(H$\rightarrow$hh$_{S}\rightarrow\tau\tau$bb) (pb)")
ax1.set_ylabel(r"$\frac{approach}{baseline}$")

ax.text(550, 0.24, 'CMS simulation', fontdict=None,size=20,weight='bold',color='black')
ax.text(575, 0.23, 'work in progress', fontdict=None,size=10,weight='bold')
ax.text(1100, 0.23, '$m_{h_{S}}$ = 60 GeV', fontdict=None,size=14)

ax.plot(mH, baselimit, 'x-', color='red',label=r"baseline h$_S\rightarrow\tau\tau$")
ax.plot(mH, nodR_0AK_boostedVarslimit, 'x-', color='black',label=r"Feat. h$_S\rightarrow\tau\tau$")
ax.plot(mH, nodR_1AK_normalVarslimit, 'x--', color='red',label=r"N$_{AK8}$ h$_S\rightarrow\tau\tau$")
ax.plot(mH, yesdR_0AK_normalVarslimit, '^-', color='red',label=r"Split. h$_S\rightarrow\tau\tau$")

ax1.plot(mH, ratio_nodR_0AK_boostedVarslimit, 'x-', color='black')
ax1.plot(mH, ratio_nodR_1AK_normalVarslimit, 'x--', color='red')
ax1.plot(mH, ratio_yesdR_0AK_normalVarslimit, '^-', color='red')

ax1.hlines(1,550,1250,'black')

ax.legend(loc="upper left")

ax.set_ylim([0.03, 0.22])
ax1.set_ylim([0.2, 1.2])
ax1.set_xlim([550, 1250])


plt.savefig('on_their_own_ratio_tautau.pdf')