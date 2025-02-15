### Description

Basic program to compute airfoil skin friction coefficient using von Karman's integral momentum equation and empirical boundary layer data. Thwaites' and Head's methods used for laminar and turbulent boundary layers respectively. Squire-Young formula used to estimate profile drag coefficient. Inviscid solution computed with linear vortex panel method.

### Verification

#### $c_l/c_d$ Verification

|      |     Inviscid      |      Viscid       |   Verification    |
| :--: | :---------------: | :---------------: | :---------------: |
| $Re$ | $5.7 \times 10^6$ | $5.7 \times 10^6$ | $5.7 \times 10^6$ |

![](https://github.com/user-attachments/assets/a4c17ebe-3670-44c4-923c-23cc3ba5326b)

#### $c_p$ Verification

|          |     Inviscid      |      Viscid       |   Verification    |
| :------: | :---------------: | :---------------: | :---------------: |
|   $Re$   | $5.7 \times 10^6$ | $5.7 \times 10^6$ | $2.2 \times 10^6$ |
| $\alpha$ |    $4.3^\circ$    |    $4.3^\circ$    |    $4.3^\circ$    |
|  $c_l$   |      $0.77$       |      $0.63$       |      $0.63$       |

![](https://github.com/user-attachments/assets/570dadf2-fcf5-4d90-bfe0-bc7157cefc25)

### Theory

![](https://github.com/user-attachments/assets/e6d7b1cf-db6e-4d4f-a5af-a856ad0093e9)

### References

- Boundary Layer - Chapter 7 of _Theoretical and Computational Aerodynamics_ by Moran (1984)
- Panel Method (see `docs`) - Chapter 5 of _Foundations of Aerodynamics_ by Kuethe and Chow (1997)
- Solution Shortcomings (see `docs`) - Page 87 of _Flight Vehicle Aerodynamics_ by Drela (2013)
- $c_l/c_d$ Verification (see `docs`) - Page 136 of _Summary of Airfoil Data_ by Abbott et al. (1945)
- $c_p$ Verification (see `docs`) - Page 23 of _Experimental Studies of Flow Separation_ by Seetharam et al. (1977)
