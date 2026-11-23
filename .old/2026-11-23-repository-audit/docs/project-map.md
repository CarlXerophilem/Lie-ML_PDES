# Project Map: 21 October 2026

**27 October update:** the active strict CAS/Python follow-up, native Priestess
retries, five-chapter dissertation and success/failure analysis are indexed in
[the final follow-up carrier](../research_artifacts/sve-final-20261027/README.md).
Its mathematical status is incomplete. The dated evidence below remains
historical and unchanged; its outline-only writing scope is superseded.

The current research route is source-faithful reproduction and extension of
the 2026 printed scalar SVE paper, then controlled full SV+bed changes and a
frozen baseline, then source-verified open 2D questions. The broader baseline
and learning programme remains incomplete. The current user request is the
completed [dissertation](../draft/dissertation.tex), superseding the earlier
[outline-only plan](superpowers/plans/2026-10-21-dissertation-writing.md).

## Current Dissertation Cycle

- [Run and scope](../build/dissertation-completion-20261026/RUN.md),
  [physical sources](../build/dissertation-completion-20261026/PHYSICAL-SOURCES.md),
  [historical benchmark audit](../build/dissertation-completion-20261026/BENCHMARK-AUDIT.md)
  and [independent review](../build/dissertation-completion-20261026/REVIEW.md).
- [New annular full-E target](../symm/LieSymm/annular2d.py): isotropic cubic
  transport, positive downslope diffusion and constant Coriolis forcing;
  six supplied verified generators, prolonged tangency, brackets, rank-two
  invariant reduction, three first integrals and sampled reconstruction.
  This is not a maximal symmetry classification or a physical validation.
- [Exact-interface checks](../scripts/verify_dissertation_interfaces.py):
  redundant invariant-graph penalties, first-integral identities, restricted
  constitutive homogeneity, diffusion sign, characteristic determinant and
  smooth non-shock control. Pure PINN remains stopped; 2D ML comparisons
  are proposed, not executed.

## Models And Accepted Scope

| Object | Current evidence | Limits / next operation |
|---|---|---|
| Printed scalar P | 18 registered families; 12/12 exact, 21/21 seed and 11/11 high-precision-reference extended IVPs | Frozen float64 campaign stays 10/11; regular scaling/mixed closed forms and singular continuation remain recorded open branches |
| Full Eulerian SV+bed E | 8 declared 1D and 17 declared 2D local point-algebra cells; 17 registered traveling/scaling reductions in the separate 1D programme | Read the certificate's model/chart/ansatz scope; not every reduction or nonlinear solution; optimal-subalgebra completeness and full equivalence groupoid remain open |
| Advectively corrected scalar M | Common-scaling first integral and local material reconstruction | Check currents, exceptional branches and further reductions independently |

No P/E/M equivalence is assumed. State positive-branch/chart assumptions,
nonzero denominators, parameter strata and compatible data. Independent-variable
reduction is not ODE-order reduction. A verified generator, finite search or
registered catalogue does not prove a maximal/global PDE classification.

The 20 October nonclassical campaign has 64 candidate certificates: 11 full-chart
passes, 2 requiring u!=0 and 51 failures, with no new classically inequivalent
solution family. See its [delivery](../build/sve-general-symm-20261020/DELIVERY.md).
Pure PINN is stopped; [conditional hybrid ideas](../research_artifacts/sve-1d-programme-20261021/ML_DECISION.md)
need an unmet task and measured added value. The PINN/KAN benchmark
arXiv:2602.15068v1 is a prospective protocol reference, not an SVE result.

## Current Evidence Index

| Entry | What it establishes |
|---|---|
| [Precision follow-up](residual-resolution-20261021.md), [delivery](../build/sve-P-residual-20261021/DELIVERY.md), [demo](../build/sve-P-residual-20261021/campaign-reviewed/index.html) | Independent 40-digit reference resolves the third-derivative noise floor at unchanged 1e-6 gate; raw float64 failure is preserved |
| [New precision carrier](../research_artifacts/sve-P-residual-20261021/README.md) | 401-file portable follow-up; source baseline 11fe2a8 |
| [Frozen P delivery](../build/sve-P-solutions-20261021/DELIVERY.md), [three delivery carriers](../research_artifacts/sve-delivery-20261021/README.md) | Earlier 10/11 campaign, library receipts, exact/series/numerical/unresolved records |
| [Portable current snapshot](../research_artifacts/sve-current-20261021/README.md) | 19/20 October evidence and retained dissertation build/week-4 inputs |
| [Solution API](../symm/LieSymm/scalar2026/SOLUTIONS.md), [library](../symm/LieSymm/README.md), [source audit/demo](../symm/LieSymm/scalar2026/README.md) | All nine source subsections processed; printed failures and corrected P pullbacks kept distinct |
| [E-focused 1D programme](../research_artifacts/sve-1d-programme-20261021/README.md), [reduction inventory](../research_artifacts/sve-1d-programme-20261021/REDUCTION_INVENTORY.md), [plan](../research_artifacts/sve-1d-programme-20261021/PLAN.md) | Separate declared E branches, domains and pending solve status |
| [Retained scalar experiment index](../research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md) | 43-test benchmark, classical/approximation outcomes and negative results |
| [12 October source reproduction](../research_artifacts/SVE-reproduced-20261012/README.md) | Printed-versus-verified audit; original scalar replay uses the dated recovery adapter |

The precision reference residual is 2.212490569e-8 at h=.003 and
2.976602120e-11 at h=.001. Agreement at output nodes and sampled residuals do
not prove a continuous error bound for float64 interpolants. Bare pytest has
separate legacy collection defects; selected passing suites are not a global pass.

## Workflow, Writing And Remote Use

- [Root commands](../README.md): integrity, focused tests, audit, data-flux, workflow and native Windows latexmk.
- [Three-stage research roadmap](research-roadmap-20261021.md): future acceptance conditions.
- [Approved P-solution plan](superpowers/plans/2026-10-21-sve-printed-solutions.md): completed cycle's declared scope.
- [Writing plan](superpowers/plans/2026-10-21-dissertation-writing.md): provisional title, outline and source-question-evidence map; completed results separated from future work.
- [Priestess handoff](priestess-handoff.md): clean astra sync, hash-checked restoration, Python environment and Windows-only compilation boundary.
- [Validation](validation.md), [documentation index](README.md), [reference guide](../ref/README.md).

The [manuscript](../draft/main.tex) remains unchanged by the current writing
cycle. The completed dissertation instead uses the retained scalar precision
surface and the fresh annular profile under build/dissertation-completion-20261026.
Older build/week-4 inputs stay retained for their historical dependants.

## Historical Packages And Search Scope

The absent 11 October external archive is a nonblocking legacy-provenance note,
not a current acceptance gate. Its failed historical receipt is unchanged.
See the [build archive guide](build-archive-20261021.md) and [archive policy](archive.md).

Eight older packages are represented by restore stubs, not live deep links:
[mathematics and symmetries](../research_artifacts/mathematics-and-symmetries/ARCHIVED.md),
[fluid baseline](../research_artifacts/fluid-baseline-20260925/ARCHIVED.md),
[free-boundary inspection](../research_artifacts/free-boundary-scope-inspection-20261014/ARCHIVED.md),
[live simulation](../research_artifacts/live-simulation-20260925/ARCHIVED.md),
[three-layer baselines](../research_artifacts/three-layer-baselines-20260927/ARCHIVED.md),
[pilot](../research_artifacts/pilot/ARCHIVED.md),
[title inspection](../research_artifacts/dissertation-title-inspection-20261014/ARCHIVED.md),
[near-cubic P0](../research_artifacts/p0-near-cubic-20261007/ARCHIVED.md).
Their ZIPs and root-history.zip are in research_artifacts/archives-20261021.
Current reproduction, 2D extension, scalar benchmark, 1D programme and delivery
packages stay expanded; frozen carriers remain immutable.

`.ignore` narrows default ripgrep discovery only. To navigate intentionally:

```bash
rg --no-ignore --files ref
rg --no-ignore -n --glob '*.md' 'failed|unresolved' research_artifacts/sve-1d-programme-20261021
rg --no-ignore --files research_artifacts/archives-20261021
rg --no-ignore -n 'source_sha256' symm/LieSymm/_snapshot/cases
```

For detailed historical theory and workflow diagrams, use the
[methodology map through 19 October](methodology-map-through-20261019.md).
