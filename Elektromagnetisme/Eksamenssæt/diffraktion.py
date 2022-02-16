import numpy as np

def f(R, m, lam, d):

    cons = []
    for i in m:
        cons.append(R*(i+1/2)*lam/d)

    print('minima er :')
    for c in cons:
        print(c)

    return

print(f(1, [-1, -2, -3, -4, 1, 2, 3, 4], 500*10**-9, 300*10**-6))




