import numpy as np
import matplotlib.pyplot as plt
import search_function1 as se
import pandas as pd
import scipy.stats as ss
import scipy.optimize as scp

fig, ax = plt.subplots(figsize = (32,16))

df = pd.read_csv('dark-charge.csv', sep = ',')
data = np.array(df.values)

bs = ['b1', 'b4', 'b8', 'b20']
setting = [['gM', 'qH', b, 'r0.1'] for b in bs]
setting = ['qL', 'r1', 'b1', 'gL']

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
                   sigma = se.error(data),
                   absolute_sigma = True)

    ax.plot(t_fit, linear_fit(t_fit, *popt), 'k--')

    ax.errorbar(ts, se.noises(data), color = 'r', fmt = 'o-') #, capsize = 4)
    ax.set_xlabel('Tid', fontsize = 16)
    ax.set_ylabel('Noise', fontsize = 16)
    ax.set_title('Dark Charge som funktion af tid', fontsize = 16)
    ax.legend()

    print(int(setting[2].split('b')[-1])**2)

    return popt[0]/((int(setting[2].split('b')[-1]))**2)

print(plot_DC(setting, data, ax))
ax.set_xlabel('', fontsize = 16)
ax.set_ylabel('', fontsize = 16)
ax.set_title('', fontsize = 16)
ax.legend()
plt.show()

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

def find_effektiv_a(setting, ds):
    
    data = sort(se.search(setting, ds))
    ts = np.array([int(d[0].split('e')[-1].split('.')[0]) for d in data])/1000

    guess = [0, 600]
    popt, pcov = scp.curve_fit(linear_fit, ts, se.noises(data), guess,
                             bounds = ((0, 500), (0.5, 700)),
                             sigma = se.error(data),
                             absolute_sigma = True)
    b = 1

    for sett in setting:
        if 'b' in sett:
            b = sett

    return popt[0], np.sqrt(np.diag(pcov))[0]
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

b1s = unique_settings(se.search(['b1'], data))
for b in b1s:
    print(b)
    print(find_a(b, data))


# print(unique_settings(data))
# steepness = [[find_a(uniq, data), uniq]for uniq in unique_settings(data)]
# print(steepness)
# print(find_a(setting[0], data))

# ax.set_xlabel('', fontsize = 16)
# ax.set_ylabel('', fontsize = 16)
# ax.set_title('', fontsize = 16)
# ax.legend()
# plt.show()
