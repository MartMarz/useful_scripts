from matplotlib import pyplot as plt
import numpy as np
from matplotlib import gridspec
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

node= ['combine','hS_bb','hS_tautau','ttbar','Wjet','Zll']
combErr=[[0.025883],[0.0261831]]
bbErr=[[0.034924],[0.0355302]]
tautauErr=[[0.0391286],[0.0397417]]
ttErr=[[1.99902],[2.01887]]
WjErr=[[2.52568],[2.59661]]
ZllErr=[[0.191115],[0.199911]]
ylower=0.5
yupper=1.5
xlower=0.25
xupper=0.75
errorwidth=1.2
capsize=5


fig = plt.figure()

gs = fig.add_gridspec(1, 6, hspace=0, wspace=0)
(ax1, ax2, ax3, ax4, ax5, ax6) = gs.subplots(sharex='col', sharey='row')

ax1.errorbar([0.5], [1], yerr=combErr, fmt='.', color='k',  ecolor='r',capsize=capsize, elinewidth=errorwidth)
ax1.set_xlim(xlower,xupper)
ax1.set_ylim(ylower,yupper)
ax1.get_xaxis().set_ticks([])
ax1.set_xlabel('comb')
ax1.set_ylabel(r'best fit $\sigma$B(H$\rightarrow$hh$_{S}\rightarrow\tau\tau$bb)')

ax2.errorbar([0.5], [1], yerr=bbErr, fmt='.', color='k',  ecolor='r',  capsize=capsize, elinewidth=errorwidth)
ax2.set_xlim(xlower,xupper)
ax2.set_ylim(ylower,yupper)
ax2.get_xaxis().set_ticks([])
ax2.set_xlabel('hS_bb')

ax3.errorbar([0.5], [1], yerr=tautauErr, fmt='.', color='k',  ecolor='r',capsize=capsize, elinewidth=errorwidth)
ax3.set_xlim(xlower,xupper)
ax3.set_ylim(ylower,yupper)
ax3.get_xaxis().set_ticks([])
ax3.set_xlabel('hS_tautau')

ax4.errorbar([0.5], [1], yerr=ttErr, fmt='.', color='k',  ecolor='r',capsize=capsize, elinewidth=errorwidth)
ax4.set_xlim(xlower,xupper)
ax4.set_ylim(ylower,yupper)
ax4.get_xaxis().set_ticks([])
ax4.set_xlabel('ttbar')

ax5.errorbar([0.5], [1], yerr=WjErr, fmt='.', color='k',  ecolor='r',capsize=capsize, elinewidth=errorwidth)
ax5.set_xlim(xlower,xupper)
ax5.set_ylim(ylower,yupper)
ax5.get_xaxis().set_ticks([])
ax5.set_xlabel('Wjet')

ax6.errorbar([0.5], [1], yerr=ZllErr, fmt='.', color='k',  ecolor='r',capsize=capsize, elinewidth=errorwidth)
ax6.set_xlim(xlower,xupper)
ax6.set_ylim(ylower,yupper)
ax6.get_xaxis().set_ticks([])
ax6.set_xlabel('Zll')

plt.figtext(0.035, 0.95, 'CMS simulation', fontdict=None,size=20,weight='bold')
plt.figtext(0.035, 0.92, 'work in progress', fontdict=None,size=10,weight='bold')
plt.figtext(0.7, 0.92, 'baseline NN', fontdict=None,size=14)
plt.figtext(0.85, 0.03, 'node', fontdict=None,size=14)


plt.savefig('uncert.pdf')