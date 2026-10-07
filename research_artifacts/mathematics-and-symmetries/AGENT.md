# Project directives and memory

Project: mathematics and symmetries / Lie-ML PDES.
Handoff date: 2026-10-06. This is an export snapshot, not a claim that all
historical chats or all locally developed repository revisions were recovered.

## Read first and resolve authority

1. Follow the current user's explicit request.
2. Read `main(1).tex`, `NEXT.md`, and `EXPORT_STATUS.md` together.
3. Read the current 2026-10-05 project checklist in `notes/original/Pasted markdown.md`.
4. Read the relevant experiment's README and source/evidence before changing it.
5. Treat `code/repository/AGENTS.md`, `CLAUDE.md`, and older research plans as
   preserved historical contracts for that public snapshot. Its Windows paths,
   environment statements, and earlier design gate are not current-host facts.

The latest checklist reports that the generic architecture was approved and
implemented. Its source is absent here. Do not ask to approve the same design
solely because an older archived contract still calls it pending; first recover
and reconcile the actual approved specification. This export request authorizes
packaging and citation/document revision, not silently implementing new theory.

## Objective and settled direction

Build a tractable, interpretable pipeline for parameter-dependent nonlinear
PDEs: specify and verify Lie symmetries, reduce an admissible family, construct
an analytical approximation, learn its unresolved correction, reconstruct,
and independently check the original equations/data. Lie mathematics and ML
evaluation are both substantive parts; a neural network is not the authority
on classification, branch validity, reduction or certification.

The current anchor is the printed Paliathanasis--Leon--Leach 2026 scalar
SVE-informed equation near exceptional transport exponent `m=3`.
An independently implemented 2+1 Eulerian Grass SWE/SVE benchmark and a
series-first KAN pilot are related experimental tracks, not interchangeable
derivations of that scalar equation.

The next bounded research question is the first-order continuation or
obstruction of `X5` at `m=3+delta`, followed by physical data/flux compatibility.
Keep cost low and use exact analysis to decide which ML task is worth running.

## Mathematical contract and notation

- `p`: independent-variable count; `q`: field count; `r`: equation count;
  `n`: differential order. State whether “2D” means 1+1 or 2+1.
- `epsilon`: group-flow displacement; `delta=m-3`: model-exponent perturbation;
  `eta_ic`: initial-curvature family parameter. They are different quantities.
- Coefficients are fixed during a point-symmetry action unless an equivalence
  transformation on parameters has been explicitly defined.
- Use `beta_tr=m*A_g*xi`; record what is held fixed when changing `m`.
- Distinguish a dependent coordinate, its physical field/section, graph, and jet.
- Record smoothness/sign/nonzero conditions, rankings, divisions and singular
  branches. Nondimensionalize before expanding a noninteger velocity power
  into a logarithm.
- Verify `pr(X) Delta = M Delta` or a correctly stated on-shell criterion;
  failure of one supplied sufficient multiplier identity is not proof that no
  symmetry exists.
- A finite polynomial candidate search does not establish a maximal local
  point algebra. Approximate, conditional, potential/nonlocal, generalized,
  variational and discrete symmetries need separately named contracts.
- An ODE reduction of a PDE with `p` independent variables generally needs
  `p-1` independent admissible orbit directions and the relevant rank conditions.
- Pull back data and fluxes separately. Do not discard residual orbit dependence
  or confuse data invariance with IBVP existence/well-posedness.
- Lie point symmetry does not automatically provide a Noether current.

## Verified anchor to preserve

For the printed scalar equation on the declared regular branch:

```text
E_m[phi] = Dt(phi_s*phi_tt - g*phi_ss/phi_s^2)
           - g*beta_tr*Ds(phi_t^(m-1)*phi_ts/phi_s)
X5 = t*d_t - 2*s*d_s
S5(epsilon): (t,s,phi) -> (exp(epsilon)*t, exp(-2*epsilon)*s, phi)
sigma = s*t^2; phi = F(sigma)
A = 2*sigma*F'^2 + 4*sigma^2*F'*F'' - g*F''/F'^2
B = 8*sigma^2*F'*(F' + sigma*F'')
R0[F] = 2*sigma*A' - g*beta_tr*B'
E3[F(s*t^2)] = R0[F]/t
F0 = C + K*sigma^(1/3), K^3 = 27*g/(1-4*g*beta_tr)
```

Retain `t>0`, `F'>0` where used and the nonzero third-derivative coefficient.
The unchanged generator is rejected at nearby noncubic exponents; this does
not decide whether a deformed generator exists. The published reduced formula
has a reported discrepancy with direct substitution; preserve the audit and
derive the reduction independently.

For bed elevation, material differentiation contains the advective term:
`b_tilde_t = b_t + phi_t*b_x`. Do not claim that solving the printed scalar
equation solves the full physical SVE system until elimination/reconstruction
has passed all original balances.

## Evidence and limits

| Track | What is present | Interpretive limit |
|---|---|---|
| Scalar cubic SVE | Four scripts, demos, numerical reference and fresh export checks | Smooth verification fixture; not arbitrary physical initial data |
| 2+1 SWE/Grass SVE | 108 archived neural pilot runs, conventional references, checkpoints, symbolic controls | Smooth short-time periodic benchmark; no shocks/dry beds or maximal Lie classification |
| Lie/KAN workflow | ML-free seven-step analyzer, 42 archived learning checkpoints, series/sensitivity controls | Declared finite ansatz; KAN/iteration does not consistently beat MLP; interpolation is not a derivative certificate |
| Older repository | Scalar engine, tests, Fisher/HAM and SAC-NO tracks, PDF corpus, historical plans | Earlier revision; lacks current `symm.generic` and three-layer evidence |
| Current draft tables | Reported Duffing, logistic PINN--PIKAN, fused and v0.2-family values | Matching raw artifacts absent; keep labeled historical pending recovery |

The Eulerian pilot identifies a Lie-loss/residual-weighting equivalence for
its supplied identities and saves compute with equivalent reweighting. It
does not establish a general advantage of symmetry losses. Conventional
integration remains the necessary matched-accuracy reference. Neural
profile and residual rankings can disagree; retain both.

No maximal generic-`m` classification, unrestricted continuation theorem,
global quotient, singular-branch theorem, physical scalar/SVE equivalence,
uniform neural error certificate, or structural ML speedup is established.
The supplied Navier--Stokes manuscript is a staged proof-workflow analogy;
its claimed blowup theorem is not validated here. Quantum decoherence is
motivation, not a mechanism inserted into classical water/sediment equations.

## Working and reporting rules

- Preserve original source snapshots, citations, all seeds and negative results.
- Reproduce a numerical claim from its exact source/configuration; never infer
  a result from a manuscript sentence or a past assistant summary alone.
- Use independent classical references, tolerance/grid refinement, held-out
  parameters and original-PDE residuals. Count preprocessing, training,
  inference, verification and fallback in total cost.
- Validate the derivative regularity needed by the residual before transferring
  a KAN architecture to the third-order scalar problem.
- Keep operator learning and structural candidate learning separate. Candidate
  proposals must be recovered/verified exactly and have a full-solve fallback.
- Do not present sampled positive margins or low residuals as interval proofs.
- State statuses such as `verified`, `branch-partial`, `unsupported`,
  `backend-unavailable`, `timeout`, and `ansatz-inconclusive` literally.
- Keep full dialogue, excerpt and summary provenance distinct. This package's
  chat coverage is incomplete; append imported genuine transcripts later.
- Explain the mathematics step by step with concrete examples and bounded
  claims. Prefer natural Chinese when the user asks in Chinese; do not add
  unnecessary English jargon.
- Do not rewrite older proposal formatting requirements onto this longer paper.
- Keep scripts together under `code/`, preserving package-local imports and
  requirements. Do not flatten colliding modules or merge result directories.

## Start commands

From the archive root:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
python code/export_tools/validate_package.py
```

Read each code README before installation. For cheap symbolic checks, use
SymPy, NumPy and SciPy and write new outputs outside archived result folders:

```bash
cd code/scalar_sve
python base_LieReduct.py --out ../../new_results/scalar --no-scene
cd ../lie_kan_workflow
python lie_analyzer.py --self-test --out ../../new_results/analyzer.json
```

Source commit: `fbdcfe361bc98027f33e639a803a93a40c393045`.
The recovered public GitHub URL is listed in `references.bib`. Remote host/service
descriptions in prior notes are historical evidence; their availability was not
tested during export. Continue with the ordered checklist in `NEXT.md`.
