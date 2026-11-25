# Verification and reproducibility

The source papers are Paliathanasis (2022, DOI [10.3390/sym14081679](https://doi.org/10.3390/sym14081679)) and Paliathanasis, Leon and Leach (2026, publisher PDF v3, DOI [10.3390/math14030433](https://doi.org/10.3390/math14030433)). The [artifact audit](artifact_audit.md) locates archived Fehlberg and DOP853 campaigns. See the [literature verification](../ref/Literature%20Verification%20and%20Source%20Boundaries.md) for the external source checks. This delivery adds a Python entry that regenerates exact certificates from the transcribed equations, without cached outputs. Equations (24)–(34) have individual audit entries, including the qualified status of (32).

## Commands

Run from the repository root. Use Python without the optimization flag so the exact assertions execute.

~~~sh
python -m pip install -r delivery/requirements.txt
python delivery/symbolic_sv2022.py
python delivery/symbolic_sve2026.py
python -B delivery/test_sve2026_ansatz_layers.py
python delivery/symbolic_new_model2026.py
python delivery/reproduce_sve2026.py --order 6 --output build/delivery/reproduction.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python delivery/ml_sv2022.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python delivery/ml_sve2026.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python delivery/ml_new_model2026.py
bash delivery/build_pdfs.sh
~~~

The symbolic entries use the standard library and SymPy and write final expressions and check summaries. The numerical entries use NumPy and SciPy. Wall times depend on the host. The PDF build requires pdfLaTeX, Beamer, Standalone, PGF/TikZ and Latin Modern. It builds the two vector figures independently, then makes three passes on each document. [Run logs](logs/) record the observed outcomes.

The [annular proof and native replay package](annular-transcritical-theorem-20261101/README.md) carries the full derivation of the annular reduction used in the dissertation. The [research path](research_path.md) records older runs and methods.

## Mathematical checks

| Model or check | Result and hypotheses |
|---|---|
| 2022 Eulerian \(E_1\) | Unrestricted local smooth point generators for all real \(m\ge1\) on \(h,u,g,K>0\). Dimension \(4\) at \(m=1,2\) and all other \(m\ne3\); dimension \(5\) at \(m=3\). One-dimensional classes use the connected inner group and arbitrary nonzero line scaling. |
| 2026 printed \(P\) and compatible \(M\) | Unrestricted local smooth point generators on \(\phi_t,\phi_s,g,\kappa>0\). At \(m=1\) the dimensions are \(5\) and \(4\), respectively. At \(m=3\) both have dimension \(5\); all remaining \(m\ge1\) cases have dimension \(4\). Connected adjoint orbit representatives use each actual algebra. |
| 2026 §3 reproduction | Nine entries, eleven displayed equation audits and 23 regular Taylor jets, including two mixed-scaling representatives. The stationary identity, undefined gradient chart, impossible vertical graph and arbitrary-profile identity have separate statuses. |
| Singular profiles | The material first integral, cubic critical profiles and the convergent material Laurent branch are checked in their individual models. Exhaustive classification of degenerate jets and singular solution germs remains open. |
| Rotating \(E_2\) | Both rotation-only and rotation plus bed drift quotients checked. The undivided rank-two profile equation is \(DH'=N\). The compact dissertation gives the saddle crossing theorem on its separate hypotheses. |
| Rotating exchange \(E_{\rm exch}\) | Exact rotation quotient in \((t,r)\) and swirl fixture with \(D_a=0\). Unrestricted planar classification and general radial solutions remain open. |

### Derivation and range

For \(E_1\), the [determining proof](derivations/eulerian-first-order.md) starts with unrestricted coefficient functions and splits the quadratic, linear and constant free-jet terms. The \(m>1\) argument uses \(q_u=(m-1)q/u>0\), \(q=mKu^{m-1}\), and a separate determinant identity handles \(m=1\) on the open velocity interval. The remaining exceptional factor is \(m-3\). The argument requires no upper bound on \(m\). The entry verifies 39 exact identities and controls.

Write \(T,X,Z\) for translations and \(D,S\) for the common and cubic relative scaling. The weights of the cubic scaling \(aD+bS\) are \((-a-b,-a,2b)\). Translation conjugations remove components with nonzero weight. A zero weight leaves one coefficient with connected normal forms \(0,1,-1\) after fixing the scaled direction. In the translation-only cubic case the two scaling actions and overall line scaling have rank three on the logarithms of magnitudes. Their orbits are therefore determined by supports and relative signs. In the generic algebra \(Z\) is central, so \(D+cZ\) retains \(c\in\mathbb R\). With \(Z\) normalized to one, the other two coefficients are either zero or an oriented unit vector. When the \(Z\) component vanishes, the lines form \(\mathbb{RP}^1\).

For the 2026 scalar equations, the [frozen ansatz layers](derivations/sve2026-ansatz-layers.md) separate the arbitrary point coefficients, necessary jet splits, affine kernels, full-equation sufficiency and the material invariant graph. The symbolic entry derives coefficient rows and exceptional exponents before constructing each basis. The independent regression suite disables the historical source fixtures during discovery and recomputes prolongation via the characteristic. See the [test log](logs/sve2026_ansatz_layers.txt).

The exact regular Taylor campaign uses rational input values and orders 3 to 8. A nonzero leading coefficient permits the analytic IVP theorem for real \(m\) on the positive chart. The Laurent example separately has a convergence disk proved by contraction. Rotation alone leaves two independent variables, while rotation plus time and bed drift leaves only radius. Fixed boundary geometry can exclude translations admitted by interior equations.

## Annular quotient and learned profile

On the selected rank-2 annular action, the invariant chart leaves one radial profile. \(V\), \(W\), and \(Z\) are then recovered exactly, and a learner on this chart approximates only that profile, or its coefficient map in the drift \(c\).

The selected generators are the commuting rotation \(R=-y\partial_x+x\partial_y-v\partial_u+u\partial_v\) and the drift \(T_c=\partial_t+c\partial_B\). For \(r>0\) both the point orbits and the base orbits have rank 2, so the invariant graph is \(h=H(r)\), \(\mathbf w=V(r)\mathbf e_r+W(r)\mathbf e_\theta\), and \(B=Z(r)+ct\). The undivided profile equation is \(DH'=N\), with \(V=C_1/(rH)\), \(W=C_2/r-fr/2\), \(Q=C_3/r-cr/2\), and \(Z'=P_Z\). Rotation alone leaves a partial differential system in \((t,r)\). The six generators span the kernel of the shared affine search, 56 coefficients of rank 50. [The annular assumptions](annular-transcritical-theorem-20261101/ASSUMPTIONS.md) keep that search inside the parameter-independent affine class.

The four sampled tasks in the data table are separate scalar equations. Bed drift, printed \(P\), and the material travelling wave each use their own reduced operator and traces. The exchange task learns the offset \(b(t)\) after the swirl fixture \(V=0\), \(W=\omega r\), \(D_a=0\) on a quotient that still has coordinates \((t,r)\).

The annular generators are the kernel of that declared affine determining system. The profile ODE is the governing system pulled back to the selected invariant graph. The crossing statement adds the saddle hypothesis, the frozen parameter slice, and an external existence argument. The slice \(g=K=G=f=C_1=C_2=1\), \(C_3=c/2-15/16\) makes \((r,H)=(1,1)\) critical. Saddles in this slice require \(c<-77/12\). At \(c=0\) the same critical point has a negative slope discriminant. In the compact dissertation the displayed proof is the disk-algebra contraction of the desingularized equation, identified there as a Briot–Bouquet equation. The annular note applies Teschl's stable-manifold theorems, Theorems 9.4–9.6, to the reduced planar field \((D,N)\). Printed \(P\) remains a transcribed scalar equation under a separate audit. The ball-contraction bound used for a profile defect is a general fixed-point fact about the chosen operator.

## Where ansätze enter

| Layer | Form used | What justifies or removes the restriction |
|---|---|---|
| Point generator | Affine trial fields in the planar \(E_2\) search | Unrestricted determining coefficients and free jets remove the affine assumption in all three \(1+1\) equations. The planar kernel retains its searched-class scope. |
| Invariant graph | \(Q_X=0\), for example \(\phi=tF(s/t)\) and axisymmetric fields | This graph follows from the chosen subgroup's characteristic equations on a transverse chart. The choice to study its invariant family is a restriction on solutions. |
| Singular prefix | \(F\sim-w_0/\sigma\) at the material cubic pole | Leading-order balance selects the parameter relation on this branch. The disk-algebra contraction proves the analytic remainder after the prefix is factored. At an annular saddle, the desingularized vector field supplies the slopes directly. |
| Physical benchmark | \(V=0\), \(W=\omega r\), \(D_a=0\) for exchange | Exact substitution verifies this prescribed swirl family. Solving the time-radius quotient with general traces would remove this benchmark restriction. |
| Approximation | Trace lift plus a Taylor, Chebyshev or smooth neural remainder | The trace factor enforces the initial derivatives independently of architecture. Replacing the basis changes the approximation errors and cost, so all methods are checked against the same original residual and held-out traces. |

The iterations are finite Taylor and Laurent coefficient recurrences and contractive maps for the local analytic branches.

## Data and benchmark meaning

| Case | Input | Computed | Independent check |
|---|---|---|---|
| \(E_1\) bed drift | \(m=2,g=1,K=1/2,p=u(0)^2\) | \(Y=u^2\) and \(h,u,B\) | Closed-form affine \(Y\) and original Exner balance |
| \(P\) shear graph | \(m=1,F(1)=0,F'(1)=1/2,tF''=p\) | Profile position at \(s=1.25\) | Exact logarithmic profile and third-order residual \((tF'')'\) |
| \(M\to E_1\) travelling wave | \(m=2,c=-1,\beta=1/10,k=1/5,p=F'(0)\) | Material velocity/depth and bed at fixed time | The original Exner defect on this lift is \(\beta((F')'-k)\) |
| Exchange swirl | Fixed swirl and radial bed; \(p=b(0)\) | Time-dependent bed and mobile-load offset | Exact exponential, five balances, throughput \(rQ_r=1/20\) |

These dimensionless tests use constructed data. Fit inputs are five prescribed traces and 24 interior midpoints per trace. Exact values enter evaluation only. The liquid cell \(v_1=v_0+\tanh(\gamma)\odot\tanh(A_1v_0)\) is a small adaptation of [Tao, Wang and Liu](https://doi.org/10.1016/j.cpc.2026.110237). SciPy optimizes both the feature parameters and readout. Chebyshev solves each requested trace from the reduced operator. Taylor uses two linked regular expansion charts. Both controls and the neural model impose the same traces. The logs report sampled errors, original residuals and elapsed time. The older fixed-tanh experiment remains an explicitly identified archive.

The material ML entry also exposes a series evaluator for the proven cubic pole, with separate position and gradient tail estimates.

## Original Klausen comparison

Replay the original algorithm at [upstream commit 178c414](https://github.com/oduwancheekee/liesolver/tree/178c4142598ea9cd6398a6180773becea48a17a2). In a checkout of that revision, install the upstream dependencies and run:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MPLBACKEND=Agg python main.py configs/heat_1d.yaml
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MPLBACKEND=Agg python main.py configs/wave_1d.yaml
~~~

The same two steps are bundled in `bash delivery/run_klausen_original.sh /path/to/pinned/checkout`. The runner checks the exact upstream revision and then runs the original commands and the independent comparator.
From this repository run `python delivery/verify_klausen.py heat /path/to/local/heat/model.npz` and its `wave` counterpart. The checker reimplements the trained brick maps, using an integrated heat Fourier reference and the odd-periodic d’Alembert wave reference. Generate the checkpoints locally before passing them to the checker. The table records the first replay. Repeating the original workflow gave slightly different numerical values with the same threshold outcomes. The wave data have a corner mismatch of \(e^{-12.5}\), so the comparison samples positive time and interior positions.

| Configuration | Bricks | Original MSE | Independent relative \(L^2\) | Original \(9\times10^{-7}\) threshold |
|---|---:|---:|---:|---|
| Heat | 40 | \(1.951\times10^{-6}\) | \(7.012\times10^{-4}\) | Above threshold at budget |
| Wave | 9 | \(8.611\times10^{-7}\) | \(4.342\times10^{-3}\) | Met |

## Remaining validation

The \(P\)–\(M\) comparison and continuation are deferred. The [audit archive](../.old/2026-11-23-repository-audit/) retains the prototype without making it part of the manuscript’s verification. Exhaustive singular classification, unrestricted planar classification and the matched-accuracy correction experiment remain open. A paired experiment would fix the target discretization, admissibility conditions, tolerances and corrector across both initializations. Function-space correction requires a bound in a reconstruction-compatible norm. Matched-accuracy cost is a measured outcome rather than an acceptance target for the small profile tests.
