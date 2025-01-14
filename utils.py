import numpy as np
import matplotlib.pyplot as plt

def plot_cf(theta, H, cf, x, trim):
    
    plt.plot(x[trim:-trim], cf[trim:-trim], label=r'$c_f$')
    plt.plot(x[trim:-trim], H[trim:-trim]*theta[trim:-trim], label=r'$\delta^*$')
    plt.ylim([0., .01])
    plt.xlabel(r'$x$')
    plt.ylabel(r'$c_f$, $\delta^*$')
    plt.legend()
    plt.grid()
    plt.show()

def plot_cp(d, cp1, cp2, x, y, beta, trim):

    _, ax = plt.subplots()
    axx = ax.twinx()

    n = len(x)//2
    ax.plot(x[n:-trim], cp2[n:-trim], label=r'$c_{p2,upper}$', zorder=10)
    ax.plot(x[trim:n], cp2[trim:n], label=r'$c_{p2,lower}$', zorder=10)
    ax.plot(x[n:-trim], cp1[n:-trim], label=r'$c_{p1,upper}$')
    ax.plot(x[trim:n], cp1[trim:n], label=r'$c_{p1,lower}$')
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$c_p$')
    ax.legend(loc='upper right')

    axx.plot(x, y, color='black', label=r'$airfoil$')
    axx.plot(x[trim:-trim] - d[trim:-trim]*np.sin(beta[trim:-trim]), \
             y[trim:-trim] + d[trim:-trim]*np.cos(beta[trim:-trim]), \
             color='red', linewidth=1, label=r'$B.L.$')
    axx.set_ylabel(r'$y$')
    axx.legend(loc='lower right')

    ax.invert_yaxis()
    ax.grid()
    axx.set_aspect('equal')
    plt.show()
