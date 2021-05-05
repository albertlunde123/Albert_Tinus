import matplotlib.pyplot as plt
import numpy as np
import search_function as sf
import pandas as pd

fig, ax = plt.subplots(figsize = (16,8))

df = pd.read_csv('../read-out-noise.csv', sep = ',')
data = np.array(df.values)

sf.plotter(['qH', 'qL'], ax)

ax.set_xlabel('', fontsize = 16)
ax.set_ylabel('', fontsize = 16)
ax.set_title('', fontsize = 16)
ax.legend()
plt.show()
