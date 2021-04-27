import numpy as np
import matplotlib.pyplot as plt
import puk as puk

fig, ax = plt.subplots(2, 2, figsize = (30,15))
ax = ax.ravel()

strings = ['Data0', 'Data2', 'Data4']

trials = []
for s in strings:
    trials.append([puk.Puk(['Data/' + s + '/KastetCenter', 'Data/' + s + '/KastetSide'], 0.0278, 0.0807),
                   puk.Puk(['Data/' + s + '/StilleCenter', 'Data/' + s + '/StilleSide'], 0.0278, 0.0807)
                   ])

colors = ['r--', 'b--', 'g-', 'k--']

a = []

for t, ax in zip(trials, ax):
    a.append(puk.plot_Puks_angular_momentum(t, ax, colors, alpha = 1))


def tot_angu_err(Puks): 
    return np.sqrt(Puks[0].angu_err()**2+Puks[1].angu_err()**2)

def tot_angu(Puks):
    return Puks[0].angular_momentum() + Puks[1].angular_momentum()

def chi_sq(ang, exp, err):
    return sum((ang - exp)**2/err**2)

print(tot_angu_err(trials[0]))

#def p_value(ang, exp, err, df):
#    return round(1 - chi.chi2.cdf(chi_sq(ang, exp, err), df), 3)

df = [len(trials[0][0].get_center(0))-1]*len(trials)

#print(chi_sq(tot_angu(trials[0]), a[0], tot_angu_err(trials[0])))
#print(p_value(tot_angu(trials[0]), a[0], tot_angu_err(trials[0]), df[0]))

# for ang, exp, err, df in zip()
# plt.tight_layout()
plt.show()
