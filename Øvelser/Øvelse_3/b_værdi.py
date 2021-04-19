import numpy as np
import puk as puk

Rota_Kastet = puk.Puk(['Data/Data0/KastetCenter','Data/Data0/KastetSide'], 1, 1)
Rota_Stille = puk.Puk(['Data/Data0/StilleCenter','Data/Data0/StilleSide'], 1, 1)
puks = [Rota_Kastet, Rota_Stille]


def b_vardi(puks):
    angle = np.arctan2(puks[0].y_velocity()[0], puks[0].x_velocity()[0])
    puk1 = np.array(puks[0].get_center(2)*np.cos(angle)-puks[0].get_center(1)*np.sin(angle))
    puk2 = np.array(puks[1].get_center(2)*np.cos(angle)-puks[1].get_center(1)*np.sin(angle))
    t = puks[0].col_t()
    b = sum(puk1[:t])/t - sum(puk2[:t])/t
    print(len(puk1[:t]), t)
    print(puk1[:t])
    return b

print(b_vardi(puks))
