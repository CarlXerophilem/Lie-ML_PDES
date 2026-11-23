# 2D SVE extension: initial research contract

Date: 2026-10-14 (Asia/Tokyo). Status: initial extension completed and reviewed.

## Objective and deliverables

Start a source-verified extension of the existing 1D research to the coupled
two-horizontal-dimensional Eulerian Saint--Venant--Exner system. Deliver a
readable derivation, reproducible symbolic calculation, a small constructed
classical numerical example, source provenance, independent review, and
validation receipts in this new directory. Preserve the uploaded context.

## Frozen initial scope

Use constant g>0, transport coefficient kappa>0, and porosity 0<=p<1;
retain the evolving bed and its slope force, omit friction and external
forcing, and use the isotropic Grass law q=kappa |(u,v)|^(m-1)(u,v).
The source researcher must verify this specialization against readable primary
equations before it is called source-grounded. Work with smooth solutions,
h>0, and speed>0 for arbitrary real exponents; handle the cubic polynomial
extension to zero speed separately. Verify candidate point generators,
derive the diagonal-scaling parameter condition, and construct a rotation
quotient on r>0. A further cubic scaling reduction may supply an ODE example.

Success requires exact checks against the original equations, declared chart
and parameter restrictions, explicit source-to-model mappings, and a fresh
review. Source statements and new derived calculations must remain distinct.

## Non-claims

No maximal point-symmetry classification; no automatic transfer of the 1D
printed scalar classification; no theorem of generic 2D well-posedness,
arbitrary initial/boundary data, global continuation, shock behavior, or ML
benefit; no publication novelty claim from this bounded source search.

## Authorization and resources

Local writes: this directory and build/sve-2d-extension-20261014 only.
Existing manuscripts, moved reference files, frozen ZIPs/manifests and other
concurrent changes are preserved. Public read-only source retrieval is allowed;
no paid services, external publication, library mutation, or commits.
No user deadline, hard token cap or monetary budget was supplied.
Operational limits: up to five primary papers, citation depth at most one,
network timeout 45 seconds with at most one transient retry; one CPU-heavy
calculation at a time, thread cap one, individual calculation/test timeout
600 seconds. These are local execution bounds, not a user-imposed budget.
Reserve a separate fresh-context review after research, with at most one
material repair round before narrowing any unresolved claims.

## Task DAG and ownership

1. `sources`: independent text/light research; verify 2D equations and closure,
   plus the uploaded ill-posedness reference; owns sources/ and SOURCE_AUDIT.md.
2. `derivation`: independent text/light calculation; derive rotation and
   diagonal-scaling reductions; owns DERIVATION_RESEARCH.md only.
3. `computation`: controller owns main.py, tests, results, report and README;
   depends on model provenance, uses one named CPU lease.
4. `fresh-review`: new isolated reviewer; depends on normalized source and
   computation records; returns accepted/qualified/rejected claim verdicts.
5. `release`: controller writes only reviewed claims, runs required project
   checks and native LaTeX/visual checks, then records manifest and limitations.

Durable ledger: RESEARCH_LEDGER.json. Agent output is evidence-ready, never
self-approved. Missing sources, timeouts and failures retain explicit statuses.

Delegation is useful because primary-source verification and independent
mathematical derivation can proceed without shared writable state; review is
reserved for a fresh context after both have finished.
