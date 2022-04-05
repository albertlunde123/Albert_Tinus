import numpy as np
import matplotlib.pyplot as plt
import os

fig, ax = plt.subplots()

path = '../data2/'
filenames = os.listdir(path)

data = np.loadtxt(path + filenames[7], skiprows = 3)

# We only want a thousand points.

skipper = int(round(len(data[:,0])/1000, 0))
data = data[::skipper, :]

# We want to select only a part of the data. Specificically the part that
# resembles a sine-function

# At first, we shall remove the tail of the data. We do this by calculating an
# average distance between points, for some sample of the data. We then go
# through the data, looking for a place where this distance is greatly
# exceeded. If a place is found, we chech whether this is an isolated idea.

start = 400
end = 600

# ave_dist = abs(np.mean(data[start:end, 1] - data[start+1:end+1, 1]))

ave_dist = 0.005

def thinner(data):
    Is = []
    for i in range(len(data) - 1):
        if data[i] != data[i+1]:
            Is.append(i)

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

def sorter(data):
    indices = []
    for i in range(len(data)-1):
        if data[i] < data[i+1]:
            indices.append(i)

def continuity(data):
    indic = []
    for i in range(len(data) - 1):
        if abs(data[i] - data[i+1]) < 0.2:
            indic.append(i)
    return indic

def local_maxima(dat):

    # dat = dat[thinner(dat[:, 2]), :]
    dat = dat[extreme_thinner(dat[:, 0]), :]
    dat = dat[continuity(dat[:, 1]), :]

    print(len(dat[:, 0]))

    # We start by thinning the data a bit. We shall reomve any consecutively
    # identical points

    threshold_data = dat[:, 0]
    data = dat[:, 1]

    indic = thinner(data)

    # We now set a threshold, that we believe all our local-maxima should
    # exceed.

    threshold = (np.max(data) - np.min(data))
    x_thresh = abs(threshold_data[0] - threshold_data[1])*10
    print(x_thresh)

    # the following function checks whether a point is greater than its
    # neighbors

    def greater(i, data):
        if i < len(data)-6:
            if data[i] >= np.median(data[i: i+4]) and data[i] >= np.median(data[i-4: i]):
                if data[i] >= data[i+1] and data[i] >= data[i-1]:
                    return True
            else:
                return False

    # We now run through the thinned data, and check whether points are local
    # maxima

    first_run = []

    for t in range(len(data)):
        if t-2 in first_run:
            continue
        if greater(t, data) and data[t] > threshold:
            first_run.append(t)

    # return dat[first_run, :]
    loc_max = []

    for i in range(len(first_run)-1):
        if abs(threshold_data[first_run[i]] - threshold_data[first_run[i+1]]) > x_thresh:
            loc_max.append(first_run[i])

    loc_max.append(first_run[-1])

    return dat[loc_max, :]

print(ave_dist)

def break_point(data, end):
    breaker = 0
    for i in range(len(data[end:, 1] - 1)):
        if abs(data[end+i, 1] - data[end+i+1, 1]) > ave_dist*10:
            breaker = 1
            for k in range(10):
                if abs(data[end+i+k, 1] - data[end+i+k+1, 1]) < ave_dist*10:
                    breaker = 0
            if breaker == 1:
                return end+i

breaker = break_point(data, end)

lms = local_maxima(data[:breaker, :])

print(len(lms))


ax.plot(lms[:, 0], lms[:, 1], 'ro')

ax.plot(data[:breaker,0],data[:breaker,1], 'k-')
ax.plot(data[breaker:,0],data[breaker:,1], 'b-')

plt.show()


