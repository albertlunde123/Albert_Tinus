import numpy as np
import matplotlib.pyplot as plt
import search_function as se
import pandas as pd

fig, ax = plt.subplots(figsize = (16,8))

df = pd.read_csv('dark-charge.csv', sep = ',')
data = np.array(df.values)

setting = ['b20', 'gH', 'qH', 'r4']

# Det her er lidt frækt.

def sort(data):
    k = []
    order = ['e500.', 'e3000', 'e5000', 'e7000', 'e10000']
    for o in order:
        for d in data:
            if o in d[0]:
                k.append(d)
    return np.array(k)

data = sort(se.search(setting, data))
ts = [int(d[0].split('e')[-1].split('.')[0]) for d in data]

def plot_DC(setting, ds, ax):
    
    data = sort(se.search(setting, ds))
    ts = [int(d[0].split('e')[-1].split('.')[0]) for d in data]

    ax.errorbar(ts, se.noises(data), yerr = se.error(data), color = 'r', fmt = 'o-') #, capsize = 4)
    ax.set_xlabel('Tid', fontsize = 16)
    ax.set_ylabel('Noise', fontsize = 16)
    ax.set_title('Dark Charge som funktion af tid', fontsize = 16)
    ax.legend()

plot_DC(setting, data, ax)

plt.show()
