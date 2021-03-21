import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp
import os
import csv

exec(open('Kalibrering/kalibrering.py').read())
exec(open('../Scripts/Statistik.py').read())
exec(open('../Scripts/data_renser.py').read())

fig, ax = plt.subplots(figsize = (16,8))

sol1 = Data('Kalibrering/20vinkel')
spænding = sol1.points
ts = sol1.t*1000

mask = sol1.rinse1(0.01)

vink = vinkel(spænding, *kali)*(360/(2*np.pi))
ax.scatter(ts[~mask], vink[~mask], color = 'blue')
ax.plot(ts[mask], vink[mask], 'ro', alpha = 0.2, markersize = 4)

error = propagation_function(spænding[mask], vinkel, list(kali), pcov)

def sinus(t, *p):
    A = p[0]
    w = p[1]
    k = p[2]
    b = p[3]
    d = p[4]
    return (A*np.sin(w*t+k)*np.exp(-b*t**2)+d)

guess = [1,1,1,1,1]

popt, pcov2 = scp.curve_fit(sinus, ts[mask], vink[mask], guess)

error1 = propagation_function(ts[mask], sinus, list(popt), pcov2)
ax.fill_between(ts[mask],
                sinus(ts[mask], *popt)-error1,
                sinus(ts[mask], *popt)+error1,
                alpha = 0.3)

ax.plot(ts[mask], sinus(ts[mask], *popt), 'k', linewidth = 2)


# with open('vink.csv', 'w', newline ='') as f:
#     writer = csv.writer(f, delimiter = ',')
#     for v in error:
#         writer.writerow([v])


ax.set_xlabel('t')
ax.set_ylabel('vinkel')
# ax.legend()

print((pcov2))
plt.show()


