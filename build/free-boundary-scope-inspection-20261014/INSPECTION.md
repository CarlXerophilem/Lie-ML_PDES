# Inspecting an extension beyond SVE

Date: 2026-10-14 (Asia/Tokyo). Status: scope recommendation and bounded checks;
independent review is recorded in REVIEW.md.

## Assessment

Yes: the three research directions are methodological and can support a
dissertation broader than SVE. The most coherent initial family is
**parameter-dependent shallow-water and related compressible-fluid balance
laws, with explicitly specified moving-boundary problems**. SVE becomes a
benchmark within the program. This is a stronger research design than simply
adding unrelated equation names to the input list.

The current manuscript already separates generic theory from SVE evidence.
Its finite determining-matrix theorem starts at draft/main.tex:218, its local
reconstruction theorem at line 652, and its task-dependent filter at line 945.
Those arguments are not specific to sediment transport. However, its abstract
at lines 33–61 and conclusions at lines 3059–3075 still place the completed
results in scalar SVE. Broader theoretical applicability is not yet broader
verified software or experimental coverage.

## What counts as a free-boundary extension

A moving boundary is part of the unknown solution. In a level-set description,
\(\Omega(t)=\{x:\Phi(t,x)<0\}\), with
\(\Gamma(t)=\{\Phi=0\}\) and \(\nabla_x\Phi\ne0\) near a regular interface.
The input includes an evolution law and boundary traces, for example

\[
\Phi_t+u\cdot\nabla\Phi=0,\qquad p=0
\quad\text{on }\Gamma(t)
\]

for a material interface with vacuum outside, in the absence of surface tension.
Other models need their own laws; the material condition is not universal.
External pressure, surface tension, permeation and contact-line conditions
change the problem and often its admitted symmetries.

An evolving Exner bed \(b(t,x,y)\) and a depth-averaged free surface can be
represented as fields on a fixed horizontal domain. That does **not by itself**
give an unknown lateral domain or a solved wet/dry shoreline problem. The
current wet-interior SVE calculation must not acquire a free-boundary theorem
merely by changing its title. Similarly, a familiar PDE on a fixed rectangle is
not a free-boundary benchmark until its unknown interface and laws are posed.

## A manageable model hierarchy

| Role | Model and parameters | Boundary/formulation task | Reason to include it |
|---|---|---|---|
| Core control | Planar, inviscid, nondispersive shallow water with flat bed, \(g>0\) | Moving wet region; \(h=0\) at a smooth material shoreline where such a formulation is valid | Closest simpler fluid subsystem; no sediment closure is needed |
| Core extension | Barotropic/polytropic Euler, \(p(\rho)=K\rho^\gamma\), \(K>0,\gamma>1\) | Material vacuum boundary, \(p=0\), specified initial density and interface | Adds a genuine constitutive exponent and retains mass and momentum structure |
| Coupled anchor | Full Eulerian SVE with an explicitly chosen sediment law, including general Grass exponent \(m\) | Specify wet-region/interface and sediment boundary laws separately; retain evolving bed-slope force | Preserves the user's original model and tests extra fields and nonconservative coupling |
| Optional later comparison | Nonlinear diffusion/porous-medium or Stefan problems | Free-support or phase-interface law, as appropriate | Useful test of boundary-aware symmetry selection, but a distinct parabolic class |

In the core family, \(h\) plays the density role and shallow water has pressure
\(p(h)=gh^2/2\). Thus flat-bed shallow water corresponds mathematically to the
polytropic member \(\gamma=2,K=g/2\). This is a model identification, not by
itself a proof that \(\gamma=2\) is an exceptional Lie-symmetry stratum.
Dorodnitsyn–Kaptsov, Remark 1 on PDF p.4, explicitly gives the normalized
\(\gamma=2\) connection [S1].

In vector conservative notation the common starting point is

\[
\rho_t+\nabla\!\cdot(\rho u)=0,\qquad
(\rho u)_t+\nabla\!\cdot(\rho u\otimes u+p_\lambda(\rho)I)=S_\lambda.
\]

SVE adds the bed equation and a bed-slope momentum source. Different closures,
friction, rotation or dispersion are separate cases, not silently included.
For a dissertation, first complete shallow water and polytropic Euler as the
two related non-scalar cases, then carry the same checks to the coupled SVE
case. Do not begin with all hyperbolic, parabolic and dispersive families.

If the final title retains “(2+1)-dimensional”, the main cases must actually
have two independent spatial variables. One-dimensional examples are valuable
controls, but cannot establish planar coverage. A rank-one action on a
three-dimensional base generally leaves a two-variable PDE; an ODE requires
effective base-orbit rank two and the other invariant-graph hypotheses.

## How the three directions extend

**1. Lagrangian coordinates: compare complete problems.** For a material map
\(x=X(t,a)\), write

\[
X_t=u(t,X),\qquad F=D_aX,\quad J=\det F>0,\qquad
\rho(t,X(t,a))J=\rho_0(a).
\]

Here \(\rho_0\) is the conserved mass density in reference coordinates:
\(\rho_0(a)=\rho(t_0,X(t_0,a))J(t_0,a)\). It equals the initial Eulerian
density as a function of \(a\) when \(X(t_0,a)=a\).

A material boundary can become a fixed label boundary. Its pressure, flux,
kinematic and initial conditions must also be transformed. This does not
remove the physical unknown or prove that a regular map exists globally.
In two spatial dimensions, \(X\) has two components and \(J\) is a determinant;
the scalar identity \(h=1/\phi_s\) is not the two-dimensional transformation.

Distinguish **mass labels** from general material labels. In one dimension,
mass normalization gives \(X_s=1/\rho\) and is singular as \(\rho\to0\).
General material labels instead give \(\rho\circ X=\rho_0/X_a\); \(\rho_0=0\)
at the boundary can coexist with a nonzero map Jacobian. Vacuum does not imply
that every Lagrangian coordinate map is singular. Sources [S1] and [S2] use
these different formulas. Boundary regularity and degeneracy still require
their own analysis.

The Exner bed is not generally advected with water particles. Its pullback
obeys \(\partial_t(b\circ X)=(b_t+u\cdot\nabla b)\circ X\); omitting the
second term changes the model. Also, a solution-dependent material change
of coordinates need not preserve the category of local point symmetries in
the original variables. Record whether a pushed-back symmetry becomes
potential, nonlocal or otherwise outside the declared search class.

**2. Parameter strata and orbit rank: keep three different changes apart.**
Study (a) where the equation determining system changes rank, (b) where the
boundary/data restrictions change the admitted candidates, and (c) where a
chosen action's projected orbit rank changes in space or field state. These
are related but not interchangeable phenomena.

Within the same declared finite candidate space, if exact splitting gives
finite linear systems, the fixed-problem constraints can be written as

\[
A_{\mathrm{problem}}(\lambda,a)c=
\begin{pmatrix}A_{\mathrm{interior}}(\lambda)\\
A_{\mathrm{boundary/data}}(\lambda,a)\end{pmatrix}c=0.
\]

Here \(\lambda\) denotes fixed model parameters and \(a\) data parameters;
this use of \(a\) is unrelated to the scale function in the example below.
For unknown interfaces the candidate action must first be lifted to the
boundary variables and their determining conditions included. Finite
splitting, constant differential order and regularity are hypotheses, not
automatic consequences of writing a matrix. Singular interfaces, vacuum and
order-changing parameter values need separate branches.

An orbit-rank “distribution” can mean a map of constant-rank regions and their
singular sets. It is not a probability distribution without a sampling law.
For example, planar rotation has base coefficients \((0,-y,x)\): rank one
away from the origin and zero at the origin. A radial chart excludes the
origin even when the physical solution itself is regular there.

**3. Task-dependent symmetry selection: add the free boundary to the task.**
Keep the chain: equation validity and closure; invariant-graph eligibility and
rank; chart and boundary/data compatibility; actual reduced equations;
reconstruction and cost at matched accuracy. A symmetry that translates a
solution's entire interface may preserve the free-boundary *equation family*
while failing to preserve a fixed initial geometry. A mere change of level-set
representation that leaves \(\Gamma\) unchanged should not be counted as
physical variable compression. Nor should a valid spatial translation be
universally discarded as “trivial”. This is an eligibility filter, not
automatically a filtration by Lie subalgebras or ideals.

Cherniha–Kovalenko explicitly include unknown boundaries and boundary jets in
their free-boundary symmetry definition [S3]. Their model is a Stefan-type
parabolic problem; its classification must not be transferred to fluid models.

## The input interface needs a real extension

The current `PDEProblem` already supports multiple fields and independent
variables. However, `symm/generic/problem.py:72` requires `DataCondition.surface`
to use only base-coordinate and fixed-parameter symbols. The check explicitly
rejects a declared dependent-field symbol as a boundary surface. This is a
symbol-dependency check, not a semantic analysis of every opaque SymPy function
that could be passed to the constructor. `chart_reduction.py:115` and `:133`
require projectable generators and affine field reconstruction. The supplied
chart checks can certify selected prescribed-surface data; their success is
not unrestricted free-boundary support. The prose documentation is older than
the code in one detail: current code has a `data-compatible` status as well as
`pulled-back-only`.

A proposed free-boundary input should specify:

1. Interior fields, residuals, differential order, constitutive parameters and
   any constraints, including the precise Eulerian/Lagrangian formulation.
2. Boundary unknowns and geometry: graph, level set, or fixed material-domain
   representation, with regularity and nondegeneracy assumptions.
3. Kinematic, dynamic and flux/interface residuals **supported on that
   boundary**. Imposing a boundary law throughout the fluid changes the PDE.
4. Initial interface and field data, external forcing, parameter ranges and
   all positivity, denominator, wet/dry and Jacobian guards.
5. Admitted transformation category, the task being reduced, reconstruction
   rules and a status for unsupported or unresolved cases.

There are two legitimate implementation routes: extend the representation to
unknown boundary fields and boundary-supported jets, or first transform a
specific problem to a fixed reference domain with a verified material map.
Either route needs development and examples; adding PDE strings alone is
insufficient. No such backend change is claimed by this inspection.

## A checked non-SVE planar example

For \(K,C,D>0\), \(\gamma>1\), choose a positive scale function \(a(t)\) obeying

\[
a''=\frac{2K\gamma D}{\gamma-1}
       a^{-[2(\gamma-1)+1]}.
\]

Inside the disk \(r<a(t)\sqrt{C/D}\), set

\[
\rho=a^{-2}\left(C-D\frac{x^2+y^2}{a^2}\right)^{1/(\gamma-1)},\qquad
u=\frac{a'}a(x,y),\qquad p=K\rho^\gamma.
\]

Direct substitution verifies the two-dimensional continuity and momentum
equations. The boundary radius has \(R'=u\cdot n\), and \(p\to0\) at the
boundary. With \(X(t,\alpha)=a(t)\alpha\), one has \(J=a^2\) and
\(\rho\circ X\,J=\rho_0\), even though \(\rho_0\) vanishes at the reference
boundary. At \(\gamma=2,K=g/2\), this becomes an exact flat-bed shallow-water
profile with \(a''=2gD/a^3\).

The script `verify_scope.py` checks **14 zero identities** and three negative
controls: translation fails to preserve a fixed centered circle; common
space-time scaling fails to preserve an initial slice at positive prescribed
time; and the current API rejects an unknown-interface surface. The first
two controls concern the specified fixed objects, not the invalidity of the
corresponding equation symmetries.

This is an independently checked affine ansatz, not a completed Lie-group
reduction, learned solution, new exact-solution claim, maximal classification,
or arbitrary-data theorem. Sideris supplies relevant prior art for affine
free-boundary Euler motion in **three** spatial dimensions [S4]; that theorem
is not the justification for this separately checked planar formula. Interior
smoothness and boundary traces do not assert uniform smoothness across vacuum
for every real \(\gamma\).

## Suggested manuscript wording and title

The quoted sentence can be expanded prospectively as follows:

> We propose to extend the verified SVE benchmark to parameter-dependent
> shallow-water and related compressible-flow models, including explicitly
> posed free-boundary problems. The three research directions are
> Eulerian–Lagrangian formulation and reconstruction, parameter strata and
> spatial variation of symmetry-orbit rank, and task-dependent selection of
> symmetries compatible with the equations, moving boundaries and prescribed
> data. SVE provides the initial evidence base; broader model coverage and any
> machine-assisted discovery remain subject to separate verification. No
> learned first integral, neural speedup, general free-boundary solver, or
> global existence theorem is claimed here.

A title that fits the broadened mathematical program is:

**Lie Symmetry Reduction of Parameter-Dependent Shallow-Water and Related
Free-Boundary Models**

If a demonstrated ML contribution remains a central dissertation requirement,
append **“with Machine-Learning-Assisted Solution Construction”**. Treat that
as a research target until supported by an actual learned proposal and the
appropriate exact or approximation checks. The three directions themselves
do not require ML. The formulation description can state nondimensionalization
or a particular coordinate transformation without the vague word “Processed”.

## Evidence and validation

See SOURCES.md for four primary references, DOI/arXiv identity checks, source
versions, PDF hashes and equation/page anchors. Search boundary: four papers,
no citation traversal, free public primary sources; not a novelty search.

- [S1] Dorodnitsyn–Kaptsov (2020), DOI
  [10.1016/j.cnsns.2020.105343](https://doi.org/10.1016/j.cnsns.2020.105343),
  source key W, arXiv:1912.13314v1.
- [S2] Coutand–Shkoller (2011), DOI
  [10.1002/cpa.20344](https://doi.org/10.1002/cpa.20344), source key E,
  arXiv:0910.3136v1.
- [S3] Cherniha–Kovalenko (2011), DOI
  [10.4064/bc93-0-8](https://doi.org/10.4064/bc93-0-8), source key S,
  arXiv:1211.6282v1.
- [S4] Sideris (2017), DOI
  [10.1007/s00205-017-1106-3](https://doi.org/10.1007/s00205-017-1106-3),
  source key A, arXiv:1512.03288v5.

The local checks were run from `D:/MATHs/math 4890 LieML`:

- `python -B build/free-boundary-scope-inspection-20261014/verify_scope.py`:
  14 exact zero identities and three expected negative controls passed.
- `python draft/proposal_support/verify_parameter_effects.py`: passed.
- Project `data-flux` checker and `workflow` runner: passed in this inspection's
  validation directory.
- Project engine/chart/script regressions plus all 43 active-package tests:
  **94 passed** after setting `PYTHONUTF8=1` for Windows file decoding.
- Project audit: **failed, 218 reported issues**. These include unavailable
  external history, reference-integrity and existing link/output checks. No
  issue names this inspection directory; frozen files and carrier checks pass.

The first audit attempt and one regression failed under the default Windows
GBK decoder. Their logs are retained beside the UTF-8 rerun receipts. This is
not an all-green repository audit. No manuscript or bibliography edit was made,
so no LaTeX build is represented as part of this inspection.
