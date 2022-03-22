import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.optimize as scp

fig, ax = plt.subplots()

# os.chdir('c:\\Users\\all\\Albert_Tinus\\Eksperimential Fysik 2\\Øvelse_2\\')

data = np.loadtxt("Vinkel_Data/Kurveformer/65_2.txt", skiprows = 3)[:2000, [0,1,2]]

# Find data points that are either rising or falling.
def sorter(data, k):
    returner = []
    for i in range(len(data)-1):
        if data[i] < data[i+k]:
            returner.append(i)
    return returner

def sorter2(data):
    returner = []
    for i in range(len(data)-1):
        if abs(data[i] -data[i+1]) < 0.4:
            returner.append(i)
    return returner
# Sinusoidal function we are trying to fit against.
def fit(V, *p):
    a = p[0]
    b = p[1]
    c = p[2]
    d = p[3]
    k = p[4]
    # e = p[4]
    return a*np.cos(b + V*d*np.exp((-k*V))) + c

# Plot the data and the fit.
def plot_fit_data(data, ax, k, i, color):
    # Data to be plotted.
    data = data[sorter(data[:, 2], i), :]
    data = data[sorter2(data[:, 1]), :]

    data = data[data[:, 2].argsort()]
    # data = np.sort(data[sorter(data[:, 2], i),:])

    # Frequencies and voltage
    freq = data[:, 2]*10
    voltage = data[:, 1]

    maks = np.max(voltage)
    min = np.min(voltage)

    # Good guesses.
    guess_a = (maks - min)/2
    guess_c = (maks + min)/2


    # Hvordan finder vi et godt estimat for b? Når funktionen antager sit maks
    # skal cos(b + V*d*exp(-kV)) = 1. Hvor V = V_maks. Vi kan aflæse et V_maks
    # fra dataet, eller vi kan bestemme det med én funktion.

    # Lad os lige skrive dette program rent.

    # Vi starter med at finde alle lokale maksima. Et lokalt maksima, vil i
    # snit være større end punkterne på hver side af det. Denne funktion løber
    # alle punkterne igennem og tjekker om de er lokale maksima.

    def local_maxima():
        indices = []
        for i in range(len(freq[:-6])):
            # Vi tjekker om vi allerede har fundet et lokalt maksima i
            # nærheden.
            if any(x in range(i-10, i) for x in indices):
                continue
            # Tjekker om punktet er større end punkterne på hver side. Vi
            # tjekker et stort antal punkter på hver side, da vi ellers kan
            # komme til at finde nogle "pseudo-maksima"
            if voltage[i] >= np.mean(voltage[i-1:i+10]) and voltage[i] >= voltage[i+1]:
                if voltage[i] >= np.mean(voltage[i-10:i+1]) and voltage[i] >= voltage[i-1]:
                    if len(voltage) != 0:
                        if abs(voltage[i]/voltage[0]) > 0.9:
                            indices.append(i)
                    else:
                        indices.append(i)
        real_indices = []
        for i in indices:
            if abs(voltage[i]/max(voltage[indices])) > 0.8:
                real_indices.append(i)

        return real_indices

    # if ax != 0:
    #     ax.plot(freq[local_maxima], voltage[local_maxima], 'ko', markersize = 10)

    first_max = np.max(voltage[50:int(round(len(voltage)/5, 0))])
    V_maks = 0
    the_i = 0
    for i in range(len(voltage)):
        if abs(voltage[i]-first_max) == 0:
            V_maks = freq[i]
            the_i = i
            break

    guess_d = 0
    start_i = the_i + 60

    while guess_d == 0:
        if abs(voltage[the_i] - voltage[start_i]) < 0.1:
            guess_d = (2*3.14)/((freq[start_i] - freq[the_i])*np.exp(k*voltage[start_i]))
            break
        start_i += 1

    def find_d_b(first, last):
        d = (-2*np.pi/(first*(np.exp(-k*first)) - last*(np.exp(-k*last))))
        b = -d*first*np.exp(-k*first)
        return d,b

    guess_d, guess_b = find_d_b(freq[the_i], freq[start_i])
    guess_d = guess_d
    guess_b = guess_b
    # guess_d = sum(ds)/len(ds)
    # guess_d = guess_d*1
    # guess_b = -guess_d*V_maks*np.exp(-k*V_maks)

    # guess_b = -2.1
    guess_params = [guess_a, guess_b, guess_c, guess_d, k]


    popt, pcov = scp.curve_fit(fit,
                        freq,
                        voltage,
                        guess_params,
                        bounds = ((guess_a-abs(guess_a*0.00001),
                                guess_b - abs(guess_b)*0.0000001,
                                guess_c-abs(guess_c*0.00001),
                                guess_d - abs(guess_d*0.0000001),
                                k - abs(k*0.00000001)),
                                (guess_a+abs(guess_a*0.00001),
                                guess_b +abs((guess_b)*0.0000001),
                                guess_c+abs(guess_c*0.00001),
                                guess_d + abs(guess_d*0.0000001),
                                k +abs(k*0.000000001))))

    Vs = np.linspace(freq[0], freq[-1], 1000)

    if ax != 0:
        ax.plot(freq, voltage, 'o', color = color)
        ax.plot(Vs, fit(Vs, *popt), '--', color = 'black')
        ax.set_ylim(guess_c - guess_a*1.2, guess_a*1.2 + guess_c)

    return popt, np.sum(np.sqrt(np.diag(pcov)))

# in theory, we should be able to extract the path distance from this.

wave_length = 650*10**-3

def path_dist(V, *p):
    a = p[0]
    k = p[1]
    return a*V*np.exp(-k*V)

ax.set_title('Measured signal - piezo-expansion', fontsize = 20)
ax.set_xlabel('$V$-piezo', fontsize = 20)
ax.set_ylabel('$V$-measured', fontsize = 20)
# fig.patch.set_facecolor('#bde5ff')
ax.set_facecolor('#dcdcdc')
# BOX
props = dict(boxstyle = 'square, pad=0.5',
            facecolor = '#ff9500',
            edgecolor = '#313847'
)

text = '$\ V_m =  D\cdot \cos (aV \\cdot e^{-kV}) + B$'

# ax.text(-1, 3.2,
#         text,
#         color = 'black',
#         bbox = props,
#         fontsize = 16)
plt.savefig('Rapport/figures/fit_example.png')

def best_fit_coeff(data, j):
    k = 0.1*10**-3
    pcovs = []
    popts = []
    for i in range(1000):
        popt, pcov = plot_fit_data(data, 0, k+i*10**(-5), j, 0)
        pcovs.append(pcov)
        popts.append(popt)
    return popts[np.argmin(np.array(pcovs))][-1]

k = best_fit_coeff(data, 1)

print(plot_fit_data(data, ax, k, 1, 'red'))

plt.savefig('example_expanse.png')
plt.show()
