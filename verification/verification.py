import numpy as np
import matplotlib.pyplot as plt

# cl_cd verification

cl = np.array([-0.18591, -0.08402, 0.01999, 0.12436, 0.22838, 0.32851, 0.42257, 0.50732, 0.58901])
cd = np.array([0.00647, 0.00639, 0.00636, 0.00630, 0.00626, 0.00640, 0.00660, 0.00683, 0.00715])

data1 = np.loadtxt('verification/data1.txt')
clv = data1[:, 0]
cdv = data1[:, 1]

plt.plot(clv, cdv, marker='o', label='verification')
plt.plot(cl, cd, marker='o', label='viscid')
plt.xlabel(r'$c_l$')
plt.ylabel(r'$c_d$')
plt.legend(loc='upper right')
plt.grid()
plt.show()

# cl_alpha verification

alpha = np.array([-4., -3., -2., -1., 0., 1., 2., 3., 4.])
cl = np.array([-0.18591, -0.08402, 0.01999, 0.12436, 0.22838, 0.32851, 0.42257, 0.50732, 0.58901])
cli = np.array([-0.22794, -0.10715, 0.01367, 0.13449, 0.25527, 0.37597, 0.49655, 0.61698, 0.73723])

data2 = np.loadtxt('verification/data2.txt')
alphav = data2[:, 0]
clv = data2[:, 1]

plt.plot(alphav, clv, marker='o', label='verification')
plt.plot(alpha, cl, marker='o', label='viscid')
plt.plot(alpha, cli, marker='o', label='inviscid', zorder=-10)
plt.xlabel(r'$\alpha$')
plt.ylabel(r'$c_l$')
plt.legend(loc='upper right')
plt.grid()
plt.show()
