
# Plot af Rs og Ts, hvor disse sammenlignes med de teoretiske kurver.

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as scp
from scipy.stats import chi2
import os

os.chdir('c:\\Users\\all\\Albert_Tinus\\Eksperimential Fysik 2\\Øvelse 1\\')

import fresnels_relations as fre

fig, ax = plt.subplots(figsize = (9, 7))

# Vi bruger Serie2 og Serie3 dataet.

Tp_data = np.loadtxt("Målinger/Serie2.txt", skiprows = 7, delimiter = ',')
Rp_data = np.loadtxt("Målinger/Serie3.txt", skiprows = 6, delimiter = ',')

Tp_vinkler = Tp_data[:,0] * fre.deg_to_rad
Rp_vinkler = Rp_data[:,0] * fre.deg_to_rad

Tp_intens = Tp_data[:,2]/2.869
Rp_intens = Rp_data[:,1]/2.869

err = 0.5*fre.deg_to_rad

# fre.plot_chi(Tp_vinkler, Tp_intens, err, ax, fre.Tp, 0.61, '#edcfa4')
fre.plot_curvefit(Tp_vinkler, Rp_vinkler, Tp_intens, Rp_intens, err, ax, fre.Tp, fre.Rp, 0.61, "#e1341e")

theta = np.linspace(0, 0.5*np.pi, 200)

# ax.plot(theta, Rp(theta, n), '-', linewidth = 9, color = '#edcfa4')
# ax.plot(theta, Tp(theta, n), '-', linewidth = 9, color = '#d989a6')

ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# ax.set_ylim(-0.1, 1.1)

fig.patch.set_facecolor('#313847')
ax.set_facecolor('#313847')

props = dict(boxstyle = 'square, pad=0.5',
            facecolor = '#e1341e',
            edgecolor = '#313847'
)

props1 = dict(boxstyle = 'square, pad=0.5',
            facecolor = '#fff000',
            edgecolor = '#313847'
)

# ax.text(0.05, 0.94, "Transmitted", color = 'white', bbox = props)
# ax.text(0.05, 0.038, "Reflected", color = '#313847', bbox = props1)

ax.set_xlabel("$\\theta_{incident} $ in rad", color = 'white', fontsize = 16)
ax.set_ylabel("Intensity", color = 'white', fontsize = 16)

ax.set_title("Sum of P-polarized light", fontsize = 16, color = 'white')



plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# ax.text(0.1, 0.1, "$R_p$", fontsize = 35, color = 'white')
# ax.text(0.1, 0.85, "$T_p$", fontsize = 35, color = 'white')
# ax.text(0.82, 0.16, "$\\theta_B$", fontsize = 35, color = 'white')
# ax.arrow(0.85, 0.12, 0, -0.05, color = 'white', width = 0.008)



# ax.set_xlabel('$\\theta$', fontsize = 25, color = 'white')
# ax.set_ylabel('Intensity', rotation = 90, fontsize = 25, color = 'white')
ax.yaxis.labelpad = 20
ax.xaxis.labelpad = 16

plt.savefig('PSum.png')
plt.show()




