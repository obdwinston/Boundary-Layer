import numpy as np
import matplotlib.pyplot as plt

def plot_cf(theta, H, cf, x, trim):
    
    plt.plot(x[trim:-trim], cf[trim:-trim], label=r'$c_f$')
    plt.plot(x[trim:-trim], H[trim:-trim]*theta[trim:-trim], label=r'$\delta^*$')
    plt.ylim([0., .01])
    plt.xlabel(r'$x$')
    plt.ylabel(r'$c_f$, $\delta^*$')
    plt.legend('upper right')
    plt.grid()
    plt.show()

def plot_cp(d, ds, cp1, cp2, istag, itranu, itranl, x, y, beta, trim):

    _, ax = plt.subplots()
    axx = ax.twinx()

    cutoff = int(4*trim) # change if required
    ax.plot(x[cutoff:-cutoff], cp2[cutoff:-cutoff], label='viscid')
    ax.plot(x[trim:-trim], cp1[trim:-trim], label='inviscid')
    
    ax.set_ylim([np.min(cp1) - .3, np.max(cp1) + .3])
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
