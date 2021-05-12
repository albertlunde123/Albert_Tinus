import numpy as np
import matplotlib.pyplot as plt
import search_function as se
import pandas as pd
import scipy.stats as ss
import scipy.optimize as scp
import darkcharge as DC
import fejlpropagering as fejl

fig, ax = plt.subplots(1, 2, figsize = (32,16))

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

ax[0].errorbar([b[1] for b in b1s],
           [b[0] for b in b1s],
           yerr = [b[2] for b in b1s],
           color = 'b',
           fmt = 'o')

ax[0].errorbar([b[1] for b in not_b1s],
           [b[0] for b in not_b1s],
           yerr = [b[2] for b in not_b1s],
           color = 'r',
           fmt = 'o')


popt1, pcov1 = fitter(linear_fit, [b[0] for b in steep], [b[2] for b in steep])
ax[0].plot(t, linear_fit(t, *popt1), 'k--')

ax[0].set_xlabel('Indstillinger', fontsize = 16)
ax[0].set_ylabel('Dark Charge pr. tid', fontsize = 16)
ax[0].set_title('Plot over samtlige dark charge indstillinger', fontsize = 16)
ax[0].legend()
fejl.plot_propagation(t, linear_fit, popt1, pcov1, ax[0])

ax[1].errorbar([b[1] for b in not_b1s],
           [b[0] for b in not_b1s],
           yerr = [b[2] for b in not_b1s],
           color = 'r',
           fmt = 'o')

popt2, pcov2 = fitter(linear_fit, [b[0] for b in not_b1s], [b[2] for b in not_b1s])
ax[1].plot(t, linear_fit(t, *popt2), 'k--')
fejl.plot_propagation(t, linear_fit, popt2, pcov2, ax[1])

# ax[1].plot(t, linear_fit(t, *fitter(linear_fit, [b[0] for b in not_b1s])[0]), 'k--')
ax[1].set_xlabel('Indstillinger', fontsize = 16)
ax[1].set_ylabel('Dark Charge pr. tid', fontsize = 16)
ax[1].set_title('dark charge indstillinger - uden \'b1\'', fontsize = 16)
ax[1].legend()

plt.show()
