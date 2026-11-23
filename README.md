# Lie–SVE: parameter-dependent symmetry and semi-analytical solution families

**Review handoff:** [Gemini review brief](docs/gemini-review-handoff.md) · [agent instructions](AGENTS.md) · [current citation/source map](ref/README.md).

**Compact dissertation:** [LaTeX source](draft/dissertation_wku_compact.tex) · [24-page PDF](draft/dissertation_wku_compact.pdf).

**Full-length review edition:** [LaTeX source](draft/dissertation_wku.tex) · [51-page PDF](draft/dissertation_wku.pdf) · [build notes](draft/README.md).

This is the MATH 4890 dissertation by **Yihong Xiao**, supervised by **Dr. Puneet Rana**. The title is *Parameter-Dependent Lie Symmetries and Semi-Analytical Solutions of Nonlinear PDEs*, with Saint–Venant–Exner case studies. The supplied WKU template supplies the cover and front matter. The recorded submission date is 11 November 2026; the declaration remains unsigned.

The 17 November 2026 synchronization installs the prepared dissertation on `codex/final`. Its research questions, model definitions, six chapters, three appendices, theorem statements and proofs are unchanged. Earlier manuscript sources and the previous README are preserved in [.old/2026-11-17-42f5654/](.old/2026-11-17-42f5654/). The archive contains an exact snapshot of the previous `draft/` tree, including its supporting assets. Solver code and frozen evidence carriers retain their existing bytes.

This README summarizes the research motivations and questions expressed in our project discussions. The current dissertation governs its mathematical claims. Earlier ambitions and exploratory questions remain visible below, but do not silently enlarge its frozen scope. The older README's five-chapter/25-page description has been superseded by this supplied-template edition.

## Compact dissertation at a glance

- **Goal.** Determine how parameter-dependent Lie symmetries can yield physically reconstructible reference solutions for specified Saint–Venant–Exner problems, including singular regimes.
- **Method.** Work in jet-space coordinates to verify selected Lie actions, restrict to invariant graphs, and derive equations on regular quotient charts. Keep the printed residual `P` and the materially compatible residual `M` separate. Compare their reduced operators in the same normalization and reconstruct from `M` on an admissible chart. Use local series and classical or neural approximations with independent residual and data checks.
- **Result.** The compact manuscript establishes local `M → E1` reconstruction, an exact material travelling wave, a convergent Laurent branch on a specified cubic stratum, and two local analytic crossings at a compatible saddle of the separate cubic annular model. Chebyshev collocation gave smaller sampled errors in all three recorded benchmarks. Matched-accuracy neural cost savings, complete point-symmetry and optimal-system classification on the full parameter domain, and additional singular-branch coverage are release obligations or research questions.

**Confirmed keywords for the final edition:** parameter-dependent Lie symmetries, jet bundles, invariant reduction, Saint–Venant–Exner system, material reconstruction, singular branches, Laurent series, structure-constrained neural approximation. The currently compiled compact PDF has the six keywords printed in its abstract.

The rotating tank used for the third computational case is the depth-averaged exchange system `E_exch` on `(t,x,y)`. Three-dimensional illustrations depict the physical tank geometry. The axisymmetric swirl benchmark and the cubic annular saddle are separate cases. The original Klausen LieSolver replay is an external method check; the SVE parameter-and-branch approach is a proposed adaptation.

Earlier interim reports are in the [archived draft](.old/2026-11-17-42f5654/draft/). The retired Gemini Python draft is recoverable from [the pre-cleanup commit](https://github.com/CarlXerophilem/Lie-ML_PDES/blob/f92d4020579ec9013511420a9f1be1c060948e93/research_artifacts/SVE-reproduced-20261012/gemini-code-1792476737954.py). Its source fails compilation at line 186. The maintained [source reproduction entry point](research_artifacts/SVE-reproduced-20261012/main.py) remains available.

## 1. Research motivation and frozen questions

The goal is to understand how **parameters, symmetry structure, and series geometry** interact in specified nonlinear PDE families, and use that understanding to construct useful semi-analytical solution families. Multi-parameter SVE is the research setting: the sediment exponent is one parameter, not a replacement for constitutive coefficients, forcing, closure choices, domain assumptions, or data parameters.

The dissertation's three motivations in §1.2 are retained:

| Motivation | Mathematical question | Present scope |
|---|---|---|
| Parameters | Which parameter strata change admitted symmetry directions, regularity, or admissible reductions? | Restricted scalar strata, exponent regularity, and an explicit annular critical parameter family |
| Symmetry structure | Which independent generators, brackets, subgroup equivalences, and orbit ranks determine useful reductions? | A restricted optimal system and a verified rank-two annular quotient |
| Series and geometry | How do coefficient recurrences, singular loci, branches, and continuation determine analytical representations? | Local series, a restricted Laurent branch, and local critical crossing results |

The guiding question expressed in the discussion was:

> 对给定多参数 SVE 方程族，确定哪些对称方向能在参数层上连续延续，哪些在特殊层出现；在选定的横截子代数族下，构造约化解与原 PDE 不变解之间的局部对应，并研究其解析表示及误差控制如何随参数和临界结构变化。

In English: for a given multi-parameter SVE family, identify continuously extendible symmetry directions and directions appearing on exceptional strata; for selected transverse subalgebras, establish the local correspondence between reduced solutions and original invariant solutions, and study parameter-dependent analytical representations and error control near critical structures.

The current manuscript's §1.3 states its operational central question:

> The central question is whether an exactly verified invariant family can serve as a useful reference for computing solutions of a specified nearby target problem.

These are linked levels of the existing programme, not newly substituted research questions. Reconstruction is a necessary consistency step, not an additional fourth motivation. The four outputs in §1.3 are an exact reference family, a controlled local representation, a candidate for changed data or parameters, and a validated target solution when the required stability estimates are available.

The practical motivations raised in the discussions are also retained: physically meaningful sediment transport, rinsing/entrainment and evolving mass distributions; transparent analytical structure instead of unexplained ansätze; reuse across parameter families; and CPU-feasible computation that can justify its cost against established classical solvers. These are motivations, not demonstrated industrial applications. The eight-minute defence should foreground the selected structural question, an actual theorem/proof mechanism, and a precisely defined measure of effectiveness.

## 2. Fixed model and parameter distinctions

| Object | Meaning and boundary |
|---|---|
| `E1` / `E` | Specified one-dimensional Eulerian water–sediment system with its constitutive closure |
| `M` | Compatible material/Lagrangian scalar equation derived with the bed-transport pullback term and a locally invertible particle map |
| `P` | Distinct printed scalar benchmark, retained for source comparison and historical experiments |
| `E2` | Separate rotating two-dimensional Cartesian system with isotropic cubic transport and a bed-slope term; the annular theorem applies to this model |

The compatible material equation is frozen. Reopening it as a choice between competing equations would undo an explicit project decision. `P`, `M`, and `E2` are not interchangeable, and a result for one cannot be transferred to another without the required transformation and reconstruction argument.

Physical parameters, integration constants, initial/boundary data, group-flow parameters and fitted coefficients play different roles. For example, the annular input vector `(g,K,G,f,C1,C2,C3,c,H0)` includes both equation and solution/data parameters; it is not claimed to be a minimal physical parameterization. Differentiating with respect to a model parameter is not automatically a symmetry of a fixed equation.

The supported examples have integer spatial dimensions, with time counted separately. A real constitutive exponent, a fractional derivative order, and a fractal spatial dimension are different mathematical objects.

## 3. Semi-analytical method and established statements

1. Specify the PDE, closure, parameter domain and admissible chart.
2. Derive and verify determining equations for the declared generator class; compute brackets and state the classification limit.
3. Select a subalgebra and check orbit rank, transversality and data compatibility before imposing its invariant-surface equations.
4. Derive the reduced ODE. Establish any first integral and its independence separately from independent-variable reduction.
5. Construct exact profiles or local Taylor/Laurent representations under their actual hypotheses; distinguish regular charts from singular/critical ones.
6. Reconstruct the physical fields and coordinate map, then check the original equations and admissibility conditions.
7. Where appropriate, propose a correction for changed data or parameters and validate it against the target problem.

| Statement or computation | What the dissertation establishes | What it does not establish |
|---|---|---|
| Proposition 3.A | Local analytic continuation of symmetry kernels on constant-rank strata in a declared finite generator class | Unrestricted maximal point-symmetry classification |
| Proposition 3.B | A necessary first-order equation for differentiable continuation of generators | Higher-order compatibility or convergence of the perturbation series |
| Material travelling-wave example | A verified invariant family with explicit field reconstruction | Arbitrary initial/boundary data or all SVE solutions |
| Cubic Laurent branch | Convergence and a tail estimate on its stated parameter stratum | Exhaustion of the third-order profile equation or global coverage |
| Appendix A, Theorem A.A | Local analytic saddle-crossing branches and local analytic parameter dependence for the specified annular SVE model | A common radius on the entire parameter stratum or global continuation |
| Appendix A, Proposition A.B | Critical coefficient recursion, nonresonance, and sufficient Taylor/derivative tail bounds | A computed numerical complex-domain certificate for every parameter |
| Chapter 5 validation proposition | A conditional Banach-space contraction criterion | Verification of all its infinite-dimensional hypotheses for the implemented SVE correction |
| Historical approximation records | Finite numerical comparisons and explicitly retained failures | Continuous PDE certification or a demonstrated learning advantage |

The constant-rank and differentiation arguments are standard facts applied to the declared question. The analytical constructions do not become novel merely by combining Lie theory, series and ML. Literature priority must be assessed claim by claim.

## 4. Questions and obstacles retained from the discussions

| Question or motivation | Existing obstacle / required distinction |
|---|---|
| What is a continuous parameter–generator picture? | Kernels may form bundles only on suitable constant-rank strata; dimensions can jump. Constant dimension does not force constant Lie-algebra type. A full multi-parameter classification remains open. |
| When are there infinitely many generators? | An infinite parameter set or an infinite series does not imply an infinite-dimensional algebra. One needs independent arbitrary-function families satisfying the completed determining equations, or another rigorous infinite-dimensionality argument. |
| Can noncommutativity make ODE solving easier? | Bracket closure, an appropriate subalgebra/ideal chain, regularity and surviving reduced symmetries must be checked. A solvable algebra alone is not a proof that the particular reduction is integrable by quadratures. |
| Does a Hopf-algebra or noncommutative-geometric formulation add something? | This is an exploratory question. The current dissertation does not construct a Hopf framework or prove additional computational value from it. |
| Are our ansätze necessary or merely convenient? | Derive invariants and invariant-surface conditions from the group action. A verified chosen subgroup is not an exhaustive optimal system, particularly for rank-two reductions. |
| How do quotient geometry and topology enter? | Local quotient charts require rank and transversality assumptions. Singular orbits, chart boundaries and global topology need separate treatment; group action is not globally linearized by assertion. |
| Can the invariant class represent general evolving solutions? | Fixed symmetry constraints restrict coverage. Group foliation, moving families and non-invariant corrections remain possible directions, not established general-solution theorems. |
| How are function-space transverse directions selected? | An explicit implemented complement/projection, appropriate function spaces, derivative-loss control and reconstruction stability remain missing for the general target architecture. |
| Can every model with spatial dimension in `[1,3]`, including fractal values, be derived physically? | No such classification has been obtained. Noninteger spatial dimension needs a specified space, measure, differential operators, conservation laws and closure interpretation. Inserting a real number into an integer-dimensional formula is insufficient. |
| How do fractional, generalized, contact or nonlocal symmetries extend the method? | These require their own definitions and determining systems. Potential variables and variational/Noether hypotheses cannot be inferred from a point-symmetry calculation. |
| What does “physical correctness” mean? | Derivation from balances and constitutive assumptions, dimensional consistency, positivity, invertible material coordinates and compatible boundary fluxes must be distinguished from empirical calibration or energy consistency. Conservation integrals are not arbitrary physical-field guesses. |
| What happens near a singular set? | A formal recurrence is not a convergence proof; an ODE denominator can vanish without being a symmetry-rank jump. Critical branches, continuation charts and computable radii need explicit analysis. |
| Can profiles be transported between models or parameters? | A modified equation's exact solution need not solve the original equation. Parameter continuation must track the target equation, admissible chart, data and reconstruction, including exceptional strata such as the cubic case. |
| How do we obtain actual analytical propositions? | State assumptions, domains, local/global scope and proof obligations. Symbolic substitution checks identities; numerical agreement cannot replace existence, uniqueness or convergence proofs. |
| When is ML useful? | A concrete unmet task and matched-accuracy total-cost benefit are needed. Small training loss, more fitted coefficients, or a learned profile does not establish order reduction, generalization, or faster solution. |
| Can this transfer to 2D/3D, compressible flow, or chemical/entrainment applications? | These require new model/data specifications and validation. The annular solution class is not arbitrary 2D flow, and compressibility requires additional equations rather than a change of dimensional label. |

Earlier discussions also asked whether a symbolic method is inherently mesh-free, whether higher dimension automatically defeats numerical methods, and whether quantum-inspired or symmetry-breaking language supplies a physical mechanism. None of these implications is assumed. The relevant object, operator, measure, computational task and testable consequence must be specified before such language supports a claim.

## 5. Effectiveness, negative results and philosophical critique

“Special structure makes semi-analytical solving effective” remains a hypothesis until **effective** is measured. For a named model, chart and parameter/data family, report:

- **Analytical compression:** independent variables and ODE order before/after, independent first integrals, and remaining free constants/functions.
- **Accuracy:** truncation degree, coverage interval, derivative error, original-PDE residual and reconstructed-field error, each with its evidence status.
- **Conditioning:** distance to singular denominators, positivity bounds, inverse-coordinate sensitivity and parameter sensitivity.
- **Cost:** symbolic preprocessing, data generation, training, failed attempts, correction, inference, memory and total wall time on stated hardware.
- **Reuse and coverage:** held-out parameters/data, number of queries needed to amortize setup, excluded regions and failure rates.

Compare a classical solver, a direct neural candidate and a reference-plus-correction candidate using the same target data and accuracy criteria; compare both learned candidates before and after the same corrector. Remove the reference, learning and correction separately to identify their contributions.

The retained [40-run scalar benchmark](research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md) reports 16 evaluation-budget stops and a strong Chebyshev control. These records concern the scalar benchmark, not the current full-PDE correction architecture. The older manuscript also records 17 planned and six exploratory neural runs with no full accuracy/residual-gate passes. These are distinct campaigns; their counts must not be pooled into a new experiment. Pure PINN work was stopped in the retained research route; a direct neural control does not imply that failed direction has become successful.

The core methodological question from the discussions remains: **what evidence would support the desired claim, and what outcome would force us to revise or abandon it?** In particular:

- If matched-accuracy total cost is not reduced, the efficiency claim is unsupported.
- If non-invariant target data cannot be represented, the claimed transverse coverage is unsupported.
- If reconstruction violates the original PDE, chart or data conditions, the reduced expression is not an admissible solution of that target problem.
- If a theorem's hypotheses are not verified, a passing finite test cannot be presented as its certificate.
- If only a restricted determining system was solved, maximality and exclusion of functional symmetries remain unproved.

Adding terminology, derivations or prospective experiments is not progress unless it closes a stated obligation. Exact, proved-under-hypotheses, symbolically verified, numerically measured, proposed and unresolved are separate statuses. An unavailable CAS backend or exhausted budget is not a mathematical obstruction. The work should remain explainable and defensible by its author; an eight-minute defence cannot substitute volume for a clear claim and its evidence.

## 6. Build and verification

The canonical manuscript is `draft/dissertation_wku.tex`; `draft/main.tex` and `draft/dissertation.tex` are compatibility entry points for the same document. Compile from inside `draft/` so the cover assets resolve:

```bash
cd draft
latexmk -pdf -interaction=nonstopmode -halt-on-error dissertation_wku.tex
# Alternatively run pdflatex three times.
python verify_coefficients.py  # requires SymPy; exact algebra only
```

The prepared PDF was compiled and visually checked: 51 A4 pages, no compilation warnings or unresolved references. The [preservation record](draft/preservation_check.json) checks the entire body after explicit layout normalization, 17 theorem/proof environments, 93 existing label numbers, the chapter sequence and embedded numerical plot tables. This synchronization preserves the prepared source/PDF bytes and does not rerun training or claim a fresh full repository test pass.

The repository's existing validation commands remain available for a separate code/evidence validation cycle, with new output directories and restored evidence as needed:

```bash
python -X utf8 scripts/project.py audit
python -X utf8 scripts/project.py data-flux --out build/data-flux-NEW
python -X utf8 scripts/project.py workflow --out build/workflow-NEW
python -B -X utf8 -m pytest -q -p no:cacheprovider symm/tests/test_engine.py symm/tests/test_chart_reduction.py research_artifacts/sve-progress-20261010/tests
```

See [validation and legacy limitations](docs/validation.md), [archive restoration](docs/build-archive-20261021.md), the [historical project map](docs/project-map.md), and the [27 October strict follow-up](research_artifacts/sve-final-20261027/README.md). Dated documents and receipts retain their original conclusions; they do not describe newly completed November experiments. Earlier manuscript copies are accessible in the `.old` snapshot rather than competing with the canonical source.

## 7. Source basis and next obligations

This synthesis uses the current dissertation §§1.2–1.3, Chapters 2–6 and Appendices A–C; the project's dated maps and experiment index; and the user's earlier questions about multi-parameter SVE, continuous generators, noncommutativity, physical derivation, fractional/fractal dimension, singular series, transverse correction and falsifiability. Earlier alternative question lists are historical context, not replacements for the current frozen settings.

Primary mathematical references remain Olver's *Applications of Lie Groups to Differential Equations* and Oliveri's *Lie Symmetries of Differential Equations: Theory, Applications, and Symbolic Computation*. The dissertation bibliography records the physical SVE derivation, invariant-solution, approximation and singular-ODE sources used for individual claims. No new literature priority claim is made by this README.

The outstanding obligations are concrete: complete the declared parameter/determining-system analysis where still open; construct and verify the missing continuous correction hypotheses and singular charts for a specified target; and run a properly matched, amortized-cost comparison only when its analytical and model prerequisites are ready. The broader exploratory questions above remain recorded without changing the dissertation's frozen model or promising a universal PDE solver.
