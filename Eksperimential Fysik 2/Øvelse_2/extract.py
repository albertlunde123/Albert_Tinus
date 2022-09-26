# Extract from Geogebra .txt-file

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
# FIT

def fit(V, *p):
    a = p[0]
    b = p[1]
    return a*V*np.exp(b*V)

ax.set_xlim(0, 150)
Vs = np.linspace(0, 150, 100)

conv = (632*10**(-9))/(4*np.pi)
print(conv*0.00612396)
#print(conv*0.35)
theoretical_vals = [[2.68*10**(-8),-2.81*10**(-3)],[2.14*10**(-8),-1.40*10**(-3)]]

# experimental_vals = [[0.34*conv, -0.0015], [0.401*conv,-0.0043]]
# experimental_vals = [[0.34*conv, -0.0015], [0.401*conv,-0.0043]]

experimental_vals = [[0.34*conv, -0.002], [0.38*conv, -0.004]]

print(experimental_vals)
for d in theoretical_vals:
    ax.plot(Vs, fit(Vs, *d), color = 'black')

for d in experimental_vals:
    ax.plot(Vs, fit(Vs, *d), color = 'red')
ax.set_ylim(0, 3*10**(-6))#*10**(-6))

# COLORS, TITLE AND AX-ELEMENTS

ax.set_title('Piezoelement - comparison', fontsize = 20)
ax.set_xlabel('$V$', fontsize = 20)
ax.set_ylabel('$\\Delta s$', fontsize = 20)
# fig.patch.set_facecolor('#bde5ff')
# ax.set_facecolor('#bde5ff')

# BOX
props = dict(boxstyle = 'square, pad=0.5',
            facecolor = '#ff9500',
            edgecolor = '#313847'
)

text = '$\\Delta s (V) =  aV \\cdot e^{-kV}$'
ax.text(5, 2.7*10**(-6),
        text,
        color = 'black',
        bbox = props,
        fontsize = 16)
# Gem plots som billede og gem fitte funktioner til senere brug.

plt.savefig('Rapport/figures/comparison.png')
plt.show()

