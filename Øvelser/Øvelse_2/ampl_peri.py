import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp

exec(open('Kalibrering/kalibrering.py').read())
exec(open('../Scripts/Statistik.py').read())
exec(open('../Scripts/data_renser.py').read())

fig, ax = plt.subplots(figsize = (16,8))

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

top = []
# for i in range(len(vinks)):
#     if vinks[i] < vinks[i+1] and vinks[i] > vinks[i-1]:
#         top.append(i)


index = []
j = 0
k = 0

j = 0
index = []
while j <= len(vinks):
    if(vinks[j] > vinks[j-1] and vinks[j]> vinks[j+1]):
        index.append(j)
    if(vinks[j] == vinks[j+1] and vinks[j] > vinks[j-1]):
        i = 2
        if i+j+10 >= len(vinks):
            break
        while i < 6:
            if(vinks[j] == vinks[j+i] and vinks[j] > vinks[j+i+1]):
                index.append(j)
                break
            i +=1
    j += 1
# bool = True
# while bool:
#     vmax = max(vinks[j:])
#     index_max = list(vinks[j:]).index(vmax)
#     index.append(index_max+j)
#     j += 350
#     if j > len(vinks):
#         bool = False

print(index)
ax.plot(ts1[index[:-1]], vinks[index[:-1]], 'ko')

def sinus(t, *p):
    A = p[0]
    w = p[1]
    k = p[2]
    b = p[3]
    d = p[4]
    return (A*np.cos(w*t+k)*np.exp(-b*t)+d)

guess = [22,-5,2,0,1]

popt, pcov2 = scp.curve_fit(sinus, ts[mask], vink[mask], guess,
                            sigma = error, absolute_sigma = True)

print(popt)

error1 = propagation_function(ts[mask], sinus, list(popt), pcov2)
ax.fill_between(ts[mask],
                sinus(ts[mask], *popt)-error1,
                sinus(ts[mask], *popt)+error1,
                alpha = 0.3)

ax.plot(ts[mask], sinus(ts[mask], *popt), 'k', linewidth = 2)

ax.set_xlabel('t')
ax.set_ylabel('vinkel')
# ax.legend()

print(np.diag(pcov2))

plt.show()


