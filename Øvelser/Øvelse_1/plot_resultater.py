import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize = (10, 6))

vinkler = [11, 13, 15, 19, 21]
eksp = [1.22, 1.39, 1.66, 1.96, 2.13]


def a(grader):
    return np.sin(grader*2*np.pi/360)*9.82*0.66

v_u = [[a(v-0.5), a(v), a(v+0.5)] for v in vinkler]

print(v_u)

ys = list(np.linspace(0, 5, 5))

# for v,y in zip(v_u, ys):
#     ax.errorbar(v[1], y, xerr = np.array([v[0], v[2]]).T)

ax.plot(v_u[0], [ys[0]]*3, 'r-' , linewidth = 2, label = "usikkerhed")
ax.plot(v_u[0][1], [ys[0]], 'ko', ms = 10, label = 'forudset a')
ax.plot(eksp[0], ys[0], 'b*', ms = 10, label = 'eksperimental a')

for v,y,e in zip(v_u[1:], ys[1:], eksp[1:]):
    ax.plot(v, [y]*3, 'r-' , linewidth = 2)
    ax.plot(v[1], y, 'ko', ms = 10)
    ax.plot(e, y, 'b*', ms = 10)



ax.set_xlabel('acceleration', fontsize = 14)
ax.set_ylabel('forsøg', fontsize = 14)
ax.set_title('Resultater', fontsize = 20)
ax.legend()
plt.show()

fig.savefig('res_rulle.png')


