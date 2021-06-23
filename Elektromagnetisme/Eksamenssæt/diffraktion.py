import numpy as np

def f(R, m, lam, d):

    cons = []
    des = []
    for i in m:
        cons.append(R*i*lam/d)

    d = (cons[0] - cons[1])/2

    des = [c+d for c in cons]

    print('maksima er :')
    for c in cons:
        print(c)

    print('minima er :')
    for c in des:
        print(c)

    return

print(f(1, [1, 2, 3, 4, 5, 6], 550*10**-9, 500*10**-6))




