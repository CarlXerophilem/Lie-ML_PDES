# Frozen layers for the printed and material scalar equations

The maintained certificate is [symbolic_sve2026.py](../symbolic_sve2026.py). It determines local smooth point symmetries of the printed scalar \(P\) and compatible material scalar \(M\) separately. The chart is open with \(p=\phi_t>0\), \(q=\phi_s>0\), \(g,\kappa>0\) and real \(m\ge 1\). Neither the planar affine search class nor any sampled reduction data enters this determination.

| Layer | Frozen input or rule | Gate before the next layer |
|---|---|---|
| Point coefficients | \(X=\tau(t,s,\phi)\partial_t+\xi(t,s,\phi)\partial_s+\eta(t,s,\phi)\partial_\phi\), with arbitrary smooth coefficients | Compute third prolongation and solve the equation for the third jet \(r=\phi_{ttt}\) using its strictly positive coefficient. |
| Necessary jet splits | For \(P\), split the \(y,w,ab,a,x\) coefficients in sequence. For \(M\), use the slice \(a=b=c=0\) and split the \(w,x\) coefficients. Here \(a,b,c\) are the second jets and \(w,x,y\) denote \(\phi_{tts},\phi_{tss},\phi_{sss}\). | Derive each coefficient from the prolonged residual. Check rank of the homogeneous linear split before restricting a coefficient function's dependencies. The required slice is a necessary test on free jets. |
| Affine family | The finite-dimensional affine forms enter only after the dependency and curvature equations have been solved. | Compute the exponent strata from the maximal minors, then compute a kernel on each stratum. When the printed time shift remains free, derive its vanishing second derivative before adding it to the affine field. |
| Sufficiency | Full equation and the basis obtained on the chosen exponent stratum | Every basis vector must give zero on the original equation manifold with all second jets free. |
| Invariant graph and first integral | For the admitted material scaling, use \(s/t\), \(\phi/t\) and \(t>0\). | Check \(Q_X=0\) on the resulting graph. Extract its leading coefficient and check the full first-integral identity before any division by that coefficient. |
| Regression fixtures | Historical formulas, named generators and expected rank strata | Test independently of discovery. Numerical IVP and profile fixtures belong to the reproduction and benchmark layers. |

For \(M\), the unrestricted \(q^4\partial_w\) coefficient on the slice has powers \(q^5,q^4,q^3,q^2\). The frozen elimination order is \(5,2\), then \(3\), then \(4\), with each step applied to the computed polynomial. The first split forces \(\xi_t=\xi_\phi=\tau_s=0\). The next forces \(\eta_s=\tau_\phi=0\), and the last forces \(\eta_t=0\). Write \(T=\tau_t\), \(S=\xi_s\) and \(U=\eta_\phi\). The \(q^2\) term of the ensuing \(x\) split gives \(3U-S-2T=0\). Each derivative depends on a different variable, so its derivative in that variable vanishes. The other row gives \((3-m)(U-T)=0\).

For \(P\), the free jets first imply \(\xi=\xi(s)\), \(\tau=\tau(t)\), and \(\eta=\eta(t,\phi)\). The \(a\) coefficient implies \(\eta_{\phi\phi}=0\), so \(\eta=A(t)\phi+B(t)\). Differentiating the first \(x\)-row in \(s,t\) and using the constant part of the \(a\)-coefficient forces \(\xi_{ss}=\tau_{tt}=A'=0\). The remaining slope equations are
\[
3U-S-2T=0,\qquad (3-m)(U-T)=0,\qquad (m-1)B'=0.
\]
For the branch that leaves \(B'\) free, the full on-shell residual supplies \(B''=0\) through its \(b\) coefficient. The rank computation gives \(m=1,3\) for \(P\) and \(m=3\) for \(M\). The generic dimensions are four. At \(m=1\) the dimensions are five for \(P\) and four for \(M\), and at \(m=3\) both are five. The code emits bases from the matrix kernel, whose normalization can differ from the named generators in the source replay.

Run the standalone regression suite with `python -B delivery/test_sve2026_ansatz_layers.py`. It disables the source replay's generator list and coefficient fixtures during discovery. Its independent prolongation computes \(D_J Q_X+\tau\,\phi_{Jt}+\xi\,\phi_{Js}\) with fourth-jet cancellation. The tests check the unrestricted material slice, every derived basis on the unsliced equation, and inadmissible controls. Synthetic rank drops test the parameter split independently of the physical exponent values. The original source replay retains the historical named generators and one-dimensional orbit reports.
