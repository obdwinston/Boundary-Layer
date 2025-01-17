import panel
import boundary
import utils
import numpy as np

M = .02                     # maximum camber [% chord]
P = .40                     # maximum camber position [% chord]
t = .12                     # thickness [% chord]
n = 64                      # half number of panels
alpha = np.radians(4.3)     # angle of attack [rad]
Re = 5.7e6                  # Reynolds number
Htran = 1.4                 # transition shape factor (1.3 to 1.4)
trim = n//20                # trim turbulent trailing edge

# panel method

X, Y = panel.airfoil(M, P, t, n)
An, At, x1, y1, S1, beta1 = panel.coefficients(X, Y)
RHS = panel.constants(alpha, beta1)
Vt, cl1, cp1 = panel.solve(An, At, RHS, alpha, beta1, S1)

# boundary layer method

Veu, Vel, su, sl, istag = boundary.split(Vt, x1, y1)
thetau, Hu, H1u, cfu, cdu, itranu = boundary.solve(Veu, su, Re, Htran, trim) # upper surface
thetal, Hl, H1l, cfl, cdl, itranl = boundary.solve(Vel, sl, Re, Htran, trim) # lower surface
Ve, s, theta, H, H1, cf = boundary.combine(Veu, su, thetau, Hu, H1u, cfu,
                                           Vel, sl, thetal, Hl, H1l, cfl)

cft = np.sum(cf*Ve**2*S1)   # total skin friction
cdt = cdu + cdl             # total profile drag
ds = theta*H                # displacement thickness
d = theta*(H + H1)          # boundary layer thickness

# panel method (again)

X = x1[trim:-trim] - ds[trim:-trim]*np.sin(beta1[trim:-trim]) # new airfoil x-coordinates
Y = y1[trim:-trim] + ds[trim:-trim]*np.cos(beta1[trim:-trim]) # new airfoil y-coordinates
An, At, x2, y2, S2, beta2 = panel.coefficients(X, Y)
RHS = panel.constants(alpha, beta2)
_, cl2, cp2 = panel.solve(An, At, RHS, alpha, beta2, S2)

print('skin friction coefficient: %.5f (%.1f%%)' % (cft, cft/cdt*100))
print('profile drag coefficient: %.5f' % cdt)
print('lift coefficient: %.5f, %.5f' % (cl1, cl2))

utils.plot_cf(theta, H, cf, s, trim)
utils.plot_cp(x1, y1, beta1, x2, y2, beta2, cp1, cp2,
              d, ds, istag, itranu, itranl, trim)
