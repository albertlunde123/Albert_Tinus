import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as scp
import os

fig, ax = plt.subplots()

n = np.arcsin(2/3)

def Rp(theta, n):
    a = np.tan(theta - n*theta)**2
    b = np.tan(theta + n*theta)**2
    return a/b

def Rs(theta):
    a = np.sin(theta - n*theta)**2
    b = np.sin(theta + n*theta)**2
    return a/b

def Tp(theta):
    a = np.sin(2*theta)*np.sin(2*n*theta)
    b = np.sin(theta + n*theta)**2*np.cos(theta - n*theta)**2
    return a/b

def Ts(theta):
    a = np.sin(2*theta)*np.sin(2*n*theta)
    b = np.sin(theta + n*theta)**2
    return a/b

theta = np.linspace(0, 0.5*np.pi, 200)

ax.plot(theta, Rp(theta, n), '-')
plt.show()

