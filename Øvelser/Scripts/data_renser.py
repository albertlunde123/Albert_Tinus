# Den script loader data, og gemmer dette i et data object.
# Det definere desuden .rinse() på dette dataobjekt, som gennemsøger
# dataet for outliers.

import numpy as np

class Data():

    def __init__(self, path):
        self.path = 'Datas/' + path +'.txt'
        self.points = np.loadtxt(self.path)[:, 1]
        self.t = np.loadtxt(self.path)[:, 0]/1000

# Her defineres .rinse() metoden. Denne tager et data objekt, samt en
# list med limits. Et limit består af 2 grænser. rinse metoden
# kigger self.points igennem og noterer første gang den rammer grænse 1.
# Den noterer alle punkter som ligger under grænse 2 og gemmer deres index.

    def rinse(self, limits):
        index = []
        for lim in limits:
            j = 0
            while self.points[j] < lim[0]:
                j += 1
            for i in list(range(len(self.points)))[j:]:
                if self.points[i] < lim[1]:
                    index.append(i)
        mask = np.full(len(self.points), True, dtype = bool)
        mask[index] = False
        return mask

# def plot_data(data, mask, ax, f):
#     ax.scatter(data.t[mask],
#                f(data.points)[mask])
               # color = col,
               # label = label)
