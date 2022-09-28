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

comb1=baselimit
comb2=yesdR_1AK_boostedVarslimit
average=0
best=0
worst=100
bestindex=0
worstindex=0
for n in range(len(baselimit)):
    diff=comb1[n]-comb2[n]
    proz=diff*100/comb1[n]
    average+=proz
    if proz>best:
        best=proz
        bestindex=n
    if proz<worst:
        worst=proz
        worstindex=n

print("Average difference: ", average/len(baselimit), "best for ", mH[bestindex]," : ", best, "worst for ", mH[worstindex]," : ", worst)
