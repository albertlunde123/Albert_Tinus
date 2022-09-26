import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.optimize as scp

fig, ax = plt.subplots(figsize = (10,10))

path = '../Data/Data1gang/'
filenames = sorted(os.listdir(path))

# We store the datasets along with the noted angle in the format [data, angle]

datasets = []
for f in filenames:
    angle = int(f.split('_')[0])*2
    data_points = np.loadtxt(path + f, skiprows = 3)
    datasets.append([data_points, angle])

# We are interested in plotting the amplitude of the incident wave as a
# function of the measured angle.

def local_maxima(amps, angs):
    lm = []
    for i in range(len(amps)-1)[1:]:
        if amps[i] > amps[i-1] and amps[i] > amps[i+1]:
            lm.append(angs[i]+0.1)
    return lm

def find_guesses(angs, amps):

    a = (np.max(amps) - np.min(amps))/2
    c = (np.max(amps) + np.min(amps))/2

    lmaxes = local_maxima(amps, angs)

    l0 = lmaxes[0]
    l1 = lmaxes[1]

    d = 2*np.pi/(l0 - l1)
    b = -l1*d
    return [a,c,d,b]

def find_amp(data):
    return (np.max(data[:,1]) - np.min(data[:,1]))/2

angs, amps = [], []
for d in datasets:
    print(d[1])
    angs.append(d[1]*2*np.pi/360)
    amps.append(find_amp(d[0]))

points = np.array([[i,j] for i,j in zip(angs,amps)])
points = points[points[:,0].argsort()]

def fit(V, *p):
    a = p[0]
    c = p[1]
    d = p[2]
    b = p[3]
    return a*np.cos(b + d*V) + c

guess = find_guesses(points[:, 0 ], points[:, 1])

a = guess[0]
c = guess[1]
b = guess[2]
d = guess[3]

print(a, b, c, d)

errs = 2*np.pi/360
errs_vec = np.zeros(len(angs)) + errs

popt, pcov = scp.curve_fit(fit,
                           angs,
                           amps,
                           guess,
                           bounds = ((a-abs(a*0.00001),
                                c - abs(c*0.0000001),
                                b-abs(b*0.00001),
                                d - abs(d*0.0000001)),
                                (a + abs(a*0.00001),
                                c + abs(c)*0.0000001,
                                b + abs(b*0.00001),
                                d + abs(d*0.0000001))),
                           sigma = errs_vec)

Vs = np.linspace(0, np.pi, 100)
ax.errorbar(angs, amps, xerr = errs, fmt = 'ko', markersize = 14)
ax.plot(Vs, fit(Vs, *popt), 'b-', linewidth = 3)

props = dict(boxstyle = 'square, pad=0.5',
            facecolor = '#272822',
            edgecolor = '#313847'
)

box_text = '$b = ' + str(round(popt[2], 1)) + ' \\pm ' +  str(round(np.diag(pcov)[1], 3)) + '$'

ax.set_ylim(0, 1)

ax.text(0, 0.94, box_text, color = 'white', bbox = props, fontsize = 26)

ax.set_title('Plot of waveplate-angle and light intensity', fontsize = 26)
ax.set_xlabel("$\\theta_{incident} $ in rad", fontsize = 26)
ax.set_ylabel("Intensity", fontsize = 26)


plt.savefig('../Rapport/inputs/waveplateres.png')
plt.show()
