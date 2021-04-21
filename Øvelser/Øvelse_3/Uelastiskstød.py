import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import scipy.optimize as scp
import puk as puk
fig,ax = plt.subplots()

puk1 = puk.Puk(['Uelastisk/KastetCenter','Uelastisk/KastetSide'],0.0569,0.0435)
puk2 = puk.Puk(['Uelastisk/StilleCenter','Uelastisk/StilleSide'],0.0285,0.0432)
 
def findColUelastisk(puk1,puk2):
    ts = puk1.get_center(0)
    xs1 = puk1.get_center(1)
    ys1 = puk1.get_center(2)
    xs2 = puk2.get_center(1)
    ys2 = puk2.get_center(2)
    t_point = 0
    i = 0
    for t in ts:
        r1 = np.array(xs1[i],ys1[i])
        r2 = np.array(xs2[i],ys2[i])
        #print(np.linalg.norm(r2-r1), puk1.get_R()+puk2.get_R())
        if(np.linalg.norm(r2-r1) <= puk1.get_r()+puk2.get_r()):
            t_point = i
        else:
            i+=1
    return t_point
        
ax.scatter(puk1.get_center(1),puk1.get_center(2))
ax.scatter(puk2.get_center(1),puk2.get_center(2))
#print(findColUelastisk(puk1,puk2))
def newObject(puk1,puk2):
    tindex = findColUelastisk(puk1, puk2)
    centerx = []
    centery = []
    angles = []
    m = puk1.get_m()+puk2.get_m()
    I = 0
    ts = np.arange(12,len(puk1.get_center(0)),1)
    
    #find positionen af massemidtpunktet
    for t in ts:
        r1 = np.array([puk1.get_center(1)[t],puk1.get_center(2)[t]])
        r2 = np.array([puk2.get_center(1)[t],puk2.get_center(2)[t]])
        r21 = r2-r1
        Lr21 = np.linalg.norm(r21)
        enhed21 = r21/Lr21
        if(np.linalg.norm(r1)<np.linalg.norm(r2)):
            cr = r2 - enhed21*1/2*Lr21
            centerx.append(cr[0])
            centery.append(cr[1])
        else:
            cr = r1 + enhed21*1/2*Lr21
            centerx.append(cr[0])
            centery.append(cr[1])
    # find ændringen i vinkel
    
    return centerx,centery

val = newObject(puk1, puk2)
xs = val[0]
ys = val[1]
ax.scatter(xs,ys)
