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
#ax.scatter(ts[~mask], vink[~mask], color = 'blue', alpha = 0.2)
#ax.plot(ts[mask], vink[mask], 'ro', alpha = 0.4, markersize = 4)

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


#for i in range(len(index)):
  #  ax.plot([ts1[index[i]] - err[i], ts1[index[i]] + err[i]], [vinks[index[i]]]*2, 'k-')
# fejlen på toppunktet. Picoscopet tager 1 måling pr,

base_error = ts1[1000] - ts1[999]

# Så usikkerheden på tiden er mindst,

base_error = base_error/2

# I tilfældet hvor der kun er én kandidat til toppunktet
# Pga opløsningen på vores data, vil der af og til flere kandidater til
# toppunktet, skal jeg vælge den "midterste". Jeg estimerer usikkerheden
# til at være længden af intervallet hvori toppunktet ligger


#ax.plot(ts1[index[:-1]], vinks[index[:-1]], 'ko')


# for i in range(len(index)):
#      if i+1 == len(index):
#          break
#       print((ts1[index[i+1]] - ts1[index[i]]))

def sinus(t, *p):
     A = p[0]
     w = p[1]
     k = p[2]
     d = p[3]
     return (A*np.cos(w*t+k)+d)

masseP = 0.585
g = 9.82
Rw = 0.1189
I = masseP * Rw ** 2
k = 2*np.pi*np.sqrt(I/(masseP*g*Rw))

print(k)

A = []
peri = []
peri_err = []
for i in range(len(index)-6):
    vink = vinks[index[i]:index[i+2]]
    ts = ts1[index[i]:index[i+2]]
    per = (ts1[index[i+2]]-ts1[index[i]])
    peri.append((ts1[index[i+2]]-ts1[index[i]]))

    peri_0 = ts1[index[-6]] - ts1[index[-7]]
    peri_err.append(np.sqrt((err[i+2]**2 - err[i]**2)/peri_0**2 +
       per**2*np.log(peri_0)**2*(err[-6]**2 + err[-7]**2)))

    guess = [50-i*2,-5,2,0]

    #ax[i].plot(ts, vink, 'ro', alpha = 0.4, markersize = 4)
    popt, pcov2 = scp.curve_fit(sinus, ts, vink, guess,
                                sigma = error[index[i]:index[i+2]], absolute_sigma = True)


    #error1 = propagation_function(ts, sinus, list(popt), pcov2)
     #ax[i].fill_between(ts,
                    # sinus(ts, *popt)-error1,
                    # sinus(ts, *popt)+error1,
                    # alpha = 0.3)

     #ax[i].plot(ts, sinus(ts, *popt), 'k', linewidth = 2)
     # print(popt[0])
    A.append(abs(popt[0]))

ax.errorbar(A[:-2], peri[:-2]/peri[-3], yerr = peri_err[:-2], fmt = 'o')

print(peri[-3])

def fitter(t, k, n):
     ns = sum([(np.math.factorial(2*n)/(2**n*np.math.factorial(n))**2)**2*np.sin(t/2)**(2*n)
           for n in range(n)])
     return ns



ttss = np.linspace(0, 0.25*np.pi, 100)

ax.plot(np.linspace(0, 45, 100), fitter(ttss, k, 10))


ax.set_xlabel('t')
ax.set_ylabel('vinkel')
ax.legend()

plt.show()


