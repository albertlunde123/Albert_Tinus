import puk as puk
import matplotlib.pyplot as plt
from matplotlib import animation

fig, ax = plt.subplots(figsize = (16,8))

Rota_Kastet = puk.Puk(['Rota/KastetCenter','Rota/KastetSide'], 1, 1)
Rota_Stille = puk.Puk(['Rota/StilleCenter','Rota/StilleSide'], 1, 1)
puks = [Rota_Kastet, Rota_Stille]

def pukanim(puks, ax):
    N = len(puks[0].get_center(0))
    color = ['bo', 'ro']

    puk1 = ax.plot(puks[0].get_center(1)[0], puks[0].get_center(2)[0], color[0], label = 'Puk distance', ms = 75)[0]
    puk2 = ax.plot(puks[1].get_center(1)[0], puks[1].get_center(2)[0], color[1], label = 'Puk distance', ms = 75)[0]

    def update(i):
        puk1.set_data(puks[0].get_center(1)[i], puks[0].get_center(2)[i])
        puk2.set_data(puks[1].get_center(1)[i], puks[1].get_center(2)[i])
        return puk1, puk2

    anim = animation.FuncAnimation(fig,
                                update,
                                frames = N,
                                interval= 100,
                                blit=True)
    return plt.show()
ax.set_xlim(-500, 500)
ax.set_ylim(-300, 300)
pukanim(puks, ax)
