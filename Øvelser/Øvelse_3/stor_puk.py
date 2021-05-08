import scipy.stats as ss
import scipy.optimize as scp
import fejlpropagering as fejl
import puk as puk
import numpy as np
import matplotlib.pyplot as plt
import Uelastiskstød as uel
import lille_puk as lille_puk

fig, ax = plt.subplots(figsize = (16,8))

class stor_Puk():
    def __init__(self, x):
        self.m = x[0]
        self.center = [x[2], x[3], x[4]]
        self.I = x[1]
        self.len = len(x[2])
        self.edge = x[6]

    def get_center(self, t):
        return self.center[t]

    def gc_err(self, t):
        err = []
        for i in self.center[t]:
            err.append(np.sqrt(2)*0.85*10**-2)
        return np.array(err)

    def get_edge(self, t):
        return self.edge[t]

    def get_r(self):
        return self.R

    def get_m(self):
        return self.m

    def ge_err(self, t):
        err = []
        for i in self.edge[t]:
            err.append(np.sqrt(2)*0.85*10**-2)
        return np.array(err)

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
                       # if a < 0:
                       #      a += 2*np.pi
                       angles.append(a)
        return angles

    def angle_err(self):

        edge_x = self.get_center(1) - self.get_edge(1)
        edge_y = self.get_center(2) - self.get_edge(2)

        def f(x,y):
            return np.arctan2(y, x)

        return fejl.propagation_function_2(f,
                                          fejl.collector([edge_x, edge_y]),
                                          fejl.collector([self.ge_err(1), self.ge_err(2)]))


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

    def x_velocity(self):

        def func(t, *p):
            a = p[0]
            b = p[1]
            return a*t + b

        guess = [0, 0]
        resses = []
        popt, pcov = scp.curve_fit(func,
                                    self.get_center(0),
                                    self.get_center(1),
                                    guess,
                                    sigma = self.gc_err(1),
                                    absolute_sigma = True)

        pcov = np.sqrt(np.diag(pcov))

        return [np.array([popt[0]]*self.len),
                         np.array([pcov[0]]*self.len)]

    def y_velocity(self):

        def func(t, *p):
            a = p[0]
            b = p[1]
            return a*t + b

        guess = [0, 0]
        resses = []
        popt, pcov = scp.curve_fit(func,
                                    self.get_center(0),
                                    self.get_center(2),
                                    guess,
                                    sigma = self.gc_err(2),
                                    absolute_sigma = True)

        pcov = np.sqrt(np.diag(pcov))

        return [np.array([popt[0]]*self.len),
                         np.array([pcov[0]]*self.len)]

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
        popt, pcov = scp.curve_fit(func,
                                    self.get_center(0),
                                    self.angle(),
                                    guess,
                                    sigma = self.angle_err(),
                                    absolute_sigma = True)

        return [popt[0], np.sqrt(np.diag(pcov))[0]]


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
           return  [np.array(np.sqrt(self.x_velocity()[0]**2 + self.y_velocity()[0]**2)),
                   np.array([self.angle_fitter()[0]] * self.len)]

    def vel_err(self):

        x_vel = self.x_velocity()
        y_vel = self.y_velocity()
        x = x_vel[0]
        y = y_vel[0]
        x_err = x_vel[1]
        y_err = y_vel[1]

        def f(x,y):
            return np.sqrt(x**2 + y**2)

        return np.array(fejl.propagation_function_2(f, fejl.collector([x,y]), fejl.collector([x_err, y_err])))

    # Giver pukkens kinetiske energi.

    def kinetic_energy(self):
        return 1/2*self.m*self.velocities()[0]**2

    def kin_err(self):
        vel = self.velocities()[0]
        vel_err = self.vel_err()
        m = self.m

        return np.sqrt(m**2*vel**2*vel_err**2)


    # Giver pukkens rotationelle energi.

    def rotational_energy(self):
        return 1/2*self.I*self.velocities()[1]**2

    def rot_err(self):
        rot = self.velocities()[1]
        angle_err = np.array([self.angle_fitter()[0][1][0]] * self.col_t() +
                   [self.angle_fitter()[1][1][0]] * (self.len - self.col_t()))
        m = self.I

        return np.sqrt(m**2*rot**2*angle_err**2)


    # Giver den totale mekaniske energi.

    def energy(self):
        return self.kinetic_energy() + self.rotational_energy()

    def energy_err(self):
        kin = self.kinetic_energy()
        rot = self.rotational_energy()
        kin_err = self.kin_err()
        rot_err = self.rot_err()

        def f(x,y):
           return x + y

        return fejl.propagation_function_2(f, fejl.collector([kin, rot]),
                                           fejl.collector([kin_err, rot_err]))

    # Giver impulsmomentet.
    # Beregner størrelsen ||r x p + Iw.||

    def angular_momentum(self):

        a = self.x_velocity()[0]
        b = self.y_velocity()[0]
        w = self.velocities()[1]

        r = np.array([[self.get_center(1)[i], self.get_center(2)[i], 0] for i in range(len(self.get_center(1)))])

        p = np.array([[a[i], b[i], 0] for i in range(len(self.get_center(1)))])*self.m

        rxp = np.cross(r, p)

        Iw = np.array([[0, 0, self.I*w[i]] for i in range(len(a))])
        return np.array([rxp[i][2] + Iw[i][2] for i in range(len(rxp))])

    def angu_err(self):

            a = self.x_velocity()[0]
            b = self.y_velocity()[0]
            w = self.velocities()[1]
            I = self.I
            m = self.m
            x = self.get_center(1)
            y = self.get_center(2)

            a_err =  self.x_velocity()[1] #np.zeros(self.len)
            b_err = self.y_velocity()[1] #  np.zeros(self.len)
            w_err = np.array([self.angle_fitter()[1]]*self.len)

            x_err = self.gc_err(1)
            y_err = self.gc_err(2)

            def f(x, y, a, b, w):
                return np.cross(np.array([x, y, 0]), np.array([a, b, 0]))[2]*m + I*w

            return np.array(fejl.propagation_function_2(f, fejl.collector([x,y,a,b,w]),
                                            fejl.collector([x_err, y_err, a_err, b_err, w_err])))

puk1 = puk.Puk(['Uelastisk/KastetCenter','Uelastisk/KastetSide'],0.0569,0.0435)
puk2 = puk.Puk(['Uelastisk/StilleCenter','Uelastisk/StilleSide'],0.0285,0.0432)

t = uel.findColUelastisk(puk1, puk2)
t1 = [0,t]
t2 = [t, puk1.len]

Puk1 = lille_puk.lille_Puk(['Uelastisk/KastetCenter','Uelastisk/KastetSide'],0.0285,0.0435, t1)
Puk2 = lille_puk.lille_Puk(['Uelastisk/StilleCenter','Uelastisk/StilleSide'],0.0569,0.0432, t1)
Puks = [Puk1, Puk2]

colors1 = ['r--', 'b--', 'g-', 'k-']
colors2 = [['ro', 'r*'], ['bo', 'b*']]

a = Puks[0].angular_momentum()
b = Puks[1].angular_momentum()
a_err = Puks[0].angu_err()
b_err = Puks[1].angu_err()

ax.errorbar(Puks[0].get_center(0), a, yerr = a_err, color = 'r', fmt = 'o-', label = 'Puk 1')
ax.errorbar(Puks[0].get_center(0), a + b, yerr = np.sqrt(a_err**2 + b_err**2), color = 'b', fmt = 'o-', label = 'Total Impulsmoment')
ax.errorbar(Puks[1].get_center(0), b, yerr = b_err, color = 'g', fmt = 'o-', label = 'Puk 2' )

stor_puk = stor_Puk(uel.newObject(puk1, puk2))
# ax.plot(puk1.get_center(1), puk1.get_center(2), 'ro')
# ax.plot(puk2.get_center(1), puk2.get_center(2), 'bo')
# ax.plot(stor_puk.get_center(1), stor_puk.get_center(2), 'ko')


ax.errorbar(stor_puk.center[0], stor_puk.angular_momentum(), yerr = stor_puk.angu_err(), color ='k', fmt = 'o-', label = 'Klistret Puk')
print(stor_puk.rotational_energy())
ax.set_xlabel('t/s', fontsize = 20)
ax.set_ylabel('L', fontsize = 20)
ax.set_title('Impulsmoment over tid', fontsize = 20)
ax.legend()
plt.show()

fig.savefig('uelastisk_impuls')
