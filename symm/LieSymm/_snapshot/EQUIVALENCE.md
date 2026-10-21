# Exact maps and the unresolved equivalence-classification obligation

This note concerns the **full coupled 1D** system, for smooth fields on
`h>0, u!=0`, with `g>0`, `K,G>=0`:

\[
E_h=h_t+(hu)_x=0,\qquad
E_u=u_t+uu_x+g(h_x+B_x)=0,
\]
\[
E_B=B_t+D_x\{K|u|^{m-1}u-G|u|^n B_x\}=0.                 \tag{1}
\]

The main registry uses the positive-speed chart, on which the flux is
`K*u**m-G*u**n*B_x`. The negative-speed statements below refer to the
signed absolute-value extension in (1). They are not an assertion about
real noninteger powers of negative numbers. The parent source/model audit
governs the physical provenance of the two slope prescriptions. No map
here identifies the printed scalar, corrected scalar, or material-coordinate
models with a local point representation of (1).

## 1. An invertible equivalence subgroup

For constant `a,b,C>0`, `s=+1` or `-1`, and real constants `t0,x0,d`, put

\[
t'=at+t_0,\quad x'=sbx+x_0,\quad
h'=Ch,\quad u'=s\frac ba u,\quad B'=CB+d.                \tag{2}
\]

The parameter map is

\[
g'=\frac{b^2}{a^2C}g,\qquad
K'=C\left(\frac ab\right)^{m-1}K,\qquad
G'=b^{2-n}a^{n-1}G,\qquad m'=m,\ n'=n.                  \tag{3}
\]

Direct substitution, with the transformed residual evaluated in primed
variables and then pulled back, gives **off-shell identities**

\[
E'_h=\frac Ca E_h,\qquad
E'_u=s\frac b{a^2}E_u,\qquad
E'_B=\frac Ca E_B.                                     \tag{4}
\]

For example, `D_x'=s D_x/b`, `|u'|=(b/a)|u|`, and

\[
K'|u'|^{m-1}u'-G'|u'|^nB'_{x'}
 =s\frac{Cb}{a}\{K|u|^{m-1}u-G|u|^nB_x\}.
\]

This proves the Exner identity without specializing an exponent or a
solution. The full point-map Jacobian is `b^2*C^2>0`. Its inverse is

\[
t=(t'-t_0)/a,\quad x=s(x'-x_0)/b,\quad h=h'/C,
\quad u=s(a/b)u',\quad B=(B'-d)/C.                       \tag{5}
\]

Thus (2) preserves `h>0`, coefficient signs and coefficient-zero strata.
Choosing `s=-1` relates the two nonzero-speed charts. Translation and
rescaling of a solution also transform its domain and data; the same fixed
initial/boundary data need not be invariant. Reflection of `x` alone fails.
The executable certificate checks both source speed signs and both values
of `s`, with free jets and symbolic real `m,n`.

## 2. Exact orbits under this subgroup

Set `r=b/a>0`. Equations (3) become

\[
g'=r^2g/C,\qquad K'=Cr^{1-m}K,\qquad
G'=br^{1-n}G,\qquad g'K'=r^{3-m}gK.                     \tag{6}
\]

If `K>0` and `m!=3`, choose

\[
r=(gK)^{1/(m-3)},\quad C=gr^2,
\quad b=\begin{cases}r^{n-1}/G,&G>0,\\1,&G=0,\end{cases}
\quad a=b/r.                                           \tag{7}
\]

This gives `g'=K'=1`, with `G'=1` if active and `G'=0` otherwise.
Every scale in (7) is positive. The division by `m-3` is forbidden on
the cubic stratum.

If `K>0,m=3`, choose `r=1,C=g`, and `b=a=1/G` when `G>0`
(or `a=b=1` when `G=0`). Then `g'=1`, `K'=gK`, and the active
`G'=1`. The dimensionless quantity `gK` is an invariant of this
subgroup. Two positive coefficient triples with fixed effective
exponents on this cubic stratum lie in the same subgroup orbit exactly
when their `gK` values agree: necessity follows from (6); sufficiency
follows by composing their maps to the common representative.

If `K=0,G>0`, choose `a=b=1/G,C=g`; then `g'=G'=1`.
If `K=G=0`, choose `a=b=1,C=g`; only `g` needs normalization.
For three active coefficients, the logarithmic parameter action has matrix

\[
\begin{pmatrix}-2&2&-1\\m-1&1-m&1\\n-1&2-n&0\end{pmatrix},
\qquad \det=3-m.                                       \tag{8}
\]

This provides an independent rank check for the coefficient modulus.
Neither (6) nor (8) proves that `gK` is invariant under every possible
admissible point transformation; that larger classification is unresolved.

## 3. Deduplicate equations before counting branches

The following are equalities of PDEs, not conjectured equivalences:

| Coefficient branch | Effective exponents | Deduplication rule |
|---|---|---|
| `K>0,G>0` | `m,n` | Retain both prescribed curves `n=m-1` and `n=m`. |
| `K>0,G=0` | `m` | Erase `n`; the two slope-law labels give the same PDE. |
| `K=0,G>0` | `n` | Erase `m`; classify one continuous interval `0<=n<=4`. |
| `K=G=0` | neither | Erase both exponents; retain one zero-transport family. |

In the slope-only branch, `n=m-1` covers `[0,3]` and `n=m` covers
`[1,4]`; their union is `[0,4]`, and their overlap is not two different
models. The endpoint `n=0` retains constant diffusivity `G>0` and cannot
be merged with `G=0`. These are continuous parameter families. Finite
samples at integer exponents do not establish their coverage.

## 4. Primitive and momentum variables are a genuine point map

Write `q=hu`. The field map `(h,u,B)->(h,q,B)` has Jacobian `h>0`
and inverse `u=q/h`. Its conservative momentum residual satisfies

\[
E_q:=(hu)_t+(hu^2+gh^2/2)_x+ghB_x=hE_u+uE_h.             \tag{9}
\]

Thus `(E_h,E_u,E_B)=0` and `(E_h,E_q,E_B)=0` are equivalent for
smooth positive-depth fields, with transport evaluated at `u=q/h`.
Under (2), `q'=sCbq/a` and `E'_q=sCbE_q/a^2`.
A point field pushes forward by
`eta_q=u*eta_h+h*eta_u`; the inverse coefficient is
`eta_u=(eta_q-u*eta_h)/h`. This transports a proved maximal point
algebra between these two local representations. It does not establish
equivalence at dry states `h=0` or for weak/shock formulations.

## 5. A bed reference must retain its derivatives

For a prescribed smooth, time-independent reference bed `b0(x)`, the map
`B=b0(x)+zeta` is invertible with field Jacobian one. Its exact rewrite is

\[
u_t+uu_x+g(h_x+b_0'(x)+\zeta_x)=0,
\]
\[
\zeta_t+D_x\{K|u|^{m-1}u-G|u|^n(b_0'(x)+\zeta_x)\}=0.    \tag{10}
\]

The mass equation is unchanged. A constant `b0` is precisely a datum
translation within (1). A general `b0(x)` produces an explicitly
inhomogeneous representation; deleting its slope or curvature changes the
PDE. An arbitrary time-dependent datum is also not a symmetry of (1),
since its time derivative remains in Exner. A general prescribed
`b0(t,x)` can be rewritten only by retaining `b0_t` as well.

## 6. A restricted necessity result, with its assumptions visible

One can prove necessity of the displayed form in the following narrower
category without a finite generator ansatz. Assume in advance

\[
T=at+t_0,\quad X=bx+ct+x_0,\quad
H=H(h),\quad U=U(u),\quad Z=Z(B),                         \tag{11}
\]

with nonzero derivatives and positive orientation/scales. This restriction
is an assumption, not a consequence already proved for arbitrary point
maps. Pull back the new mass equation and eliminate `h_t` using the old
one. Its free `h_x` coefficient gives `U=(bu+c)/a`, and its `u_x`
coefficient gives `H=hH_h`. Hence `H=Ch`. The two hydrostatic-gradient
coefficients in the new momentum equation give
`g'C/b=bg/a^2` and `Z_B=C`, so `Z=CB+d` and the first map in (3).

The pulled-back Exner equation has the standalone term
`-Cc B_x/(ab)`. The other flux terms contain `u_x`, `B_xx`, or
`u_x B_x`, so free-jet splitting forces `c=0`. There is no Galilean
boost in category (11). With `K,K'>0` and `m,m'>=1`, comparing the
`u_x` coefficients on a positive-speed interval forces `m'=m` and
the second map in (3). With `G,G'>0`, comparing `B_xx` forces
`n'=n` and the third map. The zero-coefficient cases remove the
corresponding exponent as in section 3. Spatial/velocity reflection is
then a separately verified discrete component.

This argument starts from arbitrary one-variable functions `H,U,Z`, so
it excludes nonlinear separated field changes in category (11). It does
not exclude mixing `h,u,B`, dependence of the new base coordinates on
fields, non-affine base maps, special exponent-changing maps, or
additional discrete components. In particular, knowing the maximal Lie
symmetry algebra of each fixed equation is insufficient by itself to
classify maps between different equations.

There is already a useful additional discrete control: when `G=0`,
`t'=-t,x'=x,u'=-u,h'=h,B'=B` preserves the signed family with
the same `g,K`. The residual multipliers are `(-1,+1,-1)`.
For `G>0` the same change would require `G'=-G`, outside the
declared nonnegative-coefficient family. The positive-time subgroup in
section 1 therefore should not be called the whole equivalence group,
even before the remaining general-map analysis is attempted.

## 7. What is certified and what remains open

`equivalence.py` exports `parameter_map()`, `effective_exponents()`,
`normal_form()`, `verify_maps()`, and `equivalence_status()`.
Run `python -B build/sve-general-symm-20261020/equivalence.py` from the
project root. The command prints exact residual remainders, guard tests,
broken-hypothesis witnesses and machine-readable status; it writes no files.

Local validation on 2026-10-20: `verify_maps()` passed all 66 checks in
0.261 seconds (excluding interpreter import). All recorded residual
remainders were exactly zero; the five deliberately broken transformations
had nonzero witnesses. The noncubic symbolic tests use a real nonzero
symbol for `m-3`, retaining the branch condition rather than sampling `m`.
The parent workflow owns the independent regression/review and project-wide
checks; this local receipt does not substitute for them.

The exact maps, subgroup orbit normalizations, coordinate rewrites and
identical-PDE deduplication are certified separately. **Full local
point-equivalence classification is unresolved.** Its completion needs
necessary equations for the most general admissible invertible point map,
their integration on every zero/exponent stratum, and a treatment of
discrete components. The strict equivalence-coverage gate therefore remains
closed. A finite list of successful maps or generators cannot open it.
