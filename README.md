Basic program to compute airfoil skin friction coefficient using von Karman's integral momentum equation and empirical boundary layer data. Thwaites' and Head's methods used for laminar and turbulent boundary layers respectively. Squire-Young formula used to estimate profile drag coefficient. Inviscid solution computed with linear vortex panel method.

References:

- Boundary Layer - Chapter 7 of _Theoretical and Computational Aerodynamics_ by Moran (1984)
- Verification - Page 23 of _Experimental Studies of Flow Separation_ by Seetharam et al. (1977)
- Shortcomings (see `docs`) - Page 87 of _Flight Vehicle Aerodynamics_ by Drela (2013)
- Panel Method (see `docs`) - Chapter 5 of _Foundations of Aerodynamics_ by Kuethe and Chow (1997)

|                       |   Inviscid   |    Viscid    | Seetharam et al. (1997) |
| :-------------------: | :----------: | :----------: | :---------------------: |
| $\alpha = 4.3\degree$ | $c_l = 0.77$ | $c_l = 0.60$ |      $c_l = 0.63$       |
