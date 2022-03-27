import numpy as np
import matplotlib.pyplot as plt
import os

fig, ax = plt.subplots()

path = '../Data/Data1gang/'
filenames = os.listdir(path)

# We store the datasets along with the noted angle in the format [data, angle]

datasets = []
for f in filenames:
    angle = int(f.split('_')[0])*2
    data_points = np.loadtxt(path + f, skiprows = 3)
    datasets.append([data_points, angle])

# We are interested in plotting the amplitude of the incident wave as a
# function of the measured angle.

def find_amp(data):
    return (max(data[:, 1]) - min(data[:, 1]))/2

angs, amps = [], []
for d in datasets:
    angs.append(d[1])
    amps.append(find_amp(d[0]))

ax.plot(angs, amps, 'ko')
plt.show()


