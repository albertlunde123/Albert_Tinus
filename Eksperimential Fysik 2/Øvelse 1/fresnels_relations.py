import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as scp
from scipy.stats import chi2
import os

fig, ax = plt.subplots(figsize = (9, 7))

# Brydningsindeks for glas
# Vi kan eventuelt også benytte os af det teoretiske brydningsindeks
# vi har bestemt.

n = np.arcsin(2/3)

# De forskellige intensitets funktioner.

def Rp(theta, n):
    a = np.tan(theta - n*theta)**2
    b = np.tan(theta + n*theta)**2
    return a/b

def Rs(theta):
    a = np.sin(theta - n*theta)**2
    b = np.sin(theta + n*theta)**2
    return a/b

def Tp(theta, n):
    a = np.sin(2*theta)*np.sin(2*n*theta)
    b = np.sin(theta + n*theta)**2*np.cos(theta - n*theta)**2
    return a/b

def Ts(theta):
    a = np.sin(2*theta)*np.sin(2*n*theta)
    b = np.sin(theta + n*theta)**2
    return a/b

# Chi^2 og p-værdi funktioner.

def chi_sq(t, x, err, f, n, df):
    chi_sq = sum((x - f(t, n))**2/err**2)
    p_value = 1 - chi2.cdf(chi_sq, df)
    return chi_sq, p_value

# def p_value(chi_sq, df):
#     return round(1 - chi2.cdf(chi_sq, df), 3)


def chisq_plot(data, f, ax):
    Intensity = data[:,0]
    Theta = data[:,1]

    theta = np.linspace(0, 0.5*np.pi, 200)

theta = np.linspace(0, 0.5*np.pi, 200)

ax.plot(theta, Rp(theta, n), '-', linewidth = 9, color = '#edcfa4')
ax.plot(theta, Tp(theta, n), '-', linewidth = 9, color = '#d989a6')

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

ax.text(0.1, 0.1, "$R_p$", fontsize = 35, color = 'white')
ax.text(0.1, 0.85, "$T_p$", fontsize = 35, color = 'white')
ax.text(0.82, 0.16, "$\\theta_B$", fontsize = 35, color = 'white')
ax.arrow(0.85, 0.12, 0, -0.05, color = 'white', width = 0.008)

ax.set_ylim(0, 1.05)
ax.set_xlim(0, 1.625)

ax.set_xlabel('$\\theta$', fontsize = 25, color = 'white')
ax.set_ylabel('Intensity', rotation = 90, fontsize = 25, color = 'white')
ax.yaxis.labelpad = 20
ax.xaxis.labelpad = 16

plt.savefig('fresnel2.png')
plt.show()

