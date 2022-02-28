import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as scp
from scipy.stats import chi2
import os

# fig, ax = plt.subplots(figsize = (9, 7))

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

print(np.arcsin(1/1.77))
print(np.arcsin(0.08))

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

def prop(f, popt, popt_err):
    f_error = 0

    err = popt_err
    for i in range(len(err)):

        j = popt[:i] + [popt[i] + err[i]] + popt[i+1:]
        f_error += (f(*j)-f(*popt))**2

    return  np.sqrt(f_error)

# De forskellige intensitets funktioner.

def Rp(theta, n):
    a = np.tan(theta - n*theta)**2
    b = np.tan(theta + n*theta)**2
    return a/b

def Rs(theta, n):
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

def plot_chi(x, y, err, ax, f, n, n_err, color, color_fill):

    # fejlpropagering med f
    
    y_err = np.array([])
    for xs in x:
        ye = np.sqrt((f(xs, n) - f(xs + err, n))**2)
        y_err = np.append(y_err, ye)

    # plot data med fejl på x og y
    ax.errorbar(x, y, fmt = 'o', xerr = err, yerr = y_err, color = color)

    # plot teoretiske funktion
    thetas = np.linspace(0, 1.55, 100)
    err = [prop(f, [theta, n], [0, 0.2]) for theta in thetas]
    
    ax.fill_between(thetas, f(thetas, n) + err,
                    f(thetas, n) - err, 
                    alpha = 0.3,
                    color = color_fill)
    
    ax.plot(thetas, f(thetas, n), '-', color = color) 

    # Lav chi2
    #chi = chi_sq(x, y, y_err, f, n, len(y))

# plot_chi(vinkler, laser_intensitet, err, ax, Tp, 0.61)

# Denne funktion plotter 2 datasæt, og fitter det til en konstant.

def plot_curvefit(x1, x2, y1, y2, err, ax, f1 , f2, n, color):

    # konstant funktion.
        
    def fit(t, *p):
        a = p[0]
        b = p[1]
        return a*t + b

    combined_set = conjoiner(np.transpose(np.array([x1, y1])), np.transpose(np.array([x2, y2])), 1, 1)
    
    comb_err = np.array([])
    for xs in combined_set[:, 0]:
        ye = np.sqrt((f1(xs, n) - f1(xs + err, n))**2 + (f2(xs, n) - f2(xs + err, n))**2)
        comb_err = np.append(comb_err, ye)

    ax.errorbar(combined_set[:, 0], 
        combined_set[:,1] + combined_set[:,2], 
        yerr = comb_err, 
        fmt ='o',
        color = color)

    # combined_err_set = conjoiner(np.transpose(np.array([x1, y_err1])), np.transpose(np.array([x2, y_err2])), 1, 1)
    # combined_err = combined_err_set[:,1] + combined_err_set[:,2]
    
    guess_params = [0, 1]
    popt, pcov = scp.curve_fit(fit, combined_set[:,0], 
            combined_set[:, 1] + combined_set[:, 2],
            guess_params, 
            sigma = comb_err)

    # plot teoretiske funktion
    thetas = np.linspace(combined_set[:, 0][0], combined_set[:, 0][-1], 100)
    

    # plot_propagation(thetas, fit, popt, pcov, ax)
    ax.plot(thetas, fit(thetas, *popt), '-', color = 'white') 
    

# plot_curvefit(vinkler, vinkler2, laser_intensitet, laser_intensitet2, err, ax, Tp, Ts, n)
# theta = np.linspace(0, 0.5*np.pi, 200)

# # ax.plot(theta, Rp(theta, n), '-', linewidth = 9, color = '#edcfa4')
# # ax.plot(theta, Tp(theta, n), '-', linewidth = 9, color = '#d989a6')

# ax.spines['bottom'].set_color('white')
# ax.spines['top'].set_color('white')
# ax.spines['left'].set_color('white')
# ax.spines['right'].set_color('white')

# ax.tick_params(axis='x', colors='white')
# ax.tick_params(axis='y', colors='white')

# fig.patch.set_facecolor('#313847')
# ax.set_facecolor('#313847')

# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)

# # ax.text(0.1, 0.1, "$R_p$", fontsize = 35, color = 'white')
# # ax.text(0.1, 0.85, "$T_p$", fontsize = 35, color = 'white')
# # ax.text(0.82, 0.16, "$\\theta_B$", fontsize = 35, color = 'white')
# # ax.arrow(0.85, 0.12, 0, -0.05, color = 'white', width = 0.008)

# ax.set_ylim(0, 1.3)
# ax.set_xlim(1.2, 1.625)

# # ax.set_xlabel('$\\theta$', fontsize = 25, color = 'white')
# # ax.set_ylabel('Intensity', rotation = 90, fontsize = 25, color = 'white')
# ax.yaxis.labelpad = 20
# ax.xaxis.labelpad = 16

# # plt.savefig('fresnel2.png')
# plt.show()

