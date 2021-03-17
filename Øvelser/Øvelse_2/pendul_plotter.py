import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp
import os

exec(open('Kalibrering/kalibrering.py').read())
exec(open('../Scripts/Statistik.py').read())
exec(open('../Scripts/data_renser.py').read())

fig, ax = plt.subplots(figsize = (16,8))

sol1 = Data('Kalibrering/30vinkel')
spænding = sol1.points
ts = sol1.t*1000

mask = sol1.rinse1(0.1)

vink = vinkel(spænding, *kali)*(360/(2*np.pi))
ax.scatter(ts[~mask], vink[~mask], color = 'blue')
ax.scatter(ts[mask], vink[mask], color = 'red', alpha = 0.02)

def sinus(t, *p):
    A = p[0]
    w = p[1]
    k = p[2]
    b = p[3]
    d = p[4]
    e = p[5]
    return (A*np.sin(w*t+k)*np.exp(-b*t**2))+d

guess = [40,1,1,1,1,1]

popt, pcov2 = scp.curve_fit(sinus, ts[mask], vink[mask], guess)
ax.plot(ts[mask], sinus(ts[mask], *popt), 'k', linewidth = 2)

error = propagation_function(spænding[mask], vinkel, list(kali), pcov)
ax.fill_between(ts[mask], vink[mask]-error, vink[mask]+error, alpha = 0.3)


ax.set_xlabel('t')
ax.set_ylabel('vinkel')
# ax.legend()

print(np.diag(pcov2))
plt.show()


