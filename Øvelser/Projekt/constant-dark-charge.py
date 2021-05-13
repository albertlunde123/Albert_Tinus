import numpy as np
import matplotlib.pyplot as plt
import search_function as se
import pandas as pd
import scipy.stats as ss
import scipy.optimize as scp
import darkcharge as DC
import fejlpropagering as fejl

fig, ax = plt.subplots(figsize = (16,8))

df = pd.read_csv('dark-charge.csv', sep = ',')
data = np.array(df.values)

def linear_fit(t, *p):
    b = p[0]
    return 0*t + b

steepness = [[DC.find_a(uniq, data), uniq] for uniq in DC.unique_settings(data)]
print(steepness)

def fitter(f, steep, error):
    guess = [0,0]
    t = list(range(len(steep)))
    popt, pcov = scp.curve_fit(f, t, steep, guess,
                   sigma = error,
                   absolute_sigma = True)
    return [popt, pcov]


# Først plottes og fittes der for alle punkter

ts = list(range(len(steepness)))

steep = [[steep[0][0], a, steep[0][1]] for steep, a in zip(steepness, ts)]
b1s = [[steep[0][0], a, steep[0][1]] for steep, a in zip(steepness, ts) if 'b1' in steep[1]]
not_b1s = [[steep[0][0], a, steep[0][1]] for steep, a in zip(steepness, ts) if 'b1' not in steep[1]]

t = np.linspace(0, len(steep), 100)

ax.errorbar([b[1] for b in b1s],
           [b[0] for b in b1s],
           yerr = [b[2] for b in b1s],
           color = 'b',
           fmt = 'o',
           label = 'hældninger')

ax.errorbar([b[1] for b in not_b1s],
           [b[0] for b in not_b1s],
           yerr = [b[2] for b in not_b1s],
           color = 'r',
           fmt = 'o',
           label = 'b1 - hældninger')


popt1, pcov1 = fitter(linear_fit, [b[0] for b in steep], [b[2] for b in steep])
ax.plot(t, linear_fit(t, *popt1), 'k--')

ax.set_xlabel('Indstillinger', fontsize = 20)
ax.set_ylabel('Dark Charge pr. tid', fontsize = 20)
ax.set_title('Plot over samtlige dark charge indstillinger', fontsize = 20)
ax.legend()
fejl.plot_propagation(t, linear_fit, popt1, pcov1, ax)
plt.tight_layout()


fig.savefig('Latex/Plots/dark_hældninger_1')

fig, ax = plt.subplots(figsize = (16,8))

ax.errorbar([b[1] for b in not_b1s],
           [b[0] for b in not_b1s],
           yerr = [b[2] for b in not_b1s],
           color = 'r',
           fmt = 'o',
           label = 'hældninger uden b1')

popt2, pcov2 = fitter(linear_fit, [b[0] for b in not_b1s], [b[2] for b in not_b1s])
ax.plot(t, linear_fit(t, *popt2), 'k--')
fejl.plot_propagation(t, linear_fit, popt2, pcov2, ax)

ax.set_xlabel('Indstillinger', fontsize = 20)
ax.set_ylabel('Dark Charge pr. tid', fontsize = 20)
ax.set_title('dark charge indstillinger - uden \'b1\'', fontsize = 20)
ax.legend()
plt.tight_layout()


fig.savefig('Latex/Plots/dark_hældninger_2')
