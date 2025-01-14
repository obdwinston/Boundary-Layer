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

def plot_cp(d, ds, cp1, cp2, istag, itranu, itranl, x, y, beta, trim):

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
    ax.invert_yaxis()
    ax.grid()
    
    axx.plot(x, y, color='black', label='airfoil')
    axx.plot(x[trim:-trim] - d[trim:-trim]*np.sin(beta[trim:-trim]), \
             y[trim:-trim] + d[trim:-trim]*np.cos(beta[trim:-trim]), \
             color='red', linewidth=1, label=r'$\delta$')
    axx.plot(x[trim:-trim] - ds[trim:-trim]*np.sin(beta[trim:-trim]), \
             y[trim:-trim] + ds[trim:-trim]*np.cos(beta[trim:-trim]), \
             color='red', linewidth=1, linestyle='--', label=r'$\delta^*$')
    axx.scatter(x[istag], y[istag], color='red', s=20, label='stagnation', zorder=10)
    axx.scatter([x[istag + itranu - 1], x[istag - itranl + 1]], \
                [y[istag + itranu - 1], y[istag - itranl + 1]], \
                color='red', marker='x', s=20, label='transition', zorder=10)
    axx.set_ylabel(r'$y$')
    axx.legend(loc='lower right')
    axx.set_aspect('equal')
    plt.show()
