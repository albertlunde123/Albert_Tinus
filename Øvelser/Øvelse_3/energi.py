import numpy as np
import matplotlib.pyplot as plt
import puk as puk
import fejlpropagering as fejl
import chi_sq as chi

fig, ax = plt.subplots(2, 2, figsize = (30,15))
ax = ax.ravel()

strings = ['Data0', 'Data2', 'Data4']

trials = []
for s in strings:
    trials.append([puk.Puk(['Data/' + s + '/KastetCenter', 'Data/' + s + '/KastetSide'], 0.0278, 0.0807),
                   puk.Puk(['Data/' + s + '/StilleCenter', 'Data/' + s + '/StilleSide'], 0.0278, 0.0807)
                   ])

colors = ['r', 'b', 'g', 'k--']

a = []

for t, ax in zip(trials, ax):
    a.append(puk.plot_Puks_energy(t, ax, colors, alpha = 0.6))


def tot_angu_err(Puks):
    return np.sqrt(Puks[0].angu_err()**2+Puks[1].angu_err()**2)

def tot_angu(Puks):
    return Puks[0].angular_momentum() + Puks[1].angular_momentum()


# for ang, exp, err, df in zip()
# plt.tight_layout()
plt.show()
fig.savefig('elastisk_energi')
