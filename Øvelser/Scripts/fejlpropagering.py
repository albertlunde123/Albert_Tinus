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

def prop(f, popt, popt_err):
    f_error = 0

    err = popt_err
    for i in range(len(err)):

        j = popt[:i] + [popt[i] + err[i]] + popt[i+1:]
        f_error += (f(*j)-f(*popt))**2

    return  np.sqrt(f_error)

def propagation_function_2(f, popt, popt_err):
    errs = []
    for i in range(len(popt)):
        errs.append(prop(f, popt[i], popt_err[i]))
    return errs

def plot_propagation(x, f, popt, pcov, ax):
    error = propagation_function(x, f, list(popt), pcov)
    ax.fill_between(x, f(x, *popt) + error,
                    f(x, *popt) - error, alpha = 0.3)

def collector(x):
    ll = []
    for i in range(len(x[0])):
                bb = []
                for j in range(len(x)):
                   bb.append(x[j][i])
                ll.append(bb)
    return ll

# x = [1,1,1,1,1]
# y = [2,2,2,2,2]
# z = [3,3,3,3,3]
# q = [4,4,4,4,4]

# print(collector([x,y,z,q]))

# def f(*p):
#     A = p[0]
#     B = p[1]
#     return A + B

# print(propagation_function_2(f, collector([x,y]), collector([z,q])))

# b = [[x[i],y[i]] for i in range(len(x))]
# x_err = [1,1,1,1,1]
# y_err = [1,1,1,1,1]


# popt = [x,y]
# popt_err = [x_err, y_err]

