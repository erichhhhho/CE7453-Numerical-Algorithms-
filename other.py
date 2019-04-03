import numpy as np

import scipy.interpolate as si

import matplotlib.pyplot as plt

t = np.arange(0, 1.1, .1)
x = np.sin(2*np.pi*t)
y = np.cos(2*np.pi*t)
tck,u = si.splprep([x,y],s=0)
unew = np.arange(0, 1.01, 0.01)
out = si.splev(unew, tck)

plt.figure()
plt.plot(x, y, 'x', out[0], out[1], np.sin(2*np.pi*unew), np.cos(2*np.pi*unew), x, y, 'b')
plt.legend(['Linear', 'Cubic Spline', 'True'])
plt.axis([-1.05, 1.05, -1.05, 1.05])
plt.title('Spline of parametrically-defined curve')
plt.show()