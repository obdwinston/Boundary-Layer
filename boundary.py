import sys
import numpy as np

def split(Vt, x, y):

    Ve = abs(Vt)
    istag = np.argmin(Ve)
    Ve[istag] = 0. # stagnation point
    Veu, Vel = Ve[istag:], np.flip(Ve[:istag + 1])

    xu, yu = x[istag:], y[istag:]
    dxu, dyu = np.diff(xu), np.diff(yu)
    dsu = np.sqrt(dxu**2 + dyu**2)
    su = np.insert(np.cumsum(dsu), 0, 0)

    xl, yl = np.flip(x[:istag + 1]), np.flip(y[:istag + 1])
    dxl, dyl = np.diff(xl), np.diff(yl)
    dsl = np.sqrt(dxl**2 + dyl**2)
    sl = np.insert(np.cumsum(dsl), 0, 0)

    return Veu, Vel, su, sl, istag

def combine(thetau, thetal, Hu, Hl, H1u, H1l, cfu, cfl):

    theta = np.concatenate((np.flip(thetal[1:]), thetau))
    H = np.concatenate((np.flip(Hl[1:]), Hu))
    H1 = np.concatenate((np.flip(H1l[1:]), H1u))
    cf = np.concatenate((np.flip(cfl[1:]), cfu))

    return theta, H, H1, cf

def solve(Ve, s, Re, Htran, trim):

    m = len(Ve)
    dVe = np.gradient(Ve, s)

    theta = np.zeros(m)
    H = np.zeros(m)
    cf = np.zeros(m)

    # laminar regime

    def get_LH(lambd):
        if lambd >  0.:
            L = .22 + lambd*(1.57 - 1.8*lambd)
            H = 2.61 - lambd*(3.75 - 5.24*lambd)
        else:
            L = .22 + 1.402*lambd + .018*lambd/(lambd + .107)
            H = 2.088 + .0731/(lambd + .14)
        return L, H
    
    L = np.zeros(m)

    theta[0] = np.sqrt(.075/Re/dVe[0])
    lambd = Re*theta[0]**2*dVe[0]
    L[0], H[0] = get_LH(lambd)
    cf[0] = 2*L[0]/(Re*theta[0])

    itran = m
    for i in range(1, m):
        if i == 1:
            theta[i] = theta[0]
        else:
            # trapezoidal rule
            dtheta = .225/Re*(s[i] - s[i - 1])*(Ve[i]**5 + Ve[i - 1]**5)
            theta[i] = np.sqrt((theta[i - 1]**2*Ve[i - 1]**6 + dtheta)/Ve[i]**6)

        # check transition
        Rex = Re*s[i]*Ve[i]
        Ret = Re*theta[i]*Ve[i]
        Retmax = 1.174*(1. + 22400./Rex)*Rex**.46
        if Ret > Retmax: # transition
            itran = i
            theta[i] = 0.
            break
        
        # laminar separation
        lambd = Re*theta[i]**2*dVe[i]
        if lambd < -.0842 or np.isnan(lambd): # separation
            sys.exit('Error: laminar separation')

        L[i], H[i] = get_LH(lambd)
        cf[i] = 2*L[i]/(Re*theta[i]*Ve[i])
    
    # turbulent regime

    def get_H1(H):
        if H <= 1.6:
            H1 = 3.3 + .8234*(H - 1.1)**-1.287
        else:
            H1 = 3.3 + 1.5501*(H - .6778)**-3.064
        return H1
    
    def get_H(H1):
        if H1 < 5.3:
            H = .6778 + 1.1538*(H1 - 3.3)**-.326
        else:
            H = 1.1 + .86*(H1 - 3.3)**-.777
        return H
    
    def get_cf(H, Ret):
        return .246*10.**-(.678*H)*Ret**-.268
    
    def get_f(theta, H1, Ve, dVe):
        H = get_H(H1)
        Ret = Re*theta*Ve
        fa = -theta*(2. + H)*dVe/Ve + .5*get_cf(H, Ret)
        fb = -H1*(dVe/Ve + fa/theta) + .0306*(H1 - 3.)**-.6169/theta
        return np.array([fa, fb])

    H1 = np.zeros(m)
    H1[itran - 1] = get_H1(Htran)

    for i in range(itran, m - trim):
        
        # RK2 method
        f1 = get_f(theta[i - 1], H1[i - 1], Ve[i - 1], dVe[i - 1])
        y1 = np.array([theta[i - 1], H1[i - 1]]) + (s[i] - s[i - 1])*f1
        f2 = get_f(y1[0], y1[1], Ve[i], dVe[i])
        y2 = np.array([theta[i - 1], H1[i - 1]]) + .5*(s[i] - s[i - 1])*(f1 + f2)
        
        theta[i] = y2[0]
        H1[i] = y2[1]

        # turbulent separation
        H[i] = get_H(H1[i])
        if H[i] > 2.4 or np.isnan(H[i]): # separation
            sys.exit('Error: turbulent separation')

        Ret = Re*theta[i]*Ve[i]
        cf[i] = get_cf(H[i], Ret)
    
    H1[:itran] = 2*H[:itran] # for laminar boundary layer thickness
    cd = 2*theta[-trim - 1]*Ve[-trim - 1]**(.5*(H[-trim - 1] + 5)) # squire-young
    
    print('surface done')

    return theta, H, H1, cf, cd, itran
