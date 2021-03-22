import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp
import os
import csv

exec(open('Kalibrering/kalibrering.py').read())
exec(open('../Scripts/Statistik.py').read())
exec(open('../Scripts/data_renser.py').read())


# fig, ax = plt.subplots(4,3,figsize = (20,12))
# ax = ax.ravel()

fig, ax = plt.subplots(figsize = (16,8))

names = ['0_681', '0_755', '0_805', '0_863', '1_036', '1_091', '1_126', '1_162',
         '1_232', '1_270', '1_319', '1_452']
freks = np.array([0.681, 0.755, 0.805, 0.863, 1.036, 1.091, 1.126, 1.162,
                  1.232, 1.270, 1.319, 1.452])*2*np.pi
driv_freks = freks / (2*np.pi)

A = []

for i in range(len(names)):
    print(i)
    sol1 = Data('Kalibrering/frek' + names[i])
    spænding = sol1.points
    ts = sol1.t*1000

    vink = vinkel(spænding, *kali)*(360/(2*np.pi))
    # ax[i].plot(ts, vink, 'ro', alpha = 0.4, markersize = 4)


    error = propagation_function(spænding, vinkel, list(kali), pcov)

    def sinus(t, *p):
        A = p[0]
        w = p[1]
        k = p[2]
        d = p[3]
        return (A*np.cos(w*t+k)+d)

    guess = [(max(vink)-0.8)/2,freks[i],0.4,0.8]

    popt, pcov2 = scp.curve_fit(sinus, ts, vink, guess,
                                sigma = error, absolute_sigma = True,
                                bounds = ((0, -10, -10, -10),(3, 10, 10, 10)))
    A.append(popt[0])
    # ax[i].plot(ts, sinus(ts, *popt), color = 'black')

    # ax[i].set_xlabel('')
    # ax[i].set_ylabel('')
    # ax[i].legend()

ax.plot(driv_freks, A, 'ro')
ax.plot(driv_freks, A, 'k--')
plt.show()

