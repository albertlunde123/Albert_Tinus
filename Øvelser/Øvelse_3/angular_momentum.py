import numpy as np
import matplotlib.pyplot as plt
import puk as puk
import chi_sq as chi

fig, ax = plt.subplots(2, 2, figsize = (30,15))
ax = ax.ravel()

strings = ['Data0', 'Data2', 'Data4']

trials = []
for s in strings:
    trials.append([puk.Puk(['Data/' + s + '/KastetCenter', 'Data/' + s + '/KastetSide'], 0.0278, 0.0807),
                   puk.Puk(['Data/' + s + '/StilleCenter', 'Data/' + s + '/StilleSide'], 0.0278, 0.0807)
                   ])

colors = ['r--', 'b--', 'g-', 'k--']

for t, ax in zip(trials, ax):
    puk.plot_Puks_angular_momentum(t, ax, colors, alpha = 1)

plt.tight_layout()
plt.show()
