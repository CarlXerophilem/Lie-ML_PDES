# Scalar symmetry, data and flux verification

Status: **verified**.

Both scalar models use common scaling: `phi=t F(s/t)` on `t>0`, `F'>0`, `F-zF'>0`.
The normalized ray `s/t=1` carries `phi/t=2`, `phi_s=1/2`, `t phi_ss=1/10`.

- Exact chart, data and current checks passed for 2/2 model records, with symbolic real `m` on the declared branch.
- The current check uses `(T,z)=(t,s/t)`, Jacobian `T`, source zero, and boundary flux `I0/T`.
- The first integral is an additional reduction of ODE order, separate from the group quotient.
- 12/12 reference cases passed: maximum cross-solve error `3.331e-15`; integral drift `1.799e-14`; required `<=1e-9`.
- 5/5 negative controls passed: constant physical `phi=2` on the moving ray, `t=0`, and a zero chart determinant.

Exact reference-tube bounds are recorded separately from the 401-point sampled guard checks.
This verifies the declared scalar current and ray data. It supplies no arbitrary IBVP theorem,
maximal physical bed-field classification, weak-solution result, or neural speedup claim.

[Detailed evidence](data_flux.json) · [Workflow](data_flux_workflow.svg)
 · [Reference profiles and boundary flux](data_flux.svg)
