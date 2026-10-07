# Lie–ML review and exploration plan

Review date: 6 October 2026. Scope: the uploaded draft, the extracted mathematics-and-symmetries archive, the astra branch, the three uploaded references, and selected primary literature on representations, conservation laws, and equivariant maps.

## 1. Reviewer position

The project has a coherent mathematical center: make reduction, reconstruction, compatibility, and branch restrictions explicit, then determine whether learning can improve a remaining computation. The present evidence establishes a much narrower center than the eventual goal of conservation-aware evolution for random initial functions on a fixed bounded domain.

The central unresolved question is **which map learning should approximate, on which space, and what the analytic part has already made inexpensive**. A network architecture cannot answer that question in advance.

Two objectives should be investigated separately:

1. Accelerate the symbolic or geometric work needed to obtain a usable reduction.
2. Extend the solution family that can be computed economically after exact invariant reduction has reached its limit.

These objectives have different inputs, outputs, costs, and correctness conditions. Random initial data generally change the second problem. They do not change the symmetry algebra of a fixed equation.

A defensible working goal is:

> For a specified SV/SVE problem family, identify exact structural maps and analytically controlled approximations; characterize the remaining task on admissible initial data; and investigate whether a learned approximation improves its accuracy–cost tradeoff while preserving the structural conditions that can be enforced exactly.

This wording permits a negative ML result, an analytic improvement, or several possible learning interfaces. It also requires “extended ability” to mean something measurable: more initial shapes, a larger parameter range, a longer regular time interval, finer spatial resolution, or a broader boundary-data family. These are distinct extensions.

The review below is an exploration plan. It does not select a new neural architecture or claim that conservative flux learning is already the best next step.

## 2. What was examined, and how to read the evidence

The archive was unzipped before inspection. It contains 951 files, including conversation exports, mathematical notes, source code, literature PDFs, numerical reports, and saved training artifacts. Its ten conversation records were read; several are explicitly partial exports of the original conversations. Their surrounding research reports and mathematical sources were examined to recover the experiments and changes of direction.

The numerical evidence below comes from saved reports and source inspection, not newly repeated training. Saved model binaries were inventoried rather than individually reinterpreted as new experiments. The current branch was inspected through GitHub; the observed recursive tree identifier was 3545f8bd074cd13fef7924f0bdcf10519ee7ec2d.

Three kinds of statement must remain separate:

| Kind | Example here | What it establishes |
|---|---|---|
| Exact structural identity | Prolongation multiplier, reduced pullback, exact initial-jet construction | The identity holds on its declared chart |
| Sampled numerical validation | Solver agreement and positive margins on sampled grids | Strong evidence on tested cases; no interval-wide theorem |
| Research hypothesis | A normalized solution family may be easier to learn | A question for further analysis and experiments |

The draft's “certificate” language is appropriate for an explicit exact structural contract. It should not suggest that sampled regularity margins also certify every point of a parameter interval.

The three uploaded references serve different purposes:

| Reference | Appropriate use | What it does not establish |
|---|---|---|
| Paliathanasis, Leon, and Leach, shallow-water/bed-elevation model, Mathematics 14, 433 (2026) | Supplied scalar equation, generators, and candidate reductions to audit | A validated random-data physical SVE benchmark |
| Akhound-Sadegh et al., Lie Point Symmetry and Physics Informed Networks (2023) | A symmetry-informed training and function-input baseline | That its heat/Burgers results transfer automatically to this SVE family |
| A. S. Mathebula, MSc thesis (2017) | Classical and nonclassical symmetry methods, reductions, multipliers, conservation-law reasoning | A shallow-water numerical comparison or a universal finite-dimensional symmetry classification |

The 2023 neural reference is especially easy to misread. Its prediction depends on an embedding of sampled initial functions and on coordinates. The heat and Burgers experiments use many initial functions. A conditional network trained on a few scalar parameter pairs is a narrower object, even if both are described informally as “parameterized PINNs.”

## 3. Freeze the problem before choosing a space to learn in

### 3.1 A problem is more than its differential expression

Use a contract such as

\[
\mathcal P=(\Delta_\lambda,\Omega,\mathcal B,a,\mathcal A,\mathcal G_{\rm reg}),
\]

where:

- \(\Delta_\lambda\) is the differential system and its model parameters;
- \(\Omega\subset\mathbb R^d\) is the spatial domain;
- \(\mathcal B\) specifies boundary operators, boundary data, and their time dependence;
- \(a\) is an initial function, or initial jet for a higher-order equation;
- \(\mathcal A\) is the admissible class of such data;
- \(\mathcal G_{\rm reg}\) lists positivity, regularity, nonzero-denominator, and invertibility conditions.

For ordinary spatial domains the current cases are \(d\in\{1,2\}\). The notation \(k\in(0,2]\) should be replaced by these integers unless a different fractional-dimensional construction is intended.

A bounded open set still requires a boundary specification. A periodic rectangle uses identifications and behaves as a torus; it has different admissible symmetries from a rectangle with walls or prescribed inflow. “Fixed bounded domain” does not identify any of these choices.

Separate model parameters \(\lambda\), group parameters \(\varepsilon\), initial-data coordinates \(\eta\), and network weights \(\theta\). In particular, the current curvature perturbation \(\eta_{\rm ic}\) is not the exponent perturbation \(\delta=m-3\).

### 3.2 Keep the scalar and Eulerian targets separate

The draft's printed scalar benchmark is

\[
E_m[\phi]
=D_t\left(\phi_s\phi_{tt}
-g\frac{\phi_{ss}}{\phi_s^2}\right)
-g\beta_{\rm tr}
D_s\left(\frac{\phi_t^{m-1}\phi_{ts}}{\phi_s}\right)=0,
\qquad
\beta_{\rm tr}=m\kappa.
\]

It has two independent variables, one dependent field, and differential order three. The cubic reduction uses

\[
X_5=t\partial_t-2s\partial_s,\qquad
\sigma=st^2,\qquad \phi=F(\sigma).
\]

This benchmark is useful and independently verifiable. Its physical interpretation as a complete eliminated SVE system remains a separate issue.

If \(x=\phi(t,s)\), the bed pullback satisfies

\[
\widetilde b_t=b_t+\phi_t b_x.
\]

Starting from an Eulerian Exner equation with flux \(\kappa u^m\), the corresponding relation is

\[
\widetilde b_t
-\frac{\phi_t}{\phi_s}\widetilde b_s
+\frac{\kappa}{\phi_s}D_s(\phi_t^m)=0.
\]

The material transport term must be retained in a complete derivation. Verification of the printed scalar equation does not resolve its omission in the source transformation.

The archive also studies an Eulerian, smooth, periodic, two-dimensional Grass SVE system. Its state includes depth, two velocities, and bed elevation. It is not the same numerical problem as the scalar third-order reduction.

For orientation, an Eulerian water system can be written schematically as

\[
\partial_t h+\nabla\cdot(hv)=0,
\]
\[
\partial_t(hv)
+\nabla\cdot\left(hv\otimes v+\frac{gh^2}{2}I\right)
=-gh\nabla b+\text{declared sources},
\]
\[
\partial_t b+\nabla\cdot q_b(v;\lambda)=0.
\]

The precise sediment coefficient, rotation, drag, and bed treatment must be declared. SV with prescribed bed, SVE with evolving bed, and their parameterized versions then become explicit contracts rather than four ambiguous labels.

### 3.3 Give “random initial data” a mathematical meaning

A useful target is a distribution \(\mu\) supported on an admissible subset \(\mathcal A\) of a function space, together with a common time interval on which the selected solution concept is meaningful.

For a smooth wet benchmark, one might begin with boundary-compatible finite spectral expansions, a positive-depth margin, prescribed means, and bounds on derivatives. These are modeling choices, not an asserted general well-posedness theorem for all SVE systems.

Training on randomly sampled coefficients of a fixed finite expansion is a controlled intermediate step. It is broader than varying one curvature scalar, but still narrower than learning an unrestricted function-space operator.

Count independently:

1. Independent initial functions.
2. Independent model-parameter values.
3. Collocation points per function.
4. Labeled trajectories, if any.
5. Spatial resolution and input spectral bandwidth.

Increasing collocation points for one function does not increase the diversity of initial conditions.

## 4. The mathematical objects that should not be conflated

| Object | Meaning | Relevant map or question |
|---|---|---|
| Base \(M\) | Independent variables, such as \((t,x)\) or \((t,s)\) | Coordinate transformation |
| Field bundle \(E\to M\) | Values of the physical dependent fields | Lift of a coordinate action |
| Jet space \(J^nE\) | Field values and derivatives through order \(n\) | Prolongation, determining equations |
| Equation locus \(\mathcal E^n\) | Jets satisfying the displayed differential relations | Preservation of the equation |
| Prolonged equation \(\mathcal E^\infty\) | Relations and differential consequences | Compatibility and differential ideals |
| Initial-data space \(\mathcal A\) | Functions satisfying positivity and boundary conditions | Input to evolution |
| Solution space \(\mathrm{Sol}(\mathcal P)\) | Admissible trajectories | Usually nonlinear; not a vector space |
| Symmetry algebra \(\mathfrak g\) | Infinitesimal transformations preserving the equation | Brackets, flows, subalgebras |
| Invariant profiles | Solutions fixed by a chosen subgroup | Exact reduction |
| Orbit quotient | Solutions or data modulo a group action | Remove equivalent coordinates |
| Approximation space | A chosen finite representation of trajectories | Truncation and error control |
| Learned latent space | Coordinates produced by an encoder | Does its action correspond to a physical one? |

A point in a jet zero-locus is not a complete solution. Derivatives must come from a field and satisfy differential compatibility. This distinction matters when a neural or polynomial fit is used to propose determining-equation data.

A finite generator ansatz can identify and verify a finite-dimensional kernel. It does not prove that all smooth generators lie in that ansatz. This is important both for maximality claims and for the meaning of a failed candidate search.

The Mathebula reference also helps distinguish classical point symmetries from conditional/nonclassical reductions. The latter impose an invariant-surface condition together with the equation, and their determining problem is generally nonlinear; its solutions should not automatically be treated as a vector space or a Lie algebra. Conversely, a linear PDE can have an infinite-dimensional superposition symmetry ideal. There is no universal finite-dimensional symmetry search space covering these cases.

Also distinguish three flows:

\[
\exp(\varepsilon X),\qquad S_t(a),\qquad \theta_{k+1}=\theta_k-\alpha\nabla L(\theta_k).
\]

These are a symmetry transformation, physical evolution, and an optimization iteration. Their use of the word “flow” does not identify them mathematically.

## 5. Three different meanings of reduction

### 5.1 Invariant-solution reduction

For a subgroup \(H\), an invariant solution satisfies

\[
T_hu=u \quad(h\in H),
\]

or, infinitesimally,

\[
Q_X[u]=\eta(x,u)-\xi^i(x,u)u_i=0.
\]

The characteristic equations then produce fewer independent coordinates. This selects a restricted solution family.

For the cubic scalar example,

\[
Q_{X_5}=-t\phi_t+2s\phi_s=0
\quad\Longrightarrow\quad
\phi=F(st^2).
\]

The dimension reduction is exact for this family. It does not say that arbitrary initial functions can be represented by one \(F\).

### 5.2 Quotient by equivalent solutions

The quotient \(\mathrm{Sol}/G\) identifies solutions related by transformations. It can retain all solutions as equivalence classes, but it generally remains infinite-dimensional.

On a periodic interval, the fixed points of all spatial translations are spatially constant fields. The quotient by translation contains arbitrary shapes modulo phase. These are very different objects.

For example,

\[
a(x)=A_1\cos(x+\varphi_1)+A_2\cos(2x+\varphi_2).
\]

Translation changes both phases. The amplitudes and the relative phase \(\varphi_2-2\varphi_1\) remain shape information. Removing one translation parameter does not remove that information.

This observation suggests a useful diagnostic: measure approximation complexity before and after phase alignment. It does not, by itself, select a neural operator.

### 5.3 Approximate reduction of dynamics

A low-dimensional projection or manifold approximation is another construction. Its validity depends on the initial-data family, time interval, norm, and truncation error.

For a discretized snapshot set \(K\), even the linear approximation question

\[
d_r(K)=\inf_{\dim V=r}\sup_{u\in K}\inf_{v\in V}\|u-v\|
\]

asks something not answered by the dimension of \(\mathfrak g\).

A finite symmetry group removes a finite amount of orbit redundancy. It does not establish that the remaining family has small approximation width.

The project should use “invariant reduction,” “orbit normalization,” and “approximate dynamical reduction” separately.

## 6. Equation symmetry, boundary symmetry, and data stabilizers

There are at least three relevant transformation groups:

\[
G_{\rm eq},\qquad
G_{\Omega,\mathcal B},\qquad
G_a.
\]

The first preserves the differential equation. The second preserves the specified domain and boundary problem, or a declared family of boundary data. The third fixes one initial datum.

For generic initial functions, \(G_a\) can be trivial even when \(G_{\rm eq}\) is large.

For spatial actions preserving the time coordinate, an admissible solution operator can satisfy

\[
S_t(T_ga)=T_gS_t(a).
\]

This relates different initial-data problems. It does not require each \(a\) to be invariant. If a transformation rescales time, the relation must transform the time argument as well; a naive commutation formula at fixed \(t\) is insufficient.

One should also qualify the claim that an invariant solution requires an invariant domain. A known invariant solution may be restricted to a non-invariant bounded region if its induced initial and boundary traces match the prescribed problem. What fails in general is coverage of arbitrary boundary data by that invariant ansatz.

Thus the draft's constructed invariant data are a legitimate compatible example. They are not evidence that arbitrary wall, inflow, or random-data problems share the reduction.

Transformations that change \(\lambda\) are equivalence transformations between problems, not necessarily symmetries of one fixed equation. Organizing the parameter family together with domain and boundary actions may be useful; it does not require immediately building a groupoid-based network.

## 7. What representation theory contributes

### 7.1 The representation has to be specified

| Action | Space acted on | Useful consequence |
|---|---|---|
| Adjoint action | \(\mathfrak g\) | Classify conjugate subalgebras |
| Prolonged action | Jets | Verify equation preservation |
| Induced action | Physical fields and initial functions | Define operator equivariance |
| Pullback on observables | Functions of states | A linear action even when state action is nonlinear |
| Action on currents | Conservation-law classes | Track how laws and charges transform |
| Latent representation \(\rho\) | Encoded features | Useful only with a justified encoder/decoder relation |

The supplied scalar algebra is solvable. Away from the cubic enhancement its displayed generators have the structure

\[
\mathfrak g_{\rm supplied}\simeq\mathbb R^3\rtimes\mathbb R,
\]

with \(\operatorname{ad}_{X_4}=-I\) on \(\langle X_1,X_2,X_3\rangle\). At \(m=3\),

\[
\mathfrak g_{\rm supplied}\simeq\mathbb R^3\rtimes\mathbb R^2,
\]

where

\[
\operatorname{ad}_{X_5}=\operatorname{diag}(-1,2,0),
\qquad [X_4,X_5]=0.
\]

This is a verified structural description of the supplied span, not an independent maximal classification. It gives weights and orbit geometry. It does not supply the orthogonal irreducible decomposition associated with a compact group.

### 7.2 A concrete representation example

For periodic translations, a complex Fourier coefficient transforms as

\[
c_k\mapsto e^{ik\vartheta}c_k.
\]

Each real coefficient pair carries a two-dimensional rotation representation with infinitesimal generator \(kJ\), where

\[
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]

The group action, generator, and coefficient transformation are explicit. This is a useful reference example for judging proposed “Lie-informed features.”

Around a homogeneous background, a translation-equivariant linearized operator preserves Fourier mode spaces. In a nonlinear equation, products couple modes with the familiar \(k+\ell\) selection rule. Equivariance organizes those couplings; it does not eliminate them.

Around a nonuniform background \(a\), the linearizations instead form a covariant family,

\[
L_{T_ga}=T_gL_aT_g^{-1},
\]

when the underlying evolution is equivariant. A single \(L_a\) need not commute with every translation.

Depth and bed elevation are scalars under physical rotations. Velocity transforms as a vector, together with the coordinates. Treating all channels as identical scalar features can miss this distinction.

### 7.3 A latent Lie algebra needs a physical bridge

If an encoder \(E\), decoder \(D\), and representation \(\rho\) are used, the relevant conditions are

\[
E(T_gu)=\rho(g)E(u),\qquad
D(\rho(g)z)=T_gD(z).
\]

A skew-symmetric latent generator preserves an encoded Euclidean norm under its exact exponential. That norm need not be physical mass, energy, or an SVE invariant. Without the bridge above, a latent Lie action is a design choice rather than a representation of the PDE symmetry.

Likewise, for a linear feature map \(W\), the intertwining condition

\[
W\,d\rho_{\rm in}(X)=d\rho_{\rm out}(X)\,W
\]

is meaningful only after the input and output representations are defined. It does not imply that the nonlinear solution operator is low-rank.

## 8. Moving frames: a possible structural interface, with local limits

Suppose a regular data action permits a local normalization

\[
a_{\rm can}=\rho(a)\cdot a.
\]

An equivariant map can then be reconstructed from its value on normalized representatives:

\[
\widehat S(a)
=\rho(a)^{-1}\cdot\widehat S_{\rm can}(a_{\rm can}).
\]

The exact group action handles orbit coordinates; the remaining map handles inequivalent shapes. This separates a computation already known from the one still requiring approximation.

Classical moving-frame constructions provide the local geometric basis; current Lie-algebra canonicalization work explores related neural-operator uses. The regularity and stabilizer conditions must be checked rather than assumed.

A simple test case is phase normalization using the first Fourier coefficient. It works where that coefficient is nonzero. It becomes ill-conditioned as the coefficient approaches zero, and cannot resolve the additional isotropy of some symmetric fields.

Possible responses include another normalization chart, a partially normalized representation, or a fallback calculation. A single global smooth canonicalizer should not be presumed.

The archive's SACNO probe used an invariant-coordinate field ansatz of the form \(N(x/\sqrt t)\). Its successful transformation test verifies that ansatz's built-in field invariance. With no initial-function input or PDE accuracy test, it does not establish an equivariant solution operator on random data.

Learning a whole orbit of one known anchor is also often unnecessary: the exact action already generates that orbit. The informative target would be different orbit representatives or departures from that orbit.

## 9. Linearization provides a deeper bridge than a symmetry penalty alone

For a solution \(u\), let

\[
\ell_\Delta[u]w
=\left.\frac{d}{d\epsilon}\Delta[u+\epsilon w]\right|_{\epsilon=0}.
\]

This operator connects several apparently separate directions.

### 9.1 Symmetry directions

The evolutionary characteristic

\[
Q_X=\eta-\xi^iu_i
\]

of a symmetry satisfies the linearized equation on a solution:

\[
\ell_\Delta[u]Q_X[u]=0.
\]

These directions are tangent to symmetry orbits.

### 9.2 Initial-data and model response

An initial-data perturbation satisfies a variational problem with changed initial traces. A parameter perturbation satisfies

\[
\ell_\Delta[u]\psi
=-\partial_\lambda\Delta[u]\,\delta\lambda,
\]

with the appropriate data and boundary perturbations.

These responses are generally much broader than the finite-dimensional symmetry tangent space. They use the same linearized operator but different forcing and traces.

### 9.3 Conditioning and gauge

Orbit directions can create nonuniqueness in a response or normalization problem. A phase or scale condition can fix that ambiguity. Any “normal complement” to the orbit requires a specified metric, projection, or gauge; there is no automatic canonical orthogonal splitting for a general PDE.

This suggests investigation of the response operator after constraints and gauges are imposed. Its cost and conditioning might support a learned inverse, a preconditioner, or an initial guess. Equally, ordinary sensitivity integration or a small linear solve may settle the task cheaply.

This is a structural connection to investigate, not yet evidence that a neural inverse is needed.

### 9.4 Symmetry deformation is a different linearized problem

For \(X_\delta=X_0+\delta X_1+\cdots\), linearizing the determining equations gives schematically

\[
\mathcal D_0X_1=-\mathcal D_1X_0.
\]

The obstruction is a cokernel question in a specified generator class, with stated equivalences and regularity. It is not the same as solving for the physical response \(\psi\).

Calling this “cohomological” can be useful motivation, but a deformation/cohomology theorem needs its complex, equivalence relation, and bracket compatibility defined explicitly.

## 10. Conservation laws connect solution spaces, adjoints, and representations

A local conservation law has the form

\[
D_t\rho+\nabla\cdot j=0
\]

on solutions. On a bounded domain,

\[
\frac{d}{dt}\int_\Omega\rho\,dx
=-\int_{\partial\Omega}j\cdot n\,dS.
\]

A source term adds its volume integral. Thus an open-flow problem can obey local conservation while its total water mass changes. Momentum and energy require their own balance laws, including bed and boundary effects.

The multiplier method seeks \(\Lambda\) such that

\[
\Lambda^A\Delta_A=D_iJ^i
\]

off shell. Its Euler-operator condition is

\[
\mathsf E_{u^\alpha}(\Lambda^A\Delta_A)=0.
\]

It applies without first finding a Lagrangian. A Noether argument requires an appropriate variational formulation.

For regular systems, multipliers satisfy an adjoint linearized condition on solutions, together with additional compatibility conditions. Not every adjoint symmetry is automatically a multiplier.

The integration-by-parts identity

\[
\Lambda\cdot\ell_\Delta w
-w\cdot\ell_\Delta^*\Lambda
=D_iC^i
\]

shows why tangent responses and adjoint information can produce conserved bilinear quantities. This is a concrete bridge between solution response and conservation, rather than an analogy between unrelated Lie algebras.

If \(C[u]\) is a conserved charge, admissible infinitesimal changes at a fixed value satisfy

\[
DC[u]w=0.
\]

The data class is then restricted to a charge level set, and its tangent directions must respect that constraint. Some symmetries change a charge, for example through scaling. They map between leaves rather than act within one fixed-charge leaf.

Conservation currents can be regarded as horizontal forms, closed on the equation and considered modulo trivial currents. Their pullbacks under prolonged symmetries induce an action on conservation-law classes. This offers another precise representation space.

At the discrete level, one shared interface flux cancels between neighboring cells. This enforces a conservation balance for the corresponding component. It does not automatically give positivity, entropy stability, or a well-balanced bed treatment.

If the chosen SV/SVE contract admits a Hamiltonian or variational structure, momentum maps, Poisson brackets, or Casimirs may provide further constraints. That structure must be derived for the actual equations and boundaries before importing conclusions from another physical theory. Quantum or decoherence motivations currently add little to the demonstrated pipeline.

## 11. What the current experiments establish

### 11.1 The scalar cubic branch

The verified control is

\[
E_3[F(st^2)]=t^{-1}R_0[F],
\]

with

\[
R_0[F]=2\sigma A'[F]-g\beta_{\rm tr}B'[F],
\]
\[
A=2\sigma(F')^2+4\sigma^2F'F''
-g\frac{F''}{(F')^2},\qquad
B=8\sigma^2F'(F'+\sigma F'').
\]

The exact profile is

\[
F_0=C+K\sigma^{1/3},\qquad
K^3=\frac{27g}{1-4g\beta_{\rm tr}}.
\]

At \(g=1,\beta_{\rm tr}=0.1\), \(K=\sqrt[3]{45}\). The PDF's cube-root typesetting is consistent with the cubic relation. Claude's \(\sqrt3/45\) reading is not a genuine inconsistency.

The family experiment fixes \(m=3\), \(\sigma\in[1,1.5]\), and varies

\[
F(1)=K,\quad F'(1)=K/3,\quad
F''(1)=-\frac{2K}{9}(1+\eta_{\rm ic}),
\qquad |\eta_{\rm ic}|\le .02.
\]

It uses seven training values, four held-out interpolation values, and three seeds. Its data are constructed on \(\Sigma_0=\{st^2=1\}\), not drawn as arbitrary spatial initial functions on a fixed-time slice.

The exact jet construction and direct reconstruction checks are positive results. The scalar family is smooth and regular at all sampled references. Neural predictions improve on the selected finite Taylor truncations.

The reported median training cost is 4.625 s; DOP853 query cost is 0.003261 s; neural query cost is 0.002616 s. The resulting 7,170-query arithmetic break-even excludes several costs and compares methods with very different observed errors. Accuracy-matched tolerances, interpolation, caching, and dense-output reuse could change or remove the online advantage.

This supports a local interpolation experiment, not an established speedup, exponent continuation, random-function operator, or interval-wide error bound.

### 11.2 The earlier symmetry-loss experiment

The archived periodic Eulerian experiments include 108 main neural runs. Their matched Lie and residual-reweighting variants coincide in the tested formulation. Computing the reweighting directly saves about 39% of the associated optimizer computation relative to explicit prolongation evaluation.

This is a useful training implementation improvement. It is not a 39% acceleration of a PDE solver.

None of the 45 family runs passes the declared 5% maximum-field evolution-error threshold. The classical reference solves are already very fast on these small smooth cases.

The conservation-loss failures should also be interpreted carefully. Positive recorded gradient cosines do not establish destructive conflict between objectives. Loss scale, quadrature, limited capacity, and optimization budget remain possible explanations.

### 11.3 The series-first experiment

The coupled time approximation

\[
P_2=U_0+t\mathcal F(U_0)
+\frac{t^2}{2}D\mathcal F(U_0)[\mathcal F(U_0)]
\]

contains actual water–velocity–bed coupling. It preserves more of the local evolution than a frozen initial anchor.

This is a local time expansion under sufficient regularity, or a formal approximation when such regularity is not established. It carries no general convergence-radius guarantee.

Under the archived short budget, a single MLP remainder is the most consistent tested improvement: the median maximum-field errors are 0.61% for flat SV and 1.71% for Grass SVE, with all three seeds passing. Pure \(P_2\) already has worst-field errors of 4.66% and 6.37%, respectively.

KAN results do not establish a general architectural advantage. In SVE, accepted chain corrections can lower sampled residual loss while every seed fails the field-error threshold.

This is evidence that an analytically derived remainder can be easier to approximate. It does not prove end-to-end acceleration or broad operator generalization. The fine reference solves take approximately 0.018–0.022 s per case, whereas training takes seconds.

Field interpolation also fails to control parameter derivatives. The very large relative derivative errors must be shown with their small absolute reference scales; neither “good fields imply good sensitivities” nor “large relative ratios mean large physical errors” is justified.

### 11.4 Symbolic reduction cost

The affine generator searches report:

| Model | Split matrix | Rank/nullity | Whole workflow |
|---|---:|---:|---:|
| 1D, three-field SWE | \(33\times30\) | 23/7 | 1.448 s |
| 2D, three-field SWE | \(68\times42\) | 34/8 | 14.573 s |

In the second case, 14.193 s is spent in exact splitting/solving as implemented. One should not describe the bottleneck simply as a large nullspace computation. Expression construction, rational simplification, and splitting dominate the observed small-matrix workflow.

Fixed equation strata can be classified and cached independently of random initial data. Repeating that classification for each initial function creates artificial work for a learned accelerator to remove.

The exact flat-SWE expansion solution and its reduced Picard certificate are useful controls. Its linear-velocity data are nonperiodic and incompatible with the random periodic benchmark. Its function-iteration contraction bound concerns the reduced ODE; spatial derivatives prevent automatically transferring a \(C^0\)-Lipschitz argument to the full PDE.

## 12. Distinguish three symmetry-related losses

The following losses answer different questions:

\[
\|Q_X[u_\theta]\|^2,
\]
\[
\|\operatorname{pr}X(\Delta)[u_\theta]\|^2,
\]
\[
\|\widehat S_\theta(T_ga)-T_g\widehat S_\theta(a)\|^2.
\]

The first selects an invariant solution family. The second constrains how an approximate residual transforms. The third enforces equivariance of a map between different initial-data problems.

For an off-shell identity

\[
\operatorname{pr}X_i(\Delta)=M_i\Delta,
\]

the squared prolongation penalty becomes

\[
\sum_i\|\operatorname{pr}X_i(\Delta)\|^2
=\Delta^\top\left(\sum_iM_i^\top M_i\right)\Delta.
\]

It is exactly a possibly state-dependent residual weighting. Such weighting may help optimization; it does not supply an independent condition on the solution map.

Residual scaling itself matters. Replacing \(\Delta\) by an equivalent \(A\Delta\) can change the loss metric while leaving the zero set unchanged. Therefore raw residual scores are not an intrinsic geometry of the solution space without a norm and scaling convention.

The evolutionary identity

\[
\ell_\Delta(Q_X)
=\operatorname{pr}X(\Delta)-\xi^iD_i\Delta
\]

adds another possibility. Its penalty can include residual derivatives rather than only a pointwise weight. Compare it against matched gradient-enhanced residual controls and include the derivative-evaluation cost. Recent generalized-symmetry PINO work discusses this distinction.

## 13. Residual, profile, and physical errors require different controls

A useful local estimate would have the form

\[
\|u_\theta-u\|_X
\le C_{\rm stab}
\bigl(\|\Delta[u_\theta]\|_Y
+\|\text{initial/boundary mismatch}\|_Z\bigr),
\]

under hypotheses that make the nonlinear problem stable. The function spaces, neighborhood, boundary conditions, and constant are essential.

The scalar reconstruction makes the issue concrete:

\[
v=\frac{2\sigma F'}{t},\qquad
h=\frac{1}{t^2F'}.
\]

A small error in \(F\) alone does not bound the derivative error, depth error near \(F'=0\), or the error obtained after inversion to the same Eulerian position.

The reduced third-order equation also has a leading-coefficient singular exit. A response operator can become badly conditioned before a sampled residual looks alarming.

A semidiscrete Grönwall estimate is not automatically a continuum error theorem; its constant may depend unfavorably on mesh spacing. Distinguish:

1. Exact algebra and reconstruction identities.
2. Numerically checked regularity and solver refinement.
3. A posteriori stability estimates or interval bounds.

The first two are already valuable. The third is not established by the current profile/residual tables.

## 14. Assessing Claude's critique

| Comment | Reviewer assessment |
|---|---|
| The exact reduced ODE is too cheap to justify current training | Supported for the tested workload. Repeated queries remain an empirical question with stronger cheap baselines |
| Sensitivity and Chebyshev baselines are missing | Correct for the narrow initial-curvature family |
| Residual rankings do not certify physical error | Correct; the required stability and reconstruction controls should be central |
| Domain and data must also be invariant | Needs qualification: an invariant family needs compatible traces; an equivariant operator relates transformed non-invariant data |
| An algebra-dimension jump makes a smooth parameterized network inappropriate | Too strong. Kernel dimension can jump while the physical solution map remains smooth on a common regular branch |
| The training protocol is insufficient | It is a short-budget pilot. Better tuning may improve errors, but does not by itself answer the economic or geometric question |
| The \(K\) constants disagree | Incorrect reading of the cube root in this PDF |
| Quantum/decoherence motivation could be removed | Reasonable: no demonstrated theorem or implementation uses it |
| The generic-m correction must be a learned two-variable field | Premature. First inspect the analytic forcing structure and cheaper response representations |
| There is “no breakthrough” | Not a precise review criterion. The current novelty claim should be narrow and compared with existing symmetry/PINN and canonicalization work |

A verified pipeline can be a meaningful engineering or mathematical exposition contribution. A broader research claim would need a new structural result, a justified approximation mechanism, or an accuracy-matched computational advantage. Combining familiar ingredients does not establish any of these by itself.

## 15. A bounded first-order exploration near the cubic stratum

This calculation is a diagnostic, not a selected learning architecture.

Fix a nondimensionalization, hold the resulting \(\kappa\) fixed, let \(m=3+\delta\), and work on a chart with \(\phi_t>0\). The logarithms below use dimensionless velocity; an exponent change with dimensional coefficients requires a stated reference scale. Define

\[
H=\frac{\phi_t^2\phi_{ts}}{\phi_s}.
\]

The exponent expansion is

\[
E_{3+\delta}=E_3+\delta E_1+O(\delta^2),
\qquad
E_1=-g\kappa D_s\{H(1+3\log\phi_t)\}.
\]

The first-order defect of the supplied cubic generator is

\[
\operatorname{pr}X_5(E_1)+E_1
=3g\kappa D_sH.
\]

Thus the unchanged \(X_5\) does not persist to first order.

For the restricted diagonal scaling class

\[
X=a\,t\partial_t+b\,s\partial_s+c\,\phi\partial_\phi,
\]

weight balance gives

\[
b=3c-2a,\qquad (m-3)(c-a)=0.
\]

At \(X_5\), \(a=1,b=-2,c=0\), so no smooth first-order continuation exists inside that class. This is not a proof against all possible \(X_1\) in an unrestricted determining problem.

Now use

\[
r=\log t,\quad z=st^2,\quad
V=2zF',\quad B=8z^2F'(F'+zF'').
\]

On the invariant cubic background,

\[
tE_1[F]
=-g\kappa\partial_z\{B(1+3\log V)\}
+3g\kappa B'r.
\]

The transformed cubic linearization has coefficients independent of \(r\), so it can be written

\[
\mathcal L=\sum_{j=0}^3L_j(z,\partial_z)\partial_r^j.
\]

An affine-log correction

\[
\psi(r,z)=A(z)+rG(z)
\]

closes this forcing class, with

\[
L_0G=-3g\kappa B',
\]
\[
L_0A+L_1G
=g\kappa\partial_z\{B(1+3\log V)\}.
\]

This gives coupled ordinary differential response problems for compatible traces. The closure was checked symbolically in the preceding analysis.

The significance is methodological: failure of a symmetry does not imply that its first-order departure requires an unrestricted two-variable neural field. The forcing can be low-complexity even while the exact algebra changes.

Limits remain explicit: arbitrary boundary/initial perturbations need not lie in this class; singular branches are excluded; no uniform \(O(\delta^2)\) error bound is established; and \(\delta\log t\) warns against extrapolation over unlimited time ranges.

## 16. Why a coarse learned dynamics may need more than the current coarse state

An unresolved-dynamics interface is another possibility, but its state must be justified.

Even a finite linear block system,

\[
\dot z=Az+Bw,\qquad \dot w=Cz+Dw,
\]

gives, after eliminating \(w\),

\[
\dot z(t)=Az(t)+Be^{Dt}w_0
+\int_0^tBe^{D(t-s)}Cz(s)\,ds.
\]

The reduced evolution depends on unresolved initial data and history. An instantaneous map of \(z\) alone cannot represent all choices of \(w_0\).

For a PDE projection this motivates checking whether unresolved initial information, memory, or extra state is needed before training a closure. It is particularly relevant when broadening from a few parameterized initial shapes to random functions.

A conservative interface flux can still be a useful parameterization. Conservation does not solve this information-loss problem.

## 17. Possible learning interfaces that remain open

| Interface | Mathematical input/output | Structural requirement | Cheap comparison and stopping rule |
|---|---|---|---|
| Candidate generator or chart proposal | Equation/parameter descriptors to finite-ansatz kernel or chart candidates | Exact identity, rank, guards, and fallback; candidate verification does not prove maximality | Cached strata, symbolic simplification, modular/sparse linear algebra; stop if proposal overhead exceeds savings |
| Data/orbit normalization | Admissible functions to chart and canonical representative | Correct action, local stabilizer handling, invertible reconstruction | Explicit phase/scale normalization; stop if the exact normalization is already cheap |
| Solver initial guess or preconditioner | Problem descriptors and current iterate to an approximate correction | Classical solver still checks convergence and guards | Standard initial guesses, Newton/Krylov/Anderson methods; compare whole solve cost |
| Parameter or data response | Background, perturbation, and traces to \(\psi\) | Gauge, charge-tangent constraints, stability and regularity | Sensitivity equations, interpolation, affine-log closure, low-rank response; stop if these meet the target |
| Unresolved evolution or flux | Resolved state plus needed history/initial information to correction | Correct balances, equivariance, boundary flux, positivity/entropy when claimed | Classical reduced models and coarse/fine solvers; test whether closure is identifiable |
| Error/cost allocation | Residual/state/mesh descriptors to refinement or fallback proposal | Estimates must be distinguished from certificates | Analytic estimators, ordinary adaptivity; stop if prediction overhead removes benefit |

A kernel on a constant-rank finite determining matrix can be regarded as a point on a Grassmannian. This avoids arbitrary basis labels for a learned proposal. Across rank changes it belongs to different strata. Exact rank and kernel verification remain necessary.

A reduced-solver preconditioner can be more appropriate than learning an entire solution if classical correction is inexpensive and makes final accuracy reliable. But the current tiny regular ODE may offer no useful preconditioning workload.

The response and normalization interfaces are attractive exploratory objects because their spaces and maps can be written explicitly. That is a reason to analyze them, not a ranking based on unmeasured performance.

## 18. Staged plan, with concrete outputs and decision gates

### Stage A — State two contracts and the intended extension

Retain the printed scalar cubic problem as a verified control. Separately state one physical Eulerian SV/SVE family with domain, boundaries, sources, sediment law, and admissible initial distribution.

Output: a one-page problem-and-space specification for each. Choose an error norm, time window, conserved balances, and one extension axis.

Gate: do not label the scalar reduction a generic random-data SVE solver. Resolve the physical elimination before transferring physical claims.

### Stage B — Audit the existing analytic and numerical assets

Recheck inexpensive symbolic identities, bracket signs, denominator guards, reconstruction, and solver refinement. Gather existing costs without retraining all networks.

Output: an evidence table separating exact facts, sampled checks, and unsupported claims; a stage-level cost profile.

Gate: if a fixed algebra can be cached, measure the workflow after caching. If a classical solver already meets the target, record that fact before introducing learning.

### Stage C — Map group actions on the actual data class

Determine which equation transformations preserve the specified domain and boundary family. Compute representative stabilizers, charge transformations, and chart singularities.

For a periodic pilot, distinguish phase changes from shape changes in a finite spectral family. Compare raw and normalized snapshot approximation complexity.

Output: explicit actions, a local normalization example, and a list of failures or alternate charts.

Gate: if only a trivial action survives the actual boundary problem, preserve that conclusion rather than importing the full equation group.

### Stage D — Explore tangent responses and departures from invariance

Form the linearized evolution, initial-data response, and model-parameter response problems. State gauges and conserved-charge constraints. On the scalar control, finish the unrestricted first-order determining question only if the stated generator class makes it tractable.

Investigate the affine-log closure as a cheap response baseline. Measure conditioning and reconstruction sensitivity on regular samples.

Output: one response operator specification and a difficulty map over the chosen regular parameter/data range.

Gate: an algebra-dimension change is not itself a target for nonsmooth prediction. Use the response regularity and conditioning actually observed or proved.

### Stage E — Perform an approximation-and-cost screening without ML

Compare direct numerical evolution, cached reductions, sensitivity integration, polynomial/Chebyshev interpolation, coupled time series, explicit phase normalization, and ordinary reduced models where relevant.

Output: an accuracy–cost table for the intended query workload, including setup and evaluation.

Gate: choose learning only where these controls leave a measurable unmet need. An analytic result that closes the task is a successful project outcome.

### Stage F — Select at most two interfaces for matched pilots

Select from the interface table based on the preceding maps and costs. Keep the analytic pipeline responsible for exact identities and make numerical correctness checks explicit.

Use independent initial functions, parameters, and seeds. Include a cheap mechanism-equivalent control: residual weighting for prolongation penalties, analytic normalization for canonicalizers, sensitivities for response models, and standard solver initialization for learned guesses.

Output: a small reproducible experiment with all failures, setup costs, and held-out cases.

Gate: reject a learned interface if it improves a training score without meeting field accuracy, balances, regularity guards, and workload cost.

### Stage G — Write the paper around the result obtained

Possible outcomes include an exact reduction contract with a source audit, an analytic perturbation-response result, a useful normalized approximation family, a measured solver accelerator, or a negative result explaining a redundant symmetry loss.

Output: claims and experiments aligned with that result, with the physical scalar/Eulerian distinction visible.

Gate: do not use “Lie + ML” alone as the novelty claim, or use a tiny interpolation family as evidence of arbitrary-function operator generalization.

## 19. Benchmark design and economics

For a genuine initial-function experiment, split by underlying shape or orbit representative before augmentation. Putting translated copies of one shape in both training and testing measures equivariance consistency, not independent shape generalization.

Parameter interpolation, parameter extrapolation, initial-shape generalization, spatial resolution transfer, and boundary transfer need separate tests. Do not combine their scores.

Use an error norm that resolves evolving bed and velocity changes rather than rewarding a large stationary background. Report per-field errors, reconstruction errors where relevant, balance defects, guards, and failure/fallback rates.

The cost comparison should include

\[
T_{\rm learned}(N)
=T_{\rm data}+T_{\rm train}+T_{\rm setup}
+N(T_{\rm query}+T_{\rm check})
+T_{\rm fallback}(N).
\]

Compare with the strongest classical workflow for the same accuracy and requested output. Include any classical setup, caching, and reuse consistently.

Only when the learned online cost is genuinely smaller does an arithmetic break-even exist. A comparison against a much tighter classical tolerance is not an accuracy-matched speedup result.

It is also useful to specify whether a query means one profile, one complete trajectory, one new parameter value, a batch of initial functions, or a new mesh. These workloads can have different economics.

## 20. Immediate next deliverable

The next deliverable should be **the problem/space/map specification and its inexpensive analytic feasibility profile**. That work can establish which actions survive the bounded-domain problem, how much of the random-data family lies beyond invariant reduction, and which remaining computations are expensive.

Only after that should one choose a neural family.

The most useful question to carry through the exploration is:

> After exact transformations and analytic approximations are accounted for, what independent shape, response, or unresolved information remains, and how does its computation scale over the admissible family?

## Appendix A. Source-paper audit detail

The uploaded 2026 source's Table 1 prints \([X_1,X_5]=X_1\) and \([X_5,X_1]=X_1\), and likewise repeats the same sign for the \(X_2,X_5\) pair. These entries violate antisymmetry.

Direct calculation from the displayed fields gives

\[
[X_5,X_1]=-X_1,\qquad [X_5,X_2]=2X_2,
\qquad [X_4,X_5]=0.
\]

The PDF table was inspected visually as well as through extracted text. This error does not invalidate a separately checked prolongation identity. It does mean that adjoint tables and optimal-system conclusions should be recalculated from the generators rather than copied.

## Appendix B. Primary references and project evidence

Uploaded sources:

1. main(1).pdf, especially sections 6.2–6.4 and the generic-exponent continuation discussion.
2. Lie Symmetries and Similarity Solutions for a Shallow-Water Model with Bed Elevation in Lagrange Variables, Mathematics 14, 433 (2026). [DOI](https://doi.org/10.3390/math14030433).
3. Lie Point Symmetry and Physics Informed Networks, NeurIPS 2023. [arXiv](https://arxiv.org/abs/2311.04293).
4. A. S. Mathebula, Symmetry Analysis and Invariant Properties of some Partial Differential Equations, MSc thesis (2017), uploaded 51-page PDF.

Selected geometric and methodological sources:

5. Peter J. Olver, Using Moving Frames to Construct Equivariant Maps. [Author PDF](https://www-users.cse.umn.edu/~olver/mf_/mfeq.pdf). Local regularity and freeness matter for the construction.
6. Shumaylov et al., Lie Algebra Canonicalization: Equivariant Neural Operators under arbitrary Lie Groups. [arXiv](https://arxiv.org/abs/2410.02698).
7. Wang et al., Generalized Lie Symmetries in Physics-Informed Neural Operators. [arXiv](https://arxiv.org/abs/2502.00373). Relevant to evolutionary representatives and residual-derivative controls.
8. George Bluman, Connections Between Symmetries and Conservation Laws. [SIGMA](https://sigma-journal.com/2005/Paper011/). Relevant to multipliers and the limits of a blanket Noether interpretation.

Inspected project evidence:

- [astra branch](https://github.com/CarlXerophilem/Lie-ML_PDES/tree/astra).
- [PDE formalization and reduction contract](https://github.com/CarlXerophilem/Lie-ML_PDES/blob/astra/docs/pde_formalization_and_reduction.md).
- [Three-layer baseline description](https://github.com/CarlXerophilem/Lie-ML_PDES/blob/astra/docs/three_layer_baselines.md).
- [Scalar family evidence](https://github.com/CarlXerophilem/Lie-ML_PDES/blob/astra/research_artifacts/three-layer-baselines-20260927/sve-family-v02/sve_family_report.json).
- Extracted archive, notes/recent/REVIEW_AND_RESULTS.md and notes/recent/RESEARCH_REPORT.md.
- Extracted original mathematical notes, worked examples, SACNO plan/probe, and conversation exports.

The primary literature was used to establish existing constructions and distinctions. This review is not a complete novelty search across all possible Lie/ML/PDE methods.
