import numpy as np
import matplotlib.pyplot as plt
import os

fig, ax = plt.subplots(figsize = (20, 10))

files = os.listdir('data_4')
sol = 'data_4/' + [f for f in files if 'sol' in f][0]

data = np.loadtxt(sol, skiprows = 14)
xs, ys = data[:, 0], data[:, 1]


spec_lines = {
    'O2':	898.765,
    'O2_1':	822.69,
    'O2_2':	759.37,
    'O2_3':	686.71,
    'Hα':	656.28,
    'O2_4':	627.66,
    'Na':	589.59,
    'Na_1':	588.995,
    'He':	587.5618,
    'Hg':	546.073,
    'Fe':	527.039,
    'Mg':	518.362,
    'Mg_1':	517.270,
    'Fe_1':	516.891,
    'Mg_2':	516.733,
    'Fe_2':	495.761,
    'Hβ':	486.134,
    'Fe_3':	466.814,
    'Fe_4':	438.355,
    'Hγ':	434.047,
    'Fe_5':	430.790,
    'Ca':	430.774,
    'Hδ':	410.175,
    'Ca_1':	396.847,
    'Ca_2':	393.366,
    'Fe_5':	382.044,
    'Fe_6':	358.121,
    'Ti':	336.112,
    'Fe_7':	302.108,
    'Ni':	299.444,
}

# Nu tager differensen og finder derefter de mindste værdier. Vi er de
# interesserede i de relative differenser

# Den funktion vi bruger vægter tingene lidt underligt. Det er klart at der vil
# være mulighed for mere blokering i de områder hvor der udsendes meget lys. Vi
# vælger derfor at kigge på spektret i zoner. Vi vælger så de mest ekstreme
# værdier i hver zone.

def spec_zone(data, begin):
    try:
        return np.argsort(data[begin: begin + 100])[0] + begin
    except:
        return np.argsort(data[begin:])[0] + begin

small_indic = []
for k in range(21):
    small_indic.append(spec_zone(np.diff(ys, n=1), k*100))

# for e in small_indic:
#     ax.vlines(xs[e], 0, 25000, color = 'red')

# Vi plotter de teoretiske linjer,

# for k in spec_lines.keys():
#     ax.vlines(spec_lines[k], 0, 25000, color = 'black')
    # ax.text(spec_lines[k], 26000, k)


h = 6.6*10**(-34)
c = 3*10**8
k = 1.38*10**(-23)

# def Boltzmann(T, l):
#     return ((2*h*c)/l**3)*(1/(np.exp(h*c/(c*k*T)-1)))

def Boltzmann(T, l):
    return ((8*np.pi*h*c)/(l**5))*(1/(np.exp(h*c/(l*k*T))-1))


ls = np.linspace(1*10**(-9), 1000*10**(-9), 500)

teo_ys = Boltzmann(6000, ls)/np.max(Boltzmann(6000,ls))*np.max(ys)
print(np.max(teo_ys))

ax.plot(ls*10**9, teo_ys, color = 'red')
ax.plot(xs, ys)
plt.show()

