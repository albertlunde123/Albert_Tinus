import numpy as np
import puk as puk
import matplotlib.pyplot as plt
import scipy.optimize as scp
fig,ax = plt.subplots()
puk1 = puk.Puk(['Elastisk/StilleCenter','Elastisk/StilleSide'],0.0278,0.0807)
puk2 = puk.Puk(['Elastisk/KastetCenter','Elastisk/KastetSide'],0.0278,0.0807)
puk3 = puk.Puk(['Rota/KastetCenter','Rota/KastetSide'],0.0278,0.0807)
puk4 = puk.Puk(['Rota/StilleCenter','Rota/StilleSide'],0.0278,0.0807)
def linear(t,a,b):
    return a*t+b
def findcol(Puk):
    xs = Puk.center[:,1]
    ts = Puk.center[:,0]
    ax.scatter(ts,xs)
    curve1 = [ts[:8], xs[:8]]
    inte = len(xs)-8
    curve2 = [ts[inte:], xs[inte:]]
    popt1,cov1 = scp.curve_fit(linear, curve1[0], curve1[1], absolute_sigma = True)
    popt2,cov2 = scp.curve_fit(linear, curve2[0], curve2[1], absolute_sigma = True)
    tfake = np.linspace(0,1.5,100)
    ax.plot(tfake, linear(tfake,popt1[0],popt1[1]))
    ax.plot(tfake, linear(tfake,popt2[0],popt2[1]))
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
        dx = abs(Puk.center[tup[1],1]-(Puk.center[tup[1]+1,1]))
        dy = abs(Puk.center[tup[1],2]-(Puk.center[tup[1]+1,2]))
        change = dx + dy
        if(change > maxc):
            maxc = change
            bestt = tup[0]
    print(bestt)


#findcol(puk1)
