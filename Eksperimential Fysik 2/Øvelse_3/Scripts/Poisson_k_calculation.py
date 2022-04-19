import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.stats as ss 
from scipy.special import factorial
import tryk as tryk

fig, ax = plt.subplots()
path = '../data2/'
filenames = os.listdir(path)


def findAllPhaseChanges(filenames):
    phases = []
    end = 600
    ave_dist = 0.005
    for filename in filenames:
        data = np.loadtxt(path + filename, skiprows = 3)
        skipper = int(round(len(data[:,0])/1000, 0))
        data = data[::skipper, :]
        
        breaker = tryk.break_point(data, end)
        lms = tryk.local_maxima(data[:breaker, :])
        phases.append(len(lms))
    return phases 


        
    


#We try to find the constant k that relates the change in pressure
# to the change in phase

wavelength = 632*10**-9
lBeholder = 0.0565
oneAtm = 101325
pressureError = 2000
phasechanges = findAllPhaseChanges(filenames)


#We try to find the mean value of the phasechanges, and assume that
#they are poisson distributed
pMean = sum(phasechanges)/len(phasechanges)
pError = np.sqrt(pMean)

k = 2*np.pi*pMean*wavelength/(oneAtm*lBeholder*2*np.pi)
print(1+k*oneAtm)

sigmaPhase = (2*np.pi*wavelength/(oneAtm*lBeholder*2*np.pi))**2*pError**2
sigmaPressure = (2*np.pi*wavelength*pMean/(-oneAtm**2*lBeholder*2*np.pi))**2*(oneAtm*0.2)**2
kError = np.sqrt(sigmaPhase + sigmaPressure)

print(kError*oneAtm)

#lets make a histogram
bins = set(phasechanges)
bins = list(bins)
print(bins)
bins = [ 21.5, 22.5, 23.5, 24.5, 25.5, 26.5]
ax.hist(phasechanges, bins = bins, rwidth = 0.2, density = False)

plt.rc("axes", labelsize=18, titlesize=22)
plt.rc("xtick", labelsize=16, top=True, direction="in")
plt.rc("ytick", labelsize=16, right=True, direction="in")
plt.rc("legend", fontsize=16)
ax.set_title('Histogram of total number of phaseshifts', fontsize = 18)
ax.set_xlabel("Total number of phaseshifts", fontsize = 18)
ax.set_ylabel("Occurences", fontsize = 18)
ax.text(21.9,4.8, r'$\mu=$ 23.8',)
ax.text(21.9,4.55, r'$\sigma=$ 4.88')
plt.savefig('../Rapport/inputs/pressureHist.png')
plt.show()