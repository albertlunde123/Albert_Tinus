import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as op

fig,ax = plt.subplots()
deltas = np.array(np.loadtxt('tension.txt')[:,0])
tensions = np.loadtxt('tension.txt')[:,1]
sigma =  np.array(len(tensions)*[0.5])


deltaAf = 0.02
deltas = deltas*deltaAf
masseP = 0.3

g = 9.82

def tension(delta,Lp,L0):
    return (Lp*masseP*g)/(L0+delta)

p0 = [0.2,0.2]
pop,cov = op.curve_fit(tension, deltas, tensions) #sigma = sigma, absolute_sigma = True)
print(pop)
ax.errorbar(deltas,tensions,sigma, linestyle ='', markersize = 5,  fmt = 's', capsize = 3, label = 'tensions' )
ax.plot(deltas,tension(deltas,pop[0],pop[1]), label = 'tensionfit')
ax.legend()

