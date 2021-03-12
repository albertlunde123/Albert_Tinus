import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp
import os

exec(open('Kalibrering/kalibrering.py').read())
exec(open('../Scripts/Statistik.py').read())
exec(open('../Scripts/data_renser.py').read())

fig, ax = plt.subplots(figsize = (10,8))

sol1 = Data('Kalibrering/20vinkel')
spænding = sol1.points
ts = sol1.t*1000

vink = vinkel(spænding, *kali)*(360/(2*np.pi))

ax.plot(ts, vink)

plot_propagation(spænding[1000:], vinkel, kali, pcov, ax)


print(np.sqrt(np.diag(pcov)))
ax.set_xlabel('t')
ax.set_ylabel('vinkel')
# ax.legend()
plt.show()


