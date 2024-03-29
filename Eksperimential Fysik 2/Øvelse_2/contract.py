# Extract from Geogebra .txt-file

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scp

fig, ax = plt.subplots()

def convert_geogebra(path, x_scaler, y_scaler):

    file = open(path, 'r')
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

    x_scale = x_scaler/xs[-1]
    y_scale = y_scaler/ys[-1]#10**(-6)/ys[-1]

    xs = xs*x_scale
    ys = ys*y_scale

    print(path)
    return xs, ys

xs1, ys1 = convert_geogebra('geo-contract.txt', 150, 2.62*10**-6)
xs2, ys2 = convert_geogebra('geo-expand.txt', 150, 2.62*10**-6)

guess = [0,0]

# FIT

def fit(V, *p):
    a = p[0]
    b = p[1]
    return a*V*np.exp(b*V)

def plot_fit(fit, x, y, guess, ax, color):

    popt, pcov = scp.curve_fit(fit,
                               x,
                               y,
                               p0 = guess)

    Vs = np.linspace(x[0], x[-1], 100)
    ax.plot(Vs,
            fit(Vs, *popt),
            'k-',
            zorder = 10)

# PLOT DATA

    ax.errorbar(x, y,
                fmt = 'o',
                color = color,
                markersize = 7,
                zorder = 0)

    print(popt)

plot_fit(fit, xs1, ys1, guess, ax, '#ff9500')
plot_fit(fit, xs2, ys2, guess, ax, 'red')

ax.set_xlim(0, 150)
ax.set_ylim(0, 3*10**(-6))#*10**(-6))

# COLORS, TITLE AND AX-ELEMENTS

ax.set_title('Piezoelement - contraction', fontsize = 20)
ax.set_xlabel('$V$', fontsize = 20)
ax.set_ylabel('$\\Delta s$', fontsize = 20)
# fig.patch.set_facecolor('#bde5ff')
ax.set_facecolor('#bde5ff')

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

plt.savefig('Rapport/figures/contraction.png')

# print(popt)
# print(np.sqrt(np.diag(pcov)))

plt.show()
