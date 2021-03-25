import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp

exec(open('Kalibrering/kalibrering.py').read())
exec(open('../Scripts/Statistik.py').read())
exec(open('../Scripts/data_renser.py').read())
exec(open('../Scripts/chi_sq.py').read())

fig, ax = plt.subplots(figsize = (16,8))
# fig, ax = plt.subplots(4,4,figsize = (16,8))
# ax = ax.ravel()

sol1 = Data('Kalibrering/40grader')
spænding = sol1.points
ts = sol1.t*1000

mask = sol1.rinse2(0.15, 0.02)
ts1 = ts[mask]

vink = vinkel(spænding, *kali)*(360/(2*np.pi))
ax.scatter(ts[~mask], vink[~mask], color = 'blue', alpha = 0.2)
ax.plot(ts[mask], vink[mask], 'ro', alpha = 0.4, markersize = 4)

error = propagation_function(spænding[mask], vinkel, list(kali), pcov)

vinks = vink[mask]

index = []
err = []
j = 0
k = 0

bool = True
while bool:
    vmax = max(vinks[j:])
    index_max = list(vinks[j:]).index(vmax)
    tp = []
    for i in [index_max + j for j in range(20)]:
        if vinks[j:][i] == vmax:
            tp.append(i+j)
    index.append(tp[int(round(len(tp)/2, 0))])
    if len(tp) == 1:
        err.append(0.0033)
    else:
        err.append((ts1[tp[-1]] - ts1[tp[0]])/2)
    j += index_max + 120
    if j > len(vinks):
        bool = False


# for i in range(len(index)):
#     ax.plot([ts1[index[i]] - err[i], ts1[index[i]] + err[i]], [vinks[index[i]]]*2, 'k-')
# fejlen på toppunktet. Picoscopet tager 1 måling pr,

base_error = ts1[1000] - ts1[999]

# Så usikkerheden på tiden er mindst,

base_error = base_error/2

# I tilfældet hvor der kun er én kandidat til toppunktet
# Pga opløsningen på vores data, vil der af og til flere kandidater til
# toppunktet, skal jeg vælge den "midterste". Jeg estimerer usikkerheden
# til at være længden af intervallet hvori toppunktet ligger


# ax.plot(ts1[index[:-1]], vinks[index[:-1]], 'ko')

ax.set_xlabel('', fontsize = 16)
ax.set_ylabel('', fontsize = 16)
ax.legend()
plt.show()
