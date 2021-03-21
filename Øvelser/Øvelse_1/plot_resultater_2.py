import numpy as np
import matplotlib.pyplot as plt

def a(grader):
    return np.sin(grader*2*np.pi/360)*9.82*0.66

def t(grader, R1, R2):
    return (np.sin(grader*2*np.pi/360)*9.82)/(1.0+1/2*((R1**2 + R2**2)/R2**2))

R2 = [7.9/2,3/2,2.7/2]
R1 = [(7.9-2*0.45)/2,(3-2*0.3)/2,(2.7-2*0.1)/2]


def plot_res(vink, eksp, save_name, f):

    fig, ax = plt.subplots()

    v_u = [[f(v-0.5), f(v), f(v+0.5)] for v in vink]
    ys = list(np.linspace(0, 5, 5))

    ax.plot(v_u[0], [ys[0]]*3, 'r-' , linewidth = 2, label = "usikkerhed")
    ax.plot(v_u[0][1], [ys[0]], 'ko', ms = 10, label = 'forudset a')
    ax.plot(eksp[0], ys[0], 'b*', ms = 10, label = 'eksperimental a')

    for v,y,e in zip(v_u[1:], ys[1:], eksp[1:]):
        ax.plot(v, [y]*3, 'r-' , linewidth = 2)
        ax.plot(v[1], y, 'ko', ms = 10)
        ax.plot(e, y, 'b*', ms = 10)

    ax.set_ylim(-1,8)
    ax.set_xlim(1.5,1.85)

    ax.set_xlabel('acceleration', fontsize = 14)
    ax.set_ylabel('forsøg', fontsize = 14)
    ax.set_title('Resultater', fontsize = 20)
    ax.legend()
    plt.show()

    fig.savefig(save_name)

def plot_res2(vink, R1, R2, eksp, save_name, f):

    fig, ax = plt.subplots()

    v_u = [[f(v-0.5, R1, R2), f(v, R1, R2), f(v+0.5, R1, R2)]
           for v,R1,R2 in zip(vink, R1, R2)]
    print(v_u)
    ys = list(np.linspace(0, 5, 5))

    ax.plot(v_u[0], [ys[0]]*3, 'r-' , linewidth = 2, label = "usikkerhed")
    ax.plot(v_u[0][1], [ys[0]], 'ko', ms = 10, label = 'forudset a')
    ax.plot(eksp[0], ys[0], 'b*', ms = 10, label = 'eksperimental a')

    for v,y,e in zip(v_u[1:], ys[1:], eksp[1:]):
        ax.plot(v, [y]*3, 'r-' , linewidth = 2)
        ax.plot(v[1], y, 'ko', ms = 10)
        ax.plot(e, y, 'b*', ms = 10)

    ax.set_ylim(-1,6)
    ax.set_xlim(1.20,1.45)

    ax.set_xlabel('acceleration', fontsize = 14)
    ax.set_ylabel('forsøg', fontsize = 14)
    ax.set_title('Resultater', fontsize = 20)
    ax.legend()
    plt.show()

    fig.savefig(save_name)


# plot_res([15]*5, [1.662, 1.611, 1.624, 1.607, 1.636], "rulle_legeme", a)
plot_res2([15]*3, R1, R2, [1.31, 1.36, 1.24], "rulle_hul", t)



