# Bounded prior-art review: symbolic Lie symmetry and reduction software

**Cutoff and scope.** Public, read-only retrieval was performed on 21 October
2026 (Asia/Tokyo; receipts use UTC). The retained set is eight implementations
or documented systems: one Python, five Maple, one REDUCE, and one MATLAB.
GitHub, GitLab, PyPI, Crossref, OpenAlex, arXiv, author-hosted software, and
vendor documentation were queried. This is a bounded engineering comparison,
not a systematic review and not evidence that unlocated code does not exist.
No external code was copied into `symm/LieSymm`.

The local comparison target is
`build/sve-general-symm-20261020/main.py`, SHA-256
`44b894144cb9006569dfb85e3404c1e6e952274012b4f78f032f3ae28fd22b82`.
It builds dynamic multi-field jets, computes point prolongations by both
characteristic and recursive formulas, solves a time-leading evolution shell,
and splits a rational numerator as a polynomial in free jets. It correctly
returns `unresolved_nonpolynomial_jet_identity` when `sympy.Poly` rejects the
identity. Its separate `generalized_power_terms` helper records exponent
collisions, but is not wired into `analyze`. These facts are implementation
scope, not a maximal-classification claim.

## Retained evidence

| System | Pin and license | Inspected scope | Relevance to the local engine |
|---|---|---|---|
| [**SymPy `lie_group`**](https://github.com/sympy/sympy/blob/b386392cd62ed543aadd696d9953ab35cb38d666/sympy/solvers/ode/lie_group.py) (Python) | `sympy/sympy@b386392cd62ed543aadd696d9953ab35cb38d666`; BSD-style SymPy license | `sympy/solvers/ode/lie_group.py`; only first-order scalar ODEs. It uses heuristic infinitesimal ansatze, numerator/denominator cancellation, bounded polynomial ansatze, coefficient dictionaries, `pdsolve`, and canonical-coordinate reduction. | A useful control for staged heuristics and delayed `cancel`/`expand`; **not a PDE-system comparator**. Its own API rejects more than one independent variable and orders other than one. |
| [**dpack 0.1.0.1**](https://github.com/juergenboehm/dpack/tree/46bee3a33f8b6c0ba3c4938c89117c7c8e84c4ab) (Maple) | `juergenboehm/dpack@46bee3a33f8b6c0ba3c4938c89117c7c8e84c4ab`; copyright/no-warranty notice but no permission grant, so `license=unknown` | `dprolong`, `dsymm`, `dlie`, and help pages. It constructs prolongations, solves equations for leading jets, substitutes on-shell, takes a normalized numerator, converts to rational form, then uses distributed `collect`/`coeffs`. It also contains Janet-basis/LPDE machinery. | Direct PDE /\determining-system comparator. It confirms the local prolong-on-shell-split pipeline, but its explicit rationalization and Janet/differential-system tools go beyond the local integrator. Maple 8 and sparse documentation are material limitations. |
| [**ReLie**](https://mat521.unime.it/~francesco/relie.php) (REDUCE) | Author ZIP retrieved from `mat521.unime.it`; SHA-256 `2d78465b8a76ea01c9c48794b33e7dfb5e32c941806708866f16c0ead464419e`; no explicit software license found, so `license=unknown` | `relie.red` (SHA-256 `0f6c8e529831e4918a70f8357d236ffec754aa825080083b72764e9da867c85e`). It declares `leadders`, clears denominators, extracts coefficients recursively, accepts `nonpolyders`, removes those jets from coefficient splitting, and passes them as auxiliary variables to CRACK. | Strongest algorithm lead for the local nonpolynomial gap. It shows a conservative representation: declared nonpolynomial jets are not falsely split as polynomial indeterminates. ReLie also delegates overdetermined determining systems to CRACK rather than one monolithic solve. REDUCE is out of implementation language and the ZIP has no commit history. |
| [**SADE**](https://arxiv.org/abs/1004.3339v2) (Maple) | arXiv `1004.3339v2`, DOI [`10.1016/j.cpc.2010.09.021`](https://doi.org/10.1016/j.cpc.2010.09.021); paper PDF SHA-256 `24cd00fefbb8988136151be01d94fe4f1254509ad4161f8f228583c2c5c2e81d`; software license not stated in the inspected paper | Paper Sections 2--4, especially PDF pp. 15--17, describe orthonomic reduction, splitting by independent derivative functions, an 18-step staged solver, selective `rifsimp`/modified Kolchin-Ritt involutive reduction, parameter controls, invariant solutions, and PDE/ODE reduction. | Direct PDE architecture evidence. The key lesson is to simplify/triage small equations before expensive involutive completion and to return unresolved systems when progress stops. The package source itself was not located in a public versioned repository, so this is paper evidence, not a source-code review. |
| [**Maple `PDEtools`**](https://www.maplesoft.com/support/help/Maple/view.aspx?path=PDEtools%2FInfinitesimals) | Current public Maplesoft help pages; proprietary Maple, source unavailable | `Infinitesimals` documents ODE/PDE-system infinitesimal computation; [`InvariantSolutions`](https://www.maplesoft.com/support/help/Maple/view.aspx?path=PDEtools%2FInvariantSolutions) documents group-invariant PDE solutions; [`casesplit`](https://www.maplesoft.com/support/help/Maple/view.aspx?path=PDEtools%2Fcasesplit) documents case splitting with integrability conditions. | Confirms that case splitting and integrability closure are first-class operations in a mature PDE workflow. Public help does not expose internal algorithms, versioned source, or a reusable license. |
| [**Lie-Symmetries**](https://github.com/GemmaMasFes6/Lie-Symmetries/tree/ad8f76e1a0ad4c7973956cae966d13ca1439503e) (MATLAB) | `GemmaMasFes6/Lie-Symmetries@ad8f76e1a0ad4c7973956cae966d13ca1439503e`; GPL-3.0 | `Lie_Symmetry.m` handles rational ODE biological models, chooses a degree-bounded polynomial infinitesimal ansatz, separates numerators/denominators, extracts polynomial coefficients, and computes a matrix nullspace. | Useful for an optional **bounded ansatz backend** and sparse linear-algebra formulation, not for complete PDE classification. Its scope is rational ODE models and structural identifiability/observability; GPL code must not be copied into a differently licensed package without a deliberate licensing decision. |
| [**GeM**](https://doi.org/10.1016/j.cpc.2006.08.001) (Maple) | DOI `10.1016/j.cpc.2006.08.001`; Crossref/OpenAlex identity confirmed; source/license unverified | The paper record identifies a Maple package for symmetries and conservation laws. The likely University of Saskatchewan site failed TLS/HTTP retrieval in this environment; OpenAlex reported no open full text. | Retained as a scope comparator only. No implementation-level claim is based on it, and no code adoption is permitted from this review. |
| [**DESOLV**](https://doi.org/10.1016/j.cpc.2007.03.005) (Maple) | DOI `10.1016/j.cpc.2007.03.005`; Crossref/OpenAlex identity confirmed; source/license unverified | The paper record identifies similarity reduction of PDEs using DESOLV. OpenAlex reported no open full text. SADE's paper names DESOLV as a Maple comparator and reports benchmark observations, which were not independently rerun here. | Retained because automatic similarity reduction is directly relevant, but it supplies no inspected algorithm or reusable code in this review. |

## What overlaps, and what remains local

The common core is not novel by itself: generate a prolonged point field,
restrict it to the equation manifold by eliminating leading derivatives, and
split the remaining identity over independent jets. That pipeline is visible
in dpack, ReLie, SADE, and the Maple documentation, while SymPy implements its
first-order ODE specialization.

The defensible local contribution is narrower: a small, readable Python engine
with dynamic multi-field jets, two independently coded prolongation paths,
explicit branch/divisor receipts, fail-closed nonpolynomial status, and
SVE-specific integration and certificate checks. The bounded search did not
locate a mature, licensed Python PDE-system package with that exact combination.
That is **not** a claim that none exists, nor a claim of algorithmic novelty over
the older CAS packages.

## Recommended symbolic improvements

1. **Add a declared leader/nonpolynomial contract before broadening splitting.**
   Let a model specify leading jets, nonpolynomial jets, positivity/chart
   assumptions, and nonzero divisors. Follow ReLie's conservative idea:
   exclude declared nonpolynomial jets from `Poly` splitting and retain them as
   auxiliary variables. Only invoke generalized-power independence after a
   positive-chart proof and after emitting all exponent-collision strata. Risk:
   treating arbitrary functions or resonant powers as independent creates false
   determining equations; therefore unsupported cases must stay unresolved.

2. **Replace `matrix.inv() * rhs` with fraction-free or solve-based shell
   elimination and record every pivot.** `inv()` expands all entries and hides
   where pivots were divided out. Use `solve_linear_system`/fraction-free
   elimination or a sparse domain matrix when expressions are polynomial, with
   explicit branches for zero pivots. Risk: a generic pivot order can be much
   worse than the present small SVE matrix, so keep the existing path as a
   measured fallback until benchmarks show improvement.

3. **Build a sparse coefficient map instead of unconditional global
   `expand`.** Accumulate monomial-to-coefficient mappings during prolongation
   and shell substitution, normalize each final coefficient once, and preserve
   the unsimplified expression plus denominator receipt. SymPy's bivariate
   heuristic, dpack's distributed `collect`, and MATLAB's coefficient-matrix
   construction all support this direction. Risk: SymPy expressions with
   algebraic/transcendental factors may not share a single polynomial domain;
   detect domain failure and return the original identity.

4. **Separate derivation from determining-system integration.** Add a staged
   solver ledger: algebraic substitutions and two-term equations first,
   dependency analysis next, optional bounded `rifsimp`/differential
   elimination last. SADE explicitly warns that full involutive reduction is
   expensive; ReLie exposes CRACK progress. Risk: a partial solver can silently
   look complete, so each stage must return `solved`, `residual_system`, and
   `conditions`, with maximality remaining unresolved unless independently
   proved.

5. **Offer bounded polynomial ansatze as a separate heuristic backend.** The
   SymPy and MATLAB implementations show the practical value of degree-bounded
   ansatze and linear nullspaces. Label the result `ansatz_complete_at_degree_d`,
   never `complete_classification`, and verify every candidate using the local
   recursive prolongation path. Risk: basis size grows combinatorially and a
   failed degree bound is not an obstruction proof.

Priority is 1, then 4, then 3. The first change closes a capability gap while
preserving the current conservative unresolved status and adding explicit proof
obligations; the second makes unresolved determining systems auditable; the
third targets cost.
No prior-art source should be adopted until its license is explicitly compatible.

## Negative and limited results

- PyPI returned HTTP 404 for `LieSymm`, `symmetries`, `lie-symmetry`, and
  `lie-symmetry-toolkit`. GitHub repository search returned zero exact
  `LieSymm` Python repositories. The located
  `sinuvasan/lie_symmetry_toolkit@041aa3f...` is an in-progress ODE tutorial:
  its README says PDE generalization and reduction have not started, and it has
  no license file. `JimmyBroomfield/LieTheorySym@6caa022...` is a 2017
  prototype with no license and no mature package surface. Neither is retained
  as reusable prior art.
- The Dimas/Tsoubelis `SYM` lead was not retained because the bounded primary
  searches did not resolve a versioned public source and the system is described
  in secondary literature as Mathematica, not MATLAB. This is `not_found`, not
  evidence of nonexistence.
- GitLab API queries were explicit. `Lie symmetry PDE` and `SADE Maple`
  returned HTTP 200 with `[]`; `LieSymm` returned HTTP 500. The failure is
  recorded as `unreachable`, not a negative search result.
- No Maple, MATLAB, or REDUCE runtime was invoked. Historical
  benchmark timings and correctness claims were not reproduced. Paper and
  vendor statements are labeled as such in `prior_art_sources.json`.

Machine-readable provenance, exact URLs, hashes, relevant files, and retrieval
outcomes are in `prior_art_sources.json`; downloaded evidence is under
`sources/prior-art/`.
