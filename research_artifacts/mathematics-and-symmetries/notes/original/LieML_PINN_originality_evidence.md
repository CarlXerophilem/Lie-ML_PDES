# LieML: evidence for a defensible PINN contribution

Research memo — 6 September 2026

## Recommendation

Adding a neural network is scientifically plausible, but does not establish originality. The most defensible direction for this project is a **boundary-compatible, branch-aware neural correction of Lie-reduced semi-analytic solutions, with independently checked error bounds**. This is a proposed research contribution, not a verified first-of-its-kind result.

Separate three questions:

1. **Feasibility:** can a physics-informed network solve the reduced equation? Existing literature and project prototypes support this direction.
2. **Added value:** does a HAM prior, neural correction, or symmetry formulation improve accuracy, cost, reliability, or generalization? This requires controlled experiments in this project.
3. **Originality:** is the particular capability absent from the closest prior work? Broad combinations already overlap existing papers. This focused search narrows a candidate contribution; it does not prove absence from all literature.

For a course project, independently deriving and implementing the pipeline can be a substantial contribution. For a research-paper novelty claim, demonstrate a new capability or result beyond combining known components.

Scope: read-only inspection of repository snapshot `fbdcfe361bc98027f33e639a803a93a40c393045`; primary-source literature checked through the search date. No production files were edited. No PINN training or published benchmark was reproduced during this review. A small exact-arithmetic manufactured check of the Blasius residual identity was run. The selected Deep Research plugin was not exposed in this session; this memo was produced through direct literature research.

## 1. What is already established

The descriptions below distinguish authors' reported results from independently reproduced findings.

| Primary source | Evidence and scope | Consequence for the project's claim |
| --- | --- | --- |
| Akhound-Sadegh et al., [Lie Point Symmetry and Physics Informed Networks](https://arxiv.org/abs/2311.04293), NeurIPS 2023 | Introduces a Lie-point-symmetry loss for PINNs and reports improved sample efficiency on its experiments. | “We combine Lie symmetry and PINNs” is not new. |
| Arora, Bihlo and Valiquette, [Invariant Physics-Informed Neural Networks for Ordinary Differential Equations](https://arxiv.org/abs/2310.17053), 2023, revised 2024 | Uses differential invariants, equivariant moving frames, and reconstruction equations in a PINN method for ODEs. | “We solve in invariant coordinates and reconstruct” has close precedent. Their moving-frame construction is not identical to selecting a PDE invariant-solution family. |
| Mutuk, [A Neural Network Study of Blasius Equation](https://doi.org/10.1007/s11063-019-10184-9), 2020 | Uses neural networks to approximate the Blasius problem. | Blasius plus a neural network is not an original application by itself. |
| Uddin, [Physics Informed Optimal Homotopy Analysis Method](https://arxiv.org/abs/2601.09567), January 2026 preprint | Optimizes HAM convergence-control parameters using a physics-informed residual objective; demonstrates Blasius. | Physics-informed optimization of HAM on Blasius is direct overlap. This is not automatically the same as training a neural remainder. Treat its performance claims as reported, not reproduced here. |
| Wang and Lai, [Multi-stage Neural Networks: Function Approximator of Machine Precision](https://arxiv.org/abs/2307.08934), 2023 preprint | Successive networks fit remaining errors; includes physics-informed examples. | Learning corrections or using multiple neural stages is established. A small remainder alone does not imply an easy training problem. |
| Hillebrecht and Unger, [Certified machine learning: A posteriori error estimation for physics-informed neural networks](https://arxiv.org/abs/2203.17055), IJCNN 2022 | Derives solution-independent a posteriori error bounds for ODE PINNs under stated hypotheses. | PINN error certification is not new. An IVP result cannot simply be relabeled as a semi-infinite nonlinear BVP certificate. |
| Huseynov, Ahmadova and Bashirov, [Reliable Error Estimation for PINNs: Lower and Upper A Posteriori Bounds](https://arxiv.org/abs/2606.12050), June 2026 preprint | Gives localized ODE error estimates and explicitly formulates certificate-informed training. | Even “certificate-informed PINN training” is too broad a novelty claim. The retrieved work is formulated for initial-value ODE problems. |
| Klausen et al., [LieSolver](https://arxiv.org/html/2510.25731v1), October 2025 preprint | Uses symmetry-generated exact PDE solutions and fits boundary/initial data; implemented for linear homogeneous PDEs. | Symmetry-built models with reliability arguments are prior art. Do not overstate its certification: its contributions section explicitly says rigorous bounds are not proved there. |
| Wang et al., [Generalized Lie Symmetries in Physics-Informed Neural Operators](https://arxiv.org/html/2502.00373v2), 2025 | Shows that some point-symmetry penalties add no training information; studies evolutionary representatives on Burgers and Darcy neural operators. | More symmetry-loss terms do not automatically improve learning. This is a neural-operator study, not direct evidence for a Falkner–Skan PINN. |
| Belden et al., [Asymptotic Approximant for the Falkner–Skan Boundary-Layer Equation](https://arxiv.org/abs/1907.09912), 2019 | Constructs non-neural analytic approximations and studies positive- and negative-wall-shear branches. | A serious comparison should include a strong semi-analytic method, not only a basic PINN. Approximate closed expressions are not exact solutions. |

### A concrete result—and its limit

Table 1 of [Wang et al.](https://arxiv.org/html/2502.00373v2) reports Burgers solution-loss values of `0.082 ± 0.006` with its generalized-symmetry method versus `0.089 ± 0.006` for its no-symmetry PINO at 25 samples. At 50 samples, both reported means are `0.044`. This is evidence that symmetry can help in a tested setting, not evidence of a universal large improvement or of a gain for our proposed model. The reported spreads also caution against reading a small mean difference as conclusive without the full experiment.

## 2. What the repository actually supports

These are code-inspection findings, not newly measured training outcomes. File links are pinned to the inspected commit.

| Inspected component | What it contains | What remains unproved |
| --- | --- | --- |
| [pinn_corrector_demo.py](https://github.com/CarlXerophilem/Lie-ML_PDES/blob/fbdcfe361bc98027f33e639a803a93a40c393045/symm/pinn_corrector_demo.py) | A 321-parameter reduced Fisher PINN with an endpoint-compatible linear baseline plus a masked network. | Despite its name, this particular demo does not correct a HAM prior. |
| [sacno_curriculum_warmstart.py](https://github.com/CarlXerophilem/Lie-ML_PDES/blob/fbdcfe361bc98027f33e639a803a93a40c393045/symm/sacno/sacno_curriculum_warmstart.py) | Actual HAM-to-PINN experiments: 12-seed cold/warm comparisons and a frozen-additive-prior experiment. Its comments report no warm-start advantage in the tested Fisher regime and a boundary-mismatch failure. | The recorded negative finding must not be replaced by an unverified speedup claim. The script was not rerun here. Total-cost comparison must count HAM construction and the extra warm-start optimization. |
| [sacno_parametric_operator.py](https://github.com/CarlXerophilem/Lie-ML_PDES/blob/fbdcfe361bc98027f33e639a803a93a40c393045/symm/sacno/sacno_parametric_operator.py) | A supervised MLP fitted to exact Burgers profiles with held-out scalar parameters. | This is not physics-informed training. Finite-parameter interpolation is not by itself evidence of general function-space operator learning. |
| [fisher_kpp_reduction.py](https://github.com/CarlXerophilem/Lie-ML_PDES/blob/fbdcfe361bc98027f33e639a803a93a40c393045/symm/fisher_kpp_reduction.py) | Symmetry/reduction checks, truncated HAM terms, sampled term ratios, residual minimization and an IVP comparison. | Finitely many ratios below one do not establish an all-orders convergence certificate. Both the homotopy-order and polynomial truncations require attention. |
| [ml_pde_solver_demo.py](https://github.com/CarlXerophilem/Lie-ML_PDES/blob/fbdcfe361bc98027f33e639a803a93a40c393045/symm/ml_pde_solver_demo.py) | A full-coordinate PINN with an injectable analysis interface and an explicitly null default. | Having an interface is not evidence of a verified, integrated HAM–PINN–certificate pipeline. |

The most useful existing result is the negative warm-start experiment. It asks the right question: **when does an analytic prior genuinely help?** A regime map with reproducible positive and negative results could be more persuasive than another successful plot of Blasius.

### Boundary mismatch: a precise explanation

For an additive ansatz

\[
v_\theta(s)=v_H(s)+b(s)N_\theta(s),\qquad b(s_L)=b(s_R)=0,
\]

the endpoint values remain those of the prior, regardless of training. If the prior has an endpoint error, this architecture cannot remove it. In particular, its uniform error cannot be less than the largest endpoint error.

This does **not** prove that every additive corrector fails, or that its interior relative-L2 error cannot improve. Repair the prior's boundary traces, or allow an appropriate boundary correction, before testing the additive strategy. Boundary lifting is a classical device; its use alone is not the novelty.

### Finite ratios are a diagnostic

The scalar sequence with terms `2^(-n)` for the first eight indices and `2^n` thereafter has seven observed ratios equal to one half, but its infinite sum diverges. Thus observed decreasing ratios cannot logically certify an unknown tail. A HAM recurrence may provide additional structure to prove a tail estimate, but that proof has to be supplied. Use labels such as `observed-contraction`, `tail-unproved`, and `error-bound-verified` for distinct statements.

## 3. Recommended research design

### Core question

Can a boundary-compatible neural remainder, conditioned on a genuine reduced-problem parameter and solution branch, improve the **total cost of obtaining an independently verified solution** over both a reduced PINN and strong non-neural solvers?

This is a testable question, not a forecast that the neural model will win.

### Fluid benchmark

Use the steady Prandtl system with exterior velocity \(U_e(x)=U_0x^m\):

\[
u_x+v_y=0,\qquad
uu_x+vu_y=U_eU_e'+\nu u_{yy}.
\]

Work on \(x>0\), \(\nu>0\), \(U_0>0\), initially with \(m>-1\), and set \(u=\psi_y,\ v=-\psi_x\). Direct scaling analysis gives the stream-function generator

\[
X=x\partial_x+\frac{1-m}{2}y\partial_y
  +\frac{m+1}{2}\psi\partial_\psi.
\]

Its invariant ansatz is

\[
\eta=y\sqrt{\frac{(m+1)U_e(x)}{2\nu x}},\qquad
\psi=\sqrt{\frac{2\nu xU_e(x)}{m+1}}\,f(\eta),
\]

and substitution yields

\[
\mathcal N_\beta[f]=f'''+ff''+\beta(1-f'^2)=0,
\quad \beta=\frac{2m}{m+1},
\]

with \(f(0)=f'(0)=0\), \(f'(\infty)=1\). These are classical equations, not proposed discoveries. [Belden et al.](https://arxiv.org/abs/1907.09912) supplies a useful comparison for the parameter family and its nonunique adverse-gradient cases.

The following residual identity is independently derived here by the chain rule:

\[
uu_x+vu_y-U_eU_e'-\nu u_{yy}
=-\frac{(m+1)U_e(x)^2}{2x}\,\mathcal N_\beta[f].
\]

It is a valuable target for a machine-checkable reconstruction test. It does not alone prove boundary compatibility, completeness of all symmetries, or completeness of all solutions.

### Neural architecture with the right constraints

For a first finite-domain experiment on \([0,L]\), replace the far-field boundary condition by \(f'(L)=1\). This is a truncated BVP; it is not yet the original infinite-domain problem.

Define the boundary projection

\[
\mathcal B_L[h](\eta)
=h(\eta)-h(0)-\eta h'(0)
-\frac{\eta^2}{2L}\bigl(h'(L)-h'(0)\bigr).
\]

Direct differentiation shows

\[
\mathcal B_L[h](0)=\mathcal B_L[h]'(0)
=\mathcal B_L[h]'(L)=0.
\]

This projection does not unnecessarily fix \(f(L)\). One candidate architecture is

\[
f_\theta(\eta;\beta,b)
=\frac{\eta^2}{2L}
+\mathcal B_L\left[f_H(\cdot;\beta,b,\hbar,M)
+N_\theta(\cdot,\beta,b)\right](\eta),
\]

where \(f_H\) is the finite semi-analytic prior, \(M\) its order, \(\hbar\) its convergence-control parameter, and \(b\) a branch identifier where needed. The affine lift supplies the required boundary traces; both the prior and neural remainder contribute only compatible corrections.

Train with the **full nonlinear residual** \(\mathcal N_\beta[f_\theta]\), not by fitting unknown true errors. An optional sparse-data loss must be disclosed. Hard boundary conditions and a stream-function representation enforce selected constraints; they do not enforce momentum exactly before training.

Call this a parameter-conditioned PINN. It becomes a broader neural-operator claim only with an appropriate function-input/operator-learning formulation and evaluation.

### Why a parameter family matters

Changing \(x\), \(U_\infty\), or \(\nu\) in Blasius merely rescales one dimensionless profile. A neural model reproducing those transformations has not learned different dimensionless dynamics. Test changes in \(\beta\), or another parameter that survives reduction.

For negative pressure-gradient parameters, branch ambiguity must be handled explicitly. Do not ask one deterministic map \((\eta,\beta)\mapsto f\) to represent two different solutions at identical inputs. Use separate branch models, a branch label, or continuation coordinates. The claim is numerical branch resolution, not proof that every computed branch is dynamically stable or physically realized.

### What might make the project distinct

- Automatically verify the selected PDE reduction and its boundary compatibility.
- Repair prior boundary traces before neural correction and compare this with warm-starting.
- Learn across genuine reduced-problem parameters, with branch-aware evaluation.
- Independently verify a posteriori bounds for the final corrected nonlinear BVP solution.
- Use verification failure to request refinement or return an honest inconclusive result.
- Map where the hybrid helps, where it does not, and why.

Every item has precedents in some form. The possible contribution lies in a demonstrated, carefully scoped capability at their intersection. Neither this search nor a list of components establishes priority.

## 4. What an actual error certificate would require

The June 2026 [localized PINN error-estimation preprint](https://arxiv.org/html/2606.12050) already proposes certificate-informed training. Merely adding a confidence term to a loss cannot be the new claim. Its IVP formulation also does not automatically establish a Falkner–Skan BVP certificate.

For the finite-domain BVP define, for example,

\[
\mathcal F(f)
=\bigl(\mathcal N_\beta[f],f(0),f'(0),f'(L)-1\bigr),
\]

as a map from \(C^3([0,L])\) to \(C^0([0,L])\times\mathbb R^3\), with specified Banach norms. Its differential-equation linearization at \(\hat f\) is

\[
D\mathcal N_\beta[\hat f]h
=h'''+\hat f h''+\hat f''h-2\beta\hat f'h'.
\]

The boundary traces must be part of the linearized BVP operator too.

A classical sufficient validation argument is as follows. Suppose \(A=D\mathcal F(\hat f)\) is invertible, a verified bound \(\|A^{-1}\|\le M_A\) is available, \(\|\mathcal F(\hat f)\|\le\varepsilon\), and the derivative is Lipschitz with constant \(K\) throughout a ball of radius \(r\). If

\[
M_A\varepsilon+\tfrac12 M_AKr^2\le r,
\qquad M_AKr<1,
\]

then a contraction argument gives a unique exact BVP solution in that ball, with error at most \(r\). This is a standard local validation principle, not a claimed new theorem. Its concrete realization here is proposed, not implemented.

The real work is obtaining trustworthy constants, enclosing residuals between collocation points, treating floating-point error, and verifying invertibility. An approximate inverse requires an additional inverse-defect estimate; a sampled matrix condition number is not a proof for the continuous operator.

Important distinctions:

1. A sampled PINN residual is not a uniform residual bound.
2. A small residual need not imply a small solution error when the BVP is ill-conditioned.
3. Failure to verify an inverse or tail bound means **inconclusive**, not necessarily an inaccurate approximation.
4. A certificate for \([0,L]\) requires an additional tail argument before it covers \([0,\infty)\).
5. The final corrected approximation needs its own certificate; a certificate for the prior is not inherited automatically.
6. Reconstruction can propagate profile error bounds to the selected invariant PDE solution on a specified domain. It does not certify arbitrary PDE solutions, Navier–Stokes modeling error, or experimental accuracy.
7. A small \(\|f-\hat f\|\) alone does not bound wall shear. The norm must also control \(f''\), or a separate observable bound is needed.

### Correction to the previous answer

For its normalization \(\eta_B=y\sqrt{U_\infty/(\nu x)}\), \(\psi=\sqrt{\nu U_\infty x}\,f_B\), the residual identity should read

\[
\psi_y\psi_{xy}-\psi_x\psi_{yy}-\nu\psi_{yyy}
=-\frac{U_\infty^2}{x}
\left(f_B'''+\tfrac12 f_Bf_B''\right).
\]

The sign and dimensional prefactor in the earlier answer were incorrect; its zero-residual ODE remains unchanged. An exact-rational manufactured check with \(U_\infty=9\), \(\nu=4\), \(x=4\), \(y=2\), \(f_B(\eta)=1+\eta+\eta^3\) gave `-42039/64` on both sides.

Also keep the two Blasius normalizations distinct. In the Falkner–Skan convention above, the coefficient of \(ff''\) is one, not one half. Writing \(f_B(\eta_B)=\sqrt2 f(\eta_B/\sqrt2)\) converts between them. Do not compare their wall-shear numbers without this conversion.

## 5. Minimum evidence package

### Controlled comparisons

| Arm | Purpose |
| --- | --- |
| Full-coordinate stream-function PINN | Measures the benefit of known symmetry reduction, not neural correction alone. |
| Lie-reduced PINN without HAM | Isolates the prior's incremental value. |
| HAM or another semi-analytic prior alone | Tests whether ML is necessary. |
| HAM warm-start followed by PINN training | Competes with frozen additive correction; include warm-start cost. |
| Boundary-compatible HAM plus neural remainder | The proposed hybrid. |
| Uncorrected-boundary additive prior | A deliberate negative control for the specific masking failure. |
| Efficient BVP solver, plus a semi-analytic reference | Tests whether the full hybrid offers practical value. |

For a claim about neural correction itself, add a comparable multistage correction baseline. For a claim about certificates improving training, compare matched runs with and without the certificate-based training mechanism while keeping final verification identical.

Use classical shooting with appropriate stabilization or adaptive collocation, and consider the [Falkner–Skan asymptotic approximant](https://arxiv.org/abs/1907.09912). That approximant uses numerical inputs such as wall shear/asymptotic constants in its construction; include their acquisition cost rather than giving any arm privileged information.

### Problem splits

- Retain a closed-form Fisher or Burgers case as a correctness regression.
- Use Blasius as a pipeline sanity check, not the only originality demonstration.
- Hold out entire Falkner–Skan parameter values, not just coordinate points from training profiles.
- Separate interpolation, extrapolation, positive-shear and negative-shear branch tests.
- Include adverse-gradient cases approaching the classical separation regime, without promising a valid boundary-layer physical model after separation.
- Include at least one deliberately incompatible boundary/inlet condition to test whether a hard similarity ansatz is incorrectly accepted.

### Measurements

Report profile and velocity errors, absolute wall-shear error, boundary errors, verified error radius when available, failed/inconclusive cases, network size, and the complete cost of prior construction, tuning, training, verification, and inference. Wall-shear relative error is unsuitable when the reference shear approaches zero.

Use repeated seeds, paired parameter splits, comparable tuning budgets, and the same boundary data. Count actual residual evaluations and wall time: equal optimizer iteration counts need not imply equal compute. Never use held-out exact profiles to choose hyperparameters or certify error.

For many-query claims, report the break-even query count from

\[
T_{\rm build}+T_{\rm train}+Q(T_{\rm infer}+T_{\rm verify})
<Q T_{\rm reference},
\]

with all costs measured on the same tasks. Include a tabulated-profile/interpolation baseline: a low-dimensional parameter family may not need a neural network.

Fair comparisons matter: [McGreivy and Hakim](https://arxiv.org/html/2407.07218) found weak baselines in 60 of 76 surveyed papers claiming an advantage for ML fluid-related PDE solvers. Their systematic review excluded PINN papers; that percentage must not be misquoted as a PINN failure rate. The relevant lesson is equal-accuracy or equal-time comparisons against efficient methods, not an exact-solution-only rule.

### Falsifiable outcomes

- If reduced PINN and hybrid are indistinguishable at matched total cost, the HAM-benefit claim fails in that regime.
- If a standard BVP solver or interpolation table wins, do not announce a forward-solver speedup. A narrower verification or representation result may remain.
- If prior correction fixes boundary error but not convergence, boundary compatibility was necessary but insufficient.
- If the residual decreases but the independent bound is unavailable, report improved residual with inconclusive certification.
- If changing only dimensional Blasius scales is the sole successful generalization test, claim symmetry-consistent reconstruction, not new-physics generalization.
- If branch selection fails, do not hide those runs by reporting only the best seed.

## 6. A more ambitious second direction

Once the exact-symmetry pipeline works, study a **symmetry-compatible component plus a symmetry-breaking neural correction** for perturbed boundary or inlet data. The motivation is structural: an architecture constrained to one invariant family cannot represent a target outside that family.

For incompressible flow, represent both components through a stream function so continuity remains satisfied. Let the extra component depend on an orbit coordinate as well as the invariant coordinate; use a normalization or gauge to avoid an ambiguous decomposition. Test the full PDE residual and actual boundary conditions.

This extension may give ML a more substantial role, but it expands the problem beyond a reduced ODE. The ODE certificate cannot certify the symmetry-breaking component. Perturbation analysis or a new full-PDE estimate would be required. Treat this as a separate later research question, not an extra claim attached to the first prototype.

## 7. Claim language and decision

Safe now: the project investigates Lie-reduced, boundary-compatible semi-analytic/PINN hybrids and their reliability on selected fluid boundary-value problems.

Potentially defensible after implementation: a reproducible branch-aware correction-and-verification workflow with a demonstrated advantage on specified held-out parameter regimes and explicit failure reporting.

Not supported now: first Lie–PINN method; first invariant-coordinate PINN; first physics-informed HAM method; first certified PINN; universal convergence; a general Navier–Stokes solver; or a proved speedup.

Recommended priority: **prove when the neural correction is useful and when the resulting solution can be trusted**. Use architecture, mathematics and matched experiments as the evidence—not the number of named techniques in the title.
