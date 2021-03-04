# Denne fil kan ikke køres som den står lige nu!
# Hvis du er interesseret i at køre den, skal du slette 'Kalibrering'
# i np.loadtxt().

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scp


# fig, ax = plt.subplots()
# Plot data
x = []
y = []

# Den fysiske afstand mellem målingerne

del_x = 4.5*10**-2

# Dataet importeres

for i in list(range(12)):
    x = x + [i*del_x]
    y = y +  [np.mean(np.loadtxt('Kalibrering/'+str(i)+'_maling.txt')[:,1])]

#ax.scatter(y,x, color = 'r', label = 'data point')

# fitte funktionen defineres og dataet fittes efter denne
# parametrene gemmes i variablen kali, func(x, *kali) kan dermed
# kaldes senere.

def func(x, *p):
    a=p[0]
    b=p[1]
    return a*x+b

guess_params = [1,2]
kali, pcov = scp.curve_fit(func,y,x,guess_params)

# x_fit = np.linspace(0,y[-1],100)
# ax.plot(y, x, 'ro', label = 'mean of data-points')
# ax.plot(x_fit, func(x_fit, kali[0], kali[1]), color = 'k', label = 'fit')

# ax.set_xlabel('U')
# ax.set_ylabel('x')
# ax.set_ylim(0,0.8)
# ax.legend()

# plt.show()

# fig.savefig('../Plots/spænding.png')
