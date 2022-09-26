import numpy as np
import matplotlib.pyplot as plt

# This functions takes a list and returns the indices for local-maxima
def thinner(data):
    Is = []
    for i in range(len(data) - 1):
        if data[i] != data[i+1]:
            Is.append(i)
    return Is

def extreme_thinner(data):
    indic = []
    non_repeater = []
    for i in range(len(data) - 1):
        if data[i] in non_repeater:
            continue
        else:
            non_repeater.append(data[i])
            indic.append(i)
    return indic

def continuity(data):
    indic = []
    for i in range(len(data) - 1):
        if abs(data[i] - data[i+1]) < 0.2:
            indic.append(i)
    return indic

def local_maxima(data, threshold_data):

    # We start by thinning the data a bit. We shall reomve any consecutively
    # identical points

    indic = thinner(data)

    # We now set a threshold, that we believe all our local-maxima should
    # exceed.

    threshold = (np.max(data) - np.min(data))/2
    x_thresh = abs(threshold_data[0] - threshold_data[-1])*0.1
    print(x_thresh)

    # the following function checks whether a point is greater than its
    # neighbors

    def greater(i, data):
        if i < len(data)-6:
            if data[i] >= np.median(data[i: i+10]) and data[i] >= np.median(data[i-10: i]):
                if data[i] >= data[i+1] and data[i] >= data[i-1]:
                    return True
            else:
                return False

    # We now run through the thinned data, and check whether points are local
    # maxima

    first_run = []

    for t in indic:
        if t-2 in first_run:
            continue
        if greater(t, data) and data[t] > threshold:
            first_run.append(t)

    loc_max = []

    for i in range(len(first_run)-1):
        if abs(threshold_data[first_run[i]] - threshold_data[first_run[i+1]]) > x_thresh:
            loc_max.append(first_run[i])

    loc_max.append(first_run[-1])

    return loc_max

data = np.loadtxt('../Data/Data1gang/60_måling.txt', skiprows = 3)

fig, ax = plt.subplots()

def sorter(data):
    indices = []
    for i in range(len(data)-1):
        if data[i] < data[i+1]:
            indices.append(i)
    return indices

data = data[::15, :]
data = data[sorter(data[:, 2]), :]

data = data[thinner(data[:, 2]), :]
data = data[data[:, 2].argsort(), :]
data = data[extreme_thinner(data[:, 2]), :]
data = data[continuity(data[:, 1]), :]

for d,k in zip(data[:, 1], data[:, 2]):
    print(d, k)

sup_thresh = (data[0, 2] - data[-1, 2])*0.1
loc_mac = local_maxima(data[:, 1], data[:, 2])

ax.plot(data[:, 2]*10, data[:, 1], 'ko')
ax.plot(data[loc_mac, 2]*10, data[loc_mac, 1], 'ro', markersize = 10)



plt.show()

