# SDD progress ledger — LieML symmetry engine v1

Plan: docs/superpowers/plans/2026-06-26-lie-symmetry-engine-v1.md
(Not a git repo; tasks tracked here + by the test suite.)

- Task 1: jet/prolongation layer — COMPLETE (4 tests pass; fixed leading-time-derivative/free_jet_syms inconsistency). MINOR for final review: `_init_onshell` takes `sol[0]` without a uniqueness guard.
- Task 2: determining matrix — COMPLETE (6 tests pass; Burgers nullity=5; controller-verified, low-risk transcription).
- Task 3: iterative elimination — COMPLETE (10 tests pass; CRITICAL bug found+fixed: stabilization kept basis/coeffs from wrong degree -> wrong generators; added real-symmetry regression gate).
- Task 4: algebra (dim/type) — COMPLETE (13 tests pass; corrected derived-series shipped; solvable=False gate validates it; closure confirms generators consistent).
- Task 5: reduction (residual-0 ODE) — COMPLETE (17 tests pass; clean travelling-wave branch; fixed latent scaling-guard bug: required a,b,e constant so projective gen returns None before engine uses it).
- Task 6: checkpoint/resume — COMPLETE (20 tests pass; exact srepr round-trip; cleaned dead-code in decode).
- Task 7: numerical cross-check — COMPLETE (21 tests pass; SVD nullity==exact dim==5).
- Task 8: reducibility (defect/index) — COMPLETE (23 tests pass).
- Task 9: engine orchestrator — COMPLETE (26 tests pass; full review: Spec OK/Quality Approved; real resume via result.json; strengthened resume test to 5/9 fields). MINOR for final review: _load_record swallows exceptions; no Dmin/Dmax/d_star-change guard on resume; _jsonify demotes Rational->float (harmless today).
- Task 10: report + interfaces — COMPLETE (29 tests pass; no-secret-leak test green; de-vacuumed ranker test).
- Task 11: CLI + shim — COMPLETE (32 tests pass; CLI runs Burgers->CERTIFIED).
- Task 12: M1 acceptance + guide — COMPLETE (36 tests pass; M1 gate green: Burgers dim5 CERTIFIED, porous dim3, neg-control rejected, resume bit-identical; guide has real trace).

ALL 12 TASKS COMPLETE + FINAL REVIEW FIXES APPLIED. 37 tests pass.

Final opus whole-branch review: no Critical; 3 Important (I1 Barenblatt residual mislabeled, I2 metric-label mismatch, I3 resume granularity) — ALL FIXED:
- I1: reduce.py scaling branch now strips common (x,t) monomial -> porous Barenblatt residual==0 (new test test_porous_scaling_reduction_residual_zero).
- I2: params_tuple W_V relabeled "column-normalized" to match defect().
- I3: engine resume = whole-record cache (result.json) + deterministic recompute, with d_star cache-invalidation guard + corrupt-record warning; test_resume_is_identical now exercises delete+recompute. Spec section 5 wording aligned + recompiled. Granular per-degree resume deferred (degrees cheap).

Accepted-for-v1 minors (for any future hardening): jet._init_onshell sol[0] no uniqueness guard; algebra_type has no explicit semisimple flag; structure-constant array not stored in record signature.

DELIVERABLES: symm/sym_engine/ package (12 modules) + sym_engine_cli.py + symmetry_engine.py shim + 12 test files (37 tests) + GUIDE_zero_to_one.md; spec .tex/.pdf; plan .md; article draft/draft.tex/.pdf.

=== v1.1 LEARNED REDUCTOR (in progress) ===
Decisions: foundation-first; taxonomy-oriented (linear/nonlinear, inf-dim/fin-dim). Engine self-labels (no external training set). Reductor = fast prioritizer for group-classification sweeps; engine always verifies. (Littlewood thread dropped per user; "sparser" style noted.)
- PDE generator — symm/reductor/generator.py (sample_pde / featurize / label_pde / build_corpus over a 12-term dictionary). DONE.
- Engine fuzz invariant locked — symm/tests/test_generator_fuzz.py: every discovered generator has residual==0 and numeric==exact dim, over 12 random PDEs. Full suite now 38 tests pass.
- Corpus — symm/reductor/corpus_v1.json (200 PDEs, 0 errors, seed 0, Dmax=3).
- Separability study (200 PDEs): inf/fin 1-NN 0.92 vs majority 0.885; dim 1-NN 0.685(all)/0.757(fin) vs majority 0.535/0.605. ML beats baselines but modestly.
  Findings: (a) linearity is NOT a perfect fin/inf proxy (~8% nonlinear PDEs have large/growing algebras); the wobble is the growth-heuristic LABEL, not the features. (b) dim signal is capped by PRESENCE-only features (they ignore coefficient values, which set special-case dims).
- Levers TESTED — both duds (honest negative): coefficient features HURT (dim 1-NN 0.685->0.395, below majority) => reducibility here is coefficient-invariant / structure-determined; `stalled` relabel = no change (same 23/177 split). Reverted featurize to PRESENCE; canonical corpus_v1.json rebuilt (200/200, presence + stalled labels).
  Real ceiling = presence 1-NN ~0.69(all)/0.76(fin) vs majority 0.54/0.61. The cap is TERM-INTERACTIONS the flat flags don't encode, NOT missing features.
- Interaction learner + honest-protocol harness — symm/reductor/train_reductor.py (numpy-only CART, deterministic LOOCV) + pinned regression test symm/tests/test_train_reductor.py. Suite now 40 tests pass.
  (a) AUDIT: 200 rows = 187 distinct structures; duplicate leakage was inflating row-LOOCV (1-NN dim 0.685 -> honest structure-LOOCV 0.591; klass 0.920 -> 0.871, now BELOW majority 0.898).
  (b) TREE WINS on dim under the honest protocol: depth-3 CART 0.747(all)/0.832(fin) vs 1-NN 0.591/0.707 vs majority 0.543/0.605. Depth curve reported (d=3 pre-registered headline).
  (c) SAFETY GATE FAILED by the dim-tree: recall on dim>=4 is 0.000 (buries every rich PDE); 1-NN recall 0.833. Fix = train the TRIAGE target directly: binary (dim>=4) depth-3 tree gets acc 0.892 / recall 0.792 / precision 0.559 (vs majority 0.871, 1-NN acc 0.839 / prec 0.435). Triage tree = the usable prioritizer; its rules are readable conjectures (absence of {u2u_xx, u_x2, uu_xx} => predict high-symmetry).
  (d) RESONANCE FOUND by the audit: structure {u, u3, xu_x} with coeff of x*u_x = -1/2 gives dims [2,2] stable (fin), coeff = 2 gives [2,3,4,7,13] growing (inf). Verified by replaying seed-0 draws + discover at Dmax=5 (rows 96/132). So the windowed label is NOT coefficient-invariant at resonances — exactly the group-classification special-value locus; presence features cannot see it (engine-always-verifies is forced, not policy). 186/187 structures label-consistent.
DELIVERABLE: ADVISORY.md (project advisory + ML operating guide, Part II).
NEXT (recommended, awaiting direction): v1.2 "enumerate, don't sample" — order<=2 dictionary has 2^11-1 = 2047 structures at ~0.26 s/PDE = ~9 CPU-min for COMPLETE ground truth (perfect train/test split by structure + full jump-candidate list via repeated coefficient draws).

=== ADVISORY.md ROADMAP EXECUTION (subagent-driven, non-git: ledger + pytest) ===
- Gate G1 (textbook validation table): COMPLETE + REVIEW CLEAN. Deliverable symm/textbook_validation.py (build/evaluate/__main__) + regression test symm/tests/test_textbook_validation.py (5 tests). Suite now 45 pass (40 + 5).
  RESULT: 6/6 PASS, zero unexplained discrepancies. Four finite MATCHes vs literature — Burgers 5, Fisher 2, porous m=2 (generic branch) 4, KdV (order 3) 4 — each corroborated by exact-rational dim == numeric SVD nullity. Two infinite algebras INF-DETECTED via the stalled flag + strictly-growing per-degree seq — heat u_t=u_xx (6+inf; windowed seq [6,8,10,11,12], dim 12@D5) and transport u_t=u_x (inf; seq [10,22,40,65,98], dim 98@D5).
  Honesty guardrail STRUCTURALLY enforced: heat textbook="6+inf" (string) makes a false finite MATCH unreachable; only claim verified for heat/transport is infinite-part detection, NOT recovery of the finite generators (window limitation, documented).
  Opus task-review independently CONFIRMED all six literature dimensions (Olver/Bluman-Kumei/Ibragimov) and verified the guardrail is by-construction. Spec full compliance; quality approved.
  Minor observations (non-blocking, logged for any future hardening): (1) PASS/DISCREPANCY summary is printed not returned as structured data; (2) no negative/mutation test proving a deliberately-wrong value surfaces as DISCREPANCY; (3) a 4-line idempotent sys.path shim was added to textbook_validation.py so `python symm/textbook_validation.py` runs by path (no-op under pytest; only new file touched).
  Run chose scope "G1 only" — STOPPED here; G2 (enumerate) awaiting go. Course-thesis bar is G1 + G5.
- 20-DAY PAPER PLAN written: PAPER_TODO_20DAYS.md (dated schedule Jul 14 - Aug 2, phases A-G mapping ADVISORY gates G2-G7 to days, application hooks per PDE, cut-lines, risk register, Day-20 done-checklist). Plan only — no implementation started.
- PURE-MATH COMPANION (pre-Phase-A, user-requested): curriculum_math.tex -> curriculum_math.pdf (8 pp, compiles clean, 4 TikZ figures) + symm/curriculum_checks.py (18/18 symbolic checks PASS). Proves the curriculum baseline: linearity of determining operator (lemma+proof); window monotonicity (lemma); ALL THREE G1 sequences derived in closed form — Burgers [4,5,5] = degree census (projective deg 2), heat [6,8,10,11,12] = f(D)+(D+1) heat polynomials, transport [10,22,40,65,98] = 2*C(D+2,2)+C(D+3,3) via a COMPLETE determination of u_t=u_x's point algebra (a(z,u)dz + b(z,e,u)de + c(z,u)du, full 6-line proof); semicontinuity prop (minors) => division-of-labor corollary; reduction/transversality section. Phase A still not started.
- CURRICULUM.md written: full math-stack map (L0-L10 with stress tests), the "machine points to group+manifold" decision procedure (5 real decision points D1-D5; manifold forced by signature, group computed as kernel), PDE-class -> group/manifold taxonomy table, and a July-2026 web-swept algorithm survey. Survey verdict: no post-2025 method supersedes exact determining systems for known PDEs; new front is data-only discovery (LieNLSD 2510.01855 ✅ = same linear determining core with data-estimated jets; spectral GFT 2603.07299 ✅ adjacent). Future-work hook logged: "discover, then certify" (data front-end + our exact verifier).
