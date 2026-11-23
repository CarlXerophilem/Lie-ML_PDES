# Assumptions, pivots and claim boundaries

| Object or operation | Guard or hypothesis | Zero/excluded stratum and consequence |
|---|---|---|
| Full PDE | Constant `g,K,G>0`, real constant `f`; porosity already absorbed in flux | Variable coefficients and other closures are not this model |
| Determining solve | All affine point coefficients, independent of parameters and shared over the open family `g,K,G,f>0` | No maximal fixed-parameter or arbitrary-smooth-function classification follows |
| Exact determining linear algebra | Rational constant pivots only | No parameter stratum is removed by division; extra parameter-specific generators remain open |
| Time/bed invariant | Linear row `[1,c]`, pivot `1` | `c=0` is retained, not discarded |
| Other polynomial invariant solves | Exact constant matrices, nonzero constant normalizations | The matrices/nullspaces are recorded in the reviewed invariant result |
| Selected group action | Rotation and `T+c B_shift`, bracket zero | Other subalgebras and their equivalences are unclassified |
| Radius and group slice | `r=sqrt(x^2+y^2)>0`; adapted Jacobian `r` | The axis has different orbit rank; no annular chart assertion there |
| Wet-state chart | `H>0` | Dry states are outside this theorem |
| Mass inversion | `V=C1/(rH)` | `r=0` and `H=0` excluded explicitly |
| Tangential division | `V!=0`, equivalently `C1!=0` on the chart | At `C1=0`, tangential momentum is identically zero and does not determine `W`; other solutions may exist |
| Current independence | Determinant `r^3 V` with respect to `(H,W,Q)` | Independence is a chart statement; it does not assert Liouville integrability |
| Exner slope inversion | `-G S!=0`, with `S=V^2+W^2>0` forced by `C1!=0` | `G=0` or `S=0` needs a separate closure reduction; no limit theorem is asserted |
| Regular explicit ODE | `D=gH-V^2!=0` | Only the regular chart divides by `D`; the reconstruction never does |
| Candidate critical point | `D=N=0`, `r,H>0` | `D=0,N!=0` rules out a C1 profile through that state |
| Smooth crossing theorem | `det A<0`, `A=d(D,N)/d(r,H)` at the critical point | Non-saddles and `det A=0` are not classified by this theorem |
| Graph projection at the saddle | `D_H=3g>0` | Both eigendirections are nonvertical; no discarded vertical branch on this stratum |
| C1 converse | Expand along a C1 graph; obtain `D=lambda(r-r*)+o(r-r*)`, `lambda!=0` | Does not assume a second derivative or divide by `D` at the point |
| Auxiliary time | `d tau/dr=1/D` on each punctured side only | Infinite auxiliary time to the saddle; no finite-time orbit passage through an equilibrium |
| Reconstruction | Fixed `C1,C2,C3,c` and bed gauge `Z(r*)=Z*` | Fixing constants/gauge is necessary for the exactly-two-PDE-germs count |
| PDE regularity | `H` C1 implies `Z` C2; theorem yields smooth fields | No weak-solution, shock, global well-posedness or general IBVP conclusion |
| Exact family | Dimensionless `g=K=G=f=C1=C2=1`, `C3=c/2-15/16`, `c<-77/12` | At `c=-77/12` a zero eigenvalue invalidates the saddle argument |
| Negative discriminant | At `c=0`, compatible critical state but discriminant `-1539/25` for the unscaled slope equation | Proves no C1 profile through this specific state, not absence of all solutions or all symmetries |

The family is a mathematical construction. No observational data have been fitted. A physical mild-slope assessment needs dimensional scales: dimensionless `Z'=7/4` alone does not determine a dimensional bed slope. A local bed elevation can be shifted using the free gauge; no nonnegative sediment-thickness model is assumed.

The first/second-order full PDE does not have the same principal symbol as a first-order inviscid water-only system. `D=0` is the radial hydraulic pivot in the derived class. This distinction prevents transferring a scalar P/M characteristic formula to this model.
