# The Mathematical Curriculum of LieML — and How a Machine Points to a Valid Group + Manifold

*2026-07-13. A stress-tested map of the full mathematical stack behind "Semi-Analytical and Machine
Learning Methods for Solving PDEs Using Lie Symmetry": what must be learned, in what order, what the
machine actually decides at each layer, which PDE classes get which group/manifold structures, and an
algorithm survey current to July 2026 (web-swept today; tags: ✅ = opened and verified, 🟡 = unverified).*

---

## 0. The central correction (read this first)

The question "how should the machine point to a valid group + manifold for a given PDE?" contains a
hidden misconception worth removing at the outset, because the whole subject becomes clearer without it:

> **The machine does not guess or select the group. The manifold is *forced* by the PDE's signature,
> and the group is *computed* — it is the kernel of a linear operator. "Pointing" is only needed at
> five other, genuinely open decision points.**

- **The manifold is not a choice.** A PDE with p independent variables, q dependent variables, and
  order k lives on the jet bundle J^k(R^p, R^q) — coordinates = variables + all derivatives up to
  order k. For our scalar (1+1) evolution equations: J^k(R², R) with coordinates
  (x, t, u, u_x, u_t, u_xx, …). The equation Δ = 0 carves out a submanifold of J^k (under the standard
  maximal-rank/local-solvability regularity). No algorithm decides this; the PDE's shape does.
- **The group is not a choice either.** The symmetry condition pr^(k)X(Δ)|_{Δ=0} = 0 is *linear* in
  the unknown infinitesimals (τ, ξ, φ) — even for a violently nonlinear PDE — so the full point-symmetry
  algebra is the null space of a linear (determining) operator. "Valid" has an exact meaning:
  a generator is valid iff its symmetry residual is identically zero on shell, which is
  machine-checkable (our engine certifies every generator this way; `symm/sym_engine/jet.py::symmetry_residual`).

**Where the machine genuinely does point** — the five real decision points, each covered by a level below:

| # | Decision | Nature | Who decides in LieML |
|---|---|---|---|
| D1 | Which *symmetry type* to search (point → contact → generalized → nonclassical → approximate) | a ladder of cost vs. power | pipeline policy (L7) |
| D2 | Which *ansatz window* for the infinitesimals (polynomial degree D vs. full differential elimination) | completeness vs. cost; dim_D is a certified lower bound | engine + `stalled` flag (L3) |
| D3 | Which *PDE to spend engine time on first* (in a sweep over a family/library) | pure prioritization | the learned reductor — ML's legitimate seat (L9) |
| D4 | Which *subalgebra to reduce by* (each inequivalent 1-dim subalgebra = one reduction) | classification of subalgebras (optimal systems) | currently: ranker stub; optimal systems = known gap (L5) |
| D5 | Which *quotient coordinates* to hand downstream (invariant coordinates for HAM/PINN/SAC-NO) | differential invariants / moving frames | reduce.py branches; SAC-NO (L8) |

ML is allowed at D3 (and assists D4/D5); it is *never* allowed to assert validity — that is D-free,
exact, and certified. The semicontinuity argument (ADVISORY.md §3) shows this division is forced, not
stylistic: symmetry dimension jumps up on measure-zero coefficient subvarieties that no feature-based
predictor can see, so a learned pointer is at best generically right and the engine must always verify.

---

## 1. Which PDE class gets which group + manifold (the taxonomy)

The professorial answer to "for what kind of PDEs": you can read off the *expected shape* of the
symmetry structure from coarse structural features, before computing anything. That expectation is
exactly what the machine uses as a prior (and what our corpus labels encode).

| PDE class | Expected group structure | Manifold picture | Anchor (verified where marked) |
|---|---|---|---|
| **Linear** (heat u_t = u_xx) | Infinite-dimensional: superposition ideal β(x,t)∂_u (β any solution) ⊕ finite part; heat's finite part is the 6-dim **Schrödinger algebra** (sl(2,R) ⋉ Heisenberg, with center) | solution space is a vector space; the group acts projectively on it | engine flags ∞ via stalled+growth, seq [6,8,10,11,12] — verified (G1 ✅) |
| **First-order scalar** (u_t = u_x; our resonance family) | Infinite-dimensional *contact* pseudogroup (Lie: first-order PDEs integrate by characteristics); *point* algebra varies with coefficients | J^0 = R³ foliated by characteristic curves; solutions woven from them | transport seq [10,22,40,65,98] ✅; resonance c=−1/2 vs c=2 measured ✅ |
| **Generic nonlinear evolution** (Fisher–KPP) | Small solvable algebra, dim 2–4: translations, sometimes a scaling | orbits are lines/scalings in (x,t); quotient = 1-dim similarity line z | Fisher dim 2 ✅; generic corpus mode dim 1–2 ✅ |
| **Linearizable / C-integrable** (Burgers) | Large point algebra *mirroring the target linear equation* (Cole–Hopf); dim 5 = image of heat's structure | the linearizing map is a change of coordinates on J^0 | Burgers dim 5 ✅ (G1) |
| **S-integrable / soliton** (KdV) | Modest point algebra (KdV: 4 — translations, Galilean boost, scaling) but an **infinite hierarchy of generalized (Lie–Bäcklund) symmetries** — the true signature of integrability; point count alone does NOT detect it | infinite jet space (diffiety); recursion operator generates the hierarchy | KdV point dim 4 ✅ (G1); hierarchy = L7 material, beyond engine scope (honest) |
| **Parameterized family** (porous u_t=(u^m u_x)_x) | Generic branch (dim 4: translations + two scalings) + upward jumps on special parameter subvarieties (m = −4/3) — group classification | parameter space stratified by the jump locus (Zariski-closed) | generic m=2 → 4 ✅; jump demo = Phase C of PAPER_TODO_20DAYS.md |
| **Variational PDEs** | Noether: each variational symmetry ↔ a conservation law (KdV's Galilean boost ↔ a momentum-type law) | multisymplectic/cotangent structure on top of the jet bundle | L7 reading; not implemented (honest) |
| **Systems / higher dimensions** | same machinery; jets and ansatz spaces grow combinatorially (p = 3·C(D+3,3) already for scalar 1+1) | J^k(R^p, R^q) | engine scope limit, stated in spec ✅ |

Reading the table as a machine would: *linearity* ⇒ predict ∞ (rule); *order 1* ⇒ predict ∞ contact
(rule); *nonlinear second-order, no structure* ⇒ predict small solvable (prior); *parameterized* ⇒
enter classification mode and hunt the jump locus. This is precisely the taxonomy the v1.1 reductor
learns statistically — and the table explains its measured ceiling: coarse structure determines the
generic answer (presence features work), while the interesting exceptions live on subvarieties
(coefficient features fail; engine must verify).

---

## 2. The curriculum, level by level (with stress tests)

Each level: the mathematics, where it lives in this project, and its **stress test** — the known way
it breaks, because a curriculum that hides failure modes is a brochure, not a curriculum.

**L0 — Flows and vector fields on R^n.** ODE flows, one-parameter groups, exp of a vector field.
*Sources:* Hall ✅ (`ref/Hall-LieGroupsLiealgebras2015...pdf`), intro.tex §2.1–2.2.
*Stress:* non-complete vector fields (flow escapes in finite time) — why everything is *local*.

**L1 — Manifolds, Lie groups, Lie algebras.** Charts, tangent spaces, closed-subgroup theorem, the
classical groups, bracket = infinitesimal non-commutativity.
*Sources:* Lee ✅ (`ref/lee_smooth_manifolds.pdf`), Hall ✅, intro.tex §2.3–2.5 (written for this project).
*Stress:* infinite-dimensional "groups" (pseudogroups of diffeomorphisms) are NOT Lie groups in the
textbook sense — exactly what heat/transport force us to handle honestly.

**L2 — Jet bundles and prolongation.** J^k as the manifold where derivatives are coordinates; total
derivatives; the prolongation formula (linear in (τ, ξ, φ)).
*Sources:* Olver ch. 2 ✅ (`ref/Olver_LieGroups_DiffEq_g.pdf`); Kruglikov–Lychagin ✅; `symm/sym_engine/jet.py` (implemented + fuzz-tested).
*Stress:* the on-shell substitution needs a solvable leading derivative (our Task-1 bug class);
non-polynomial jet data breaks monomial splitting (the m = −4/3 risk, Phase C spike).

**L3 — Determining systems.** Split the on-shell residual on free-jet monomials → overdetermined
LINEAR system → exact null space = the algebra. The single most important fact of the subject.
*Sources:* Olver ch. 2–3 ✅; `ref/Notes on Lie symmetry group methods...` ✅; `symm/sym_engine/determining.py`, `eliminate.py`.
*Stress:* completeness. A degree-D polynomial window yields dim_D = certified LOWER bound; stabilization
is evidence, not proof; the `stalled` flag marks suspected infinite parts; full completeness belongs to
differential elimination (Riquier–Janet → rif / Rosenfeld–Gröbner; Maple escape hatch). Never state a
dim without its window.

**L4 — Structure theory of the computed algebra.** Brackets, structure constants, derived and
lower-central series, solvability; Lie's theorem: solvable algebra ⇒ reduce order by quadratures,
one symmetry at a time.
*Sources:* Hall ✅; `symm/sym_engine/algebra.py`.
*Stress:* structure constants depend on the basis the null space happened to return; classify by
invariants (series dimensions), never by raw constants.

**L5 — Invariants, reduction, and the subalgebra menu.** Characteristic system dx/ξ = dt/τ = du/φ →
invariants → invariant-solution ansatz → reduced equation on the quotient. One-dim subalgebra ↔ one
reduction; *inequivalent* subalgebras (up to the adjoint action) ↔ genuinely different reductions —
the **optimal system**.
*Sources:* Olver ch. 3 ✅; Ovsiannikov 🟡; intro.tex §"characteristic system" (worked Fisher example, verified); `symm/sym_engine/reduce.py` (translation + scaling branches, residual-0 gated).
*Stress:* **transversality** — a generator with τ = ξ = 0 (vertical) gives a constraint, not a
reduction; projective generators fall outside our two branches (engine correctly returns None).
*Known gap, stated honestly:* optimal systems are NOT implemented; the ranker stub orders candidates
by expression size, which is a heuristic, not mathematics. This is the most valuable D4 upgrade available.

**L6 — Group classification and the jump locus.** For families, dim is constant on a Zariski-open set
of parameters and jumps UP on special subvarieties (upper-semicontinuity of nullity: matrix entries
polynomial in parameters ⇒ rank lower-semicontinuous). Group classification = mapping the jump locus.
*Sources:* Ovsiannikov 🟡; Ibragimov handbook 🟡; ADVISORY.md §3 (the semicontinuity spine); our measured
resonance {u, u3, xu_x} ✅ — the phenomenon caught live in a random corpus.
*Stress:* the *windowed* label can itself jump at resonant coefficients even when the true algebra
doesn't change class (c = 2 vs c = −1/2) — window artifacts and true jumps must be distinguished by
escalation (higher D, then elimination).

**L7 — Beyond point symmetries (the ladder D1 climbs).** Contact symmetries (first-order: infinite,
by Lie); generalized/Lie–Bäcklund symmetries (integrability hierarchies; KdV); nonclassical/conditional
symmetries (Bluman–Cole: more solutions, nonlinear determining equations — our `symm/bgi_probe.py`);
approximate symmetries (perturbed equations, BGI).
*Sources:* Bluman–Kumei 🟡; Olver ch. 5 ✅; `ref/Generalized Lie Symmetries in Physics-Informed Neural Operators.pdf` ✅.
*Stress:* each rung up the ladder loses linearity or finiteness somewhere (nonclassical determining
equations are NONLINEAR) — cost explodes; climb only when point symmetries are exhausted.

**L8 — Differential invariants, moving frames, quotient coordinates.** Fels–Olver moving frames 🟡;
Lie–Tresse finiteness ✅ (`ref/LieTresse_2011.05101.pdf`): the algebra of differential invariants is
finitely generated — the theoretical license for SAC-NO's "learn on the orbit quotient" design.
*Stress:* non-compact orbits make global cross-sections fail; only local frames exist — mirrored in
ML as the canonicalization difficulty for non-compact groups (LieLAC's topic).

**L9 — The ML layer, honestly scoped.** Four seats at the table, each with a named failure mode:
(a) *triage/prioritization* (our reductor: triage tree acc 0.892 / recall 0.792 / precision 0.559,
structure-LOOCV, ✅) — fails on jump loci by construction (semicontinuity), hence engine-always-verifies;
(b) *inductive bias in solvers* (penalty/augmentation/equivariance/canonicalization — the five ref/
papers ✅) — documented dead-signal and non-compactness pathologies;
(c) *correction* (our 321-param invariant PINN ✅) — validate only against exact solutions
(McGreivy–Hakim ✅, `ref/Weak baselines...pdf`);
(d) *discovery from data* (2024–26 wave; see §3) — needs the equation to be UNKNOWN to earn its keep.
*Stress for all four:* baselines and leakage (our own measured lesson: duplicate structures inflated
1-NN 0.685 → honest 0.591).

**L10 — Certification.** HAM closure with the Turkyilmazoglu ratio 🟡 operationalized + a computable
a-posteriori residual bound on the *reduced* equation; the deliberately vacuous branch reported as
vacuous. *Sources:* `symm/fisher_kpp_reduction.py` ✅; plan.txt S2.
*Stress:* a certificate that cannot come out vacuous is not a certificate; ours can, and says so.

---

## 3. Algorithm survey — is anything (≤ July 2026) better than what came before?

Web sweep run 2026-07-13 (six queries; two post-January-2026 papers opened and read). Split the
question by regime, because the answer differs:

### 3.1 The PDE is known symbolically (our regime)

**Verdict: no. Nothing surfaced that beats exact determining systems + differential elimination.**
The state of the art for completeness remains the Riquier–Janet lineage: rif (Reid) and
Rosenfeld–Gröbner (Boulier et al.) 🟡, with incremental improvements (Buchberger-style criteria, order
bounds) predating 2025. Our engine's degree-window elimination is a deliberate lightweight variant of
this stack (certified lower bound + stall detection + escape hatch), and the sweep found no successor
to migrate to. The classical packages (CRACK/LIEPDE, GeM, SYM) remain the completeness reference.

### 3.2 The equation is UNKNOWN and only data is available (the genuinely new 2024–26 front)

- **LieNLSD** — "Explicit Discovery of Nonlinear Symmetries from Dynamic Data" (Hu, Li, Lin;
  arXiv:2510.01855, Oct 2025) ✅ abstract read. First method to output the *number and explicit
  expressions* of nonlinear infinitesimal generators from trajectory data: function library for the
  infinitesimals + the observation that the prolongation formula is LINEAR in the coefficient matrix +
  SVD null space, with neural-network Jacobians standing in for exact jets. **The professor's point:
  this is our determining-matrix pipeline with data-estimated derivatives instead of symbolic ones.**
  Independent convergence on the same linear core — validating the design, not superseding it. Where
  the PDE is known, exact beats estimated (no noise, rational arithmetic, certificates); where only
  data exists, LieNLSD-style discovery is the new capability. Claimed +20% rollout improvement when
  its symmetries feed LPSDA-style augmentation 🟡 (their number, not reproduced here).
- **Spectral symmetry discovery via Generalized Fourier Transforms** (Karjol, Shubham, Prathosh AP;
  arXiv:2603.07299, Mar 2026) ✅ abstract read. Detects symmetry as a *sparsity pattern in a spectral
  domain* instead of searching generator space — interpretable, but demonstrated on mechanics/tagging
  tasks, NOT on PDE point-symmetry computation. Watch, don't adopt.
- **LieGAN → LieSD → nonlinear extensions** (2023–2025) 🟡: the lineage moved from linear-only symmetry
  discovery to nonlinear generators; LieNLSD is its current endpoint.
- **Symmetry-invariant equation discovery** (Yang et al., arXiv:2505.12083 ✅ in `ref/`): uses
  invariants as the variable set for symbolic regression — the "coordinates" philosophy applied to
  *finding* equations rather than solving them; adjacent ally to SAC-NO.
- **LieLAC canonicalization** (Shumaylov et al., ICLR 2025, arXiv:2410.02698 ✅ in `ref/`): still the
  reference for imposing non-compact Lie symmetry on pre-trained solvers; cost documented; our
  quotient-coordinate route remains the structural alternative.

### 3.3 What this means for the paper (one paragraph, paste-ready)

No method published through July 2026 replaces exact symbolic computation of point symmetries for
explicitly given PDEs; the 2024–2026 innovation concentrated on the data-only regime, and its
strongest representative (LieNLSD) independently rediscovers the linearity of the prolongation
formula — the same structural fact our determining-matrix engine exploits exactly. This suggests a
natural division of labor that, to our knowledge, no surfaced system implements: a data-driven
front end proposes generators when the equation is unknown, and an exact engine of our kind verifies
and certifies them (residual ≡ 0, rational arithmetic) before any reduction is trusted —
"discover, then certify." We record this as future work.

---

## 4. Pointers

- Decision procedure + gates on a dated schedule: `PAPER_TODO_20DAYS.md`.
- Claim ceilings and prior-art table: `ADVISORY.md` §2.4; semicontinuity spine §3.
- Worked reduction pedagogy: `intro.tex` §"Variable compression made precise" (characteristic system +
  Fisher end-to-end + why the whole algebra matters).
- All ✅ in-tree sources are under `ref/`; all 🟡 externals must pass the Day-16 citation audit before
  appearing in `draft/draft.tex`.
