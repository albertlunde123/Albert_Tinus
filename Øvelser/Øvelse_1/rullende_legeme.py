import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as scp
import scipy.special as ss

exec(open('kalibrering.py').read())
exec(open('data_renser.py').read())

# Vi har nu adgang til funktion func(U, *popt), som er defineret i
# kalibrering.py.

fig, ax = plt.subplots()

# Importer data

sol1 = Data('Messing')
x = func(sol1.points, *popt)
t = 1000*sol1.t

mask = sol1.rinse([[-1, 0.1], [0.4, 0.3], [0.6, 0.4]])

ax.scatter(t[~mask], x[~mask], color = 'blue', label = 'outliers')
ax.scatter(t[mask], x[mask], color = 'red', label = 'data points')



def func(t,*p):
    a = p[0]
    t0 = p[1]
    c = p[2]
    b = p[3]
    return (1/2*a*(t-t0)**2+b*(t)+c)

guess_params = [1,1,1,1]

popt,pcov = scp.curve_fit(func, t[mask], x[mask], guess_params)

t_fit = np.linspace(-0.4,1.0,1000)

ax.plot(t_fit, func(t_fit, *popt), color = 'k', linewidth = 3,
        label = 'fitted function')

ax.set_ylim(-0.2,0.7)
ax.set_ylabel('x/m')
ax.set_xlabel('t/s')
ax.legend()

plt.show()

###############

grader = 15
theta = grader*(2*np.pi/360)

a = [np.sin(theta)*9.82*0.66, popt[0]]
print(a)



# fig.savefig('ruller.png')

