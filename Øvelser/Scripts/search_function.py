import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
print(os.getcwd())
os.chdir('C:/Users/123ti/Albert_Tinus/Øvelser/Projekt')
df = pd.read_csv('read-out-noise.csv', sep = ',')
#df = pd.read_csv('../read-out-noise.csv', sep = ',')
data = np.array(df.values)

def search(paths):
    result = []
    for d in data:
        i = 0
        for p in paths:
            if p in d[0]:
                i += 1
        if i == len(paths):
            result.append(d)
    a = np.array(result)
    return a[a[:, 1].argsort()]

def string_splitter(string):
    return string.split('_')[1:-1] + [string.split('_')[-1].split('.tif')[0]]

def ordered_search(path, first_order, origin):
    res = []
    for d in first_order:
        search_path = string_splitter(d)
        search_path.remove(origin)
        res.append(search([path] + search_path)[0])
    return np.array(res)

def noises(data):
    res = []
    for d in data:
        res.append(d[1])
    return np.array(res)

def error(data):
    res = []
    for d in data:
        res.append(d[2])
    return np.array(res)

def paths(data):
    res = []
    for d in data:
        res.append(d[0])
    return np.array(res)

def plotter(settings, ax):

    col1 = ['r', 'b', 'k', 'g']
    col2 = ['r--', 'b--', 'k--', 'g--']
    first = search([settings[0]])

    ax.errorbar(range(len(first)),
                noises(first),
                yerr = error(first),
                color = col1[0],
                fmt = 'o',
                capsize = 5)

    ax.plot(range(len(first)),
            noises(first),
            col2[0],
            label = settings[0],
            alpha = 0.6)

    for sett, c1, c2 in zip(settings[1:], col1[1:], col2[1:]):

        ax.errorbar(range(len(first)),
                noises(ordered_search(sett, paths(first), settings[0])),
                yerr = error(ordered_search(sett, paths(first), settings[0])),
                color = c1,
                fmt = 'o',
                capsize = 5)

        ax.plot(range(len(first)),
                noises(ordered_search(sett, paths(first), settings[0])),
                c2,
                label = sett,
                alpha = 0.6)
