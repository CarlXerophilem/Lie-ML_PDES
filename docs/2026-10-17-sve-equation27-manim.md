> 21 October archive notice: the build-linked evidence below is preserved in the verified local archive. Follow the [restore guide](build-archive-20261021.md) to recover the video package.

# From an epsilon-flow to five generators, then Equation (27)

**Revision 2: unrestricted determining equations with geometry continuously visible.**

Source: [the handwritten manuscript](sve_equation27_handwritten_manuscript.md),
Sections 2–5, 7, 10–14 and Appendices C–D. Workflow: `paper2manim`.
Duration: **480 seconds**. Revision 2 was explicitly approved; the nine scenes
have been authored and rendered. Final review results and the playable film are
in the [production package](build-archive-20261021.md).
The rejected first proposal is preserved under
`../build/sve-equation27-manim-20261017/revision-01/`.

## The central change

Begin with arbitrary smooth functions, derive their restrictions, then extract
the five generators. Do not introduce a guessed scaling generator at the start:

\[
\Gamma_\epsilon\longrightarrow
X=\tau(t,s,\phi)\partial_t+\xi(t,s,\phi)\partial_s+\eta(t,s,\phi)\partial_\phi
\longrightarrow
\left.\operatorname{pr}^{(3)}X(\Delta_3)\right|_{\Delta_3=0}=0
\longrightarrow\mathfrak g=\operatorname{span}_{\mathbb R}\{X_1,\ldots,X_5\}.
\]

Every dependence restriction and affine form must follow a displayed equation.
No polynomial, affine, scaling or separated-dependence ansatz is allowed at the
start. The eight-minute film shows a complete decisive implication chain;
the full 118-coefficient expansion remains a supporting audit table.

The first 5 minutes 20 seconds derive and organize the symmetry algebra. The
last 2 minutes 40 seconds connect it to the original Equation (27) objective.
Detailed intermediate profile and Abel coefficient arithmetic remains available
in the companion handout rather than being presented as fully taught on screen.

## Why these operations are interesting

The practical question is how to describe a nonlinear PDE with fewer unknowns.
A symmetry is a motion that preserves the equation. Differentiating that motion
gives a field whose unknown coefficients can be found from linear determining
equations. Splitting those equations removes dependencies that the PDE forbids;
integrating the remaining conditions turns arbitrary functions into five real
controls. This is the Lie algebra as a **variable-compression tool**.

The algebra then organizes choices. A bracket tests how motions interact; a
subalgebra selects a coherent family of orbits. An invariant solution uses one
label for each orbit, reducing the number of independent variables. The later
quotients remove an irrelevant profile offset and scaling freedom, lowering
ODE order while retaining constants needed for reconstruction. The reciprocal
shift finally exposes an Abel cubic; recognizing its form does not solve it
in general. These motivations appear in the film's amber captions and in the
[presenter notes](build-archive-20261021.md).

## Geometry remains on board

Reserve the **right 34% of every frame** for geometry and the left 66% for
calculation. A narrow footer identifies the current space, operation and chart.
Keep geometry visible during equations and pauses. A formula-only slide fails
the revised specification.

Use an explicit **1280 by 720, 15 fps** preview to keep both panels legible,
replacing the original 854-by-480 preview. Use short English captions and
live-presenter notes. No synthesized voiceover is planned.

| Stage | Geometry board | Meaning and guardrail |
|---|---|---|
| Flow | Point \(q=(t,s,\phi)\), curve \(\Gamma_\epsilon(q)\), tangent \(X(q)\) | \(\epsilon\) is transformation amount, not physical time. The unknown motion is labeled **candidate**. |
| Prolongation | Point-space card connected to a jet-space card | Derivatives change by the chain rule, not by new arbitrary choices. |
| Determining equations | Schematic hypersurface \(\mathcal E_3\) with a prolonged tangent arrow | Label the picture schematic: \(\dim J^3\pi=12\), \(\dim\mathcal E_3=11\). It is not a literal 3D plot. |
| Coefficient splitting | The same tangent arrow with dependencies removed only after their equations | The condition holds for every admissible jet, not one chosen solution. |
| Five constants | Three translation controls and a plane of allowed scaling slopes | The plane is parameter space. Five independent fields can act on three-dimensional point space. |
| Algebra and subalgebra | Two flow-order paths; then the highlighted direction \(\mathfrak h_5\) | Brackets organize motions; closure distinguishes a subalgebra from an arbitrary selected span. |
| Invariant graph | Orbit curves lying in a graph; labels \((\sigma,w)\) | Graph tangency \(Q=0\) is a new condition, distinct from PDE-hypersurface tangency. |
| ODE quotients | Vertically shifted profiles sharing a slope; scaling orbits of slope jets | Quotienting retains reconstruction constants; it is not another translation-invariant graph condition. |
| Abel and reconstruction | \(M\leftrightarrow N\) coordinate arrow and reverse reconstruction route | The dependent-variable change preserves ODE order; recovery is local and chart-dependent. |

Keep \(G\), \(T_eG\), point space \(E\), and \(T_qE\) distinct. Differentiating
an action gives a vector field; it does not identify the group with point space.
Define the vector-field bracket explicitly as \([A,B]f=A(Bf)-B(Af)\). Do not
assert a sign-free identification with the abstract group bracket: it depends
on left/right action conventions. An orbit-space picture is not automatically
a Lie-algebra quotient.

All scenes concern the printed scalar model at \(m=3\), \(g,\beta>0\),
\(b=g\beta\), on the positive local chart. The conventional full Eulerian SVE
system is a separate model question.

## Timeline

| Time | Scene | Algebra | Geometry that remains visible |
|---|---|---|---|
| 0:00–0:45 | 1. Flow to infinitesimal motion | Differentiate the epsilon-flow; retain arbitrary \(\tau,\xi,\eta\). | Point, flow curve and tangent; \(\epsilon\ne t\). |
| 0:45–1:40 | 2. Equation constrains motion | Work one prolongation coefficient; introduce tangency and free-jet splitting. | Point-to-jet lift and \(\mathcal E_3\) tangency. |
| 1:40–3:05 | 3. Derive dependencies | Work the \(V\)-factorization, then four conditional \(R\)-coefficients. | Allowed dependencies disappear only when forced. |
| 3:05–4:25 | 4. Solve and extract five fields | Integrate remaining conditions; count five constants; check sufficiency. | Three translations, scaling-slope plane, five controls. |
| 4:25–5:20 | 5. Algebra to subalgebra | Work a bracket; show closure; select \(\mathfrak h_5\). | Flow-order paths and selected subgroup direction. |
| 5:20–6:05 | 6. Orbits to a profile | Derive \(\sigma\), impose \(Q=0\), retain residual identity. | Orbits on a graph collapse to one profile coordinate. |
| 6:05–6:50 | 7. Order of the quotients | Inherit \(Z,Y\); take the slope quotient; construct \(\Sigma,M\). | Normalizer descent, offset family, scaling-orbit labels. |
| 6:50–7:45 | 8. Equation (27) and return | Show reciprocal shift, its derivative, cubic form and reconstruction. | Coordinate map, three constants, reverse route. |
| 7:45–8:00 | 9. Read all the arrows | Replay the derivation and reduction chain. | All spaces and operations remain labeled. |

## Scene 1 — unknown motion (45 s)

**0–20 s:** show an identity \(e\in G\), a direction \(A\in T_eG\), and
the local action \(\Phi:G\times E\to E\). Connect them explicitly:
\[
\Gamma_\epsilon(q)=\Phi(\exp(\epsilon A),q),\qquad
X(q)=\left.\partial_\epsilon\Gamma_\epsilon(q)\right|_0.
\]
The corresponding local flow has \(\Gamma_0=\mathrm{id}\) and
\(\Gamma_{\epsilon+\delta}=\Gamma_\epsilon\circ\Gamma_\delta\), where defined.
Keep the group direction and its action-induced point tangent in separate
cards connected by the action arrow. Admissibility and the dimension of the
symmetry group have not yet been established.

**20–45 s:** expand the three coordinates:
\[
\bar t=t+\epsilon\tau(t,s,\phi)+O(\epsilon^2),\quad
\bar s=s+\epsilon\xi(t,s,\phi)+O(\epsilon^2),\quad
\bar\phi=\phi+\epsilon\eta(t,s,\phi)+O(\epsilon^2),
\]
\[
X(q)=\left.\frac{d}{d\epsilon}\Gamma_\epsilon(q)\right|_0
=\tau\partial_t+\xi\partial_s+\eta\partial_\phi.
\]

Presenter cue: “We do not yet know which motions preserve the equation. These
three coefficients are arbitrary smooth functions of all three point
coordinates. The determining equations will tell us what they can be.”

Source: Sections 3.0–3.1, C.1–C.2. Do not show the five named generators yet.

## Scene 2 — prolongation is the chain rule (55 s)

**0–20 s:** display the actual equation being tested, with a compact jet key:
\[
(v,\rho)=(\phi_t,\phi_s),\quad
(a,\ell,c)=(\phi_{tt},\phi_{ts},\phi_{ss}),\quad
(T,U,R,V)=(\phi_{ttt},\phi_{tts},\phi_{tss},\phi_{sss}).
\]
\[
\begin{aligned}
\Delta_3={}&\rho T+\ell a
-g(\rho^{-2}+\beta v^2\rho^{-1})R\\
&+g(2\rho^{-3}+\beta v^2\rho^{-2})\ell c
-2g\beta v\rho^{-1}\ell^2=0.
\end{aligned}
\]
Keep the jet key on the geometry board through Scene 3. Write
\(\Delta_3=\rho T+K\), where the displayed remaining terms define \(K\);
then \(T_*=-K/\rho\) explicitly eliminates the leading jet.

**20–40 s:** work the first prolonged coefficient:
\[
D_t\eta=\eta_{,t}+v\eta_{,\phi},\qquad
\eta^{[t]}=D_t\eta-vD_t\tau-\rho D_t\xi,
\]
\[
\eta^{[t]}=\eta_{,t}+(\eta_{,\phi}-\tau_{,t})v-\xi_{,t}\rho
-\tau_{,\phi}v^2-\xi_{,\phi}v\rho.
\]
Distinguish \(\eta_{,t}\) from \(\eta^{[t]}\): moving the independent
variables also changes the slope.

**40–55 s:** show the recurrence
\[
\eta^{[Ji]}=D_i\eta^{[J]}-\phi_{Jt}D_i\tau-\phi_{Js}D_i\xi,
\]
then \(\left.\operatorname{pr}^{(3)}X(\Delta_3)\right|_{T=T_*}=0\).
Here \(T=\phi_{ttt}\) and \(\partial_T\Delta_3=\rho>0\), so solve the PDE
for \(T\). The remaining free derivative coordinates are
\((v,\rho,a,\ell,c,U,R,V)\). Define
\[
\mathscr P=\rho^4\left.\operatorname{pr}^{(3)}X(\Delta_3)\right|_{T=T_*}.
\]
Its polynomial coefficients must vanish because the free jets vary in an open
set. Multiplying by \(\rho^4\) preserves the zero condition on this chart.

Presenter cue: “The lifted motion must stay tangent at every admissible jet.
One polynomial identity therefore becomes linear equations for the unknown
coefficient functions.” Source: Sections 2.3–4, 5.1. Retain the local
solvability qualification in the notes, not merely the rank condition.

## Scene 3 — derive the dependencies (85 s)

**0–35 s: calculate the first coefficient.** With \(V=\phi_{sss}\), its only
source in the prolonged residual is
\[
-g(\rho^{-2}+\beta v^2\rho^{-1})\eta^{[tss]},\qquad
\eta^{[tss]}\big|_V=-(\xi_{,t}+v\xi_{,\phi})V.
\]
After clearing denominators,
\[
\mathscr P\big|_V=g(\rho^2+\beta v^2\rho^3)
(\xi_{,t}+v\xi_{,\phi})V.
\]
Expand and read two different monomials:
\[
[v^3\rho^3V]\mathscr P=g\beta\xi_{,\phi}=0,\quad
[v^2\rho^3V]\mathscr P=g\beta\xi_{,t}=0.
\]
Thus \(\xi=Z_0(s)\), because \(g\beta>0\). Only now remove the two
dependencies on the geometry board.

**35–65 s: use the first conclusion.** Substitute \(\xi=Z_0(s)\) before
displaying the relevant part proportional to \(g\beta R\), with no
second-order jets:
\[
g\beta R\left(-2\tau_{,\phi}v^3\rho^3-2\tau_{,s}v^3\rho^2
+2\eta_{,s}v^2\rho^2-2\eta_{,t}v\rho^3\right).
\]
Four distinct monomials force
\(\tau_{,\phi}=\tau_{,s}=\eta_{,s}=\eta_{,t}=0\).

**65–85 s:** conclude
\[
\boxed{\tau=T_0(t),\qquad\xi=Z_0(s),\qquad\eta=H_0(\phi).}
\]
Label this “deduced dependencies”. Recompute the remaining polynomial; the
selected six rows are not presented as the whole determining system.

Presenter cue: “The first pair restricts xi. Feeding that result back into the
identity restricts tau and eta. None of these dependencies was guessed.”
Source: Section 5.2, Appendix D. The last four coefficients are conditional on
the first restriction; do not present them as unrestricted identities.

## Scene 4 — affine form is forced; five is a count (80 s)

**0–25 s:** let \(L=3H_0'-2T_0'-Z_0'\). Show decisive entries from the
complete remaining eleven-coefficient list:

| Monomial | Coefficient |
|---|---|
| \(\rho^5va\) | \(4H_0''\) |
| \(\rho^5a\) | \(-3T_0''\) |
| \(\rho^2\ell\) | \(-gZ_0''\) |
| \(\rho^2R\) | \(gL\) |

Hence \(H_0''=T_0''=Z_0''=0\), \(3H_0'-2T_0'-Z_0'=0\). All eleven
remaining coefficients vanish under these conditions. Do not divide by
\(b-1\) or \(5b-1\); no positive-\(b\) exception is discarded.

**25–45 s:** integrate:
\[
T_0=a_0+a_t t,\quad Z_0=b_0+a_s s,\quad H_0=e_0+a_\phi\phi,
\qquad 3a_\phi-2a_t-a_s=0.
\]
Draw the slope plane in parameter space \((a_t,a_s,a_\phi)\).
Three translations plus three slopes subject to one relation give
\(3+(3-1)=5\).

**45–65 s:** choose \(a_\phi=c_0\), \(a_t=c_0+d_0\), so
\[
\tau=a_0+(c_0+d_0)t,\quad\xi=b_0+(c_0-2d_0)s,\quad\eta=e_0+c_0\phi.
\]
Collect constants in \(X=a_0X_1+b_0X_2+e_0X_3+c_0X_4+d_0X_5\):
\[
X_1=\partial_t,\quad X_2=\partial_s,\quad X_3=\partial_\phi,\quad
X_4=t\partial_t+s\partial_s+\phi\partial_\phi,\quad
X_5=t\partial_t-2s\partial_s.
\]
Light up the five controls as their coefficients are extracted.

**65–80 s:** verify sufficiency on the original residual:
\[
\operatorname{pr}^{(3)}X(\Delta_3)=-(2c_0+d_0)\Delta_3.
\]
Constant linear independence holds over an open set, not at one point. The
conclusion is exactly five local smooth point-symmetry directions for this
scalar equation on the declared chart.

Presenter cue: “The second derivatives vanish, forcing affine functions. Six
constants remain with one relation. Every resulting field passes the original
criterion. That gives five independent symmetry directions.” Source: Sections
5.3–5.5; companion handout contains all eleven rows and independence proof.

## Scene 5 — algebra, closure and a subalgebra (55 s)

**0–25 s:** define the real span and work
\[
[X_2,X_5]f=\partial_s(tf_t-2sf_s)
-(t\partial_t-2s\partial_s)f_s=-2f_s,
\qquad [X_2,X_5]=-2X_2.
\]
Compare translating \(s\) then scaling with scaling then translating, with
explicit action order. Do not attach a commutator-loop sign without checking
that precise composition. The result stays in the real span; the full table is
checked in the companion audit.

**25–55 s:** choose
\[
\mathfrak h_5=\operatorname{span}_{\mathbb R}\{X_5\},\qquad
[\mathfrak h_5,\mathfrak h_5]=0\subseteq\mathfrak h_5.
\]
Highlight its line and the corresponding subgroup orbits. Explain why closure
matters using
\[
[X_1+X_2,X_5]=X_1-2X_2
\notin\operatorname{span}_{\mathbb R}\{X_1+X_2,X_5\}.
\]

Presenter cue: “The algebra contains admitted infinitesimal motions. A subalgebra
is a chosen collection that stays closed under brackets. The X5 direction is
the choice leading to equation 27.” Source: Sections 5.6–5.8. Span coefficients
are constants; a bracket table does not replace the determining calculation.

## Scene 6 — subgroup orbits and graph tangency (45 s)

**0–20 s:** integrate the derived field:
\[
\dot{\bar t}=\bar t,\quad\dot{\bar s}=-2\bar s,\quad\dot{\bar\phi}=0
\quad\Longrightarrow\quad
(\bar t,\bar s,\bar\phi)=(e^\epsilon t,e^{-2\epsilon}s,\phi).
\]
Obtain the orbit labels \(\sigma=st^2\), \(w=\phi\).

**20–35 s:** show an orbit tangent to the selected graph:
\[
Q_{X_5}=-t\phi_t+2s\phi_s=0
\quad\Longrightarrow\quad\phi=F(st^2).
\]
Keep equation-hypersurface tangency and graph tangency separately labeled.

**35–45 s:** retain the checked profile link
\[
\left.\Delta_3\right|_{\phi=F(st^2)}
=-\frac{2\sigma}{t(F')^3}\mathcal R_3.
\]
The multiplier is nonzero on the positive chart. The profile equation is still
third order. Source: Sections 6–9; the full residual is in the handout.

## Scene 7 — geometry explains the order of reductions (45 s)

**0–15 s:** the normalizer is
\(\mathfrak n_{\mathfrak g}(\mathfrak h_5)=\operatorname{span}\{X_3,X_4,X_5\}\).
These fields preserve the selected orbits. On their labels,
\[
X_3\mapsto Z=\partial_F,\qquad
X_4\mapsto Y=3\sigma\partial_\sigma+F\partial_F.
\]
Use \(\mathfrak n_{\mathfrak g}(\mathfrak h_5)/\mathfrak h_5\), not
\(\mathfrak g/\mathfrak h_5\), for the inherited Lie-algebra quotient.

**15–30 s:** \([Y,Z]=-Z\) explains why the translation quotient retains the
scaling direction. Vertically shifted profiles share \(\mu=F'\). Store \(F_0\)
and change ODE order from three to two. Scaling descends to
\(Y_1=3\sigma\partial_\sigma-2\mu\partial_\mu\).

**30–45 s:** its differential invariants are
\[
\Sigma=\sigma^{2/3}\mu,\quad M=\sigma^{5/3}\mu',\quad
W=M+\tfrac23\Sigma,\quad \frac{d\Sigma}{d\sigma}=\frac W\sigma.
\]
On \(W\ne0\) the order changes from two to one. Do not require \(\mu'\ne0\).
This is quotienting a family, not imposing \(Q_Z=0\), since \(Q_Z=1\).
Source: Sections 5.9, 10–12.

## Scene 8 — reciprocal map and reconstruction (55 s)

**0–20 s:** start from \(\Sigma DW M_\Sigma+AM^2+BM+C=0\), then use
\[
N=\frac1{M+2\Sigma/3},\qquad M=\frac1N-\frac23\Sigma,\qquad
M_\Sigma=-\frac{N_\Sigma}{N^2}-\frac23.
\]
Highlight the final \(-2/3\); show \(M\leftrightarrow N\) with \(\Sigma\)
fixed. The order stays one.

**20–35 s:** multiply by \(N^3/(\Sigma D)\) to obtain
\[
N_\Sigma=a_3N^3+a_2N^2+a_1N,
\]
\[
a_3=\frac{2\Sigma[g+(4b-1)\Sigma^3]}{9D},\quad
a_2=\frac{g+8(1+2b)\Sigma^3}{3D},\quad
a_1=\frac{2[2(b-1)\Sigma^3-g]}{\Sigma D},\quad
D=g+4(b-1)\Sigma^3.
\]
Reveal successive rows; the full collection is companion material. The manuscript
identifies these with printed Equation (27). The supplied local paper PDF,
page 7, and its exact publisher record were checked during production: the
three coefficients agree after distinguishing the printed variable from the
reciprocal coordinate (N). See the [source check](build-archive-20261021.md).

**35–55 s:** reverse the arrows:
\[
\frac{d\sigma}{d\Sigma}=\sigma N,\qquad
\frac{dF}{d\Sigma}=\Sigma\sigma^{1/3}N,\qquad \phi(t,s)=F(st^2).
\]
Retain \(N_0,\sigma_0,F_0\) and the chart \(\Sigma>0\), \(D\ne0\), finite
nonzero \(N\). An excluded \(W=0\) branch returns to the undivided equation;
it is not declared nonexistent. No elementary general Abel solution is claimed.
Source: Sections 12–15.

## Scene 9 — read all the arrows (15 s)

Replay local flow → generator → prolonged tangency → algebra → subalgebra →
invariant graph → ODE quotients → local reconstruction, with the geometry board
and spaces continuously visible.

Presenter cue: “Determining equations found allowed motions. A subalgebra chose
orbits. Invariance removed an independent variable; differential invariants
lowered the order; reconstruction restored the profile constants.”

## Verification, companion material and production subplans

The companion algebra handout expands the prolongation, sequential split, all
eleven separated coefficients, integration, basis independence, sufficiency and
bracket examples. It retains full profile and Abel formulas for demonstration
questions after the film.

An independent SymPy verifier starts with arbitrary functions of \((t,s,\phi)\),
constructs third prolongation, eliminates \(T\), and splits the free jets. Its
receipts record actual counts, restrictions, the final general-family identity
and the bracket table under
`../build/sve-equation27-manim-20261017/revision-02/math/`.
This supports the explicit analytic argument; it is not an autonomous general
PDE-classification claim. Original sources and frozen evidence remain unchanged.

Production workflow (approval recorded in `confirmation.json`):

1. Recheck the source and semantic hashes, source correspondence for Equation
   (27), and actual ManimCE/ffmpeg versions.
2. Implement the nine approved scenes with shared geometry states and timings.
   Compile before rendering; retain the unrestricted starting functions.
3. Sample every second and around transitions. Check continuous geometry-board
   visibility, readable formulas, correctly ordered deductions, labeled spaces,
   and the difference between equation symmetry and graph invariance.
4. Review mathematical accuracy and beginner comprehension; repair within the
   skill's total three-round limit. This is design round two. Any semantic
   change requires a new confirmation hash.

Canonical proposal, digests, mirrors, validation and confirmation are under
`../build/sve-equation27-manim-20261017/`.
