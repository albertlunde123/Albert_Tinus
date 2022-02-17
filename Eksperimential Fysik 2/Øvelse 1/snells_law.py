import numpy as np
import matplotlib.pyploy as plt
import scipy.optimize as scp
import os

fig, ax = plt.subplots()

def fit(t, *p):
    a = p[0]
    b = p[1]
    return a*t + b

# expects a 2d-np-array
# def linearize(data):
#     return np.sin(data)

title = 'Snells Law'

def plot_data(data, ax, labels, title):

    # lineariser dataet
    ind_vinkel = np.sin(data[0])
    ud_vinkel = np.sin(data[1])

    # plot dataet
    ax.scatter(np.sin(data[0]), np.sin(data[1]), color = 'blue')

    # lav fittet
    popt, pcov = scp.curve_fit(fit, ind_vinkel, ud_vinkel,
                               guess_params)

    # range som fittet skal løbe over.
    t_fit =np.linspace(ind_vinkel[0], ind_vinkel[1], 100)

    # plot fittet
    ax.plot(t_fit, fit(t_fit, *popt), color = 'k', linewidth = 2)



