from matplotlib import pyplot as plt
import numpy as np
from matplotlib import gridspec
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec


mH= [600,700,800,900,1000,1200]

baselimit = [0.0308,0.0269,0.0239,0.0200,0.0151,0.0112]
hSbb= [0.0396,0.0303,0.0249, 0.0200,0.0151,0.0112]
hStautau=[0.0513,0.0581,0.0781,0.1030, 0.1147,0.1890]

hSbb_split= [0.0327,0.0239,0.0171, 0.0132,0.0103,0.0073]
hStautau_split=[0.0522,0.0586,0.0845,0.1147, 0.1118,0.2012]

hSbb_ak= [0.0308,0.0259,0.0210, 0.0190,0.0142,0.0112]
hStautau_ak=[0.0366,0.0361,0.0439,0.0542, 0.0688,0.1147]

hSbb_boost= [0.0317,0.0239,0.0171, 0.0142,0.0103,0.0073]
hStautau_boost=[0.0376,0.0396,0.0513,0.0679, 0.0669,0.1030]

# nodR_0AK_normalVars
# CL95down = [0.0168,0.0147,0.0127,0.0106,0.0080,0.0060]
# CL68down = [0.0225,0.0189,0.0173,0.0144,0.0103,0.0083]
# limit= [0.0308,0.0269,0.0239,0.0200,0.0151,0.0112]
# CL68up = [0.0430,0.0376,0.0335,0.0280,0.0204,0.0166]
# CL95up = [0.0584,0.0503,0.0448,0.0380,0.0280,0.0224]

# nodR_0AK_boostedVars
# CL95down = [0.0131,0.0109,0.0088,0.0075,0.0054,0.0041]
# CL68down = [0.0175,0.0146,0.0120,0.0096,0.0069,0.0053]
# limit= [0.0239,0.0200,0.0161,0.0142,0.0103,0.007]
# CL68up = [0.0335,0.0286,0.0230,0.0200,0.0145,0.0106]
# CL95up = [0.0451,0.0380,0.0316,0.0269,0.0195,0.0146]

# nodR_1AK_normalVars
# CL95down = [0.0123,0.0112,0.0104,0.0096,0.0075,0.0060]
# CL68down = [0.0170,0.0152,0.0136,0.0130,0.0096,0.0076]
# limit= [0.0239,0.0210,0.0190,0.0181,0.0142,0.0112]
# CL68up = [0.0327,0.0294,0.0266,0.0253,0.0200,0.0152]
# CL95up = [0.0443,0.0393,0.0359,0.0341,0.0269,0.0214]

# nodR_1AK_boostedVars
CL95down = [0.0103,0.0088,0.0078,0.0065,0.0049,0.0041]
CL68down = [0.0143,0.0120,0.0108,0.0083,0.0068,0.0053]
limit= [0.0200,0.0161,0.0146,0.0122,0.0093,0.0073]
CL68up = [0.0274,0.0230,0.0207,0.0165,0.0137,0.0106]
CL95up = [0.0370,0.0312,0.0278,0.0226,0.0187,0.0146]

# yesdR_1AK_normalVars
# CL95down = [0.0120,0.0098,0.0080,0.0065,0.0049,0.0041]
# CL68down = [0.0161,0.0136,0.0111,0.0090,0.0068,0.0053]
# limit= [0.0220,0.0190,0.0151,0.0122,0.0093,0.0073]
# CL68up = [0.0314,0.0266,0.0224,0.0180,0.0137,0.0115]
# CL95up = [0.0428,0.0359,0.0301,0.0249,0.0196,0.0159]

# yesdR_1AK_boostedVars
# CL95down = [0.0104,0.0078,0.0060,0.0043,0.0036,0.0023]
# CL68down = [0.0139,0.0104,0.0076,0.0065,0.0046,0.0035]
# limit= [0.0190,0.0146,0.0112,0.0093,0.0063,0.0054]
# CL68up = [0.0272,0.0207,0.0159,0.0131,0.0100,0.0078]
# CL95up = [0.0373,0.0285,0.0219,0.0183,0.0138,0.0107]

# yesdR_0AK_normalVars
# CL95down = [0.0144,0.0120,0.0088,0.0070,0.0051,0.0041]
# CL68down = [0.0198,0.0161,0.0122,0.0097,0.0067,0.0053]
# limit= [0.0278,0.0220,0.0171,0.0132,0.0103,0.0073]
# CL68up = [0.0389,0.0314,0.0244,0.0195,0.0145,0.0106]
# CL95up = [0.0521,0.0428,0.0335,0.0269,0.0200,0.0153]

# yesdR_0AK_boostedVars
# CL95down = [0.0115,0.0088,0.0060,0.0043,0.0036,0.0023]
# CL68down = [0.0153,0.0117,0.0083,0.0062,0.0046,0.0035]
# limit= [0.0210,0.0171,0.0112,0.0093,0.0063,0.0054]
# CL68up = [0.0300,0.0239,0.0166,0.0131,0.0100,0.0078]
# CL95up = [0.0409,0.0327,0.0235,0.0183,0.0144,0.0107]

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.set_xlabel("$m_{H}$ (GeV)")
ax.set_ylabel(r"95% CL limit on $\sigma$B(H$\rightarrow$hh$_{S}\rightarrow\tau\tau$bb) (pb)")

plt.figtext(0.035, 0.95, 'CMS simulation', fontdict=None,size=20,weight='bold')
plt.figtext(0.035, 0.92, 'work in progress', fontdict=None,size=10,weight='bold')
plt.figtext(0.75, 0.92, '$m_{h_{S}}$ = 60 GeV', fontdict=None,size=14)

plt.plot(mH, baselimit, '-', color='black',label=r"baseline")
# plt.plot(mH, hSbb, '--', color='red',label=r"H$\rightarrow$h($\tau\tau$)h$_{S}$(bb)")
# plt.plot(mH, hStautau, '--', color='dodgerblue',label=r"H$\rightarrow$h(bb)h$_{S}(\tau\tau)$")
plt.plot(mH, limit, '--', color='black',label=r"Feat.+N$_{AK8}$")

plt.fill_between(mH, limit, CL68up,
    alpha=0.5, facecolor='green', label=r"68% exp")
plt.fill_between(mH, limit, CL68down,
    alpha=0.5, facecolor='green', )

plt.fill_between(mH, CL68up, CL95up,
    alpha=0.5, facecolor='gold', label=r"95% exp")
plt.fill_between(mH, CL68down, CL95down,
    alpha=0.5, facecolor='gold')

plt.legend(loc="upper right")

plt.ylim(top=10)
plt.ylim(bottom=0.001)

plt.savefig('nodR_1AK_boostedVars.pdf')