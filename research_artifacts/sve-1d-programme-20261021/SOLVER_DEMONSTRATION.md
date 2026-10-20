# Bounded exact solver demonstration

This check is deliberately smaller than a symmetry classification. The runnable source is verify_structures.py and the machine receipt is verification.json. It performs exact SymPy simplification only; no numerical solve, training, or classification search was run.

## Printed/corrected scalar profile identities

For phi=t F(z), z=s/t, define P=F', V=F-zP, beta=m*kappa, and

    A = F''*(z^2*P - g/P^2)
    J = z*V^(m-1)*F''/P

The script independently pulls back the field jets and applies the fixed-s and fixed-t total derivatives to each scalar equation. It verifies

    t^2 E_print = D_z(L_print*F'')
    t^2 E_corrected = D_z(L_corrected*F'')

with

    L_print = -z^3*P + g*z/P^2 + g*beta*z*V^(m-1)/P
    L_corrected = F*(g/P^3-z^2) + g*beta*z*V^(m-1)/P

Both identities pass with symbolic real m and separately at m=1,2,3,4. SymPy needs the explicit positive-chart rewrite V^m=V*V^(m-1) in the symbolic-m simplification; this is recorded in the checker and requires V>0. The first integral lowers profile order from three to two only on a subinterval where the relevant L is nonzero.

## Traveling-wave reduction of E

The checked positive-u system is

    h_t + (h*u)_x = 0
    u_t + u*u_x + g*(h+B)_x = 0
    B_t + D_x(K*u^m - G*u^n*B_x) = 0

The slope equation is mixed second order in space when G>0. With z=x-c*t and (h,u,B)=(H(z),U(z),Z(z)), one integration of each row gives

    H*(U-c) = q
    (U-c)^2/2 + g*(H+Z) = C
    K*U^m - G*U^n*Z' - c*Z = j

Write w=U-c. On U>0, w!=0, q/w>0, g>0,

    H=q/w
    Z=C/g - w^2/(2g) - q/w
    D=dZ/dU=q/w^2-w/g

For G>0 and D!=0, the third relation yields

    U' = (K*U^m-c*Z-j)/(G*U^n*D)

The verifier substitutes this f(U), and U''=f_U*f, Z''=D_U*f^2 + D*f_U*f, into the three original PDE residuals. The continuity and momentum residuals vanish by differentiating the first two integrals; the bed residual vanishes by differentiating the third, including its U'' contribution. The three exact symbolic remainders are zero for generic real m,n on U>0. No numerical sampling is used.

On a connected interval where N=K*U^m-c*Z-j is also nonzero, the exact implicit solution is

    z-z0 = integral from U0 to U of G*r^n*D(r)/N(r) dr.

The derivative of this map is nonzero, so a local inverse U(z) exists. This is an exact quadrature, not necessarily an elementary formula. Constant equilibria N=0 and D=0 singular strata must be handled separately.

For G=0, the bed equation after one integration is K*U^m-c*Z=j, algebraic in the traveling profiles. The checker does not divide by G or claim an ODE there. It is a separate branch and can impose a further algebraic constraint on the first two profile integrals.

## Independent exact control

This control is a different family, with stationary H,U and an evolving bed; it is not a traveling profile with stationary Z(x-c*t). Choose m=2, g=K=q=alpha=1, beta=2, G=0:

    U(x)=sqrt(x+2)
    H(x)=1/U(x)
    B(t,x)=3-H(x)-U(x)^2/2-t

The prescribed sediment flux is K*U^2=x+2=alpha*x+beta, so B_t=-alpha cancels its derivative alpha. The independent Bernoulli constant is C/g=3; it is not alpha+beta. Direct substitution into the original three PDE residuals gives (0,0,0): continuity, momentum, sediment. The domain is x>-2, where U>0 and H>0, for all t. This is a constructed exact field solution, not a blanket initial-boundary compatibility claim.

Perturb only the bed to B+epsilon*x. The residual vector becomes (0,epsilon,0); hence it is not a solution for epsilon!=0. This tests the momentum coupling directly while retaining the same mass and G=0 sediment balances.

## Receipt

verification.json records 19 pass conditions: two symbolic-m identities, eight integer-exponent identities, three traveling-reduction residuals, three exact-control PDE residuals, and three perturbation-control outcomes. The perturbation momentum check is marked pass when its exact remainder is nonzero, because that is the expected negative control.
