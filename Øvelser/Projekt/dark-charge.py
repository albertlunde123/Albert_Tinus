import numpy as np
import matplotlib.pyplot as plt
import search_function as se
import pandas as pd
import scipy.stats as ss
import scipy.optimize as scp

fig, ax = plt.subplots(figsize = (32,16))

df = pd.read_csv('dark-charge.csv', sep = ',')
data = np.array(df.values)

bs = ['b1', 'b4', 'b8', 'b20']
setting = [[b, 'gM', 'qH', 'r0.1'] for b in bs]

def sort(data):
    k = []
    order = ['e500.', 'e3000', 'e5000', 'e7000', 'e10000']
    for o in order:
        for d in data:
            if o in d[0]:
                k.append(d)
    return np.array(k)

def linear_fit(t, *p):
    a = p[0]
    b = p[1]
    return a*t+b

def plot_DC(setting, ds, ax):

    data = sort(se.search(setting, ds))
    ts = np.array([int(d[0].split('e')[-1].split('.')[0]) for d in data])/1000

    t_fit = np.linspace(ts[0], ts[-1], 100)

    guess = [0, 600]
    popt, pcov = scp.curve_fit(linear_fit, ts, se.noises(data), guess,
                   # sigma = error,
                   absolute_sigma = True)

    ax.plot(t_fit, linear_fit(t_fit, *popt), 'k--')

    ax.errorbar(ts, se.noises(data), color = 'r', fmt = 'o-') #, capsize = 4)
    ax.set_xlabel('Tid', fontsize = 16)
    ax.set_ylabel('Noise', fontsize = 16)
    ax.set_title('Dark Charge som funktion af tid', fontsize = 16)
    ax.legend()

    print(int(setting[0].split('b')[-1])**2)

    return popt[0]/((int(setting[0].split('b')[-1]))**2)

for sett in setting:
    print(plot_DC(sett, data, ax))


plt.show()
