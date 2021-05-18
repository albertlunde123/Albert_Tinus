import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
# sys.path.append('C:/Users/123ti/Albert_Tinus/Øvelser/Scripts')
import search_function1 as se
# print(os.getcwd())
# os.chdir('C:/Users/123ti/Albert_Tinus/Øvelser/Projekt')
import scipy.stats as ss
import scipy.optimize as scp

fig, ax = plt.subplots(figsize = (16,8))

df = pd.read_csv('dark-charge.csv', sep = ',')
data = np.array(df.values)

bs = ['b1', 'b4', 'b8', 'b20']
#setting = [['gM', 'qH', b, 'r0.1'] for b in bs]

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

    data = sort(se.search(setting,ds))
    ts = np.array([int(d[0].split('e')[-1].split('.')[0]) for d in data])/1000

    t_fit = np.linspace(ts[0], ts[-1], 100)

    guess = [0, 600]
    popt, pcov = scp.curve_fit(linear_fit, ts, se.noises(data), guess,
                   bounds = ((0, -np.inf), (np.inf, np.inf)),
                   sigma = se.error(data),
                   absolute_sigma = True)

    ax.plot(t_fit, linear_fit(t_fit, *popt), 'k--')

    ax.errorbar(ts, se.noises(data), color = 'r', fmt = 'o-', markersize = 20) #, capsize = 4)
    ax.set_xlabel('Tid', fontsize = 16)
    ax.set_ylabel('Noise', fontsize = 16)
    ax.set_title('Dark Charge som funktion af tid', fontsize = 16)
    ax.legend()

    print(int(setting[2].split('b')[-1])**2)

    return popt[0]/((int(setting[2].split('b')[-1]))**2)

# for sett in setting:
#      print(plot_DC(sett, data, ax))

def find_a(setting, ds):

    data = sort(se.search(setting, ds))
    ts = np.array([int(d[0].split('e')[-1].split('.')[0]) for d in data])/1000

    guess = [0, 600]
    popt, pcov = scp.curve_fit(linear_fit, ts, se.noises(data), guess,
                             bounds = ((0, -np.inf), (np.inf, np.inf)),
                             sigma = se.error(data),
                             absolute_sigma = True)
    b = 1

    for sett in setting:
        if 'b' in sett:
            b = sett

    return popt[0]/((int(b.split('b')[-1]))**2), np.sqrt(np.diag(pcov))[0]/((int(b.split('b')[-1]))**2)

def unique_settings(data):
    all_setts = []
    for d in data:
        all_setts.append(se.string_splitter(d[0].split('_e')[0]))

    unique_setts = []
    for sett in all_setts:
        if sett in unique_setts:
            continue
        else:
            unique_setts.append(sett)
    return unique_setts

val = plot_DC(['gM', 'qH', 'b1', 'r1'], data, ax)


# print(unique_settings(data))
steepness = [[find_a(uniq, data), uniq]for uniq in unique_settings(data)]
print(steepness)
# print(find_a(setting[0], data))

ax.set_xlabel('Tid(s)', fontsize = 26)
ax.set_ylabel('Signal pr. pixel', fontsize = 26)
ax.set_title('Dark current som funktion af tid', fontsize = 26)
ax.legend()
plt.show()
fig.savefig('Latex/Plots/DarkCurrent')
# fig.savefig('C:/Users/123ti/Albert_Tinus/Øvelser/Projekta/Latex/Plots/DarkCurrent')
