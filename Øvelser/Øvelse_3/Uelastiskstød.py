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
    #Tjek om de to radier er tæt nok på hinanden til at de har kollideret, hvor efter t-værdiens
    #index retuneres
    for t in ts:
        r1 = np.array(xs1[i],ys1[i])
        r2 = np.array(xs2[i],ys2[i])
        if(np.linalg.norm(r2-r1) <= puk1.get_r()+puk2.get_r()):
            t_point = i
        else:
            i+=1
    return t_point
        
ax.scatter(puk1.get_center(1),puk1.get_center(2))
ax.scatter(puk2.get_center(1),puk2.get_center(2))
#print(findColUelastisk(puk1,puk2))
#Lav et nyt pukobjekt som i virkeligheden ikke er en puk, men to pukker der sidder sammen. Dette
#gøres så man kan bruge metoderne fra puk, hvilket stadig burde være gyldigt.
def newObject(puk1,puk2):
    tindex = findColUelastisk(puk1, puk2)
    centerx = []
    centery = []
    angles = []
    m1 = puk1.get_m()
    m2 = puk2.get_m()
    radius1 = puk1.get_r()
    radius2 = puk2.get_r()
    #Beregn inertimomentet udfra parallelaske sætningen
    I = 1/2*m1*radius1**2 + m1*radius1**2 + 1/2*m2*radius2**2+m2*radius2**2
    ts = np.arange(tindex,len(puk1.get_center(0)),1)
    
    #find positionen af massemidtpunktet over tid. Dette gøres ved at finde retningsvektoren 
    #mellem de to centre, det halve af denne retningsvektor lægges til retningsvektoren af den 
    #ene puk. Fordi så får man netop en retningsvektor til centrum. Det er 
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
    edge_x = centerx - puk1.get_center(1)[tindex:]
    edge_y = centery - puk1.get_center(2)[tindex:] 
    for i in range(len(edge_x)):
        a = np.arctan2(edge_y[i], edge_x[i])
        if a < 0:
            a += 2*np.pi
        angles.append(a)
    print(angles)
    
    return centerx,centery,angles

val = newObject(puk1, puk2)
xs = val[0]
ys = val[1]
ax.scatter(xs,ys)
plt.show()