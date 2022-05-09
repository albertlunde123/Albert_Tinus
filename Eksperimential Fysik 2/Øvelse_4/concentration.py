import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.optimize as scp

fig, ax = plt.subplots(figsize = (10,10))


path = "data_4/"
print(os.getcwd())
filenames = sorted(os.listdir(path))
#remove the one data file with the sun spectrum
for f in filenames:
    if 'sol' in f:
        filenames.remove(f)

data1 = np.loadtxt(path + filenames[0], skiprows = 14 )

dataSet = []

for f in filenames:
    data = np.loadtxt(path + f, skiprows= 14)
    dataSet.append(data)
    
# for data in dataSet:
#     plt.errorbar(data[900:950,0], data[900:950,1])

#Since there are a lot of noise near the large absorbtion lines
#we choose areas with small absorbtion and compare.

#længden af beholderen er taget højde for i mølingen af vand
absorbanceLists = []
drops = np.linspace(1,14,14)
i = 0
while i < 10:
    absorbances = []
    for data in dataSet:
        absorbances.append(data[900 + i,1])
    absorbanceLists.append(absorbances)
    i = i+1 
        #plt.errorbar(data[900,0], data[900,1], fmt = 'o')
# print(len(absorbances))
# plt.errorbar(np.linspace(1,14,14), absorbances, fmt ='o')

def linFunc(x, a):
    return x*a


popt, pcov = scp.curve_fit(linFunc, drops, absorbanceLists[0])
plt.errorbar(drops, absorbanceLists[0], fmt = 'o')

xs = np.linspace(1,14, 100)
# yerr = [np.sqrt(pcov[0][0])]*100
print(np.sqrt(pcov))
plt.plot(xs, linFunc(xs, popt[0]), label = 'Linear fit')
ax.legend()
plt.fill_between(xs, linFunc(xs, popt[0]), linFunc(xs, popt[0]+np.sqrt(pcov[0][0])), alpha = 0.3, color = 'orange')
plt.fill_between(xs, linFunc(xs, popt[0]), linFunc(xs, popt[0]-np.sqrt(pcov[0][0])), alpha = 0.3, color = 'orange')

plt.rc("axes", labelsize=18, titlesize=22)
plt.rc("xtick", labelsize=16, top=True, direction="in")
plt.rc("ytick", labelsize=16, right=True, direction="in")
plt.rc("legend", fontsize=16)
ax.set_title('Absorbance of green food coloring concentration', fontsize = 24)
ax.set_xlabel("Number of droplets", fontsize = 21)
ax.set_ylabel("Absorbance", fontsize = 21)
ax.text(0.6,1.1, r'a = 0.06$\pm$ 0.006', fontsize = 15)
plt.savefig('droplets.png')
plt.show()

