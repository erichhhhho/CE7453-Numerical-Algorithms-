import numpy as np
import other.interpolate as si


def bspline(cv, n=100, degree=3, periodic=False):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
        periodic: True - Curve is closed
                  False - Curve is open
    """

    # If periodic, extend the point array by count+degree+1
    cv = np.asarray(cv)
    count = len(cv)

    if periodic:
        factor, fraction = divmod(count+degree+1, count)
        cv = np.concatenate((cv,) * factor + (cv[:fraction],))
        count = len(cv)
        degree = np.clip(degree,1,degree)

    # If opened, prevent degree from exceeding count-1
    else:
        degree = np.clip(degree,1,count-1)


    # Calculate knot vector
    kv = None
    if periodic:
        kv = np.arange(0-degree,count+degree+degree-1)
    else:
        kv = np.clip(np.arange(count+degree+1)-degree,0,count-degree)

    # Calculate query range
    u = np.linspace(periodic,(count-degree),n)


    # Calculate result
    return np.array(si.splev(u, (kv,cv.T,degree))).T

import matplotlib.pyplot as plt
colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')

cv = np.array([[ 0.,  0.],
   [ 0.2564844513907702,  2.1550008704893964],
   [ 0.9996139332696855, 2.1550008704893964],
   [ 3.160208137886828, 5.362680653978816],
   [ 5.666321047964407, 2.288812262341087],
   [ 4.0, 0.0]])
unew = np.arange(0, 1.01, 0.01)

plt.plot(cv[:,0],cv[:,1], 'o-', label='Control Points')
out = si.splev(unew, tck)

p = bspline(cv,n=100,degree=3,periodic=False)
x,y = p.T
plt.plot(x,y,'k-',label='Degree %3',color=colors[3%len(colors)])

plt.minorticks_on()
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(35, 70)
plt.ylim(0, 30)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()