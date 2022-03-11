import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.optimize as scp

fig, ax = plt.subplots()

# os.chdir('c:\\Users\\all\\Albert_Tinus\\Eksperimential Fysik 2\\Øvelse_2\\')

data = np.loadtxt("Data2øvelsesgang/Måling1.txt", skiprows = 3)

def sorter(data):
    returner = []
    for i in range(len(data)-1):
        if data[i] < data[i+1]:
            returner.append(i)
    return returner

def fit(V, *p):
    a = p[0]
    b = p[1]
    c = p[2]
    d = p[3]
    k = p[4]
    # e = p[4]
    return a*np.cos(b + V*d * np.exp((-k*V))) + c

indices = sorter(data[:, 1])

freq = data[indices, 1]*10
voltage = data[indices, 2]

maks = np.max(voltage[:200])
min = np.min(voltage[:200])


guess_a = (maks - min)/2
guess_c = (maks + min)/2

def plot(freq, voltage, ax):
    ax.plot(freq, voltage, 'o', color = 'blue')

guess_d = 0.023 * 2*3.14*2 / 0.7# 0.4
guess_k = 0.00179

guess_params = [guess_a, -2.1, guess_c, guess_d, guess_k]


popt, pcov = scp.curve_fit(fit,
                    freq,
                    voltage,
                    guess_params,
                    bounds = ((guess_a-1, -2.11,
                               guess_c-1,
                               guess_d - 0.001,
                               guess_k - 0.0001),
                              (guess_a+1, -2.09,
                               guess_c+1,
                               guess_d + 0.001,
                               guess_k + 0.0001)))

Vs = np.linspace(0, 150, 100)

ax.plot(Vs, fit(Vs, *popt), '-')
plot(freq, voltage, ax)

# in theory, we should be able to extract the path distance from this.

wave_length = 650*10**-3

def path_dist(V, *p):
    a = p[0]
    k = p[1]
    return a*V*np.exp(-k*V)

# ax.plot(Vs, path_dist(Vs, *[0.4142, 0.00102])*wave_length/(4*3.14))


plt.show()
