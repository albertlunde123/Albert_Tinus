import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os 
import sys
sys.path.append('C:/Users/123ti/Albert_Tinus/Øvelser/Projekt')
import search_function1 as se
os.chdir('C:/Users/123ti/Albert_Tinus/Øvelser/Projekt')
import scipy.stats as ss
import scipy.optimize as scp
import darkcharge as dc
fig, ax = plt.subplots(figsize = (16,8))

dataframedc = pd.read_csv('dark-charge.csv', sep = ',')
datadc = np.array(dataframedc.values)

dataframeron = pd.read_csv('read-out-noise.csv')
dataron = np.array(dataframeron.values)

#print(dataron[0][1:])
def same_setting(ron, dcur):
    dcs = []
    rons = []
    for i in range(len(ron)):
        setting = se.string_splitter(ron[i][0])
        setting.append('e500')
        val = 0
        for k in range(len(dcur)):
            j = 0
            #print(dcur[k][0])
            for s in setting:
                #print(s)
                if(s in dcur[k][0]):
                    j += 1
            if(j == len(setting)):
                val = dc.find_effektiv_a(setting, dcur)
                #print(res)
                #Pga af flukturationen af dataet kan man godt få en hældning
                #der er tæt på 0, derfor har vi valgt at fjerne de hældninger
                #hvor dark current er tilnærmelsesvis 0, fordi det både giver
                #et grimt plot, plus at fejlen på datapunket bliver ekstremt
                #stor pr. den fejlfunktionen længere nede.
                if(val[0] > 10**-6):
                    dcs.append([val[0],val[1],setting])
                    rons.append([ron[i][1],ron[i][2],setting])
                    setting.pop(-1)
                    break
            
    return dcs,rons
dcs,ros = same_setting(dataron,datadc)

#wantd = []
#wantr = []
#for i in range(len(dcs)):
#    dcs[i][2].pop(-1)
#    for o in dcs[i][2]:
#        j=0
#        print(o)
#        if o in ['gL', 'qH', 'b1', 'r0.1']:
#            j += 1
#        if(j == 2):
#           print('hello')
#            wantd.append(dcs[i])
#            wantr.append(ros[i])
#            break
#print(wantd)
def find_cut(darks, rons):
    roots = []
    for i in range(len(darks)):
        f = lambda x: np.sqrt(darks[i][0]*x)-rons[i][0]
        root = scp.fsolve(f,20)
        roots.append(root[0])
    return roots

ans = find_cut(dcs,ros)
def find_cut_error(darks, rons, roots):
    root_errors = []
    for i in range(len(darks)):
        #Denne fejl er udledet i opgaven
        err_dark = roots[i]*1/(2*np.sqrt(darks[i][0]*roots[i]))*darks[i][1]
        root_error = np.sqrt(err_dark**2 + rons[i][0])
        root_errors.append(root_error)
    return root_errors

errs = find_cut_error(dcs, ros, ans)
#print(errs)
points = range(len(ans))
ax.errorbar(points,ans, errs, fmt = 's--')

#ax.plot(points[25:],ans[25:], marker  = '*')
    
#print(len(dataron))
#print(len(datadc))



    
        
    
#print(datadc)