import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.optimize as scp

fig, ax = plt.subplots(figsize = (10,10))


path = "data_4/"
print(os.getcwd())
filenames = sorted(os.listdir(path))
for f in filenames:
    if 'sol' in f:
        filenames.remove(f)

data1 = np.loadtxt(path + filenames[0], skiprows = 14 )

dataSet = []

for f in filenames:
    data = np.loadtxt(path + f, skiprows= 14)
    dataSet.append(data)
    
for data in dataSet:
    plt.errorbar(data[:,0], data[:,1])
