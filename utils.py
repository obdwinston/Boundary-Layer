import numpy as np
import matplotlib.pyplot as plt

def plot_cf(theta, H, cf, s, trim):
    
    plt.plot(s[trim:-trim], cf[trim:-trim], label=r'$c_f$')
    plt.plot(s[trim:-trim], H[trim:-trim]*theta[trim:-trim], label=r'$\delta^*$')
    plt.ylim([0., .01])
    plt.xlabel(r'$s$')
    plt.ylabel(r'$c_f$, $\delta^*$')
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()

def plot_cp(x1, y1, beta1, x2, y2, beta2, cp1, cp2,
            d, ds, istag, itranu, itranl, trim):

    _, ax = plt.subplots()
    axx = ax.twinx()

    data = np.loadtxt('data.txt')
    xv, cpv = data[:, 0], data[:, 1]
    ax.scatter(xv, cpv, s=20, label='verification')

    cutoff = int(3*trim) # change if required
    ax.plot(x2[cutoff:-cutoff], cp2[cutoff:-cutoff], label='viscid')
    ax.plot(x1[trim:-trim], cp1[trim:-trim], label='inviscid')
    
    ax.set_ylim([np.min(cp1) - .3, np.max(cp1) + .3])
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$c_p$')
    ax.legend(loc='upper right')
    ax.invert_yaxis()
    ax.grid()
    
    axx.plot(x1, y1, color='black', label='airfoil')
    axx.plot(x1[trim:-trim] - d[trim:-trim]*np.sin(beta1[trim:-trim]), \
             y1[trim:-trim] + d[trim:-trim]*np.cos(beta1[trim:-trim]), \
             color='red', linewidth=1, label=r'$\delta$')
    axx.plot(x1[trim:-trim] - ds[trim:-trim]*np.sin(beta1[trim:-trim]), \
             y1[trim:-trim] + ds[trim:-trim]*np.cos(beta1[trim:-trim]), \
             color='red', linewidth=1, linestyle='--', label=r'$\delta^*$')
    axx.scatter(x1[istag], y1[istag], color='red', s=20, label='stagnation', zorder=10)
    axx.scatter([x1[istag + itranu - 1], x1[istag - itranl + 1]], \
                [y1[istag + itranu - 1], y1[istag - itranl + 1]], \
                color='red', marker='x', s=20, label='transition', zorder=10)
    
    axx.set_ylabel(r'$y$')
    axx.legend(loc='lower right')
    axx.set_aspect('equal')
    plt.show()
