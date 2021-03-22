import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as op

fig,ax = plt.subplots()
deltas = np.array(np.loadtxt('tension.txt')[:,0])
tensions = np.loadtxt('tension.txt')[:,1]
sigma =  np.array(len(tensions)*[0.05])

tens_1 = 1/tensions

deltaAf = 0.01
deltas = deltas*deltaAf
masseP = 0.581

g = 9.82

# def tension(delta,Lp,L0):
#     return (Lp*masseP*g)/(L0+delta)

def tension(delta, *p):
    a = p[0]
    b = p[1]
    return b + a*delta


p0 = [0.2,0.2]
pop,cov = op.curve_fit(tension, deltas, tens_1, p0) #sigma = sigma, absolute_sigma = True)

# a = 1/Rw*Fw

Rw = (pop[0]*g*masseP)**-1
I = masseP * Rw ** 2

print(Rw)

ax.errorbar(deltas,tensions,sigma, linestyle ='', markersize = 5,  fmt = 's', capsize = 3, label = 'tensions' )
ax.plot(deltas,tension(deltas,pop[0],pop[1]), label = 'tensionfit')
ax.set_xlabel('')
ax.set_ylabel('')
ax.legend()

plt.show()
