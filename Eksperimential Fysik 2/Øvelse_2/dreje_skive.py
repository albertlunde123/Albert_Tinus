import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.optimize as scp

fig, ax = plt.subplots()

def load_data(path):
    data = {}
    for file in os.listdir(path):
        if 'serie' not in file:
            print('hello')
            angle = file.split('_')[0]
            tmp = np.loadtxt(path + file, skiprows = 3)
            data.update({angle: tmp})
    return data

data = load_data('Vinkel_Data/Kurveformer/')


# Nu skal vi lave en funktion som klistrer dataet sammen ved skiftet omkring 80
# grader.

def stitch_data(angle, data): # angle is a string.
    keys = [key for key in data.keys() if angle in key]

    dat1 = data[keys[0]]
    dat2 = data[keys[1]]

    amp_dat1 = max(dat1[:,1]) - min(dat1[:,1])/2
    amp_dat2 = max(dat2[:,1]) - max(dat1[:,1])/2

    off_dat1 = max(dat1[:,1]) + min(dat1[:,1])/2
    off_dat2 = max(dat2[:,1]) + min(dat1[:,2])/2

    b = off_dat2 - off_dat1
    a = -amp_dat2#/amp_dat1

    # index_length = min(len(dat1[:,0]), len(dat2[:,0]))
    # diff = dat1[:index_length,:] - dat2[:index_length:,:]
    return [a,b]



def convert(data, *p):
    a = p[0]
    b = p[1]
    return a*(data-b*0)

# Min idé
# Nu skal vi lave en funktion som fitter data'et. Den skal så returnerer
# amplituden og plotte denne mod vinklen.

# stitch = stitch_data('80', data)

# dat1 = data['80']
# dat2 = data['80 aa.txt']

# ax.plot(dat1[:,2], dat1[:,1])
# ax.plot(dat2[:,2], dat2[:,1]) #convert(dat2[:,1], *stitch))

# måsker fjerne offsettet på det hele.

# Lad os prøve bare at plotte amplituderne af data'et mod-vinklen

angles = []
amps = []

sca1 = (max(data['80'][:500,1]) - min(data['80'][:500,1]))/2
sca2 = (max(data['80 aa.txt'][:500,1]) - min(data['80 aa.txt'][:500,1]))/2

scaling = sca1 / sca2

for key in list(data.keys()):
    if 'aa' in key:
        continue
    if int(key) < 80:
        angles.append(float(key))
        amps.append((max(data[key][:500,1]) - min(data[key][:500,1]))/2)
    if int(key) > 80:
        angles.append(float(key))
        amps.append(scaling*(max(data[key][:500,1]) - min(data[key][:500,1]))/2)
print(angles)
angles = (np.array(angles)-55)*(6.28/360)

# Den teoretiske funktion ser ud på følgende måde.

amps = np.array(amps)/max(amps)*0.91

def T(vink):
    return 10**(-(vink*0.00741*360/6.28))


print(10**(-0.04))
vink = np.linspace(0, 6.28, 100)
ax.plot(vink, T(vink), 'b-', label = "Theoretical")

x_err = np.array([5*3.14/360]*len(amps))
y_err = np.array([0.04]*len(amps))

x_err = np.array([0.5*6.28/360]*len(amps))
ax.errorbar(angles,
            amps,
            xerr = x_err,
            color = 'red',
            fmt = 'o',
            capsize = 2)

def fit(vink, *p):
    a = p[0]
    return 10**(-vink*a)

guess = [0.02]

popt, pcov = scp.curve_fit(fit,
                           angles,
                           amps,
                           guess,
                           sigma = y_err)


def propagation_function(x, f, popt, pcov):
    f_error = 0

# Standard afvigelser gemmes

    err =  list(np.sqrt(np.diagonal(pcov)))
    for i in range(len(err)):

# funktionen med standard afvigelsen på den i'te parameter konstrueres

        j = popt[:i] + [popt[i] + err[i]] + popt[i+1:]
        f_error += (f(x, *j)-f(x, *popt))**2

    return  np.sqrt(f_error)

def plot_propagation(x, f, popt, pcov, ax):
    error = propagation_function(x, f, list(popt), pcov)
    ax.fill_between(x, f(x, *popt) + error,
                    f(x, *popt) - error, alpha = 0.3,
                    color = '#d989a6')
plot_propagation(vink, fit, popt, pcov, ax)

ax.plot(vink, fit(vink, *popt), 'k-', label = "Experimental")
print(popt)
print(np.sqrt(pcov))

ax.set_title('Plot of transmission-coefficient', fontsize = 20)
ax.set_xlabel('$\\theta$', fontsize = 20)
ax.set_ylabel('Transmission', fontsize = 20)
ax.legend()
plt.savefig('transmission.png')
plt.show()
