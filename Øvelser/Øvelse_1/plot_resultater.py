import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize = (10, 6))

vinkler = [11, 13, 15, 19, 21]
eksp = [1.22, 1.39, 1.66, 1.96, 2.13]


def a(grader):
    return np.sin(grader*2*np.pi/360)*9.82*0.66

v_u = [[a(v-0.5), a(v), a(v+0.5)] for v in vinkler]

print(v_u)

ys = [11, 13, 15, 19, 21]

# for v,y in zip(v_u, ys):
#     ax.errorbar(v[1], y, xerr = np.array([v[0], v[2]]).T)

ax.plot([ys[0]]*3, v_u[0], 'r-' , linewidth = 2, label = "usikkerhed")
ax.plot([ys[0]], v_u[0][1], 'ko', ms = 10, label = 'forudset a')
ax.plot(ys[0], eksp[0], 'b*', ms = 10, label = 'eksperimental a')

for v,y,e in zip(v_u[1:], ys[1:], eksp[1:]):
    ax.plot([y]*3, v, 'r-' , linewidth = 2)
    ax.plot(y, v[1], 'ko', ms = 10)
    ax.plot(y, e, 'b*', ms = 10)

ax.set_ylabel('acceleration', fontsize = 14)
ax.set_xlabel('grader', fontsize = 14)
ax.set_title('Resultater', fontsize = 20)
ax.legend()
plt.show()

fig.savefig('res_rulle.png')


