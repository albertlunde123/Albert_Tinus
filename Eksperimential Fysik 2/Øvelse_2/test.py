import numpy as np
import os

data = []
len_dir = 10
data_files = os.listdir('Data2øvelsesgang')

print('list')
print(data_files)

print('elems')
for dat in data_files:
    # name = str(base + i*5) + '_1.txt'
    print(dat)
    # data.append(np.loadtxt('Data2øvelsesgang/' + dat, skiprows = 5))

