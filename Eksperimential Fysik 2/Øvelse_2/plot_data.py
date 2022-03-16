import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.optimize as scp

fig, ax = plt.subplots()

# os.chdir('c:\\Users\\all\\Albert_Tinus\\Eksperimential Fysik 2\\Øvelse_2\\')

data = np.loadtxt("Data2øvelsesgang/Måling2.txt", skiprows = 3)

# Find data points that are either rising or falling.
def sorter(data, k):
    returner = []
    for i in range(len(data)-1):
        if data[i] < data[i+k]:
            returner.append(i)
    return returner

# Sinusoidal function we are trying to fit against.
def fit(V, *p):
    a = p[0]
    b = p[1]
    c = p[2]
    d = p[3]
    k = p[4]
    # e = p[4]
    return a*np.cos(b + V*d * np.exp((-k*V))) + c

# Plot the data and the fit.
def plot_fit_data(data, ax, guess_d, guess_k, i):
    # Data to be plotted.
    indices = sorter(data[:, 1], i)

    # Frequencies and voltage
    freq = data[indices, 1]*10
    voltage = data[indices, 2]

    maks = np.max(voltage[:200])
    min = np.min(voltage[:200])

    # Good guesses.
    guess_a = (maks - min)/2
    guess_c = (maks + min)/2

    ax.plot(freq, voltage, 'o', color = 'blue')


    # Hvordan finder vi et godt estimat for b? Når funktionen antager sit maks
    # skal cos(b + V*d*exp(-kV)) = 1. Hvor V = V_maks. Vi kan aflæse et V_maks
    # fra dataet, eller vi kan bestemme det med én funktion.

    # b =

    guess_d = d * 2*3.14*2 / 0.660# 0.4
    guess_k = k

    V_maks = 0
    for i in range(200):
        if freq[i] == maks:
            V_maks = freq[i]
            break

    print(V_maks)
    guess_b = -14*guess_d*np.exp(-k*V_maks)

    # guess_b = -2.1
    guess_params = [guess_a, guess_b, guess_c, guess_d, guess_k]


    popt, pcov = scp.curve_fit(fit,
                        freq,
                        voltage,
                        guess_params,
                        bounds = ((guess_a-1,
                                guess_b - 0.01,
                                guess_c-1,
                                guess_d - 0.001,
                                guess_k - 0.0001),
                                (guess_a+1,
                                guess_b +0.01,
                                guess_c+1,
                                guess_d + 0.001,
                                guess_k + 0.0001)))

    Vs = np.linspace(0, 150, 100)

    ax.plot(Vs, fit(Vs, *popt), '-')

d = 0.0214
k = 0.00140

# d = 0.0268
# k = 0.0281

plot_fit_data(data, ax, d, k, 1)

# in theory, we should be able to extract the path distance from this.

wave_length = 650*10**-3

def path_dist(V, *p):
    a = p[0]
    k = p[1]
    return a*V*np.exp(-k*V)

# ax.plot(Vs, path_dist(Vs, *[0.4142, 0.00102])*wave_length/(4*3.14))


plt.show()
