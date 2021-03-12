# Dette script skal med tiden implementere en række statistiske funktioner

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss

# Denne funktion implementerer den funktionelle metode til at lave
# fejlpropagering. Funktionen tager en vilkårlig fitte funktion samt dennes
# estimerede parametre samt covariansmatrice.
# Den beregner derefter fejlen for en given x-værdi

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
                    f(x, *popt) - error, alpha = 0.3)

