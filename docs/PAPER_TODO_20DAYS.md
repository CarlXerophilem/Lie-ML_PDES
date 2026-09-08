# 20-Day Completion Plan — "Semi-Analytical and Machine Learning Methods for Solving PDEs Using Lie Symmetry"

Course math 4890. Written 2026-07-13. Window: **Day 1 = Tue 2026-07-14 → Day 20 = Sun 2026-08-02.**
This file is self-contained: a later autonomous session can execute any phase from it without chat
context. It operationalizes ADVISORY.md §5 (gates G2–G7; G1 is already complete) on a dated schedule,
with each phase motivated by a concrete application in mathematical physics / engineering.

---

## 0. Standing rules for every working session

- Honesty gates: every numeric claim must be reproduced by a runnable script; negatives (vacuous
  bounds, failed gates, non-reproducing numbers) are reported plainly and count as results.
- Ledger: append progress to `.sdd/progress.md` at the end of each phase (same format as existing).
- Tests stay green: `python -m pytest symm/tests -q` from the project root. Baseline today: **45 passed**.
  Each phase adds its own regression test; never leave the suite red overnight.
- Ad-hoc probe scripts run with `PYTHONPATH="/d/MATHs/math 4890 LieML"` (bash) from the project root.
- Citations carry ✅ (opened and verified) or 🟡 (unverified) tags until the Day-16 citation audit.
- This folder is NOT a git repo. Deliver everything as files in the paths named below.

## 1. Verified starting state (do not re-derive; trust ledger + suite)

| Asset | Evidence |
|---|---|
| Symmetry engine v1 (exact, resumable, fuzz-tested) | `symm/sym_engine/` (12 modules), 45-test suite |
| G1 textbook validation: 6/6 PASS (Burgers 5, Fisher 2, porous m=2 → 4, KdV 4; heat & transport correctly flagged infinite) | `symm/textbook_validation.py` + test |
| Reducibility record (dim, algebra type, defect δ, index ρ, π-tuple, LATENT storage) | `symm/sym_engine/reducibility.py`, spec §6 |
| Reductor v1.1, honest protocol: struct-LOOCV tree beats 1-NN on dim 0.747/0.832 vs 0.591/0.707; triage (dim≥4) acc 0.892 / rec 0.792 / prec 0.559; verified coefficient resonance in structure {u, u3, xu_x} (c=−1/2 stable dim 2 vs c=2 growing 2,3,4,7,13) | `symm/reductor/train_reductor.py` + pinned test; ledger |
| HAM closure + 3-part certificate on Fisher (bounded variable s=e^{z/√6}; deliberately vacuous branch) | `symm/fisher_kpp_reduction.py` |
| PINN corrector (321 params, invariant coordinate) | `symm/pinn_corrector_demo.py` |
| SAC-NO probes (companion sub-thesis) | `symm/sacno/` + `SACNO_PLAN.txt` |
| Paper skeleton (positioning + methods, NO results yet) | `draft/draft.tex` (compiles) |
| Beginner map / background material | `intro.tex` (23 pp, incl. §"characteristic system" + §"why the whole algebra matters") |
| Full advisory + gate definitions | `ADVISORY.md` |

## 2. The application arc (what motivates each computation — use these hooks in the paper's prose)

| PDE / object | Application (math-physics / engineering) | Role in the paper |
|---|---|---|
| Fisher–KPP `u_t=u_xx+u(1−u)` | gene-propagation fronts (Fisher 🟡), combustion/flame fronts | **The spine**: end-to-end certified pipeline; exact Ablowitz–Zeppetella front at c=5/√6 is the ground truth |
| Porous medium `u_t=(u^m u_x)_x` | groundwater mound spreading, high-pressure gas filtration (Barenblatt) | Scaling branch (self-similar solutions) + group-classification jump at special exponent (m=−4/3, fast diffusion) |
| Burgers `u_t+uu_x=νu_xx` | shock waves, traffic flow | Already validated (dim 5); "big algebra = linearizable (Cole–Hopf)" exhibit; exact tanh shock |
| KdV `u_t+uu_x+u_xxx=0` | shallow-water solitons | Order-3 validation (done in G1) |
| Heat / transport | diffusion / advection | The honesty exhibit: infinite algebras *flagged*, never faked as finite |
| Learned reductor | screening large families of candidate models (an engineering "model library" triage) before expensive symbolic classification | The ML-that-knows-its-place story: prioritizer, engine always verifies |
| Blasius boundary layer | aerodynamics | OPTIONAL heritage example (HAM literature); first thing to cut |

## 3. Sub-aims of the study, decomposed → phases

- **SA1 Reduce complex PDEs to simpler forms automatically** — engine DONE + G1; residual work = sweep
  coverage in Phase C. (Phases: none new / C)
- **SA2 Exact solutions where they exist** — Burgers shock, Barenblatt profile, AZ front; formalized as
  the validation targets inside the pipeline. (Phases: D, E)
- **SA3 Approximate analytical solutions with certificates** — HAM + Turkyilmazoglu ratio + a-posteriori
  bound, integrated behind the engine instead of hand-fed. (Phase: D)
- **SA4 ML, honestly scoped** — (a) reductor triage on complete ground truth; (b) small invariant PINN
  corrector; negatives reported. (Phases: A, B, D)
- **SA5 Applications + McGreivy–Hakim-compliant validation** — exact-solution comparisons only; results
  tables. (Phases: C, E)
- **SA6 The paper** — assemble, audit, compile. (Phases: F, G)

## 4. Schedule

### Phase A — Days 1–2 (Jul 14–15): G2 "Enumerate, don't sample" (complete ground truth)

*Application hook: the complete symmetry landscape of a model dictionary — what an engineer would want
as a lookup table before modeling.*

- Write `symm/reductor/enumerate_v12.py`: enumerate ALL 2^11−1 = 2047 non-empty subsets of the 11
  order-≤2 MASTER terms (everything except `u_xxx`; dictionary in `symm/reductor/generator.py`).
  For each structure: draw generic coefficients (same COEFFS set), label via `discover(pde, 1, 3)`
  exactly as `label_pde` does; then a SECOND independent draw per structure; a label disagreement
  between draws = jump candidate. Budget: measured ~0.26 s/PDE ⇒ ~2 × 9 CPU-min. Output
  `symm/reductor/landscape_v1.json` (one row per structure: feat, dim, stalled, klass per draw,
  jump flag) + a `__main__` summary printer.
- Add `symm/tests/test_landscape.py`: pins row count 2047, zero errors, the {u, u3, xu_x} structure
  flagged as jump candidate (already verified by hand), and fuzz invariants (residual==0,
  numeric==exact) on a fixed 10-structure sample.
- GATE (falsifiable): 2047/2047 rows, 0 crashes; jump-candidate list printed with count; runtime logged.
  Ledger updated. Expected suite ≈ 47+.

### Phase B — Days 3–4 (Jul 16–17): G3 reductor evaluated on complete ground truth

*Application hook: triage quality you can state exactly, because the test set is the whole universe.*

- Extend evaluation (new `symm/reductor/eval_on_landscape.py` or extend `train_reductor.py`): fixed
  80/20 split BY STRUCTURE (seed 0) over `landscape_v1.json`; majority / 1-NN / depth-3 tree on dim,
  and the triage target (dim≥4) with acc/recall/precision; depth curve printed.
- Rule verification loop: extract the depth-3 triage tree's rules; for each rule, check it against the
  ENTIRE landscape (exhaustive, free — the table is complete). Verified rules become boxed conjecture-
  theorems for the paper ("in this dictionary, no PDE containing u²u_xx has dim ≥ 4" — or its refutation,
  equally reportable).
- GATE: honest scoreboard vs both baselines; ≥3 rules exhaustively verified or refuted; pinned test.

### Phase C — Days 5–7 (Jul 18–20): G4 group-classification sweep (the jump-detection demo)

*Application hook: nonlinear diffusion design — which material exponents admit extra symmetry
(= extra exact solutions) is a physical design question (Barenblatt/fast-diffusion).*

- Day 5 SPIKE (timeboxed, half a day): test whether the engine's determining-matrix splitter accepts
  `u_t=(u^m u_x)_x` with rational m = −4/3 (non-polynomial powers of u). If yes → full rational sweep.
  If no → record the limitation honestly and use the two fallbacks below (both polynomial-safe).
- Primary sweep: integer m ∈ {1, 2, 3, 4}: expect dim 4 at every generic m (constant row = the generic
  branch), engine-verified.
- Guaranteed jump demo (fallback that CANNOT fail — phenomenon already verified): sweep the resonance
  family `u_t = u + 2u³ + c·x·u_x` over c ∈ {−2, −1, −1/2, 1/2, 1, 3/2, 2, 3}; the windowed dim jumps
  at resonant c (c=2 verified: 2,3,4,7,13 growing vs stable 2 at c=−1/2). Automated detection rule:
  flag any c whose per-degree sequence grows.
- Deliverable `symm/classification_sweep.py` + `symm/tests/test_sweep.py` (pins the c=−1/2 vs c=2
  contrast; pins integer-m porous row). Optional: reductor-priority evaluation on the sweep — expected
  and acceptable NEGATIVE (presence features cannot see c); write it as the motivation for parametric
  features in future work.
- GATE: at least one automated jump-detection table; m=−4/3 either detected or documented as a window/
  scope limitation with the Maple `rifsimp` escape hatch named.

### Phase D — Days 8–11 (Jul 21–24): G5 end-to-end CCS-SYM+ on Fisher (THE PAPER'S SPINE)

*Application hook: a reaction–diffusion front computed with a certificate — the full promise of the
title in one command.*

- Build `symm/ccs_pipeline.py`, one command, six stages, each emitting its artifact:
  1. REDUCE-discover: engine on Fisher → dim 2, CERTIFIED record (reuse `Engine.run`).
  2. REDUCE-apply: pick the travelling-wave generator ∂t + c∂x via `interfaces.propose_reductions`,
     `reduce_by` → ODE U″+cU′+U(1−U)=0 with residual-0 check (already in `reduce.py`).
  3. CLOSE: HAM series at c=5/√6 in the bounded variable s=e^{z/√6} (adapt functions from
     `symm/fisher_kpp_reduction.py`; adapt, don't rewrite).
  4. CERTIFY: Turkyilmazoglu ratio sequence + computable a-posteriori residual bound; the vacuous
     branch is REPORTED AS VACUOUS in the output (it is a feature — falsifiability).
  5. CORRECT: invariant-coordinate PINN corrector (adapt `symm/pinn_corrector_demo.py`, CPU, seconds);
     error before/after vs the exact Ablowitz–Zeppetella front (McGreivy–Hakim compliance: exact
     ground truth only).
  6. REPORT: write `results/ccs_fisher_report.md` + CSVs (ratio-vs-order, error-vs-z) for figures.
- `symm/tests/test_ccs_pipeline.py`: smoke run + pinned key numbers (algebra dim, ODE residual 0,
  certificate values, corrector error-reduction factor).
- Day 11 (only if Days 8–10 land): second end-to-end, porous/Barenblatt through the scaling branch.
  This is cut-line item #2 — skip without guilt.
- GATE: ONE command reproduces every stage number that the standalone demos produce; report file
  generated; suite green.

### Phase E — Days 12–13 (Jul 25–26): G6-lite — results tables + figure data

- Consolidate into `results/`: G1 validation table, landscape statistics (dim histogram over 2047,
  jump-candidate count), sweep table, reductor scoreboard, pipeline error/runtime table.
- Figures: prefer **pgfplots/TikZ from CSV** (MiKTeX available). First check whether matplotlib is
  installed (`python -c "import matplotlib"`); it is NOT assumed. Needed plots: (i) certificate ratio
  vs order; (ii) |error| vs z before/after PINN correction; (iii) landscape dim histogram.
- The full bench harness (`symm/bench/BUILD_PLAN.md`) is NOT built in this window — record as
  descoped in the ledger (cut-line item #3); the tables above are its minimal core.
- GATE: every table/figure datum traceable to a script path named in the CSV header comment.

### Phase F — Days 14–18 (Jul 27–31): G7 — assemble the paper (`draft/draft.tex`)

- Day 14: restructure skeleton — Abstract / 1 Introduction (application arc of §2 above) / 2 Related
  work (already drafted) / 3 Methods: engine + record (from spec) / 4 Methods: CCS pipeline /
  5 Results: validation, landscape, sweep, end-to-end / 6 The ML components, honestly /
  7 Limitations & negatives / 8 Reproducibility. Map every results subsection to its artifact file.
- Day 15: methods sections final. MUST include verbatim the lower-bound sentence: "dim_D is a
  certified lower bound within the polynomial window; stabilization is evidence, not proof, of
  completeness; the stalled flag marks suspected infinite parts; completeness is delegated to the
  escape hatch." Include defect/index definitions copied from the spec (§6) with the π-tuple.
- Day 16: CITATION AUDIT. In-tree ✅ (all in `ref/`, already read): Olver; Notes on Lie symmetry
  methods; Kruglikov–Lychagin; Lie–Tresse (2011.05101); Brandstetter LPSDA (2202.07643); Helwig G-FNO
  (2306.05697); LieLAC canonicalization; NeurIPS-2023 LPS+PINNs; Generalized Lie Symmetries in PINOs;
  LieSolver; McGreivy–Hakim weak baselines; the two ML-for-PDE reviews; Expert's Guide to PINNs; FNO.
  External 🟡 → verify bibliographic data before promoting to ✅: Ablowitz–Zeppetella 1979 (exact
  Fisher front); Turkyilmazoglu (ratio criterion); Ovsiannikov; Bluman–Kumei; Ibragimov handbook;
  Boulier et al. (Rosenfeld–Gröbner); Reid (rif); Raissi et al. 2019. Anything unverifiable stays
  🟡-labeled in a footnote or is dropped. NEVER invent DOIs/arXiv IDs.
- Day 17: figures + tables in; full `pdflatex` ×2 clean; fix overfull boxes.
- Day 18: honesty pass — the negatives section is a selling point, written in paste-ready prose:
  coefficient features hurt (0.685→0.395); depth-3 dim-tree recall 0.000 on rich PDEs (why triage
  target replaced it); the vacuous certificate branch; infinite-window limitation; duplicate-leakage
  correction (0.685→0.591). Reproducibility appendix: exact commands, test count, seed values.
- GATE: compiles clean; claims audit against ADVISORY.md §2.4 table (no claim exceeds its verdict);
  every number in the text carries a script name.

### Phase G — Days 19–20 (Aug 1–2): buffer + red-team

- Day 19: absorb overruns from any phase (the schedule assumes one full day will be eaten). If
  everything landed: draft the 1-page SAC-NO appendix from `symm/sacno/SACNO_PLAN.txt` (cut-line #1).
- Day 20: adversarial read-through as a hostile referee (checklist: is any dim claimed without the
  window sentence? any ML number without both baselines? any citation still 🟡 in a load-bearing
  spot?); final abstract/title; final compile; close the ledger with a DONE entry listing artifact
  paths + final test count.

## 5. Cut-lines (descope in THIS order when behind schedule)

1. SAC-NO appendix (keep a one-paragraph pointer to `symm/sacno/SACNO_PLAN.txt`).
2. Second end-to-end run (porous/Barenblatt) — Day 11.
3. Bench harness beyond the results tables (already assumed descoped).
4. Porous rational-m (m=−4/3) inside our engine — fall back to integer sweep + resonance family +
   documented escape hatch.

**Never cut:** the Fisher end-to-end (Phase D), the citation audit (Day 16), the negatives/limitations
section (Day 18). Course-thesis bar = G1 (done) + Phase D. Everything else raises the external bar.

## 6. Risk register

| Risk | Mitigation |
|---|---|
| Engine splitter rejects fractional powers (m=−4/3) | Day-5 timeboxed spike; two polynomial-safe fallbacks pre-planned (Phase C) |
| matplotlib may not be installed | pgfplots/TikZ from CSV; check before relying |
| HAM/certificate code resists integration | Adapt existing functions; timebox to Day 10; if stuck, pipeline calls the standalone script and parses its output (ugly but honest) |
| A phase slips | Day 19 buffer + cut-lines §5; report the descope in the ledger, never silently |
| Overclaiming under deadline pressure | Day 18 + Day 20 audits are non-negotiable; ADVISORY.md §2.4 is the ceiling on claims |

## 7. Definition of done (Day 20 checklist)

- [ ] `draft/draft.pdf` compiles clean; results, figures, negatives, reproducibility appendix all in.
- [ ] `python -m pytest symm/tests -q` green (expected ≈ 50+ tests).
- [ ] One-command Fisher pipeline runs end-to-end and regenerates every paper number it owns.
- [ ] Landscape (2047), sweep, and reductor tables regenerable from named scripts.
- [ ] Every citation ✅ or explicitly 🟡; zero invented identifiers.
- [ ] `.sdd/progress.md` closed with artifact manifest.
