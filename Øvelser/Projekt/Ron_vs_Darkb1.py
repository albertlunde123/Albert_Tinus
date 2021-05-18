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

fig, ax = plt.subplots(figsize = (16,8))
setting = ['gL', 'qH', 'b1', 'r0.1']

dataframedc = pd.read_csv('dark-charge.csv', sep = ',')
datadc = np.array(dataframedc.values)

dataframeron = pd.read_csv('read-out-noise.csv')
dataron = np.array(dataframeron.values)

res = (0,0)
for d in dataron:
    i = 0
    for s in setting:
        if s in d[0]:
            i += 1
    if(i == len(setting)):
        res = (d[1],d[2])
val = dc.find_effektiv_a(setting,datadc)

def kfit(x):
    return res[0]
def sqfit(x, error):
    return np.sqrt((val[0]+error)*x)

ts = np.linspace(0,300,200)
ks = np.empty(len(ts))
ks.fill(res[0])
ax.plot(ts,sqfit(ts,0), label = 'dark noise')
ax.plot(ts,ks, label = 'read-out noise', color = 'red')
ax.fill_between(ts, ks + res[1], ks - res[1], alpha = 0.2, color = 'red')
ax.fill_between(ts, sqfit(ts,val[1]), sqfit(ts,-val[1]), alpha = 0.2, color = 'red')

ax.set_xlabel('Tid(s)', fontsize = 16)
ax.set_ylabel('Signal(pr. effektive pixel)', fontsize = 16)
ax.set_title('Dark Noise vs Read-out Noise', fontsize = 25)
ax.text(245,0.15,'Indstilling = [gL, qH, b1, r0.1]', fontsize = 12, backgroundcolor = 'yellow',)
ax.legend(fontsize = 16)
fig.savefig('C:/Users/123ti/Albert_Tinus/Øvelser/Projekt/Latex/Plots/DNvsRONb1')