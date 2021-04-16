import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp

fig, ax = plt.subplots(2, 2, figsize = (20,12))
ax = ax.ravel()

class Puk():

    # Initialze puk-objekt. Dette objekt tager en liste med 2 stier, hvor disse
    # stier til datasæt for henholdsvis "edge" og "center". Objektet skal
    # desuden have pukkens radius R og masse m. Inertimomentet og antallet af
    # datapunkter beregnes.

    def __init__(self, path, m, R):
        self.path = path
        self.center = np.loadtxt(path[0])
        self.edge = np.loadtxt(path[1])
        self.m = m
        self.R = R
        self.I = 1/2*self.m*self.R**2
        self.len = len(self.center[:, 0])

    def get_center(self, t):
        return self.center[:, t]

    def get_edge(self, t):
        return self.edge[:, t]

    # Denne funktion bestemmer usikkerheden på henholdsvis t,x og y. Hvor denne
    # usikkerhed er antaget til at være den 0.5*10**-n, hvor n er antallet af
    # decimaler.

    # def error(self):
    #     t_err =
    #     x_err =
    #     y_err =

    # Bestemmer pukkens vinkel med origo

    def angle(self):
        angles = []
        edge_x = self.get_center(1) - self.get_edge(1)
        edge_y = self.get_center(2) - self.get_edge(2)
        for i in range(len(edge_x)):
                       a = np.arctan2(edge_y[i], edge_x[i])
                       if a < 0:
                            a += 2*np.pi
                       angles.append(a)
        return angles

    # Bestemmer pukkens afstand fra origo

    def dist(self):
        return np.sqrt(self.get_center(1)**2 + self.get_center(2)**2)

    # Man kan evt. forsøge på at samle de næste 3-funktioner i én enkelt.
    # Indtil videre fungerer det her nu fint nok.

    # Plotter pukkens x,y koordinater

    def plot_Puk_xy(self, ax, color):
        ax.plot(self.get_center(1), self.get_center(2), color[0], label = 'CM')
        ax.plot(self.get_edge(1), self.get_edge(2), color[1], label = 'Edge')

    # Plotter pukkens afstand fra origo som funktion af tiden.

    def plot_Puk_dist(self, ax, color):
        ax.plot(self.get_center(0), self.dist(), color, label = 'Puk distance')
        ax.set_title(self.path[0], fontsize = 20)
        ax.set_xlabel('T / s', fontsize = 20)
        ax.set_ylabel('Dist / m', fontsize = 20)

    # Plotter pukkens vinkel med origo som funktion af tiden.

    def plot_Puk_angle(self, ax, color):
        ax.plot(self.get_center(0), self.angle(), color, label = 'Puk angle')
        ax.set_title(self.path[0], fontsize = 20)
        ax.set_xlabel('T / s', fontsize = 20)
        ax.set_ylabel('Angle / $\theta$', fontsize = 20)

    # Indexet for kollisionstiden beregnes.

    # Skal evt. ændres. Magnitude af hældning er et dårligere mål end retning.
    # Det her er nok den mest sårbare del af koden. Vil gerne snakke med dig om
    # en smartere måde at håndtere problemet på.

    def col_t(self):
        xs = self.get_center(1)
        a = xs[1] - xs[2]
        i = 3
        while a - 2 < xs[i] - xs[i+1] < a + 2:
            i += 1
        return i

    #def col_t1(self):

    # Der skal implementeres usikkerhed på self.dist(). Jeg har gjort mig
    # nogle overvejelser omkring dette, men gider ikke at gøre det nu.

    # Bestemmer hastighed før og efter kollision.


    def x_velocity(self):

        def func(t, *p):
            a = p[0]
            b = p[1]
            return a*t + b

        guess = [0, 0]
        resses = []
        popt, pcov = scp.curve_fit(func,
                                    self.get_center(0)[:self.col_t()],
                                    self.get_center(1)[:self.col_t()],
                                    guess,
                                    absolute_sigma = True)

        popt1, pcov1 = scp.curve_fit(func,
                                    self.get_center(0)[self.col_t()+1:],
                                    self.get_center(1)[self.col_t()+1:],
                                    guess,
                                    absolute_sigma = True)

        return np.array([popt[0]]*self.col_t() + [popt1[0]]*(len(self.get_center(0))-self.col_t()))

    def y_velocity(self):

        def func(t, *p):
            a = p[0]
            b = p[1]
            return a*t + b

        guess = [0, 0]
        resses = []
        popt, pcov = scp.curve_fit(func,
                                    self.get_center(0)[:self.col_t()],
                                    self.get_center(2)[:self.col_t()],
                                    guess,
                                    absolute_sigma = True)

        popt1, pcov1 = scp.curve_fit(func,
                                    self.get_center(0)[self.col_t()+1:],
                                    self.get_center(2)[self.col_t()+1:],
                                    guess,
                                    absolute_sigma = True)

        return np.array([popt[0]]*self.col_t() + [popt1[0]]*(len(self.get_center(0))-self.col_t()))

    def dist_fitter(self):

        def func(t, *p):
            a = p[0]
            b = p[1]
            return a*t + b

        guess = [0, 0]
        resses = []
        popt, pcov = scp.curve_fit(func,
                                    self.get_center(0)[:self.col_t()],
                                    self.dist()[:self.col_t()],
                                    guess,
                                    absolute_sigma = True)
        resses.append([popt, np.sqrt(np.diag(pcov))])

        popt1, pcov1 = scp.curve_fit(func,
                                    self.get_center(0)[self.col_t()+1:],
                                    self.dist()[self.col_t()+1:],
                                    guess,
                                    absolute_sigma = True)

        resses.append([popt1, np.sqrt(np.diag(pcov1))])
        return resses

    # Der skal implementeres usikkerhed på self.angle(). Jeg har gjort mig
    # nogle overvejelser omkring dette, men gider ikke at gøre det nu.

    # Bestemmer vinkelhastighed før og efter kollision.

    def angle_fitter(self):

        def func(t, *p):
            a = p[0]
            b = p[1]
            return a*t + b

        guess = [0, 0]
        resses = []
        popt, pcov = scp.curve_fit(func,
                                    self.get_center(0)[:self.col_t()],
                                    self.angle()[:self.col_t()],
                                    guess,
                                    absolute_sigma = True)
        resses.append([popt, np.sqrt(np.diag(pcov))])

        popt1, pcov1 = scp.curve_fit(func,
                                    self.get_center(0)[self.col_t()+1:],
                                    self.angle()[self.col_t()+1:],
                                    guess,
                                    absolute_sigma = True)

        resses.append([popt1, np.sqrt(np.diag(pcov1))])
        return resses

    # Plotter enten fit af hastighed eller vinkelhastighed.

    def plot_fit(self, ax, f, color):

        def func(t, *p):
            a = p[0]
            b = p[1]
            return a*t + b

        ts = self.get_center(0)
        t_col = self.get_center(0)[self.col_t()]
        t_col2 = self.get_center(0)[self.col_t()+1]

        ts_1 = np.linspace(ts[0], t_col, 100)
        ts_2 = np.linspace(t_col2, ts[-1],100)

        popt1 = f[0][0]
        popt2 = f[1][0]

        ax.plot(ts_1, func(ts_1, *popt1), color)
        ax.plot(ts_2, func(ts_2, *popt2), color)

    # Giver en liste bestående af hastigheder og vinkelhastigheder.

    def velocities(self):
            return [np.array([self.dist_fitter()[0][0][0]] * self.col_t() +
                   [self.dist_fitter()[1][0][0]] * (self.len - self.col_t())),
                   np.array([self.angle_fitter()[0][0][0]] * self.col_t() +
                   [self.angle_fitter()[1][0][0]] * (self.len - self.col_t()))]

    # Giver pukkens kinetiske energi.

    def kinetic_energy(self):
        return 1/2*self.m*self.velocities()[0]**2

    # Giver pukkens rotationelle energi.

    def rotational_energy(self):
        return 1/2*self.I*self.velocities()[1]**2

    # Giver den totale mekaniske energi.

    def energy(self):
        return self.kinetic_energy() + self.rotational_energy()

    # Giver impulsmomentet.
    # Beregner størrelsen ||r x p + Iw.||





    def angular_momentum(self):

        r = np.array([[self.get_center(1)[i], self.get_center(2)[i], 0] for i in range(len(self.get_center(1)))])

        p = np.array([[self.x_velocity()[i], self.y_velocity()[i],
                      0] for i in range(len(self.get_center(1)))])

        rxp = np.cross(r, p)
        print(rxp)

        Iw = np.array([[0, 0, self.I*self.velocities()[1][i]] for i in range(len(self.velocities()[1]))])

        return np.array([rxp[i][2] + Iw[i][2] for i in range(len(rxp))])
        # return np.array([np.linalg.norm(rxp[i] + Iw[i]) for i in range(len(Iw))])








def plot_Puks_xy(Puks, ax, colors):
    for i in range(len(Puks)):
        Puks[i].plot_Puk_xy(ax, colors[i])
    ax.set_xlabel('x', fontsize = 20)
    ax.set_ylabel('y', fontsize = 20)
    ax.set_title('Puk bevægelse over tid', fontsize = 20)
    ax.legend()

def plot_Puks_energy(Puks, ax, colors, alpha = 1):
    ax.plot(Puks[0].get_center(0), Puks[0].energy(), colors[0], alpha = alpha, label = 'Puk 1')
    ax.plot(Puks[0].get_center(0), Puks[1].energy(), colors[1], alpha = alpha, label = 'Puk 2')
    ax.plot(Puks[0].get_center(0), Puks[0].energy()+ Puks[1].energy(), colors[2], alpha = alpha, label = 'Samlet')
    ax.set_xlabel('t / s', fontsize = 20)
    ax.set_ylabel('E / J', fontsize = 20)
    ax.set_title('Energi over tid.', fontsize = 20)
    ax.legend()

def plot_Puks_angular_momentum(Puks, ax, colors, alpha = 1):
    ax.plot(Puks[0].get_center(0), Puks[0].angular_momentum(), colors[0], alpha = alpha, label = 'Puk 1')
    ax.plot(Puks[0].get_center(0), Puks[1].angular_momentum(), colors[1], alpha = alpha, label = 'Puk 2')
    ax.plot(Puks[0].get_center(0), Puks[0].angular_momentum()+ Puks[1].angular_momentum(),
            colors[2], alpha = alpha, label = 'Samlet')
    ax.set_xlabel('t / s', fontsize = 20)
    ax.set_ylabel('L / $kg\cdot m^2 / s$', fontsize = 20)
    ax.set_title('Impulsmoment over tid.', fontsize = 20)
    ax.legend()

Rota_Kastet = Puk(['Elastisk/KastetCenter','Elastisk/KastetSide'], 1, 1)
Rota_Stille = Puk(['Elastisk/StilleCenter','Elastisk/StilleSide'], 1, 1)
Puks = [Rota_Kastet, Rota_Stille]

colors1 = ['r--', 'b--', 'g-']
colors2 = [['ro', 'r*'], ['bo', 'b*']]

plot_Puks_energy(Puks, ax[0], colors1, alpha = 0.5)
plot_Puks_angular_momentum(Puks, ax[1], colors1, alpha = 0.5)
plot_Puks_xy(Puks, ax[2], colors2)
Puks[0].plot_Puk_dist(ax[3], 'ro')
Puks[0].plot_fit(ax[3], Puks[0].dist_fitter(), 'k-')


print(Rota_Stille.velocities()[1])
print(Rota_Kastet.velocities()[1])
plt.tight_layout()
plt.show()
