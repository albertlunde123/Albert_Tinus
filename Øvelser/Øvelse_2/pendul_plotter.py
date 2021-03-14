import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp
import os

exec(open('Kalibrering/kalibrering.py').read())
exec(open('../Scripts/Statistik.py').read())
exec(open('../Scripts/data_renser.py').read())

fig, ax = plt.subplots(figsize = (16,8))

sol1 = Data('Kalibrering/10vinkel')
spænding = sol1.points
ts = sol1.t*1000

vink = vinkel(spænding, *kali)*(360/(2*np.pi))
ax.plot(ts, vink)

def sinus(t, *p):
    A = p[0]
    w = p[1]
    k = p[2]
    b = p[3]
    d = p[4]
    return A*np.sin(w*t+k)*np.exp(-b*t)+d

guess = [1,1,1,1,1]

popt, pcov2 = scp.curve_fit(sinus, ts[1000:], vink[1000:], guess)
ax.plot(ts, sinus(ts, *popt))
error = propagation_function(spænding, vinkel, list(kali), pcov)[1000:]


ax.fill_between(ts[1000:], vink[1000:]-error, vink[1000:]+error, alpha = 0.3)

# ax.fill_between(ts[1000:], sinus(ts[1000:], *popt)-error, sinus(ts[1000:], *popt)+error, alpha = 0.3)
#print([vinkel(a, *kali) - propagation_function(a, vinkel, list(kali), pcov) for a in spænding])

ax.set_xlabel('t')
ax.set_ylabel('vinkel')
# ax.legend()

print(np.sqrt(np.diag(pcov2)))
plt.show()


