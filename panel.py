import numpy as np

def airfoil(M, P, t, n):

    xx = (1 - np.cos(np.linspace(0, np.pi, n + 1)))/2 # cosine spacing
    yy = np.zeros(n + 1)

    for i in range(len(xx)):
        if xx[i] < P:
            yy[i] = (M/P**2)*(2*P*xx[i] - xx[i]**2)
        else:
            yy[i] = (M/(1 - P)**2)*(1 - 2*P + 2*P*xx[i] - xx[i]**2)

    a0, a1, a2, a3, a4 = .2969, -.1260, -.3516, .2843, -.1036
    yt = t/.2*(a0*xx**.5 + a1*xx + a2*xx**2 + a3*xx**3 + a4*xx**4)
    yu, yl = yy + yt, yy - yt

    X = np.concatenate((np.flip(xx), xx[1:]))
    Y = np.concatenate((np.flip(yl), yu[1:]))
    
    return X, Y

def coefficients(X, Y):

    x = 0.5*(X[1:] + X[:-1])
    y = 0.5*(Y[1:] + Y[:-1])

    dX = X[1:] - X[:-1]
    dY = Y[1:] - Y[:-1]
    S = np.sqrt(dX**2 + dY**2)
    beta = np.arctan2(dY, dX)

    m = len(x) # number of control points
    An = np.zeros((m + 1, m + 1))
    At = np.zeros((m, m + 1))
    Cn1 = np.zeros((m, m))
    Cn2 = np.zeros((m, m))
    Ct1 = np.zeros((m, m))
    Ct2 = np.zeros((m, m))

    for i in range(m):
        for j in range(m):
            A = -(x[i] - X[j])*np.cos(beta[j]) - (y[i] - Y[j])*np.sin(beta[j])
            B = (x[i] - X[j])*(x[i] - X[j]) + (y[i] - Y[j])*(y[i] - Y[j])
            C = np.sin(beta[i] - beta[j])
            D = np.cos(beta[i] - beta[j])
            E = (x[i] - X[j])*np.sin(beta[j]) - (y[i] - Y[j])*np.cos(beta[j])
            F = np.log(1 + (S[j]*S[j] + 2*A*S[j])/B)
            G = np.atan2(E*S[j], B + A*S[j])
            P = (x[i] - X[j])*np.sin(beta[i] - 2*beta[j]) + (y[i] - Y[j])*np.cos(beta[i] - 2*beta[j])
            Q = (x[i] - X[j])*np.cos(beta[i] - 2*beta[j]) - (y[i] - Y[j])*np.sin(beta[i] - 2*beta[j])

            Cn2[i, j] = D + 0.5*Q*F/S[j] - (A*C + D*E)*G/S[j]
            Cn1[i, j] = 0.5*D*F + C*G - Cn2[i, j]
            Ct2[i, j] = C + 0.5*P*F/S[j] + (A*D - C*E)*G/S[j]
            Ct1[i, j] = 0.5*C*F - D*G - Ct2[i, j]

    np.fill_diagonal(Cn1, -1.0)
    np.fill_diagonal(Cn2, 1.0)
    np.fill_diagonal(Ct1, np.pi/2)
    np.fill_diagonal(Ct2, np.pi/2)

    An[:-1, 0] = Cn1[:, 0]
    An[:-1, 1:-1] = Cn1[:, 1:] + Cn2[:, :-1]
    An[:-1, -1] = Cn2[:, -1]

    # Kutta condition
    An[-1, 0] = 1
    An[-1, -1] = 1

    At[:, 0] = Ct1[:, 0]
    At[:, 1:-1] = Ct1[:, 1:] + Ct2[:, :-1]
    At[:, -1] = Ct2[:, -1]

    return An, At, x, y, S, beta

def constants(alpha, beta):

    m = len(beta) # number of control points
    RHS = np.zeros(m + 1)

    RHS[:-1] = np.sin(beta - alpha)

    return RHS

def solve(An, At, RHS, alpha, beta, S):

    gamma = np.linalg.solve(An, RHS)
    
    Vt = np.cos(beta - alpha) + At@gamma
    cl = 4*np.pi*sum((gamma[1:] + gamma[:-1])/2*S)
    cp = 1 - Vt**2

    return Vt, cl, cp
