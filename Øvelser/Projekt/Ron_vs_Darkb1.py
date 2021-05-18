import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os 
import sys
sys.path.append('C:/Users/123ti/Albert_Tinus/Øvelser/Projekt')
import search_function1 as se
print(os.getcwd())
os.chdir('C:/Users/123ti/Albert_Tinus/Øvelser/Projekt')
import scipy.stats as ss
import scipy.optimize as scp
import darkcharge as dc
import Ron_vs_Darkts as rd

fig, ax = plt.subplots(figsize = (16,8))
setting = ['qH', 'gM', 'b1', 'r4']

dataframedc = pd.read_csv('dark-charge.csv', sep = ',')
datadc = np.array(dataframedc.values)

dataframeron = pd.read_csv('read-out-noise.csv')
dataron = np.array(dataframeron.values)


dcs,ros = rd.same_setting(dataron, datadc)
wantd = []
wantr = []
for i in range(len(dcs)):
    #print(dcs[i][2])
    #print('')
    #print(setting)
    if(dcs[i][2] == setting):
        wantd.append(dcs[i])
        wantr.append(ros[i])
        break
#print(wantr[0][0])
root = rd.find_cut(wantd, wantr)
root_err = rd.find_cut_error(wantd, wantr, root)
#print(root)
#roots 
def kfit(x):
    return wantr[0][0]
def sqfit(x, error):
    return np.sqrt((wantd[0][0]+error)*x)
ts = np.linspace(0,300,200)
ks = np.empty(len(ts))
ks.fill(wantr[0][0])
ax.plot(ts,sqfit(ts,0), label = 'dark noise')
ax.plot(ts,ks, label = 'read-out noise', color = 'red')
ax.fill_between(ts, ks + wantr[0][1], ks - wantr[0][1], alpha = 0.2, color = 'red')
ax.fill_between(ts, sqfit(ts,wantd[0][1]), sqfit(ts,-wantd[0][1]), alpha = 0.2, color = 'blue')
ax.errorbar(root,wantr[0][0], xerr = root_err, fmt = 's', color = 'black', ms = 10)
ax.set_xlabel('Tid(s)', fontsize = 16)
ax.set_ylabel('Signal(pr. effektive pixel)', fontsize = 16)
ax.set_title('Dark Noise vs Read-out Noise', fontsize = 25)
ax.text(245,1.5,'Indstilling' + str(setting), fontsize = 12, backgroundcolor = 'yellow',)
ax.legend(fontsize = 16, loc = 'lower right')
fig.savefig('C:/Users/123ti/Albert_Tinus/Øvelser/Projekt/Latex/Plots/DNvsRONb1')