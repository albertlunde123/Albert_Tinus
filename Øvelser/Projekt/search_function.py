import numpy as np
import pandas as pd

df = pd.read_csv('read-out-noise.csv', sep = ',')
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
    return np.array(result)

def noises(data):
    res = []
    for d in data:
        res.append(d[1])
    return np.array(res)

def noise_spread
b1 =
b4 =
b8 =
b20 =


