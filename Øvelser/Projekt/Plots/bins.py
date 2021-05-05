import matplotlib.pyplot as plt
import numpy as np
import search_function as sf
import pandas as pd

fig, ax = plt.subplots(figsize = (16,8))

df = pd.read_csv('../read-out-noise.csv', sep = ',')
data = np.array(df.values)

sf.plotter(['b1', 'b4', 'b8', 'b20'], ax)

ax.set_xlabel('Indstillinger', fontsize = 18, labelpad = 20)
ax.set_ylabel('Read-Out Noise', fontsize = 18, labelpad = 20)
ax.set_title('Plot af bins indstillinger', fontsize = 20, pad = 30)
plt.tick_params(right = False, labelbottom = False, bottom = False)
plt.tight_layout()
ax.legend()
plt.show()

fig.savefig('bins')
