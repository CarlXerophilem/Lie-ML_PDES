# Independent review of line subalgebras and release controls

Review date: 20 October 2026. The reviewer did not author `subalgebras.py`,
`SUBALGEBRAS.md`, `gatekeeper.py`, or `run_all.py`. Author sources were
read-only. Reviewer outputs are this document, `review_subalgebras.py`, and
`subalgebra_review.json`. The exact reviewed hashes and computation receipts
are in the JSON file; sources are snapshotted before author imports and
checked unchanged at completion.

## Verdicts

**One-dimensional subalgebra classification: accepted.** For every supplied
maximal 1D PDE point algebra, the generated families are exhaustive and
nonredundant under the **connected inner adjoint action and arbitrary nonzero
line-generator rescaling**. This includes all slope-only exponents in the
continuous interval `0<=n<=4`, with the required four resonance strata.
It is not a classification under disconnected point transformations or outer
automorphisms, and not a classification of higher-dimensional subalgebras.

**Release controls: accepted for the produced receipts on a frozen source
snapshot.** The revised gatekeeper checks individual child outcomes, logs,
child-source hashes, branch identities, source stability, the current
classification review, required validation commands, and the specifically
required data/parent review. The independent controls use a virtual in-memory
filesystem; this review neither creates nor unlocks a live stage gate.
The root must still run the actual children and required project validations.

The optimality verdict is separate from fixed-PDE point-algebra maximality.
A stage-1 maximality gate does not by itself certify this optimal-system
result, and this result does not justify the full equivalence groupoid or
usefulness of every representative for reduction.

## Independent mathematical audit

Write the verified algebra as `g=V semidirect A`, with abelian `V,A` and real
diagonal weights `W`: `[A_j,V_i]=W_ij V_i`. The source derives these weights
from the actual coordinate vector fields. The reviewer independently forms
all coordinate brackets by differentiation and reconstructs them from the
exported adjoint matrices. Thus the argument applies to the actual SVE
algebras, not a guessed abstract table. The checked weights are:

| Algebra | Weights on `(T,X,Z)` |
|---|---|
| First-order, positive K, m!=3 | `(-1),(-1),(0)` |
| First-order cubic or K=G=0 | `(-1,-1),(-1,0),(0,2)` |
| Positive K and G, m!=3 | no diagonal direction; abelian translations |
| Cubic slope or slope-only | `(2-n),(1-n),(-2)` |

For `Y=v+a`, the full elementary adjoint actions are

`Ad(exp(w))Y = v - diag(Wa)w + a`, for `w in V`,

`Ad(exp(s))Y = diag(exp(Ws))v + a`, for `s in A`.

The translation adjoint squares to zero. Its minus sign agrees with
`[w,a]=-[a,w]` and with direct matrix action. Since `V` is an ideal and both
subgroups are abelian, products of elementary transformations can be
reordered into a translation and a diagonal transformation. Hence these
formulas describe the entire connected inner action. In particular, the
projection `a` is unchanged. There is no hidden inner transformation which
mixes the two diagonal directions or permutes translation coordinates.

### Translation-only lines

When `a=0`, the translation subgroup acts trivially. Positive real diagonal
factors preserve support and the sign of every nonzero coefficient. A
negative line factor reverses all signs simultaneously; fixing the first
supported coefficient positive removes precisely that one ambiguity.

For a supported set `S`, let `y=log(abs(v_S))`. Its complete magnitude action
is the affine translation `y -> y+M theta`, with `M=[1 | W_S]`. Thus two
points with the same support and oriented signs are equivalent if and only
if their log difference belongs to `im(M)`.

The source's independent row/column minor sets pivot log coordinates to
zero. Its projector `Pi` satisfies `Pi*M=0`, `Pi^2=Pi`, and has an identity
block on the unselected columns. Consequently `ker(Pi)=im(M)`: inclusion
follows from the first identity, and dimensions agree. The unselected
coordinates are therefore independent quotient coordinates, not an
overcomplete list of invariants. Exponentiation is a bijection from each
real quotient coordinate to a positive modulus.

The independent verifier also computes a complete annihilator `N` of
`im(M)` from `ker(M.T)`, separately from the exported projector. It checks
that normalization preserves these invariants and that their restriction
to the canonical free coordinates is invertible. This provides a second
linear-algebra certificate for coverage and uniqueness on every support.
Support/sign enumeration is checked exhaustively, rather than through random
orbits. For three translation directions there are thirteen representative
families; a family can have continuous moduli.

The significant retained moduli are correct. An abelian three-dimensional
algebra has two independent full-support ratios. With only the common
first-order dilation, the time/space translation ratio remains invariant.
With the two first-order diagonal directions, the full-support augmented
weight matrix has determinant `-1`, so no positive magnitude modulus
remains. Restricting every coefficient to `0,+1,-1` in the former two cases
would have been incomplete; the implementation does not do that.

### Nonzero diagonal projection

Normalize the first nonzero coefficient of `a` to one. This uses the unique
line factor and leaves no further global sign/rescaling freedom. Inner
transformations preserve the normalized `a` exactly.

Every component with `(Wa)_i!=0` is removed by choosing
`w_i=v_i/(Wa)_i`. All zero-eigenvalue components survive every translation
action. The independent check uses the actual adjoint matrices, verifies
nilpotence, and confirms that this move removes exactly the nonkernel
coordinates while leaving `a` and every kernel coordinate unchanged.

On a supported subset of that kernel, the only remaining magnitude action
has matrix `M=W_S`; there is **no** line-scaling column. Every sign remains
invariant. The same quotient argument now proves coverage and uniqueness.
With one diagonal direction, a kernel translation is central and its full
real coefficient survives: for example `C+cZ` cannot be reduced merely to
`C,C+Z,C-Z`. Its disjoint representation by zero and positive/negative
modulus families is correct.

With two diagonal directions, the projective charts `(1,r)` and `(0,1)` are
disjoint and exhaustive. For the actual first-order weights, the finite
exceptional directions are exactly `r=0,-1`, and the infinite direction has
its own kernel. The resulting nonzero-A representatives are

`C+rR`, `r in R minus {0,-1}`;

`C+epsilon Z`, `C-R+epsilon T`, and `R+epsilon X`, each with
`epsilon in {-1,0,1}`.

The remaining independent scaling normalizes the single surviving magnitude
in each exceptional direction. These ten families, plus thirteen translation
families, are complete and nonredundant. No ratio of diagonal coefficients
is silently changed by an outer automorphism.

### Continuous slope parameter and resonances

For `W=(2-n,1-n,-2).T`, a new kernel requires a zero weight, giving `n=1,2`.
For translation magnitudes with one diagonal direction, every possible rank
jump of `[1|W_S]` requires equal weights, giving `n=3,4`. The time/space
weight difference is constantly one. Thus these mechanisms exhaust all
relevant rank/kernel changes; the complete exceptional set in `[0,4]` is
`{1,2,3,4}`. In particular, `n=0` is regular and belongs to the generic
stratum. The software's generic interval plus four singleton strata are
disjoint and cover the whole requested interval, not merely integer samples.

At `n=1,2`, the lines `D_1+cX` and `D_2+cT` retain a real central modulus.
At `n=3,4`, the corresponding equal-weight translation pairs retain their
positive ratio. Full-support translation lines always have one continuous
invariant

`abs(v_Z)*abs(v_T)^(3-n)*abs(v_X)^(n-4)`.

Its limits at `n=3,4` are respectively `abs(v_Z)/abs(v_X)` and
`abs(v_Z)/abs(v_T)`, agreeing with the resonant pair geometry. No special
parameter value is removed by dividing by a zero weight or a vanishing
normalization minor; each required nonzero condition is retained within
the appropriate stratum.

These arguments prove necessity of the invariants and sufficiency of the
normalization moves. Passing finite representative tests alone would not
prove optimality; the complete orbit formulas and quotient proof do.

## Release-control audit and repairs

The first inspected gatekeeper trusted aggregate child success without
rechecking each child exit/status/log, did not check the derivation's model
identity, and allowed any nonempty accepted review list to stand in for the
required data/parent review. These were reported to the author and repaired
in author-owned files before this accepted review. The reviewer did not
modify those files.

The revised gate requires exactly the declared set and count of children,
each with zero exit and normal termination, the expected log path and digest,
and the current child-script digest. It requires the matching model id and
successful classification/generator/traveling-reduction fields. The runner
also exits unsuccessfully when its supported scaling, subalgebra, or exact
data controls fail. Both source snapshots must agree and remain current.

The required data review is now the specifically named receipt, with accepted
status, declared review domains, and the required reviewed source hashes.
A classification receipt alone cannot replace it. The stage gate retains
hashes of source files, branch output files, logs, validation receipts, and
independent review receipts. A changed source or evidence file therefore
invalidates the subsequent gate check. No stage receipt hashes itself.

The independent virtual controls test successful creation and subsequent
checking; changed source/evidence; a nonzero child exit; a timeout disguised
as zero exit; changed child log/source; wrong model identity; duplicate child;
source snapshot drift; protected-input failure; changed validation log;
non-audit validation failure; missing data-review scope; and substitution of
the classification review for the data review. A bare `passed` flag cannot
open the gate. An unchanged pre-existing audit issue set is retained explicitly
as a **failed audit qualification**, rather than relabeled as passing.

`run_all.py` takes before/after hashes of cycle, child, and test Python
sources, runs each child separately with bounded subprocess execution, and
preserves exit status and log hashes. Downstream dispatch requires the
preceding stage gate. These are release-integrity controls for the generated
receipts and stable-source workflow, not a signature/authentication system
against someone deliberately rewriting all code and receipts together.

The gate's stage-1 maximality scope and this optimality review remain distinct.
Full equivalence-groupoid classification remains unresolved. Full child runs,
project audit/data-flux/workflow, and project test suites must still be supplied
by the root release process; this review does not impersonate those executions.

## Reproduction and limitations

Run `python -B build/sve-general-symm-20261020/review_subalgebras.py` from
the repository root. It writes only `subalgebra_review.json`. Review fixtures
never write a live stage gate. Exact check counts, source hashes, elapsed
time, branch family counts, and virtual gate controls are preserved in the
receipt. The enclosing run used a bounded subprocess under the symbolic CPU
lease.

The accepted mathematical equivalence is connected inner adjoint plus line
rescaling only. Disconnected reflection, outer automorphisms, higher-dimensional
subalgebras, global action on arbitrary restricted domains, reduction
usefulness, and fixed initial/boundary data are separate questions. In
particular, a pure bed-translation line has zero projected base rank and
does not itself reduce the number of independent variables.
