# Mathematical ML Q&A Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current Q&A with a formal, self-contained guide that explains pure machine learning first and then derives, classifies, and audits its interactions with Lie-symmetry reduction of PDEs.

**Architecture:** Build the revision outside the repository target, in two ordered parts: Q1–Q5 introduce ordinary machine learning without PDE or Lie terminology; Q6–Q16 specialize those objects to residual-based PDE learning and then to the exact Lie-reduction pipeline. Treat exact geometry, analytical approximation, learned numerics, and certification as separate layers connected by explicit interfaces and failure gates. Audit the complete temporary draft before atomically replacing the untracked target file.

**Tech Stack:** GitHub-flavored Markdown, LaTeX mathematics, Python 3.14 in isolated mode for structural and small symbolic checks, SymPy 1.14 for formula verification, Git Bash for read-only repository checks, and verified local/official literature sources.

**Spec:** `docs/superpowers/specs/2026-10-08-mathematical-essence-ml-qa-design.md`

## Global Constraints

- Modify only `docs/The Mathematical Essence of Machine Learning.md`; use the specification, manuscript, and bibliography as read-only sources.
- Preserve all pre-existing working-tree changes. The target is untracked at plan time; do not stage, commit, delete, restore, or rewrite any other path.
- Do not commit or push unless the user explicitly requests it after reviewing the completed rewrite.
- Construct and audit the new document in `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md` before replacing the target.
- Preserve the original target at `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-original-2026-10-08.md` and record its SHA-256 digest before editing.
- Part I is Q1–Q5 and must be a self-contained pure-ML primer. It must not use PDE, PINN, collocation, Lie, quotient, invariant-surface, or reduced-profile concepts.
- Part II is Q6–Q16 and must introduce PDE learning before Lie reduction, then introduce Lie notation before any ML–Lie fusion.
- Define every symbol before first use. In particular, define `x`, `u`, `i`, `alpha`, `xi`, `eta`, `u_i^alpha`, `Q^alpha`, and `v_Q` before using the invariant-surface condition.
- Use `Q=(Q^alpha)` for the characteristic and `v_Q=sum_alpha Q^alpha partial_{u^alpha}` for the associated evolutionary representative.
- Distinguish equation symmetry, invariant solution graphs, equivariant models, and sampled symmetry penalties.
- Treat the domain, initial/boundary/interface data, admissibility conditions, parameter stratum, regularity chart, and reconstruction map as part of the PDE problem.
- Preserve the classification boundary: a bounded ansatz or numerical rank test produces candidates, not a complete Lie classification.
- Preserve the reduction boundary: a symmetry of the equation alone is insufficient if the domain or data do not descend to the quotient.
- Keep exact, analytical, learned, and certified claims visibly separate.
- Do not infer a solution-error bound from a small sampled residual without a stated stability estimate, controlled norm/quadrature, admissible data, and reconstruction bound.
- Do not assert that a neural method is preferable when a conventional reduced solver is faster or more accurate at the same task.
- Every literature citation must be tagged `✅` after the cited source and exact supporting passage have been opened and checked. Omit a claim whose source cannot be verified; do not invent metadata.
- Remove the external chat-share link and all unresolved citation placeholders from the scholarly rewrite.
- Use standard Markdown mathematics: `$...$` inline and `$$...$$` for display equations.
- Report failed verification gates plainly; do not silently weaken or omit them.

## File Structure

### Permanent deliverable

- **Modify:** `docs/The Mathematical Essence of Machine Learning.md` — the complete sixteen-question explanatory Q&A and compact verified references.

### Read-only project sources

- **Read:** `docs/superpowers/specs/2026-10-08-mathematical-essence-ml-qa-design.md` — approved content, correction list, and acceptance criteria.
- **Read:** `draft/main.tex:99-517` — exact reduction contract, quotient dimension, ML target, and four-layer workflow.
- **Read:** `draft/main.tex:1002-1199` — representation-theoretic interface, explicit reduction anchor, and neural construction.
- **Read:** `draft/main.tex:1257-1352` — negative speed result, certificate-gated prototype, and parameter-family evidence.
- **Read:** `draft/references.bib` — candidate metadata and official URLs; do not modify it in this task.

### Temporary implementation artifacts

- `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-original-2026-10-08.md` — byte-for-byte backup of the current untracked Q&A.
- `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md` — working draft that is installed only after all gates pass.
- `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-citation-ledger-2026-10-08.md` — claim-to-source ledger used during drafting.
- `C:/Users/Administrator/AppData/Local/Temp/lieml-status-before-2026-10-08.txt` — pre-edit Git status snapshot.
- `C:/Users/Administrator/AppData/Local/Temp/lieml-staged-before-2026-10-08.txt` — pre-edit staged-file snapshot.
- `C:/Users/Administrator/AppData/Local/Temp/lieml-dirty-manifest-before-2026-10-08.json` — kind and SHA-256 manifest for every pre-existing dirty/untracked path except the intended Q&A target.
- `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-final.diff` — complete original-to-final document diff for review.
- `C:/Users/Administrator/AppData/Local/Temp/lieml-status-after-2026-10-08.txt` — post-install Git status snapshot.
- `C:/Users/Administrator/AppData/Local/Temp/lieml-staged-after-2026-10-08.txt` — post-install staged-file snapshot.

No temporary artifact is a project deliverable or should be staged.

---

### Task 1: Preserve the source and verify the evidence base

**Files:**
- Read: `docs/The Mathematical Essence of Machine Learning.md:1-323`
- Read: `docs/superpowers/specs/2026-10-08-mathematical-essence-ml-qa-design.md:1-631`
- Read: `draft/main.tex:99-517`
- Read: `draft/main.tex:1002-1199`
- Read: `draft/main.tex:1257-1352`
- Read: `draft/references.bib`
- Create outside repository: the nine temporary artifacts listed above

**Interfaces:**
- Consumes: the approved specification, current Q&A, companion manuscript, and candidate bibliography.
- Produces: a recoverable source backup, a clean working draft path, a repository-status baseline, and a verified claim-to-source ledger used by Tasks 2–6.

- [ ] **Step 1: Record the working-tree baseline and protect the untracked source**

Run from the repository root:

```bash
python -I - <<'PY'
from hashlib import sha256
from pathlib import Path
import shutil

root = Path(r"D:/MATHs/math 4890 LieML")
source = root / "docs/The Mathematical Essence of Machine Learning.md"
backup = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-qa-original-2026-10-08.md")
rewrite = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md")
shutil.copy2(source, backup)
rewrite.write_text("", encoding="utf-8")
print("SOURCE_SHA256", sha256(source.read_bytes()).hexdigest())
print("BACKUP_SHA256", sha256(backup.read_bytes()).hexdigest())
assert source.read_bytes() == backup.read_bytes()
PY
git status --porcelain=v1 > 'C:/Users/Administrator/AppData/Local/Temp/lieml-status-before-2026-10-08.txt'
git diff --cached --name-only > 'C:/Users/Administrator/AppData/Local/Temp/lieml-staged-before-2026-10-08.txt'
python -I - <<'PY'
from hashlib import sha256
from pathlib import Path
import json, subprocess

root = Path(r"D:/MATHs/math 4890 LieML")
target = "docs/The Mathematical Essence of Machine Learning.md"

def git_paths(*args):
    raw = subprocess.check_output(["git", "-C", str(root), *args])
    return {
        p.decode("utf-8", errors="surrogateescape")
        for p in raw.split(b"\0") if p
    }

paths = set()
paths |= git_paths("diff", "--name-only", "-z")
paths |= git_paths("diff", "--cached", "--name-only", "-z")
paths |= git_paths("ls-files", "--others", "--exclude-standard", "-z")
paths.discard(target)
manifest = {}
for path in sorted(paths):
    p = root / path
    manifest[path] = {
        "kind": "file" if p.is_file() else "missing-or-directory",
        "sha256": sha256(p.read_bytes()).hexdigest() if p.is_file() else None,
    }
out = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-dirty-manifest-before-2026-10-08.json")
out.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
print("DIRTY_PATHS_RECORDED", len(manifest))
PY
```

Expected: the source and backup SHA-256 digests are identical, the Git snapshots record the pre-existing repository state, and `DIRTY_PATHS_RECORDED <N>` is printed. This step itself changes no repository file.

- [ ] **Step 2: Build a claim-to-source ledger from opened sources**

Create `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-citation-ledger-2026-10-08.md` with columns:

```markdown
| ID | Claim used in Q&A | Source opened | Exact section/page/passage | Status |
|---|---|---|---|---|
```

Verify only claims that will appear in the document. Use this fixed minimum source set:

1. Shalev-Shwartz and Ben-David, *Understanding Machine Learning: From Theory to Algorithms* (2014), official Cambridge/author material, for empirical risk minimization, hypothesis classes, and capacity/generalization. Use no quantitative Rademacher bound unless its exact theorem and assumptions are checked there or in a second named primary text.
2. Lagaris, Likas, and Fotiadis (1998), local file `ref/public-pdfs/lagaris.pdf` and official/arXiv record `physics/9705023`, for analytically constrained neural trial functions.
3. Raissi, Perdikaris, and Karniadakis, *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations* (2019), official DOI `10.1016/j.jcp.2018.10.045`, for the residual-based PINN formulation.
4. Wang, Teng, and Perdikaris (2021), local file `ref/public-pdfs/wanggradient.pdf` and official/arXiv record `2001.04536`, for PINN gradient-flow pathologies.
5. Olver, *Applications of Lie Groups to Differential Equations*, second edition (1993), official DOI `10.1007/978-1-4612-4350-2`, for prolongation, characteristics, invariant-surface conditions, and local reduction.
6. Anderson, Fels, and Torre (2000), official DOI `10.1007/s002200000215` and arXiv `math-ph/9910015`, for nontransverse invariant solutions.
7. Akhound-Sadegh et al. (2023), local file `ref/pdfs/Lie Point Symmetry and Physics Informed Networks.pdf`; Otto et al. (2025), local file `ref/public-pdfs/otto.pdf`; and Shumaylov et al. (2025), local file `ref/public-pdfs/lieLAC.pdf`, for symmetry penalties, the enforcement/discovery/promotion taxonomy, and canonicalization under Lie-group actions.
8. Kirillov, *An Introduction to Lie Groups and Lie Algebras*, local file `ref/kb/liegroups.pdf`, especially sections 4.4–4.7, for intertwiners, Schur’s lemma, compact-group Haar measure, character orthogonality, and Peter–Weyl; and Hall, *Lie Groups, Lie Algebras, and Representations*, second edition (2015), local file `ref/kb/Hall-LieGroupsLiealgebras2015.Springer.Elementaryintro.pdf`, as a complementary representation-theory source. The ledger must cite the exact theorem/page for the `L^2(G)` matrix-coefficient statement; do not infer Peter–Weyl from Schur’s lemma alone.
9. Cohen and DeVore (2015), official arXiv `1502.06797`, only if Kolmogorov widths or parameter-to-solution regularity remain in the rewrite.

For each source, open the official page or actual paper/book excerpt, record the supporting location, and mark `✅` only after the passage is checked. If an official page cannot be fetched, use the listed local PDF and record the actual page or theorem location. A bibliography entry or search-result snippet is not sufficient evidence.

- [ ] **Step 3: Reject unsupported source claims before drafting**

Remove from the planned content any claim that lacks a checked source or direct derivation. In particular, reject these source-document formulations:

- all ML is an ill-posed inverse problem;
- equivariance reduces sample complexity by the volume of a symmetry group;
- symplectic preservation alone enforces energy conservation;
- every bounded group-equivariant operator is convolution with an `L^2` filter;
- every continuous equivariant map has the asserted three-operation factorization;
- Peter–Weyl applies without qualification to noncompact scaling, translation, boost, or affine groups.

Expected: every retained literature-dependent statement has one ledger row marked `✅`, while definitions and calculations are identified as direct derivations rather than citations.

- [ ] **Step 4: Review the task boundary before writing**

Run:

```bash
git status --porcelain=v1
```

Expected: it matches the saved baseline exactly; only temporary files have been created.

---

### Task 2: Draft Part I — pure machine learning, Q1–Q5

**Files:**
- Modify outside repository: `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md`
- Read: citation ledger from Task 1

**Interfaces:**
- Consumes: verified pure-ML sources and the approved Q1–Q5 contracts.
- Produces: title, reader orientation, and a self-contained pure-ML primer ending immediately before the Part II heading.

- [ ] **Step 1: Write the title and reading contract**

Begin the temporary draft with:

```markdown
# The Mathematical Essence of Machine Learning

This Q&A has two parts. Part I develops machine learning as a mathematical subject in its own right. Part II then asks how those ideas change when the unknown object is a PDE solution and how Lie symmetry reduction can alter the learning problem before any neural approximation is introduced.

## Part I. Machine learning on its own
```

Do not include the old external chat-share URL. Do not mention PINNs, collocation, Lie groups, or PDE residuals before Part II.

- [ ] **Step 2: Write Q1, “What is the mathematical essence of machine learning?”**

Give a one-paragraph direct answer: learning selects an action, predictor, function, operator, parameter, or distributional model from incomplete information by minimizing a declared criterion and testing performance beyond the information used for selection.

Then introduce the supervised statistical case:

$$
Z=(X,Y)\sim P,\qquad h\in\mathcal H,\qquad
R(h)=\mathbb E_P[\ell(h(X),Y)],
$$

$$
R_n(h)=\frac1n\sum_{i=1}^n\ell(h(x_i),y_i),
\qquad
\widehat h_n\approx\operatorname*{argmin}_{h\in\mathcal H}R_n(h).
$$

Explain the five distinct questions: target identification, representation, finite-sample estimation, optimization, and validation. State that probability-space risk minimization is an important framework, not a universal definition of every ML problem.

- [ ] **Step 3: Write Q2, “What are the fundamental components of a learning problem?”**

Use

$$
\mathfrak L=(\mathcal Z,P,\mathcal H,\ell,\Omega,
\mathsf{Alg},\mathsf{Val}).
$$

Define every entry and include an interaction table with columns `Component`, `Mathematical role`, `What changes if it is replaced`, and `Dependence on other components`.

Make explicit that:

- `P` may be unknown and observed only through samples;
- `Omega` may be absent or encoded implicitly by architecture/optimization;
- `Alg` need not return the global empirical minimizer;
- `Val` specifies the population, metric, and uncertainty under which success is claimed.

- [ ] **Step 4: Write Q3, “Is a neural network necessary?”**

Answer no before giving any qualification. Compare at least these hypothesis classes:

| Class | Structural assumption | Typical strength | Typical limitation |
|---|---|---|---|
| Linear/generalized-linear | additive or link-linear structure | convex and interpretable | limited nonlinear interactions |
| Trees/ensembles | recursive partitions | strong tabular baseline | nonsmooth, weak extrapolation |
| Kernels/Gaussian processes | similarity and smoothness through a kernel | convex or probabilistic structure | scaling with sample size |
| Splines/basis expansions | chosen smooth basis | transparent approximation | basis design and dimension |
| Neural networks | compositional parameterization | flexible shared features | nonconvex training and opaque bias |

Conclude with the decision rule: use the simplest class that meets the declared accuracy, generalization, interpretability, and computational requirements.

- [ ] **Step 5: Write Q4 with a checked constant-prediction example**

Use observations `y=(0,0,10)` and constant predictors `h_c(x)=c`.

Show explicitly:

$$
\frac13\sum_i(c-y_i)^2
$$

is minimized by `c=10/3`, while

$$
\frac13\sum_i|c-y_i|
$$

is minimized by the median `c=0`. Explain that the loss changes the population quantity being estimated: conditional mean for squared loss, conditional median for absolute loss, and a Bayes class for zero-one classification loss.

Then distinguish approximation, estimation, and optimization without asserting an unconditional exact identity. Define `h^*` as a Bayes-risk minimizer in a declared ambient class `H_all` containing `H`, assuming the relevant infima/minimizers exist. Use the safe decomposition

$$
R(\widehat h)-R(h^*)
=
\bigl[R(\widehat h)-\inf_{h\in\mathcal H}R(h)\bigr]
+
\bigl[\inf_{h\in\mathcal H}R(h)-R(h^*)\bigr],
$$

and explain that the first bracket is an in-class excess-risk term that can be further bounded or decomposed into estimation and optimization contributions only after specifying the empirical comparator, algorithm, and existence assumptions.

- [ ] **Step 6: Verify the loss example computationally**

Run:

```bash
python -I - <<'PY'
from fractions import Fraction
ys = (0, 0, 10)
mean = Fraction(sum(ys), len(ys))
abs_losses = {c: sum(abs(c-y) for y in ys) for c in ys}
print("MEAN", mean)
print("ABSOLUTE_LOSS_CANDIDATES", abs_losses)
assert mean == Fraction(10, 3)
assert min(abs_losses, key=abs_losses.get) == 0
PY
```

Expected:

```text
MEAN 10/3
ABSOLUTE_LOSS_CANDIDATES {0: 10, 10: 20}
```

Record the checked numbers in Q4; do not claim this toy example proves a generalization theorem.

- [ ] **Step 7: Write Q5, “What can ordinary machine learning establish, and what remains unproved?”**

Use an evidence ladder:

1. low training loss;
2. low held-out loss under a stated sampling protocol;
3. a finite-sample generalization statement under named assumptions;
4. calibration or uncertainty coverage under named assumptions;
5. robustness under distribution shift, which requires separate evidence;
6. a formal guarantee, which is theorem- and assumption-specific.

Explain identifiability, data leakage, hyperparameter selection bias, and distribution shift. End Part I with a compact checklist: target, data law, hypothesis class, loss, regularization, optimization, and validation population.

- [ ] **Step 8: Run the Part I isolation gate**

Run:

```bash
python -I - <<'PY'
from pathlib import Path
p = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md")
s = p.read_text(encoding="utf-8")
heading = "## Part I. Machine learning on its own"
assert heading in s
part1 = s[s.index(heading):]
for forbidden in ("PINN", "collocation", "PDE", "Lie symmetry", "invariant-surface", "reduced profile"):
    assert forbidden not in part1, forbidden
for q in range(1, 6):
    assert f"### Q{q}." in part1
print("PART_I_ISOLATED")
PY
```

Expected: `PART_I_ISOLATED`.

---

### Task 3: Draft the PDE transition and exact reduction contract, Q6–Q8

**Files:**
- Modify outside repository: `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md`
- Read: `draft/main.tex:99-517`
- Read: citation ledger from Task 1

**Interfaces:**
- Consumes: the pure-ML tuple and evidence vocabulary from Part I.
- Produces: the PDE specialization, precise characteristic notation, and the complete global-scope/admissibility contract required before any ML–Lie socket is discussed.

- [ ] **Step 1: Add the Part II heading and Q6 PDE specialization**

Append:

```markdown
## Part II. Machine learning combined with PDEs and Lie reduction

### Q6. What changes when the unknown object is a PDE solution rather than a labelled-data predictor?
```

Introduce

$$
\mathcal P_\lambda=
(\mathscr O,\Delta_\lambda,\mathcal B_\lambda,
\mathcal C_\lambda,\mathcal D_\lambda),
$$

with physical domain, PDE system, data residuals, admissibility/branch predicates, and parameter/data family defined separately.

Specialize the pure-ML objective to a strong-form PINN:

$$
\mathcal L(\theta)=
\int_{\mathscr O}\!\|\Delta_\lambda[j^n u_\theta]\|^2\,d\mu_C
+
\sum_b w_b\int_{\Gamma_b}\!\|\mathcal B_b[j^n u_\theta]\|^2\,d\mu_b
+
\mathcal L_{\mathrm{obs}}(\theta).
$$

Define the collocation and data measures as numerical design choices. Explain automatic differentiation, differential-order smoothness, residual normalization, and the distinction between quadrature error and PDE solution error.

Compare PINNs with finite differences, finite volumes, finite elements, spectral methods, shooting, and direct ODE integration. State explicitly that a neural solver has no demonstrated one-query advantage when a conventional reduced solver is faster and more accurate.

- [ ] **Step 2: Write Q7 and define the characteristic before using it**

Use the exact sequence:

$$
x=(x^1,\ldots,x^p),\qquad
u=(u^1,\ldots,u^q),
$$

$$
X=\xi^i(x,u)\frac{\partial}{\partial x^i}
+\eta^\alpha(x,u)\frac{\partial}{\partial u^\alpha},
$$

$$
u_i^\alpha=\frac{\partial u^\alpha}{\partial x^i},
\qquad
Q^\alpha[j^1u]=\eta^\alpha-\xi^i u_i^\alpha,
$$

$$
\mathbf v_Q=
\sum_{\alpha=1}^{q}Q^\alpha\frac{\partial}{\partial u^\alpha}.
$$

State that `j^1u` denotes the first jet—the field values and all first derivatives at a base point—and that repeated indices `i=1,...,p` are summed. Use `Q=(Q^1,...,Q^q)` for the characteristic and `v_Q` for the evolutionary representative. Explain `eta^alpha` and `xi^i u_i^alpha` clause by clause.

Then distinguish

$$
\left.\operatorname{pr}^{(n)}X(\Delta_A)\right|_{\Delta=0}=0
$$

from

$$
Q^\alpha[j^1u]=0,
\qquad \alpha=1,\ldots,q.
$$

Use `X=partial_x` as the concrete example: `xi=1`, `eta=0`, `Q=-u_x`, and `Q=0` selects fields independent of `x`. State that the first equation verifies an equation symmetry; the second selects invariant solution graphs.

- [ ] **Step 3: Explain quotient reduction without overclaiming**

Define projected orbit rank `ell`, quotient dimension `d=p-ell`, invariant coordinates `z`, profile `F(z)`, and reconstruction `u=T_{lambda,H}F`. State:

$$
\mathcal R_{\lambda,H}[F]=0
\Longleftrightarrow
\Delta_\lambda[\mathcal T_{\lambda,H}F]=0
$$

only on the declared regular chart, branch, and invariant family. Explain that this is not a representation of every PDE solution.

Classify:

- `d=0`: algebraic/consistency conditions;
- `d=1`: ODE or differential-algebraic profile problem;
- `d>=2`: reduced PDE or constraints;
- rank-changing points: separate singular strata.

- [ ] **Step 4: Write Q8 as the global research-scope contract**

Include both classification and admissibility tables.

The classification table must distinguish exact point, full-data-problem, invariant-solution, approximate, nonclassical, variational, equivalence, discrete/global, generalized/contact/nonlocal, and learned near-symmetry classes.

The admissibility sequence must contain all eight gates:

1. equation symmetry;
2. Lie closure;
3. regular projected-orbit rank;
4. transversality;
5. quotient chart and reconstruction;
6. domain/data compatibility;
7. reduced-equation closure;
8. admissible reconstruction.

Then give the four global project classes: core admissible, conditional extension, baseline/fallback, and outside present scope. Include explicit exits rather than silently forcing reduction.

- [ ] **Step 5: Check the notation and ordering of Q6–Q8**

Run:

```bash
python -I - <<'PY'
from pathlib import Path
s = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md").read_text(encoding="utf-8")
for q in range(6, 9):
    assert f"### Q{q}." in s
ordered = [
    "X=", "Q^\\alpha", "\\mathbf v_Q",
    "\\operatorname{pr}^{(n)}X", "Q^\\alpha[j^1u]=0"
]
pos = [s.index(token) for token in ordered]
assert pos == sorted(pos), pos
for phrase in ("equation symmetry", "invariant solution", "data compatibility", "regular", "reconstruction"):
    assert phrase.lower() in s.lower(), phrase
print("Q6_Q8_CONTRACT_OK")
PY
```

Expected: `Q6_Q8_CONTRACT_OK`.

---

### Task 4: Draft the ML–Lie interaction core, Q9–Q12

**Files:**
- Modify outside repository: `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md`
- Read: `draft/main.tex:328-414`
- Read: `draft/main.tex:417-517`
- Read: `draft/main.tex:1002-1199`

**Interfaces:**
- Consumes: the pure-ML tuple, full PDE problem, verified quotient, and scope classes.
- Produces: the four ML sockets, componentwise reduction map, worked direct-versus-reduced PINN example, and corrected component-generalization taxonomy.

- [ ] **Step 1: Write Q9, “Where exactly can ML enter?”**

Distinguish these learned objects in a table:

1. full field `u_theta(x)` — baseline/fallback;
2. reduced profile `F_theta(z)` — primary admissible socket;
3. analytical remainder in
   $$
   \widehat F_\theta=F_{\mathrm{an}}+\omega N_\theta;
   $$
4. reduced parameter-to-profile operator
   $$
   (z,\lambda,a)\mapsto F_{\lambda,a}(z);
   $$
5. closure term — separate inverse/identifiability problem;
6. candidate symmetry generator — discovery aid requiring exact verification.

For each, state inputs, output, required evidence, and whether exact symmetry is built in, verified afterward, or only softly encouraged.

- [ ] **Step 2: Write Q10 as a componentwise transformation**

Use

$$
(x,u,\Delta,\mathcal B,P,\mathcal H)
\longmapsto
(z,F,\mathcal R,\overline{\mathcal B},
\overline P,\mathcal H_{\mathrm{red}}).
$$

Explain separately how reduction changes:

- independent variables and domain;
- profile hypothesis class;
- differential operator/order/constraints;
- boundary and initial data;
- collocation measure and weighting;
- regularization and architecture;
- reconstruction;
- profile versus physical-field errors.

Include the exact geometric–analytical–learned–certification layer table. Exact identities must not be described as learned, and numerical residual checks must not be labelled exact.

- [ ] **Step 3: Write Q11 around a checked Burgers comparison**

Use viscous Burgers

$$
u_t+u u_x=\nu u_{xx}
$$

and the travelling-wave coordinate `z=x-ct`, `u(t,x)=F(z)`. Derive

$$
u_t=-cF',\qquad u_x=F',\qquad u_{xx}=F'',
$$

and hence

$$
\mathcal R[F]=(F-c)F'-\nu F''=0.
$$

Compare:

- direct PINN: input `(t,x)`, two-dimensional collocation, full PDE residual;
- reduced PINN: input `z`, one-dimensional collocation, reduced ODE residual;
- analytical remainder: `F_an+omega N_theta` with exact data encoded when justified.

State every limitation: the travelling-wave ansatz selects one invariant family; data must be compatible; lower dimension does not prove lower training time; reconstruction and original-PDE evaluation remain necessary.

- [ ] **Step 4: Verify the Burgers pullback with SymPy**

Run:

```bash
python -I - <<'PY'
import sys
sys.path.append(r"C:/Users/Administrator/AppData/Roaming/Python/Python314/site-packages")
import sympy as sp
assert sp.__version__ == "1.14.0", sp.__version__
t, x, c, nu, zz = sp.symbols("t x c nu zz", nonzero=True)
z = x - c*t
F = sp.Function("F")
u_field = F(z)
full = sp.diff(u_field, t) + u_field*sp.diff(u_field, x) - nu*sp.diff(u_field, x, 2)
reduced_zz = (F(zz)-c)*sp.diff(F(zz), zz) - nu*sp.diff(F(zz), zz, 2)
reduced = reduced_zz.subs(zz, z)
assert sp.simplify(full - reduced) == 0
print("BURGERS_PULLBACK_OK")
PY
```

Expected:

```text
BURGERS_PULLBACK_OK
```

- [ ] **Step 5: Write Q12, “Which components can be tuned, replaced, or generalized?”**

Organize the answer by domain/geometry, sampling, hypothesis class, loss/discrepancy, regularization, optimizer, and validation. For each change, identify which other components must be reconsidered.

Correctly distinguish:

- orbit `G·x`;
- stabilizer `G_x`;
- homogeneous orbit `G/G_x` under the usual regularity assumptions;
- global orbit space `M/G`, which may be singular or nonmanifold;
- quotient coordinate chart used in local reduction.

Cover vector bundles, function/operator spaces, metric-measure spaces, ergodic data, distributional robustness, Sobolev losses, total variation, Riemannian optimization, and mirror descent only where each construction directly clarifies a replaceable component. Remove decorative examples that do not help the central research question.

- [ ] **Step 6: Run the ML-socket and worked-example gate**

Run:

```bash
python -I - <<'PY'
from pathlib import Path
s = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md").read_text(encoding="utf-8")
for q in range(9, 13):
    assert f"### Q{q}." in s
for phrase in (
    "full field", "reduced profile", "analytical remainder",
    "parameter-to-profile", "closure", "candidate symmetry",
    "direct PINN", "reduced PINN", "original PDE"
):
    assert phrase.lower() in s.lower(), phrase
for obj in ("$G\\cdot x$", "$G_x$", "$G/G_x$", "$M/G$"):
    assert obj in s, obj
print("Q9_Q12_INTERFACES_OK")
PY
```

Expected: `Q9_Q12_INTERFACES_OK`.

---

### Task 5: Draft symmetry-aware architectures and compact representation theory, Q13–Q14

**Files:**
- Modify outside repository: `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md`
- Read: `draft/main.tex:1002-1036`
- Read: verified representation-theory and equivariant-ML sources from Task 1

**Interfaces:**
- Consumes: exact reduction and ML-socket taxonomy.
- Produces: a nonconflating comparison of reduction/equivariance/regularization and a corrected compact-group representation account with an explicit noncompact boundary.

- [ ] **Step 1: Write Q13 as a three-strategy comparison**

Use a table with rows:

1. invariant-solution reduction: impose `Q=0`, pass to quotient coordinates, and learn/solve a profile;
2. equivariant architecture: retain the full domain and require
   $$
   \Phi(\rho_{\mathrm{in}}(g)x)
   =\rho_{\mathrm{out}}(g)\Phi(x);
   $$
3. symmetry regularization or augmentation: penalize sampled defects or add transformed observations.

Columns must state domain retained, guarantee, learned object, data compatibility requirement, and failure mode. Explain that a sampled penalty does not certify global equivariance and that an equivariant architecture does not imply the output is fixed by the group.

- [ ] **Step 2: Introduce compact representation theory only after its scope is stated**

Open Q14 by stating that translations, scalings, boosts, and affine PDE symmetry groups are often noncompact. Therefore the compact Peter–Weyl machinery below is a specialized architecture tool, not the universal foundation of the manuscript’s reductions.

For compact `G` with normalized Haar measure and unitary dual `G-hat`, state:

$$
\left\{\sqrt{d_\lambda}\,D_{ij}^{\lambda}
:\lambda\in\widehat G,\ 1\le i,j\le d_\lambda\right\}
$$

is an orthonormal basis of `L^2(G)` under the declared coefficient convention, and

$$
L^2(G)\cong
\widehat{\bigoplus}_{\lambda\in\widehat G}
V_\lambda\otimes V_\lambda^*.
$$

Define every symbol.

- [ ] **Step 3: State Schur’s lemma and linear layer constraints correctly**

Use multiplicity spaces:

$$
V_{\mathrm{in}}
\cong\bigoplus_{\lambda}
M_{\mathrm{in}}^\lambda\otimes V_\lambda,
\qquad
V_{\mathrm{out}}
\cong\bigoplus_{\lambda}
M_{\mathrm{out}}^\lambda\otimes V_\lambda.
$$

For complex irreducibles, state:

- inequivalent irreducibles have zero intertwiner space;
- equivalent irreducibles have scalar intertwiners after identifying the copies.

Then derive

$$
L=\bigoplus_{\lambda}
W_\lambda\otimes I_{V_\lambda}.
$$

Do not repeat the source’s erroneous identical hypotheses for both Schur cases.

- [ ] **Step 4: Qualify convolution and nonlinear operations**

State that sufficiently regular translation-equivariant operators can be represented as group convolutions, while general bounded intertwiners may require kernels that are measures or distributions rather than `L^2` filters. Fix one Fourier convention before stating multiplication order.

For nonlinearities, distinguish:

- pointwise scalar nonlinearities on regular scalar feature fields, which can be equivariant;
- nontrivial irreducible feature types, for which arbitrary coordinatewise nonlinearities generally fail;
- tensor products, Clebsch–Gordan projections, invariant norms, and scalar gating as construction tools rather than a universal factorization theorem.

- [ ] **Step 5: Run the representation-theory correction gate**

Run:

```bash
python -I - <<'PY'
from pathlib import Path
s = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md").read_text(encoding="utf-8")
for q in (13, 14):
    assert f"### Q{q}." in s
for phrase in (
    "invariant-solution reduction", "equivariant architecture",
    "symmetry regularization", "noncompact", "unitary dual",
    "inequivalent irreducibles", "multiplicity"
):
    assert phrase.lower() in s.lower(), phrase
bad_claims = (
    "every bounded linear equivariant operator",
    "standard point-wise non-linearities generally do not preserve",
    "any continuous, polynomial, or analytic equivariant"
)
for phrase in bad_claims:
    assert phrase.lower() not in s.lower(), phrase
print("Q13_Q14_REPRESENTATION_OK")
PY
```

Expected: `Q13_Q14_REPRESENTATION_OK`.

---

### Task 6: Draft certification, workflow, and verified references, Q15–Q16

**Files:**
- Modify outside repository: `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md`
- Read: `draft/main.tex:378-414`
- Read: `draft/main.tex:495-516`
- Read: `draft/main.tex:1169-1199`
- Read: `draft/main.tex:1257-1352`
- Read: citation ledger from Task 1

**Interfaces:**
- Consumes: all preceding mathematical and evidentiary distinctions.
- Produces: certification ladder, final project decision workflow, honest negative cases, and compact verified bibliography.

- [ ] **Step 1: Write Q15 as an implication ladder**

Distinguish:

$$
\text{training objective}
\;\not\Rightarrow\;
\text{held-out residual norm}
\;\not\Rightarrow\;
\text{profile error}
\;\not\Rightarrow\;
\text{physical-field error}.
$$

Then state sufficient interfaces rather than promises. A residual-to-profile estimate has the form

$$
\|\widehat F-F\|_X
\le C_{\mathrm{stab}}
\|\mathcal R[\widehat F]\|_Y,
$$

when a problem-specific stability theorem supplies finite `C_stab`. Reconstruction requires

$$
\|\mathcal T\widehat F-\mathcal T F\|_Z
\le L_{\mathcal T}\|\widehat F-F\|_X.
$$

Explain controlled quadrature, data mismatch, chart/branch guards, held-out parameters, independent original-PDE evaluation, and why a certificate on a reduced ODE is not automatically a certificate for an unrestricted PDE solution.

- [ ] **Step 2: Include the seven evidence labels**

Define and use consistently:

- Exact;
- Certified;
- Conditional;
- Numerically verified;
- Empirical;
- Candidate;
- Unsupported/out of scope.

Give one Lie–ML example for each label. Do not call a finite collocation residual exact.

- [ ] **Step 3: Write Q16 as the project decision workflow**

Use

$$
\boxed{
\text{specify}
\to\text{classify or verify}
\to\text{reduce}
\to\text{analyze}
\to\text{learn only the unresolved part}
\to\text{reconstruct}
\to\text{verify}
}.
$$

Add a decision table with pass and fail routes for:

- symmetry classification/verification;
- boundary and initial data compatibility;
- regular quotient construction;
- analytical closure or approximation;
- certificate availability;
- demonstrated ML value against conventional solvers.

The fail routes must include another subgroup/chart, a reduced PDE rather than ODE, a conventional solver, a full-space baseline, an explicitly conditional approximate-symmetry branch, and an out-of-scope result.

- [ ] **Step 4: Anchor the workflow to the companion manuscript without duplicating it**

Explain that the manuscript’s primary socket is

$$
\widehat F_\theta
=F_{\mathrm{an}}+\omega N_\theta,
\qquad
\widehat u_\theta=\mathcal T_{\lambda,H}\widehat F_\theta.
$$

State the project’s negative evidence plainly: for a single reduced SVE initial-value query, the conventional DOP853 solver is much faster than neural training; the more plausible neural use is amortization over a parameter/data family, and even that requires a measured break-even analysis and held-out tests.

Do not copy historical numerical values unless they are directly checked against the manuscript and clearly labelled as manuscript-reported evidence.

- [ ] **Step 5: Add “Research boundary” and “Verified references” sections**

End the substantive Q&A with the approved scope statement: the core program concerns parameter-dependent PDE problems admitting a useful, data-compatible reduction on a declared regular stratum; its primary learned object is the reduced profile family or a quantitatively identified remainder.

Add a compact reference list. Each entry must include:

- authors;
- title;
- year;
- DOI or official URL;
- `✅ opened and claim checked`;
- the Q&A questions for which it supplies evidence.

Do not include a source merely because it appears in `draft/references.bib`.

- [ ] **Step 6: Run the completion gate for Q15–Q16 and references**

Run:

```bash
python -I - <<'PY'
from pathlib import Path
s = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md").read_text(encoding="utf-8")
for q in (15, 16):
    assert f"### Q{q}." in s
for phrase in (
    "training objective", "held-out residual", "profile error",
    "physical-field error", "stability", "reconstruction",
    "Exact", "Certified", "Conditional", "Numerically verified",
    "Empirical", "Candidate", "Unsupported/out of scope",
    "Research boundary", "Verified references"
):
    assert phrase.lower() in s.lower(), phrase
assert "✅" in s
print("Q15_Q16_CERTIFICATION_OK")
PY
```

Expected: `Q15_Q16_CERTIFICATION_OK`.

---

### Task 7: Perform independent mathematical, citation, and readability audits

**Files:**
- Modify outside repository if corrections are required: `C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md`
- Read: complete approved specification
- Read: complete temporary rewrite
- Read: citation ledger

**Interfaces:**
- Consumes: the complete Q1–Q16 draft.
- Produces: a corrected, source-verified draft that satisfies every specification item before installation.

- [ ] **Step 1: Run a fresh pure-ML review**

Assign a reviewer who did not draft Part I. Require a line-by-line report on:

- risk and empirical-risk definitions;
- loss-dependent Bayes targets;
- approximation/estimation/optimization distinctions;
- model-family comparisons;
- generalization versus validation claims;
- accessibility to a PDE researcher new to ML;
- absence of unexplained Part II concepts.

Accept a suggested change only after checking the underlying mathematics or source. Record rejected suggestions and the reason in the execution notes rather than altering correct text performatively.

- [ ] **Step 2: Run a fresh Lie/PDE/representation review**

Assign a different reviewer. Require checks of:

- prolongation versus invariant-surface conditions;
- characteristic `Q` versus evolutionary representative `v_Q`;
- orbit/stabilizer/quotient distinctions;
- transversality, rank, and data-compatibility gates;
- direct versus reduced PINN comparison;
- compactness boundary for Peter–Weyl;
- Schur hypotheses and multiplicity-space layer form;
- convolution and nonlinearity qualifications;
- certification implications.

Again, independently verify every accepted finding.

- [ ] **Step 3: Check all twenty-three source corrections from the specification**

Use specification section 11 as a literal checklist. In particular, verify that the draft:

- does not universalize inverse-problem language;
- qualifies uniform convergence and empirical-risk consistency;
- restricts conditional-expectation claims to squared loss;
- handles evaluation continuity topology-dependently;
- avoids treating a singular Fisher matrix as automatically Riemannian;
- distinguishes mean-field continuity equations from diffusive Fokker–Planck equations if either remains;
- removes the symmetry-group-volume sample-complexity claim;
- corrects symplectic/energy and Banach fixed-point claims;
- states nonlinear infinitesimal equivariance correctly;
- uses `G-hat` for the unitary dual;
- states Schur’s lemma correctly;
- qualifies convolution and pointwise nonlinearities;
- removes universal equivariant-factorization language;
- removes unresolved citation markers and malformed copied mathematics.

Delete unnecessary topics instead of retaining them solely because they appeared in the source document.

- [ ] **Step 4: Audit every citation against the ledger**

For each in-text citation, require a matching ledger row marked `✅` and a matching verified-reference entry. For each verified-reference entry, require at least one actual supporting use in the Q&A. Remove orphan references and unsupported performance numbers.

- [ ] **Step 5: Run the full structural audit on the temporary draft**

Run:

```bash
python -I - <<'PY'
from pathlib import Path
import re

p = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md")
s = p.read_text(encoding="utf-8")
questions = [int(x) for x in re.findall(r"^### Q(\d+)\.", s, flags=re.M)]
assert questions == list(range(1, 17)), questions
part1 = s[s.index("## Part I."):s.index("## Part II.")]
for forbidden in ("PINN", "collocation", "PDE", "Lie", "invariant-surface", "reduced profile"):
    assert forbidden not in part1, forbidden
markers = ["T"+"ODO", "T"+"BD", "FIX"+"ME", "PLACE"+"HOLDER", "[ci"+"te:"]
for marker in markers:
    assert marker not in s, marker
assert "neccessary" not in s
assert "gemini.google.com/app" not in s
assert s.count("$$") % 2 == 0
assert "Q^\\alpha" in s and "\\mathbf v_Q" in s
assert "\\widehat G" in s
assert "data compatibility" in s.lower()
assert "original PDE" in s
print("FULL_STRUCTURE_OK", len(s.splitlines()), "lines")
PY
```

Expected: `FULL_STRUCTURE_OK <N> lines` with no assertion failure.

- [ ] **Step 6: Run a prose pass for formality and readability**

Read the document continuously, not only by section. Correct:

- paragraph openings that repeat the same formula without motivation;
- undefined acronyms;
- sentences exceeding a reasonable cognitive load;
- headings that do not receive a direct answer in their first paragraph;
- abrupt changes from general ML to project-specific claims;
- excessive block quotations or decorative jargon;
- duplicated warnings that can be consolidated without weakening scope.

Require every question to end with either a concrete implication, a limitation, or a decision rule.

---

### Task 8: Install the audited rewrite and verify repository scope

**Files:**
- Replace: `docs/The Mathematical Essence of Machine Learning.md`
- Read: original backup and complete temporary rewrite
- Do not modify or stage any other file

**Interfaces:**
- Consumes: the fully audited temporary draft and the pre-edit Git status snapshot.
- Produces: the final project deliverable plus evidence that unrelated working-tree state was preserved.

- [ ] **Step 1: Atomically replace the target after rechecking the backup**

Run:

```bash
python -I - <<'PY'
from hashlib import sha256
from pathlib import Path
import os

root = Path(r"D:/MATHs/math 4890 LieML")
target = root / "docs/The Mathematical Essence of Machine Learning.md"
backup = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-qa-original-2026-10-08.md")
rewrite = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-qa-rewrite-2026-10-08.md")
tmp = target.with_suffix(target.suffix + ".installing")
assert backup.exists() and rewrite.exists()
assert target.read_bytes() == backup.read_bytes(), "Target changed after backup; stop and reconcile"
data = rewrite.read_bytes()
assert data.strip(), "Rewrite is empty"
tmp.write_bytes(data)
os.replace(tmp, target)
print("ORIGINAL_SHA256", sha256(backup.read_bytes()).hexdigest())
print("FINAL_SHA256", sha256(target.read_bytes()).hexdigest())
PY
```

Expected: two different nonempty digests and no `.installing` file left behind.

- [ ] **Step 2: Re-run the full structural audit against the installed target**

Run the Task 7 structural script again with:

```python
p = Path(r"D:/MATHs/math 4890 LieML/docs/The Mathematical Essence of Machine Learning.md")
```

Expected: the same `FULL_STRUCTURE_OK` result.

- [ ] **Step 3: Inspect the complete original-to-final diff**

Run:

```bash
git diff --no-index -- \
  'C:/Users/Administrator/AppData/Local/Temp/lieml-qa-original-2026-10-08.md' \
  'D:/MATHs/math 4890 LieML/docs/The Mathematical Essence of Machine Learning.md' \
  > 'C:/Users/Administrator/AppData/Local/Temp/lieml-qa-final.diff' || test $? -eq 1
```

Read the complete diff. Confirm that it is a conceptual rewrite rather than a partial append, that Q1–Q5 precede all PDE/Lie material, and that no source placeholder, chat link, or broken copied equation survived.

- [ ] **Step 4: Verify that no unrelated repository state changed**

Run:

```bash
git status --porcelain=v1 > 'C:/Users/Administrator/AppData/Local/Temp/lieml-status-after-2026-10-08.txt'
python -I - <<'PY'
from pathlib import Path
before = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-status-before-2026-10-08.txt").read_text()
after = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-status-after-2026-10-08.txt").read_text()
assert before == after, (before, after)
print("WORKTREE_SCOPE_PRESERVED")
PY
```

Expected: `WORKTREE_SCOPE_PRESERVED`. This verifies the status categories, but not yet the bytes of paths that were already dirty.

- [ ] **Step 5: Verify every unrelated dirty path byte-for-byte**

Run:

```bash
python -I - <<'PY'
from hashlib import sha256
from pathlib import Path
import json, subprocess

root = Path(r"D:/MATHs/math 4890 LieML")
before_path = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-dirty-manifest-before-2026-10-08.json")
before = json.loads(before_path.read_text(encoding="utf-8"))
for rel, expected in before.items():
    p = root / rel
    actual_kind = "file" if p.is_file() else "missing-or-directory"
    actual_hash = sha256(p.read_bytes()).hexdigest() if p.is_file() else None
    assert actual_kind == expected["kind"], (rel, expected["kind"], actual_kind)
    assert actual_hash == expected["sha256"], (rel, expected["sha256"], actual_hash)
print("UNRELATED_DIRTY_BYTES_PRESERVED", len(before))
PY
```

Expected: `UNRELATED_DIRTY_BYTES_PRESERVED <N>`. Any mismatch is a blocker; do not restore or overwrite the user’s file automatically.

- [ ] **Step 6: Confirm that execution did not change the staged-file set**

Run:

```bash
git diff --cached --name-only > 'C:/Users/Administrator/AppData/Local/Temp/lieml-staged-after-2026-10-08.txt'
python -I - <<'PY'
from pathlib import Path
before = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-staged-before-2026-10-08.txt").read_text()
after = Path(r"C:/Users/Administrator/AppData/Local/Temp/lieml-staged-after-2026-10-08.txt").read_text()
assert before == after, (before, after)
print("STAGED_SCOPE_PRESERVED")
PY
```

Expected: `STAGED_SCOPE_PRESERVED`. Do not run `git add`, `git commit`, or `git push` during implementation.

- [ ] **Step 7: Prepare the completion report**

Report:

- the final file link;
- the Q1–Q5 pure-ML / Q6–Q16 ML–Lie structure;
- the precise definition of `Q^alpha` and `v_Q`;
- the small computations actually run;
- the citation and mathematical audits actually completed;
- any claim removed because verification failed;
- the fact that no unrelated file was modified, staged, committed, or pushed.

Do not claim success if any gate above failed; state the exact failed command and leave the target at the last verified state.
