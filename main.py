import panel
import boundary
import utils
import numpy as np

M = .02                     # maximum camber [% chord]
P = .40                     # maximum camber position [% chord]
t = .12                     # thickness [% chord]
n = 128                     # half number of panels
alpha = np.radians(4.3)     # angle of attack [rad]
Re = 5.4e6                  # Reynolds number
Htran = 1.4                 # transition shape factor (1.3 to 1.4)
trim = n//20                # trim turbulent trailing edge

X, Y, x, y, S, beta = panel.airfoil(M, P, t, n)
An, At = panel.coefficients(X, Y, x, y, S, beta)

RHS = panel.constants(alpha, beta, 0.)
Vt, cl1, cp1 = panel.solve(An, At, RHS, alpha, beta, S)

Veu, Vel, su, sl, istag = boundary.split(Vt, x, y)
thetau, Hu, H1u, cfu, cdu, itranu = boundary.solve(Veu, su, Re, Htran, trim)
thetal, Hl, H1l, cfl, cdl, itranl = boundary.solve(Vel, sl, Re, Htran, trim)
Ve, s, theta, H, H1, cf = boundary.combine(Veu, su, thetau, Hu, H1u, cfu,
                                           Vel, sl, thetal, Hl, H1l, cfl)

cft = np.sum(cf*Ve**2*S)        # total skin friction
cdt = cdu + cdl                 # total profile drag
ds = theta*H                    # displacement thickness
d = theta*(H + H1)              # boundary layer thickness
Vn = np.gradient(Ve*ds, s)      # normal velocity

RHS = panel.constants(alpha, beta, Vn)
_, cl2, cp2 = panel.solve(An, At, RHS, alpha, beta, S)

print('skin friction coefficient: %.5f (%.1f%%)' % (cft, cft/cdt*100))
print('profile drag coefficient: %.5f' % cdt)
print('lift coefficient: %.5f, %.5f' % (cl1, cl2))

utils.plot_cf(theta, H, cf, x, trim)
utils.plot_cp(d, ds, cp1, cp2, istag, itranu, itranl, x, y, beta, trim)
