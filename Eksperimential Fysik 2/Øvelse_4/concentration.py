import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.optimize as scp

fig, ax = plt.subplots(figsize = (10,10))


path = "data_4/"
#print(os.getcwd())
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

def linFunc(x, *p):
    a = p[0]
    b = p[1]
    return x*a + b 

def polyFunc(x, *p):
    a = p[0]
    b = p[1]
    c = p[2]
    return a*x**2+b*x+c

plt.errorbar(drops, absorbanceLists[0], fmt = 'o')
def drawFunc(func, xs, ys, guesses, name, fillColor):
    popt, pcov = scp.curve_fit(func, xs, ys, guesses)
    xs = np.linspace(1,14, 100)
    # yerr = [np.sqrt(pcov[0][0])]*100

    plt.plot(xs, func(xs, *popt), label = name)
    ax.legend()
    errs = np.sqrt(np.diagonal(pcov))
    err = 0
    i = 0
    while i < len(errs):
        newPopt = popt.copy()
        newPopt[i] = popt[i]+errs[i]
        i = i+1
        err = (func(xs[3], *newPopt) - func(xs[3], *popt))**2
        
    plt.fill_between(xs, func(xs, *popt), func(xs, *popt-err), alpha = 0.2, color = fillColor)
    plt.fill_between(xs, func(xs, *popt), func(xs, *popt+err), alpha = 0.2, color = fillColor)
    return popt, np.sqrt(np.diagonal(pcov))
    
linParams, aError = drawFunc(linFunc,drops, absorbanceLists[0], [1,1], 'Linear fit', 'blue')
polParams, bError = drawFunc(polyFunc, drops, absorbanceLists[0], [1,1,1], 'Polynomial fit', 'green')
print(linParams)
print(aError)
print(polParams)
print(bError)

plt.rc("axes", labelsize=18, titlesize=22)
plt.rc("xtick", labelsize=16, top=True, direction="in")
plt.rc("ytick", labelsize=16, right=True, direction="in")
plt.rc("legend", fontsize=16, loc = 'upper left')
ax.set_title('Absorbance of green food coloring solution', fontsize = 24)
ax.set_xlabel("Number of droplets", fontsize = 21)
ax.set_ylabel("Absorbance", fontsize = 21)
ax.legend()
plt.savefig('droplets.png')
plt.show()

