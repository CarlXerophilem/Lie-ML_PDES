# SVE boundary-case animation

This project visualizes a **fixed, flat-bed limit** of equations (1)-(4) in:
Paliathanasis, A., Leon, G. & Leach, P. G. L. (2026), *Lie Symmetries and Similarity Solutions for a Shallow-Water Model with Bed Elevation in Lagrange Variables*, Mathematics 14(3), 433. DOI: https://doi.org/10.3390/math14030433.

The paper supplies the SVE model and symmetry framework. The dry-bed dam-break initial/boundary conditions below are **chosen for this demonstration**; they are not an initial-value experiment reported in the paper. This project does not model sediment motion, a general mobile-bed solution, or a two-horizontal-dimensional flow. The picture is a time-dependent x-z cross-section of a (1+1)D, depth-averaged model, with vertical exaggeration. The x-t panels show the complete space-time history, while a horizontal cursor selects the current cross-section.

## 1. Start from the paper's Eulerian system

With depth h, horizontal velocity u, bed elevation B and gravitational acceleration g,

\[
h_t+(hu)_x=0,\qquad
(hu)_t+(hu^2+gh^2/2)_x+ghB_x=0,
\]
\[
B_t+\beta u^{m-1}u_x=0,\qquad \beta=mA_g\xi.
\]

Set A_g=beta=0 and B(x,0)=0. Then B=0 at all times and the two remaining PDEs are the classical shallow-water equations. The exponent m has no effect in this limit. In particular this is not a demonstration of the paper's additional m=3 mobile-bed symmetry.

## 2. Specify the boundary case and boundary data

At t=0 a dam at x=0 is instantaneously removed:

\[
(h,u)(x,0)=\begin{cases}(h_0,0),&x<0,\\(0,0),&x>0,\end{cases}
\qquad h_0=1\ \mathrm m,\quad g=9.81\ \mathrm{m/s^2}.
\]

We simulate -40 <= x <= 60 m until t=8 s. Constant ghost states are (h,hu)=(1,0) on the left and (0,0) on the right. The exact fan head and dry front stay inside the domain throughout this interval. At the dry front, h and hu approach zero continuously. The fluid-side velocity approaches the shoreline speed, whereas velocity is physically undefined in the dry region. Arrays store dry velocity as zero only as a numerical convention; velocity heatmaps mask h<1e-4 m.

## 3. Lie scaling turns the PDEs into ODEs

The Eulerian scaling generator is X=t*d/dt+x*d/dx, with h and u unchanged. Its characteristic system is

\[
dt/t=dx/x,\qquad dh=du=0.
\]

Therefore zeta=x/t, h=H(zeta), u=U(zeta). This is consistent with the paper's simultaneous scaling of t,s,phi under X4=t*partial_t+s*partial_s+phi*partial_phi, since x=phi, u=phi_t and h=1/phi_s. We derive the flat-bed solution directly from equations (1)-(4), rather than using a potentially singular branch of the master equation.

For any f(zeta), partial_t f=-(zeta/t)f' and partial_x f=f'/t. Continuity and the primitive momentum equation yield

\[
(U-\zeta)H'+HU'=0,\qquad
gH'+(U-\zeta)U'=0.
\]

For a nonconstant solution the determinant vanishes:

\[
(U-\zeta)^2-gH=0.
\]

Choose the left-family rarefaction: zeta=U-c, c=sqrt(gH). Substitution into continuity gives c H'+H U'=0. Since H=c^2/g, this becomes 2c'+U'=0, and hence U+2c=constant. Matching the still reservoir sets the constant to 2c0, c0=sqrt(g h0). Solving U-c=zeta and U+2c=2c0 gives

\[
c=(2c_0-\zeta)/3,\quad U=2(c_0+\zeta)/3,\quad H=(2c_0-\zeta)^2/(9g).
\]

## 4. Match the exact solution

For t>0,

\[
h(x,t)=\begin{cases}
h_0,&x\le-c_0t,\\
(2c_0-x/t)^2/(9g),&-c_0t<x<2c_0t,\\
0,&x\ge2c_0t.
\end{cases}
\]

In the fan, u=2(c0+x/t)/3; in the undisturbed reservoir u=0. The exact front is xf=2c0t, and the fan head is xh=-c0t. This is the classical Ritter dry-bed rarefaction, not a shock. At t=8 s, xf=50.11347 m and xh=-25.05674 m.

For background on shallow-water characteristic speeds, rarefactions and dry states, see the primary [Clawpack Riemann book](https://www.clawpack.org/riemann_book/html/Shallow_water.html).

### Connection back to the paper's Lagrange variables

Choose a conserved mass label s<=0, measured from the dry front. In the fan,

\[
s=-\frac{(2c_0t-x)^3}{27gt^2},\qquad
x=\phi(s,t)=2c_0t-3(-gs)^{1/3}t^{2/3}.
\]

Here s_x=h and s_t=-hu, so s is constant on fluid trajectories. The fan has -h0*c0*t < s < 0; before a parcel enters the fan, phi=s/h0. Differentiation gives phi_t=u and phi_s=1/h. Direct substitution verifies the paper's flat-bed equation (5), phi_tt-g*phi_ss/phi_s^3=0, and therefore equation (7) with beta=0. The map is regular inside the wet fan and becomes singular at s=0, where depth vanishes. The formula obeys phi(lambda*s,lambda*t)=lambda*phi(s,t), linking this benchmark to the paper's X4 invariance. We do not use the paper's nonzero-beta bed transformation to extrapolate this fixed-bed result.

## 5. Compute an independent numerical solution

`solve_sve.py` evolves conserved cell averages Q=(h,q), q=hu, with flux F=(q,q^2/h+gh^2/2). It uses first-order finite volumes with the local Lax-Friedrichs/Rusanov interface flux

\[
\widehat F_{i+1/2}=\tfrac12(F_i+F_{i+1})-\tfrac12 a_{i+1/2}(Q_{i+1}-Q_i),
\quad a_{i+1/2}=\max(|u_i|+\sqrt{gh_i},|u_{i+1}|+\sqrt{gh_{i+1}}),
\]
\[
Q_i^{n+1}=Q_i^n-\frac{\Delta t}{\Delta x}(\widehat F_{i+1/2}-\widehat F_{i-1/2}).
\]

Use CFL=0.45, N=1200 and dx=1/12 m. No positive depth floor is imposed. Momentum is zeroed when h<=1e-12 m to avoid division by essentially zero depth. Negative depths below -1e-13 m trigger an error. The plotted simulation comes from these numerical arrays, not from substituting the exact formula. The exact solution is shown as a separate dashed reference.

## 6. Verification

`verification.json` records actual run results. SymPy reduces both PDE residuals to exactly zero in the smooth fan; the bed equation vanishes because B=beta=0. At interfaces, h and hu are continuous, making the interface jump conditions zero; the initial dam discontinuity is approached in the weak sense.

Depth errors compare numerical cell averages with **exact cell averages**, not point samples. The normalized L1 error is integral|h_num-h_exact| dx divided by the initial water area (40 m^2 per unit width). Mesh refinement uses N=600,1200,2400 and checks decreasing final error. The movie's N=1200 run additionally aligns time steps with 161 output times, so its error differs slightly from the convergence run. Expect numerical diffusion near the fan head and thin advancing front; this baseline is deliberately simple and is not claimed to be an optimal solver.

## Run

Install a working Manim Community environment (including its Cairo/Pango and LaTeX system dependencies), then:

```bash
python -m pip install -r requirements.txt
python solve_sve.py
python plot_solution.py
python -m manim -qm --fps 24 --disable_caching --media_dir media pde_scene.py SVEProcess
```

The movie has animated equation derivations followed by scientific simulation frames. `pde_scene.py` uses Manim for the full timeline; `plot_solution.py` uses Matplotlib to rasterize the numerical fields reproducibly. Equation paths are generated using `pdflatex` and Poppler's `pdftocairo`, avoiding a dependency on `dvisvgm`; install those commands as well. All arrays and verification results are in output/. The PNG is a high-resolution final snapshot. The MP4 in the delivered package is the rendered movie.

To change h0, g, extent or final time, update the solver constants and plot axes together; ensure the wave boundaries do not reach the outer boundaries unless new boundary conditions are intentionally supplied.
