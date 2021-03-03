import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scp
import scipy.special as ss
import os

exec(open('kalibrering.py').read())
exec(open('Statistik.py').read())
exec(open('data_renser.py').read())

print(os.getcwd())

# Vi har nu adgang til funktion func(U, *popt), som er defineret i
# kalibrering.py.

fig, ax = plt.subplots(1, 3, figsize = (20, 5))

# Importer data

def fit(t,*p):
    a = p[0]
    t0 = p[1]
    c = p[2]
    b = p[3]
    return (1/2*a*(t-t0)**2+b*(t-t0)+c)

def plot_data(data, ax, labels, title, kali):

    sol1 = Data(data)
    x = func(sol1.points, *kali)
    t = sol1.t

    mask = sol1.rinse([[-1, 0.1], [0.4, 0.3], [0.6, 0.4]])

    ax.scatter(t[~mask], x[~mask], color = 'blue', label = 'outliers')
    ax.scatter(t[mask], x[mask], color = 'red', label = 'data points')

    guess_params = [1,1,1,1]
    popt,pcov = scp.curve_fit(fit, t[mask][300:], x[mask][300:],
                            guess_params)


    t_fit = np.linspace(-0.4,1.0,1000)
    ax.plot(t_fit, fit(t_fit, *popt), color = 'k', linewidth = 3,
            label = 'fitted function')

    print((pcov))

    error = propagation_function(t_fit, fit, list(popt), pcov)
    ax.fill_between(t_fit, fit(t_fit, *popt) + error,
                    fit(t_fit, *popt) - error, alpha = 0.3)

    ax.set_ylim(-0.2,0.7)
    ax.set_ylabel('x/m')
    ax.set_xlabel('t/s')
    ax.set_title(title)
    ax.legend()


plot_data("Sol1", ax[0], labels = None, title = 'solid cylinder 1',
          kali = kali)

plot_data("Sol2", ax[1], labels = None, title = 'solid cylinder 1',
          kali = kali)

plot_data("Sol3", ax[2], labels = None, title = 'solid cylinder 1',
          kali = kali)

plt.show()

    ###############

    # grader = 15
    # theta = grader*(2*np.pi/360)

    # a = [np.sin(theta)*9.82*0.66, popt[0]]



    # fig.savefig('ruller.png')

