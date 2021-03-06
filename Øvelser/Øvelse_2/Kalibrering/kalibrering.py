import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as scp

# fig, ax = plt.subplots()

U = []
for i in [320, 330, 340, 350, 0, 10, 20, 30, 40]:
    U = U +  [np.mean(np.loadtxt('Kalibrering/' + str(i) + 'kaligrader.txt', skiprows = 3)[:, 1])]

degrees =  np.array([-40, -30, -20, -10, 0, 10, 20, 30, 40])*(2*np.pi/360)

def func(theta, *p):
    a=p[0]
    b=p[1]
    c=p[2]
    d=p[3]
    return a/(1+b*np.exp(-c*theta))-d

guess_params = [1, 1, 1, 1]
kali, pcov = scp.curve_fit(func, degrees, U, guess_params)

# spænding = np.loadtxt("20vinkel.txt", skiprows = 3)[:,1]

# ts = np.linspace(0,1, 100)

# ax.plot(ts, func(ts, *kali))
# ax.set_xlabel('')
# ax.set_ylabel('')
# ax.legend()
# plt.show()

def vinkel(V, *p):
    a=p[0]
    b=p[1]
    c=p[2]
    d=p[3]
    return (-1/c)*np.log(1/b*(a/(V+d)-1))

# print(vinkel(spænding, *kali)*360/(2*np.pi))



