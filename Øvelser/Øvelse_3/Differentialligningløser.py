import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp
from matplotlib import animation, rc
import puk as puk
from scipy.integrate import solve_ivp
rc('animation', html='jshtml')
fig,ax = plt.subplots()
puk2 = puk.Puk(['Elastisk/KastetCenter','Elastisk/KastetSide'],0.0278,0.0807)
puk1 = puk.Puk(['Elastisk/StilleCenter','Elastisk/StilleSide'],0.0278,0.0807)
r02 = [puk2.get_center(1)[0],puk2.get_center(2)[0]]
r01 = [puk1.get_center(1)[0],puk1.get_center(2)[0]]
I = 1/2*0.0278*0.0807**2
R = 0.0807
m = 0.0278
def findv0(puk):
    xs = puk.get_center(1)[:5]
    ys = puk.get_center(2)[:5]
    ts = puk.get_center(0)[:5]
    angs = puk.angle()[:5]
    f = lambda x,a,b : a*x+b
    popt1, cov1 = scp.curve_fit(f,ts,xs, absolute_sigma= True)
    popt2, cov2 = scp.curve_fit(f,ts,ys, absolute_sigma= True)
    popt3, cov3 = scp.curve_fit(f,ts,angs, absolute_sigma= True)
    return [popt1[0],popt2[0],popt3[0]]
v01 = findv0(puk1)
v02 = findv0(puk2)
t_end = 2
steps = 100 * t_end
svinkel1= puk1.angle()[0]
svinkel2= puk1.angle()[0]
a = 0.8
b = 0.2

y0 = np.concatenate((r01,r02,v01[:2],v02[:2],[svinkel1],[svinkel2],[v01[2]],[v02[2]]))

def dydt(t,y):
    r1 = y[:2]
    r2 = y[2:4]
    v1 = y[4:6]
    v2 = y[6:8]
    th1 = y[8:9]
    th2 = y[9:10]
    w1 = y[10:11]
    w2 = y[11]
    dr1xdt = v1[0]
    dr1ydt = v1[1]
    dr2xdt = v2[0]
    dr2ydt = v2[1]    
    Fp = np.array([0,0])
    Fv = np.array([0,0])
    r21 = r2-r1
    if(np.linalg.norm(r21)<= 2*R):
        enhed21 = (r21)/np.linalg.norm(r21)
        Fp = -a*enhed21
        Fv = b*[-enhed21[1],enhed21[0]]
    F1 = Fp + Fv
    print(F1)
    F2 = -1*F1
    dv1xdt = F1[0]/m
    dv1ydt = F1[1]/m
    dv2xdt = F2[0]/m
    dv2ydt = F2[1]/m
    dth1dt = w1
    dth2dt = w2
    dw1dt = R*Fp/I
    dw2dt = R*(-Fp)/I
    result = [dr1xdt,dr1ydt,dr2xdt,dr2ydt,dv1xdt,dv1ydt,dv2xdt,dv2ydt,dth1dt,dth2dt,dw1dt,dw2dt]
    print(result)
    return result
    
times = np.linspace(0,t_end,steps)
mysol = solve_ivp(dydt,[0,t_end],y0,max_step=1e-3, t_eval = times)
    
    
    
