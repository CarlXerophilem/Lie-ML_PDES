# Independent review of the 2D SVE extension

Reviewer: fresh-context `fresh_review` agent. Date: 2026-10-14 (Asia/Tokyo).
Reviewed scientific claims: C1-C7, revision 1. Review method: attempted
falsification against primary equations, independent symbolic calculations,
source-image inspection, provenance checks, and a fresh numerical replay.

**Scientific verdict: C1-C7 are accepted within their explicitly declared
scopes. No material mathematical or source-mapping defect was found.**
An initially identified minor thread-provenance issue was repaired and
independently traced below; no unresolved actionable finding remains.
The final resource-only repair trace is recorded in `REVIEW.json`.
This is approval of the listed bounded claims, not an independent discovery,
maximality, general stability, physical calibration, or publication-novelty
certificate. Material future changes to a claim or its evidence require
re-review.

## Claim-by-claim verdicts

| Claim | Verdict | Basis and necessary restrictions |
|---|---|---|
| C1 | Accepted | The actual Fernandez-Nieto journal p.116 equation (1.1), Grass paragraph and equation (1.2) support the displayed vector model and coefficient convention. This is a mathematical frictionless specialization of the introductory classical model. |
| C2 | Accepted | Candidate prolonged-residual identities reproduce, and an independently constructed general diagonal prolongation yields the same parameter condition. This classifies only the specified diagonal ansatz. |
| C3 | Accepted | The four radial equations, centrifugal term, azimuthal transport term and sediment divergence are correct on the polar chart. Rotation removes the angle, leaving a PDE in time and radius. |
| C4 | Accepted | Independent substitution into the original conservative Cartesian equations gives the claimed four profile residuals, including both factors of four. Full seven-component commutator and annular balances also vanish. |
| C5 | Accepted | The first integral and exact evolving family pass independent direct checks. The wet exact family requires `2*g*K<1`, whereas the general local ODE family does not. |
| C6 | Accepted | The fresh replay reproduces the saved profile CSV hash and all recorded numerical gates. This is sampled finite-interval consistency for a constructed reduced ODE example. |
| C7 | Accepted | The actual JFM Appendix D visibly uses a low-Froude quasi-steady approximation, a frictional growth-rate formula, and transport nonlinearity greater than one. The package appropriately declines theorem transfer. |

### C1: source-to-model mapping

The source variables are water depth `h1`, vector discharge `q1=h1*U`,
sediment thickness `h2`, and fixed bedrock elevation. Its momentum force is
`g*h1*grad(h2+bedrock)`. Setting the momentum shear stress to zero and defining
the project bed elevation as `b=bedrock+h2` gives the claimed water equations.
Because bedrock is time independent, `b_t=(h2)_t`.

The source Exner equation uses `h2_t+div(q_b)=0`, and its flux convention
includes inverse solid fraction. Defining solid-volume flux
`q_s=kappa*|U|^(m-1)*U` and `q_b=q_s/(1-p)` therefore gives
`(1-p)*b_t+div(q_s)=0`; equivalently `K=kappa/(1-p)`. Keeping an explicit
solid fraction while identifying the source `A_g` with `kappa` would be a
different convention. The current mapping avoids that error. JFM p.467
explicitly confirms its own pore-inclusive flux convention.

The Grass exponent in this source is in `[1,4]`. Arbitrary real exponents
are correctly labeled as a mathematical extension on positive speed. This
is not the later arbitrary-slope or energy-consistent model advertised in
the Fernandez-Nieto paper's title. Removing stress from momentum while
retaining transport is an idealization, not a validated sediment experiment.
An unconstrained bed elevation is not by itself a proof of positive
sediment thickness or an adequate finite supply.

### C2-C4: invariance, reduction, and data

All candidate identities reproduce, including
`pr(R)E=(0,-E_v,E_u,0)` and `pr(S)E=-E`. For the general diagonal field,
my separate jet calculation gives the necessary weights
`beta=a+c`, `d=e=2*c`, and `(m-3)*c=0`. It uses fixed nonzero `g,K`;
it makes no division by `m-3`. The sign-equivalent condition in the claim,
`(3-m)*c=0`, is correct. Candidate verification and this restricted ansatz
do not exclude other point symmetries.

The rotation quotient must rotate both spatial coordinates and velocity
components. At a rotation section `theta=0`, independently differentiating
the moving basis gives `u_y=-w/r` and `v_y=a/r`; substitution reproduces
all four radial equations. This verifies the terms `-w^2/r`, `a*w/r`, and
the radial divergence factor, including the swirl contribution to speed.
The chart requires `r>0`; positive speed is needed for general real powers.
The cubic closure separately extends smoothly through zero speed.

The complete seven-component bracket `[R,D]` vanishes. The projected
determinant is `-r^2`, so the joint quotient leaves time only on `r>0`.
For the quadratic/linear Cartesian family, conservative residuals factor as

```
mass       = r^2 F_H
momentum_x = u*r^2 F_H + h*(x*F_A-y*F_W)
momentum_y = v*r^2 F_H + h*(y*F_A+x*F_W)
Exner      = r^2 F_B
```

The four `F` are precisely the displayed ODE residuals. Primitive and
conservative equivalence additionally needs `h>0`. The origin, where this
family has zero depth, is not covered by the wet chart. A constant added
bed datum requires `D-2*b0*partial_b`, as stated; a time-dependent offset
is not supplied by the symmetry. Independently integrating mass and solid
bed content over the annulus reproduces both balances with the correct
inner-boundary orientation and porosity factor.

The annulus is preserved by rotation, but not by spatial scaling. It is
therefore correct to derive a solution family and then restrict it, using
matched initial and boundary traces. Those traces do not establish a
well-posed boundary formulation for arbitrary nearby data.

### C5: exact integral and solution

`d(W^2/H)/dt=0` is verified independently for `H>0`; the signed quantity
`W/sqrt(H)` is also constant there. Eliminating `W` using the square-root
formula must retain its sign, and `W=0` is a separately invariant branch.
This changes the number of ODE unknowns, not the number of independent
variables of the original PDE.

Direct substitution of the stated `cstar/t^2` family into the original
conservative PDE gives four exact zero residuals. The assumptions are
`t>0`, `r>0`, `g,K>0`, real `omega`, and `2*g*K<1` for wetness. At equality
the depth vanishes; for larger `2*g*K` it is negative. This restriction
belongs to the special family, not to all locally defined ODE solutions.

### C6-C7: numerical and source-scope limits

The fresh replay produced 68 exact zero residual entries, all five expected
nonzero controls, and the same CSV SHA-256
`c2aa0e5d2a47a26c0c8d34d7afc77ed480b129e5b65d506b1659ec38884a5a6a`.
The new independent script imports no reviewed implementation and passes
28 additional identities.

| Replayed numerical quantity | Value |
|---|---:|
| DOP853/Radau maximum difference | 1.7392753903777702e-12 |
| Loose/fine DOP853 maximum difference | 1.2822916062305012e-9 |
| First-integral maximum absolute drift | 2.0816681711721685e-17 |
| Exact-family numerical maximum error | 3.3306690738754696e-16 |
| Minimum sampled depth coefficient | 0.9782863027785879 |
| Minimum sampled speed at radius one | 0.1978186211845709 |
| Fine finite-difference defect | 7.319824450346957e-6 |
| Coarse/fine finite-difference defect ratio | 3.9548263702416566 |

The finite-difference ratio is a recorded diagnostic; the `passed` field
does not threshold that ratio. The four named comparison/invariant/exact
gates do pass. Neither cross-solver agreement nor the finite sample grid
certifies continuous error, general PDE stability, global continuation,
or adequacy of a physical transport law. DOP853 and Radau are distinct
solver algorithms within SciPy and share the same supplied ODE.

JFM Appendix D actually includes a unisize four-field model, so relevance
cannot be dismissed on the basis of mixed-size variables. The package
correctly identifies this. Its actual displayed proof also assumes a
quasi-steady response under low Froude number, retains `C_f` in (D2), and
assumes `n>1` in (D7). A frictionless full-unsteady theorem does not follow
from those expressions alone. I did not independently certify the entire
JFM proof or prove the opposite well-posedness statement.

## Severity-ordered actionable findings

**R1 — Minor, resource provenance; resolved.** The initially reviewed `main.py:20`
used `os.environ.setdefault(name, "1")`, which preserves an inherited
value above one, while the evidence record always asserted `thread_cap=1`.
This does not falsify the numerical receipts: the reviewer explicitly
exported all three thread limits as one before replay. The requested repair
was to enforce the limits before imports or record actual environment
values. The controller changed exactly that line to `os.environ[name] = "1"`.
Reversing this single line restores the complete old script hash, which
independently confirms that no mathematical implementation changed.
The new script hash is
`3e5c2b4daaa12bb234fbaa37c3846d223e2ad57c02a9907ebc2509f712177c16`.
The updated evidence records 68 zero checks and a passed numerical gate;
the CSV, PNG and generated LaTeX table are byte-identical to the reviewer's
fresh replay. The adversarial incoming-thread-value probe is recorded in
`results/thread_cap_repair.json` and independently repeated in the review
trace. This is a resource-only issue, not a material repair of a scientific
claim.

No other actionable defect was found within the assigned scope. In
particular, there is no unsupported maximality or novelty claim requiring
removal. The numerical and source-scope qualifications above are already
present in the package and must be preserved.

## Evidence inspected and independent receipts

Read: root `AGENTS.md`, `README.md`, manuscript front matter, project map,
current experiment index, and package `RUN_CONTRACT.md`, `CLAIMS.json`,
`SOURCE_AUDIT.md`, `sources/source_manifest.json`, `main.py`,
`tests/test_extension.py`, `results/evidence.json`, `report.tex`, and the
relevant sections of `DERIVATION_RESEARCH.md`.

Primary evidence: journal title pages for both papers; Fernandez-Nieto
journal pp.116-117 extracted text; JFM pp.467 and 491 extracted text;
visual comparison of Fernandez-Nieto PDF p.2 and JFM PDF p.31. The source
PDF hashes and all 58 source-manifest artifact hashes verify. Citations,
authors, journal years, volumes, pages, and DOIs match the actual primary
title pages. No fresh literature or novelty search was performed.

Reproducible reviewer outputs are under
`build/sve-2d-extension-20261014/reviewer-replay/`:

- `evidence.json`, `profiles.csv`, `profiles.png`, `numerical_table.tex`:
  fresh replay with explicitly set single-thread environment.
- `independent_checks.py` and `independent_checks.json`: separate
  general-scaling, radial, conservative-PDE, integral, exact-family and
  annular checks. Successful calculation time was under one second.
- `source_integrity.json`: all 58 source-artifact hashes match.
- Two retained `independent_checks_*_simplification_failure.json` files:
  initial reviewer false negatives caused by SymPy leaving equivalent
  speed powers uncombined. Expansion before simplification resolved them;
  no reviewed mathematical equation or package code was changed for this.

Commands were `python -B main.py --out <reviewer-replay>` from the package
and `python -B build/sve-2d-extension-20261014/reviewer-replay/independent_checks.py`
from the repository, with `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and
`MKL_NUM_THREADS` all explicitly set to `1`.

The controller owns project-wide checks, final native LaTeX rebuilding and
rendered-page release. I did not rerun those global checks or claim to have
visually approved the report PDF. I also did not adjudicate unrestricted
classification, novelty, full arbitrary-data PDE well-posedness,
general perturbation stability, shocks, global continuation, or real-data
physical validity. All remain outside this review approval.
