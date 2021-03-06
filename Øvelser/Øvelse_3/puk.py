import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp
import fejlpropagering as fejl

# fig, ax = plt.subplots(2, 2, figsize = (20,12))
# ax = ax.ravel()

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

    def gc_err(self, t):
        err = []
        for i in self.center[:, t]:
            err.append(0.85*10**-2)
            # err.append(5*10**(-len(str(i).split('.')[-1])))
        return np.array(err)

    def get_edge(self, t):
        return self.edge[:, t]

    def get_r(self):
        return self.R

    def get_m(self):
        return self.m

    def ge_err(self, t):
        err = []
        for i in self.edge[:, t]:
            err.append(0.85*10**-2)
            # err.append(5*10**(-len(str(i).split('.')[-1])))
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
                       if a < 0:
                            a += 2*np.pi
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

    def col_t(self):
        xs = self.get_center(1)
        a = xs[1] - xs[2]
        i = 3
        while a - 2 < xs[i] - xs[i+1] < a + 2:
            i += 1
        return i


    def col_t(self):

        def linear(t,a,b):
            return a*t+b

        xs = self.get_center(1)
        ts = self.get_center(0)

        curve1 = [ts[:8], xs[:8]]
        inte = len(xs)-8
        curve2 = [ts[inte:], xs[inte:]]

        popt1,cov1 = scp.curve_fit(linear, curve1[0], curve1[1], absolute_sigma = True)
        popt2,cov2 = scp.curve_fit(linear, curve2[0], curve2[1], absolute_sigma = True)

        # find intersection
        f = lambda x: popt1[0]*x+popt1[1]-(popt2[0]*x+popt2[1])

        tpoint = scp.fsolve(f,0)
        tlist = []
        i = 9
        for t in ts[8:-8]:
            if(abs(tpoint-t) <= 0.1 ):
                tlist.append((t,i))
                i +=1
            else:
                i+= 1
        maxc = 0
        bestt = 0
        for tup in tlist:
            dx = abs(self.get_center(1)[tup[1]]-self.get_center(1)[tup[1]+1])
            dy = abs(self.get_center(2)[tup[1]]-self.get_center(2)[tup[1]+1])
            change = dx + dy
            if(change > maxc):
                maxc = change
                bestt = tup
        return bestt[1]
    #def col_t1(self):

    # Der skal implementeres usikkerhed på self.dist(). Jeg har gjort mig
    # nogle overvejelser omkring dette, men gider ikke at gøre det nu.

    # Bestemmer hastighed før og efter kollision.


    def x_velocity(self):

        def func(t, *p):
            a = p[0]
            b = p[1]
            return a*t + b

#Man går muligvis glip af et punkt her
        guess = [0, 0]
        resses = []
        popt, pcov = scp.curve_fit(func,
                                    self.get_center(0)[:self.col_t()],
                                    self.get_center(1)[:self.col_t()],
                                    guess,
                                    sigma = self.gc_err(1)[:self.col_t()],
                                    absolute_sigma = True)

        popt1, pcov1 = scp.curve_fit(func,
                                    self.get_center(0)[self.col_t()+1:],
                                    self.get_center(1)[self.col_t()+1:],
                                    guess,
                                    sigma = self.gc_err(1)[self.col_t()+1:],
                                    absolute_sigma = True)

        pcov = np.sqrt(np.diag(pcov))
        pcov1 = np.sqrt(np.diag(pcov1))

        return [np.array([popt[0]]*self.col_t() + [popt1[0]]*(len(self.get_center(0))-self.col_t())),
                         np.array([pcov[0]]*self.col_t() + [pcov1[0]]*(len(self.get_center(0))-self.col_t()))]

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
                                    sigma = self.gc_err(2)[:self.col_t()],
                                    absolute_sigma = True)

        popt1, pcov1 = scp.curve_fit(func,
                                    self.get_center(0)[self.col_t()+1:],
                                    self.get_center(2)[self.col_t()+1:],
                                    guess,
                                    sigma = self.gc_err(2)[self.col_t()+1:],
                                    absolute_sigma = True)

        pcov = np.sqrt(np.diag(pcov))
        pcov1 = np.sqrt(np.diag(pcov1))

        return [np.array([popt[0]]*self.col_t() + [popt1[0]]*(len(self.get_center(0))-self.col_t())),
                         np.array([pcov[0]]*self.col_t() + [pcov1[0]]*(len(self.get_center(0))-self.col_t()))]

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
                                    sigma = self.angle_err()[:self.col_t()],
                                    absolute_sigma = True)
        resses.append([popt, np.sqrt(np.diag(pcov))])

        popt1, pcov1 = scp.curve_fit(func,
                                    self.get_center(0)[self.col_t()+1:],
                                    self.angle()[self.col_t()+1:],
                                    guess,
                                    sigma = self.angle_err()[self.col_t()+1:],
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
           return  [np.array(np.sqrt(self.x_velocity()[0]**2 + self.y_velocity()[0]**2)),
                   np.array([self.angle_fitter()[0][0][0]] * self.col_t() +
                   [self.angle_fitter()[1][0][0]] * (self.len - self.col_t()))]

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

        return np.array(fejl.propagation_function_2(f, fejl.collector([kin, rot]),
                                           fejl.collector([kin_err, rot_err])))

    # Giver impulsmomentet.
    # Beregner størrelsen ||r x p + Iw.||

    def angular_momentum(self):

        a = self.x_velocity()[0]
        b = self.y_velocity()[0]
        w = self.velocities()[1]

        r = np.array([[self.get_center(1)[i], self.get_center(2)[i], 0] for i in range(len(self.get_center(1)))])

        p = np.array([[a[i], b[i], 0] for i in range(len(self.get_center(1)))])*self.m

        rxp = np.cross(r, p)

        Iw = np.array([[0, 0, self.I*w[i]**2] for i in range(len(a))])
        return np.array([rxp[i][2] + Iw[i][2] for i in range(len(rxp))])

    def angu_err(self):

        a = self.x_velocity()[0]
        b = self.y_velocity()[0]
        w = self.velocities()[1]
        I = self.I
        m = self.m
        x = self.get_center(1)
        y = self.get_center(2)

        a_err = self.x_velocity()[1]
        b_err = self.y_velocity()[1]
        w_err = np.array([self.angle_fitter()[0][1][0]] * self.col_t() +
                   [self.angle_fitter()[1][1][0]] * (self.len - self.col_t()))

        x_err = self.gc_err(1)
        y_err = self.gc_err(2)

        def f(x, y, a, b, w):
            return np.cross(np.array([x, y, 0]), np.array([a, b, 0]))[2]*self.m + I*w

        return np.array(fejl.propagation_function_2(f, fejl.collector([x,y,a,b,w]),
                                           fejl.collector([x_err, y_err, a_err, b_err, w_err])))

def plot_Puks_xy(Puks, ax, colors):
    for i in range(len(Puks)):
        Puks[i].plot_Puk_xy(ax, colors[i])
    ax.set_xlabel('x', fontsize = 20)
    ax.set_ylabel('y', fontsize = 20)
    ax.set_title('Puk bevægelse over tid', fontsize = 20)
    ax.legend()

def plot_Puks_energy(Puks, ax, colors, alpha = 1):

    a = Puks[0].energy()
    b = Puks[1].energy()
    a_err = Puks[0].energy_err()
    b_err = Puks[1].energy_err()
    tot_err = np.sqrt(a_err**2 + b_err**2)

    ax.errorbar(Puks[0].get_center(0), a, yerr = a_err, fmt = 'o-',
            color = colors[0], alpha = alpha, label = 'Puk 1')

    ax.errorbar(Puks[0].get_center(0), b, yerr = b_err, fmt = 'o-',
            color = colors[1],alpha = alpha, label = 'Puk 2')

    ax.errorbar(Puks[0].get_center(0), a+b, yerr = tot_err, fmt = 'o-',
            color = colors[2], alpha = alpha, label = 'Samlet')

    ax.set_xlabel('t / s', fontsize = 20)
    ax.set_ylabel('E / J', fontsize = 20)
    ax.set_title('Energi over tid.', fontsize = 20)
    ax.legend()

def plot_Puks_angular_momentum(Puks, ax, colors, alpha = 1):
    a = Puks[0].angular_momentum()
    a_err = Puks[0].angu_err()
    b = Puks[1].angular_momentum()
    b_err = Puks[1].angu_err()
    tot_err = np.sqrt(a_err**2 + b_err**2)

    ax.errorbar(Puks[0].get_center(0), a, yerr = a_err,
                color = colors[0], fmt = 'o-', capsize = 2,
                alpha = alpha, label = 'Puk 1')

    ax.errorbar(Puks[0].get_center(0), b, yerr = b_err,
                color = colors[1], fmt = 'o-', capsize = 2,
                alpha = alpha, label = 'Puk 2')

    ax.errorbar(Puks[0].get_center(0), a + b, yerr = tot_err,
            color = colors[2], fmt = 'o-', capsize = 2,
                alpha = alpha, label = 'Samlet')

    def f(t, *p):
        a = p[0]
        return a + t*0

    guess = [a[0]+b[0]]
    t = Puks[0].get_center(0)

    popt, pcov = scp.curve_fit(f, t, a+b, guess,
                   sigma = tot_err,
                   absolute_sigma = True)

    ts = np.linspace(t[0], t[-1], 100)

    ax.plot(ts, f(ts, *popt), colors[3], alpha = 1, label = 'constant fit')
    fejl.plot_propagation(ts, f, popt, pcov, ax)

    ax.set_xlabel('t / s', fontsize = 20)
    ax.set_ylabel('L / $kg\cdot m^2 / s$', fontsize = 20)
    ax.set_title('Impulsmoment over tid.', fontsize = 20)
    ax.legend()

    return popt

Rota_Kastet = Puk(['Rota/KastetCenter','Rota/KastetSide'], 0.0278, 0.0807)
Rota_Stille = Puk(['Rota/StilleCenter','Rota/StilleSide'], 0.0278, 0.0807)
Puks = [Rota_Kastet, Rota_Stille]


