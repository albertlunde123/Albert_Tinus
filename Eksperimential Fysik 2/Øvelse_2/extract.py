# Extract from Geogebra .txt-file

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scp

fig, ax = plt.subplots()

file = open('geo-expand.txt', 'r')
lines = file.readlines()

xs = []
ys = []

# The points are embedded in parentheses, with a specific pattern.

for l in [lin for lin in lines if 'dotstyle)' in lin][2:]:

    xs.append(round(float(l.split('(')[2].split(',')[0]), 2))
    ys.append(round(float(l.split('(')[2].split(',')[1].split(')')[0]), 2))

# We must now scale the points, so they match the graph. The max-value for the
# y-axis should be 2.62 * 10-6. For the x-axis 150. the graph should intersect
# (0, 0)

xs = np.array(xs) - xs[0]
ys = np.array(ys) - ys[0]

x_scale = 150/xs[-1]
y_scale = 2.62/ys[-1]#10**(-6)/ys[-1]

xs = xs*x_scale
ys = ys*y_scale

# Nu prøver vi at fitte dette data,

def fit(V, *p):
    a = p[0]
    b = p[1]
    return a*V*np.exp(b*V)

ax.plot(xs, ys, 'o')

ax.set_xlim(0, 150)
ax.set_ylim(0, 3)#*10**(-6))

guess = [0,0]

popt, pcov = scp.curve_fit(fit,
                           xs,
                           ys,
                           guess)

Vs = np.linspace(xs[0], xs[-1], 100)

ax.plot(Vs, fit(Vs, *popt), 'k-')

print(popt)

# Gem plots som billede og gem fitte funktioner til senere brug.

plt.show()
