import puk as puk
import matplotlib.pyplot as plt
from matplotlib import animation

fig, ax = plt.subplots(figsize = (16,8))

Rota_Kastet = puk.Puk(['Uelastisk/KastetCenter','Uelastisk/KastetSide'], 1, 1)
Rota_Stille = puk.Puk(['Uelastisk/StilleCenter','Uelastisk/StilleSide'], 1, 1)
puks = [Rota_Kastet, Rota_Stille]

def pukanim(puks, ax):
    N = len(puks[0].get_center(0))
    color = ['bo', 'ro', 'ko', 'ko']

    puk11 = ax.plot(puks[0].get_center(1)[0], puks[0].get_center(2)[0], color[0], label = 'Puk distance', ms = 75)[0]
    puk21 = ax.plot(puks[1].get_center(1)[0], puks[1].get_center(2)[0], color[1], label = 'Puk distance', ms = 75)[0]
    puk12 = ax.plot(puks[0].get_edge(1)[0], puks[0].get_edge(2)[0], color[2], label = 'Puk distance', ms = 20)[0]
    puk22 = ax.plot(puks[1].get_edge(1)[0], puks[1].get_edge(2)[0], color[3], label = 'Puk distance', ms = 20)[0]

    def update(i):
        puk11.set_data(puks[0].get_center(1)[i], puks[0].get_center(2)[i])
        puk21.set_data(puks[1].get_center(1)[i], puks[1].get_center(2)[i])
        puk12.set_data(puks[0].get_edge(1)[i], puks[0].get_edge(2)[i])
        puk22.set_data(puks[1].get_edge(1)[i], puks[1].get_edge(2)[i])
        return puk11, puk21, puk22, puk12

    anim = animation.FuncAnimation(fig,
                                update,
                                frames = N,
                                interval= 100,
                                blit=True)
    return plt.show()
ax.set_xlim(-500, 500)
ax.set_ylim(-300, 300)
pukanim(puks, ax)
