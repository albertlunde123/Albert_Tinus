import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as scp
from scipy.stats import chi2
import os

fig, ax = plt.subplots(figsize = (9, 7))

os.chdir('c:\\Users\\all\\Albert_Tinus\\Eksperimential Fysik 2\\Øvelse 1\\')
# print(os.getcwd())


deg_to_rad = 2*3.14/360

data = np.loadtxt("Målinger/Serie2.txt", skiprows = 7, delimiter = ',')
data2 = np.loadtxt("Målinger/Serie3.txt", skiprows = 6, delimiter = ',')

vinkler = data[:,0]*deg_to_rad
vinkler2 = data2[:,0]*deg_to_rad


laser_intensitet = data[:,2] / 2.869
laser_intensitet2 = data2[:,1] / 2.869

# Return lists with shared datapoints.
def conjoiner(A, B, k, j):
    C = []
    for i in range(len(A[:,0])):
        for q in range(len(B[:,0])):
            if A[i,0] == B[q, 0]:
                C.append([A[i, 0], A[i, k], B[q, j]])
    return np.array(C)

err = 0.5*deg_to_rad

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

def Ts(theta,n):
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

# def chisq_plot(data, f, ax):
#     Intensity = data[:,0]
#     Theta = data[:,1]

#     theta = np.linspace(0, 0.5*np.pi, 200)

def plot_chi(x, y, err, ax, f, n):

    # fejlpropagering med f
    
    y_err = np.array([])
    for xs in x:
        ye = np.sqrt((f(xs, n) - f(xs + err, n))**2)
        y_err.append(ye)

    print(y_err)
    # plot data med fejl på x og y
    ax.errorbar(x, y, fmt = 'o', xerr = err, yerr = y_err)

    # plot teoretiske funktion
    thetas = np.linspace(0, 1.6, 100)
    ax.plot(thetas, f(thetas, n), '-') 

    # Lav chi2
    #chi = chi_sq(x, y, y_err, f, n, len(y))

# plot_chi(vinkler, laser_intensitet, err, ax, Tp, 0.61)

# Denne funktion plotter 2 datasæt, og fitter det til en konstant.

def plot_curvefit(x1, x2, y1, y2, err, ax, f1 , f2, n):

    # konstant funktion.
        
    def fit(t, *p):
        a = p[0]
        b = p[1]
        return a*t + b

    y_err1 = np.array([])
    for xs in x1:
        ye = np.sqrt((f1(xs, n) - f1(xs + err, n))**2)
        y_err1 = np.append(y_err1, ye)

    y_err2 = np.array([])
    for xs in x2:
        ye = np.sqrt((f2(xs, n) - f2(xs + err, n))**2)
        y_err2 = np.append(y_err2, ye)

    combined_set = conjoiner(np.transpose(np.array([x1, y1])), np.transpose(np.array([x2, y2])), 1, 1)
    
    ax.errorbar(x1, y1, xerr = err, yerr = y_err1, fmt = 'o')
    ax.errorbar(x2, y2, xerr = err, yerr = y_err2, fmt = 'o')

    ax.plot(combined_set[:, 0], combined_set[:,1] + combined_set[:,2], 'o')

    combined_err_set = conjoiner(np.transpose(np.array([x1, y_err1])), np.transpose(np.array([x2, y_err2])), 1, 1)
    combined_err = combined_err_set[:,1] + combined_err_set[:,2]
    
    guess_params = [0, 1]
    popt, pcov = scp.curve_fit(fit, combined_set[:,0], 
            combined_set[:, 1] + combined_set[:, 2],
            guess_params, 
            sigma = combined_err)

    # plot teoretiske funktion
    thetas = np.linspace(0, 1.6, 100)
    ax.plot(thetas, fit(thetas, *popt), '-') 
    

plot_curvefit(vinkler, vinkler2, laser_intensitet, laser_intensitet2, err, ax, Tp, Ts, n)
theta = np.linspace(0, 0.5*np.pi, 200)

# ax.plot(theta, Rp(theta, n), '-', linewidth = 9, color = '#edcfa4')
# ax.plot(theta, Tp(theta, n), '-', linewidth = 9, color = '#d989a6')

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

# ax.text(0.1, 0.1, "$R_p$", fontsize = 35, color = 'white')
# ax.text(0.1, 0.85, "$T_p$", fontsize = 35, color = 'white')
# ax.text(0.82, 0.16, "$\\theta_B$", fontsize = 35, color = 'white')
# ax.arrow(0.85, 0.12, 0, -0.05, color = 'white', width = 0.008)

ax.set_ylim(0, 1.3)
ax.set_xlim(1.2, 1.625)

# ax.set_xlabel('$\\theta$', fontsize = 25, color = 'white')
# ax.set_ylabel('Intensity', rotation = 90, fontsize = 25, color = 'white')
ax.yaxis.labelpad = 20
ax.xaxis.labelpad = 16

# plt.savefig('fresnel2.png')
plt.show()

