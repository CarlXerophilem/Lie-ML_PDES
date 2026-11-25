# What the completeness gates do and do not prove

The 43 conditions are tracked in `results/OBLIGATIONS.md`, with machine evidence,
conditional evidence, source proofs and unimplemented obligations separated.
They are a proof-obligation ledger, not 43 booleans that automatically establish
an unrestricted theorem. A finite list of reduced equations does not itself
solve all their local solution germs, handle singular orbits, or establish
coverage by a chart-preserving group.

Several proposed theorem formulations need qualification:

- A simple principal root proves algebraic regularity locally, not PDE local
  solvability or formal integrability. For example `(u_t)**2=0` has the same zero
  set as `u_t=0`, but its differential presentation has vanishing gradient on
  that set. Its infinitesimal criterion is degenerate. The new input gate rejects
  it instead of treating `solve()`'s unique root as a certificate.
- Janet/Riquier or Cartan–Kuranishi completion is one route to a completeness
  proof, with analytic/formal, regularity and termination qualifications. It is
  not a necessary implementation when an exact elimination proof already shows
  every smooth solution of the determining system has a specified form. It is
  not an unconditional finite algorithm for arbitrary smooth PDE input.
- Parameter rank-drop loci are algebraic on polynomial/rational charts. Real
  inequalities make the admissible strata semialgebraic. Gröbner ideals alone
  do not produce a full real stratification. Symbolic real powers `u**m` do not
  become a polynomial problem merely by declaring `u>0`.
- ODE reduction requires **base orbit rank d-1**, with the relevant regularity
  and transversality. Subalgebra dimension need not equal orbit rank. Pure
  vertical fields with no zeros (e.g. `d/du`) have no invariant graphs; fields
  such as `u*d/du` have fixed graphs (`u=0`) on charts containing that locus.
- A local section and flow give local correspondence. A conjugating local group
  transformation must be defined and preserve the chosen chart on the patch.
  No global group element or globally unique section intersection is assumed.
- The normalizer quotient describes inherited projectable symmetries under
  suitable descent hypotheses; its action may have a kernel. Hidden reduced
  symmetries require separate analysis. Point, contact, generalized and
  nonclassical symmetries are not one universally nested hierarchy.
- Euler-operator exactness is local in the appropriate differential-function
  setting. A checked differentiated flux is sufficient evidence here; global
  topology and physical bed reconstruction are separate questions.
- Picard–Lindelöf gives local existence/uniqueness for a suitably Lipschitz RHS.
  Analyticity of the solution requires analytic RHS assumptions. Nonresonance
  gives the stated analytic BB germ; resonance does **not necessarily** force
  logarithms: `rho*w'=w` has analytic solutions `w=C*rho`, whereas
  `rho*w'=w+rho` has the logarithmic obstruction. Each resonant recurrence must
  be checked. Uniqueness among arbitrary C1 patched profiles requires the
  corresponding desingularized dynamics argument, not only formal recurrence.
- Hyperbolicity means every eigenvalue has **nonzero real part**. Real nonzero
  eigenvalues are not required in general. In a real 2x2 saddle, `det J<0`
  supplies two real eigenvalues of opposite signs. Nodes can be hyperbolic,
  yet the specific saddle two-branch conclusion does not follow for nodes.
- For smooth one-forms, closedness gives local exactness; on a simply connected
  region it gives global exactness. General-degree Poincare statements need
  stronger topology. Prescribed IBVP symmetry and merely finding an invariant
  solution that happens to satisfy some data are different claims.
- Richardson-type undecidability prevents a universal elementary-expression
  identity oracle. Failure of `simplify` to return zero is not proof of nonzero;
  a successful transformation can still be useful under its branch assumptions.
  Exact rational/algebraic normalization and explicit unknown outcomes bound
  the implemented claim. This code does not replace all frozen symbolic proofs
  by a new proof assistant.

The numbered Olver theorem references in the proposed text are edition-dependent
and have not been independently page-verified in this coding stage. They are not
new citation claims in the manuscript. No dissertation prose has been changed.
