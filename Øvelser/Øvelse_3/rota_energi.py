import numpy as np
import matplotlib.pyplot as plt
import puk as puk
import fejlpropagering as fejl
import chi_sq as chi

fig, ax = plt.subplots(figsize = (30,15))

strings = ['Data0', 'Data2', 'Data4']

trials = []
trials.append([puk.Puk(['Rota/KastetCenter', 'Rota/KastetSide'], 0.0278, 0.0807),
               puk.Puk(['Rota/StilleCenter', 'Rota/StilleSide'], 0.0278, 0.0807)])

colors = ['r', 'b', 'g', 'k--']

a = []

a.append(puk.plot_Puks_energy(trials[0], ax, colors, alpha = 0.6))
ax.set_xlabel('t/s', fontsize = 20)
ax.set_ylabel('E', fontsize = 20)
ax.set_title('Energi_over tid', fontsize = 24)
ax.legend()
plt.show()
fig.savefig('rota_energi')
