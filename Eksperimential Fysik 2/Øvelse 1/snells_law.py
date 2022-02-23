import numpy as np
import matplotlib.pyplot as plt
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

os.chdir('c:\\Users\\all\\Albert_Tinus\\Eksperimential Fysik 2\\Øvelse 1\\')
# print(os.getcwd())


deg_to_rad = 2*3.14/360

data = np.loadtxt("Målinger/Snells_law.txt", skiprows = 2) * deg_to_rad
title = 'Snells Law'

err = 0.512

# Propagate through deg to rad function

err = err * deg_to_rad

# Propagate through sin

def propagation_function(x, f, popt, pcov):
    f_error = 0

# Standard afvigelser gemmes

    err =  list(np.sqrt(np.diagonal(pcov)))
    for i in range(len(err)):

# funktionen med standard afvigelsen på den i'te parameter konstrueres

        j = popt[:i] + [popt[i] + err[i]] + popt[i+1:]
        f_error += (f(x, *j)-f(x, *popt))**2

    return  np.sqrt(f_error)

def plot_propagation(x, f, popt, pcov, ax):
    error = propagation_function(x, f, list(popt), pcov)
    ax.fill_between(x, f(x, *popt) + error,
                    f(x, *popt) - error, alpha = 0.3,
                    color = '#d989a6')

def plot_data(data, ax, err): #, labels, title):

    # lineariser dataet
    ind_vinkel = np.sin(data[:,0])
    ind_err =  np.cos(ind_vinkel)*err

    ud_vinkel = ind_vinkel - np.sin(data[:,1])
    ud_err =  np.cos(ud_vinkel)*err*np.sqrt(2)

    # plot dataet
    ax.errorbar(ud_vinkel,
                ind_vinkel,
                fmt = 'o',
                xerr = ud_err,
                yerr = ind_err,
                color = 'white')

    guess_params = [1,0]
    # lav fittet
    popt, pcov = scp.curve_fit(fit,
                               ud_vinkel,
                               ind_vinkel,
                               guess_params,
                               sigma = ind_err)

    # range som fittet skal løbe over.
    t_fit =np.linspace(ud_vinkel[0], ud_vinkel[-1], 100)

    # plot fittet
    ax.plot(t_fit, fit(t_fit, *popt), color = '#d989a6', linewidth = 2)

    plot_propagation(t_fit, fit, popt, pcov, ax)

    # print(popt[0])
    # print(np.sqrt(np.diag(pcov)))


ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

fig.patch.set_facecolor('#313847')
ax.set_facecolor('#313847')

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plot_data(data, ax, err)
plt.show()
