# Independent review of data experiments and parent-model controls

Reviewer: first-order researcher, acting only as an independent reviewer of
`data_experiments.py` and `parent_models.py`. This review does **not** approve
the reviewer's own first-order maximality proof. The already integrated
coefficients are inputs to the data-stabilizer checks; their completeness is
the responsibility of the separate classification review.

## Current disposition

**Accepted for the stated data/parent-control scope.** The final independent
review passed **171/171 exact checks in 2.98 seconds**, under a 60-second
per-process timeout. There are no unresolved review qualifications on the
reviewed hashes. This acceptance does not expand the claim scope stated
below or substitute for the separate classification review.

| Reviewed artifact | Final SHA256 |
|---|---|
| `data_experiments.py` | `8dbc763cc9780afa13d4c997e972b34f5f4a6e648fca11c1b2b7d269f4245989` |
| `parent_models.py` | `cf4d4d59239b95d116c1cfb3c766aa40d2afbf052a337956abc36cf8c986f7c7` |
| `review_data_parent.py` | `013ff36427095873e6cb821e7be63792a8eb1fdf270af46f8260266399ce1257` |
| prior source ledger | `b95ec52815d182ff8c8e9fed7e48b7f6d084e6bdebd853aa4a47fdd72c49f27c` |

## Rejected first pass and verified repair

The first review run completed 168 exact checks in 2.93 seconds: 167 passed,
one failed. The original mathematical controls passed. The failure concerns
input validation and certification scope:

```python
uniform_flow('grass_generic', substitutions={g: sympy.I})
```

returned `verified_exact_solution` while its report still claimed the
positive-real `g>0` parameter domain. Its constant graph has zero formal PDE
residuals, but that does not make the supplied parameter admissible.
`_context` rejected known nonpositive replacements but did not reject known
nonreal replacements. Separately, substituting a real symbolic parameter
`r` for `g` retained only the text `g>0`; the required condition `r>0` must be
explicitly attached to the result. This is an API guard-provenance issue;
the default constructed controls and accepted positive numeric parameters
were unaffected.

The failed data-module SHA256 was
`4cf6aab29ee134e8717676e545913013a3fc041d3265621eee705ccb7a8db02c`.
The unchanged reviewed parent-module SHA256 was
`cf4d4d59239b95d116c1cfb3c766aa40d2afbf052a337956abc36cf8c986f7c7`.
The failed receipt is preserved at
`runs/review_data_parent_initial_failure.json`. The root agent repaired the
data module; this reviewer made no edits to either reviewed file.

The repaired parameter checker rejects known nonreal, nonfinite, and
coordinate-dependent substitutions. It specializes the actual domain
conditions and records the substitution map. Fresh review checks confirm
rejection of `g=I`, `K=I`, and `G=I`, alongside the original contradictory
numeric exponent/coefficient cases. For a symbolic replacement `g=r`, the
report now explicitly carries `r>0`. The same provenance is present in
standalone flux and zero-speed lake reports; the reviewer explicitly checks
the lake case `G=r,n=0`. The repair preserves the already passing physical
and mathematical controls.

## Mathematical findings

1. **Exact flows accepted.** All eight registered 1D cells admit the checked
   uniform states and constant-slope accelerating states
   \(h=H, u=U-gk(t-t_0), B=kx+B_0\), restricted to positive depth and velocity.
   The independent oracle directly differentiates the three original PDEs;
   it does not call the shared `graph_check` or reuse a prolonged residual.
   The sediment flux may vary in time, while its spatial derivative is zero.

2. **Specified initial stabilizers accepted.** For constant positive depth
   and velocity, flat, nonzero-linear, and quadratic initial beds yield the
   independently expected dimensions. Their computed coefficient fields are
   substituted into \(\tau|_{t_0}=0\) and
   \(\eta_i-\xi U'_{0,i}=0\). Two fixed endpoints remove the remaining
   uniform-data base motions. These are initial-graph stabilizers, not
   existence results or stabilizers of unspecified future boundary traces.
   The frozen-profile diagnostic is kept separate from evolving solutions.

3. **Parameter rank guards accepted.** An unspecified linear-bed slope
   retains its nonzero pivot guard and the unresolved zero-slope branch;
   the separately evaluated zero-slope profile has the predicted larger
   stabilizer. The slope-only data \((x^2,x,x^2)\), on a positive chart,
   retain the exponent rank guard; direct specialization to \(n=2\) recovers
   its one-dimensional stabilizer. These tests do not replace a generic
   classification proof.

4. **Flux prolongation accepted.** For
   \(\tau=Tt,\xi=Xx,\eta_u=Vu,\eta_B=WB\), the independently derived result is
   \[
   \operatorname{pr}X(J)=mVK u^m
      -G(nV+W-X)u^nB_x.
   \]
   The code agrees on every registered branch. A separate tilted-time
   coefficient \(\tau=x\) verifies the otherwise easy-to-omit
   \(-B_tD_x\tau\) term in \(\eta_{B_x}\). Incompatible prescribed initial
   flux is rejected. Time-dependent prescribed fluxes are checked only on
   the initial slice, as the report explicitly states.

5. **Zero-speed extension accepted within its declared restriction.** The
   admitted signed closures are polynomial only for transport exponents
   \(m=1,3\) and active diffusivity exponents \(n=0,2,4\) in the stated
   ranges. Other exponents remain outside this extension. For \(n=0\), a
   static quadratic lake has bed residual \(-2G\), while the paired moving
   bed and level \(B=x^2+2Gt\), \(L=L_0+2Gt\) have zero residuals and fixed
   depth \(L_0-x^2\). The reports do not extend the positive-speed maximal
   algebra to zero speed.

6. **P/M separation and material signs accepted.** With
   \(q=\phi_s>0,v=\phi_t>0\),
   \[
   D_x=q^{-1}\partial_s,\qquad
   D_t|_x=\partial_t-(v/q)\partial_s.
   \]
   The original momentum equation gives \(B_s=-A/g\); the original Exner
   equation gives \(B_t=-vA/(gq)-C\), not merely \(-C\). Closedness therefore
   gives \(M=P-\partial_s(vA/q)\). The relative material conservation law
   \((qB)_t+(Kv^m-vB)_s=0\) has the correct negative transport sign.
   The explicit \(\phi=s^2/2+ct\) counterexample gives \(P=0\) and
   \(M=-3gc/s^4\ne0\) on \(s,c,g>0\). The constant-slope mass label has
   \(s_x=H>0,s_t=-Hu\), inverse Jacobian \(\phi_s=1/H\), and the missing
   printed material bed-time term is exactly \(ku\). These controls are
   explicitly restricted to \(G=0\), with no asserted point equivalence
   between a scalar model and the three-field system.

7. **Source-byte audit accepted.** All six required source IDs
   `R01,R02,R03,R04,R07,R08` are present and their local hashes match the
   prior source ledger. The repaired parent receipt explicitly checks the
   required-ID set, avoiding vacuous acceptance of an empty selection.
   This is current local-byte verification of earlier primary-source
   retrieval, not new web retrieval or a fresh bibliographic-content audit.

## Reproduction and evidence

Run the independent reviewer with a hard per-process timeout:

```powershell
python -c "import subprocess; subprocess.run(['python','-B','build/sve-general-symm-20261020/review_data_parent.py'], timeout=60, check=True)"
```

`review_data_parent_results.json` contains every check, exact
source/dependency hash, and elapsed time. It has `review_status=accepted`
and an empty qualifications list. The first failed receipt remains at the
path recorded above; it was not erased by the repair run.
The checker does not call the original first-order proof verifier, does not
approve that proof, and performs no 2D work.
