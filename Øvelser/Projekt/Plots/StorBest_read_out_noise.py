import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import os 
import sys
sys.path.append('C:/Users/123ti/Albert_Tinus/Øvelser/Scripts')
import search_function as sf
print(os.getcwd())
os.chdir('C:/Users/123ti/Albert_Tinus/Øvelser/Projekt')
fig, ax = plt.subplots(figsize = (16,8))


df = pd.read_csv('read-out-noise.csv')
df.sort_values(by=['Read-Out-Noise'], inplace = True, ascending = True)
data = df.to_numpy()
rons = [data[i][1] for i in np.arange(0,len(data))]
errs = [data[i][2] for i in np.arange(0,len(data))]
settings = [data[i][0] for i in np.arange(0,len(data))]
print(settings)
#Bedste:
#'ron_qH_gL_b4_r0.1.tif', 
#'ron_qH_gL_b20_r0.1.tif', 
#'ron_qH_gL_b1_r0.1.tif', 
#'ron_qH_gL_b1_r1.tif', 
#'ron_qH_gL_b4_r1.tif'
ax.errorbar(np.arange(1,6),rons[:5], errs[:5], capsize = 5, fmt = 's--', color = 'blue')
ax.errorbar(np.arange(6,len(rons)+1),rons[5:], errs[5:], capsize = 5, fmt = 's--', color = 'red')

ax.set_xlabel('Indstillinger', fontsize = 18, labelpad = 20)
ax.set_ylabel('Read-Out Noise', fontsize = 18, labelpad = 20)
ax.set_title('Plot af bedste read-out noise indstillinger', fontsize = 20, pad = 30)
plt.tick_params(right = False, labelbottom = False, bottom = False)
plt.tight_layout()
plt.show()

fig.savefig('C:/Users/123ti/Albert_Tinus/Øvelser/Projekt/Latex/Plots/stortbest_read-out-noise')
