# LieSymm

`symm.LieSymm` is an importable, equation-first interface to the pinned
20 October general-SVE implementation. It keeps the existing `symm` modules
intact. It derives determining equations for supported normal forms and uses
explicit necessity certificates only for exactly matching declared SVE models.
It is **not an automatic maximal-classification solver for arbitrary PDEs**.

See the [delivery and validation](docs/DELIVERY.md),
[online software comparison](docs/PRIOR_ART.md),
[symbolic-computation assessment](docs/SYMBOLIC_COMPUTATION.md), and
[2026 printed-scalar solution demo](scalar2026/README.md).

Python 3.10+ and SymPy are required for the core (tested with Python 3.14.2 and
SymPy 1.14.0). pytest is required for the packaging tests. The separate
`scalar2026` demo has its own numerical/plotting dependencies; importing the
core does not import it. No network, external archive, or original `build/`
directory is needed by the supported core APIs.

## Use from the project root

```python
from symm.LieSymm import analyze, branch_model, traveling_reduction

model = branch_model("zero_transport")
report = analyze(**model)
print(report["classification_status"])
print(report["integration"]["basis"])
reduction = traveling_reduction(model, report["integration"]["basis"])
print(reduction["status"])
```

The CLI writes to a **new directory outside the installed package**:

```powershell
python -B -m symm.LieSymm --branch zero_transport --out build/liesymm-zero-new
python -B -m symm.LieSymm --dimension 2 --branch grass_cubic_f0 --out build/liesymm-2d-new
python -B -m symm.LieSymm --check-integrity
python -B -m pytest -q -p no:cacheprovider symm/LieSymm/tests
```

`--trace full` prints the mathematical derivation. Full 2D symbolic work can
be expensive; `--check-integrity` performs only byte/gate checks. The API has
no internal process timeout; callers running large symbolic cases should use
a bounded subprocess. The original campaign runners and gate-creation commands
are archived evidence, not portable public entrypoints.

For a standalone copy, copy the **entire `LieSymm` directory**, including
`_snapshot`, `SOURCE_MANIFEST.json` and `PORT_MANIFEST.json`, into a directory
on `PYTHONPATH`. Then use `import LieSymm` and `python -m LieSymm`. The relocation
test executes this layout from a temporary directory without the original
project on `PYTHONPATH`. This is a source-layout library, not a published wheel.

## A user-supplied equation

```python
import sympy as sp
from symm.LieSymm import JetSpace, analyze, verify_generator

t, x, u = sp.symbols("t x u", real=True)
J = JetSpace((t, x), (u,))  # derivative indices follow (t, x)
equations = (J.jet(u, (1, 0)) - J.jet(u, (0, 1)),)
report = analyze((t, x), (u,), equations, (),
                 {"model_id": "my_transport_equation"})
assert report["classification_status"] == "unresolved"
assert verify_generator(J, equations, (0, 1), (0,))["verified"]
```

This example has determining equations and a verified spatial translation,
but no integrated necessity certificate. A familiar `model_id` alone cannot
authorize a classification: equations, variables, parameters and guards must
also match the certificate. The current dispatcher accepts 1+1 and 2+1
coordinates; the 2D mixed-order backend is specifically adapted to its declared
SVE system. Singular time-leading matrices, exhausted jet order, or unsupported
normal forms can raise an explicit error. Unresolved nonpolynomial jet
identities remain in the report; they are not silently split.

## Public modules

| Module | Purpose |
| --- | --- |
| `core` (also top-level exports) | `JetSpace`, total derivatives, arbitrary coefficients, characteristic, prolongation, `analyze`, `verify_generator`, graph checks, brackets, serialization |
| `models`, `models_2d` | Eight 1D / seventeen 2D declared branch builders and their exact symbols |
| `reductions`, `reductions_2d` | Traveling/scaling, plane-wave, rotating/radial reductions with chart and reconstruction checks |
| `subalgebras`, `algebra_2d` | Adjoint and subalgebra calculations with their original completeness statuses |
| `data_experiments`, `data_experiments_2d` | Constructed flows and initial-data/boundary controls |
| `equivalence` | The supported point maps and explicit unresolved equivalence questions |
| `parent_models` | Separate printed scalar P, advectively corrected M, and material-coordinate controls |
| `nonclassical`, `nonclassical_equivalence`, `ml_adapter` | Bounded conditional/distribution tests and checked graph exports; no learning/training |
| `provenance` | `verify_snapshot`, `verify_adapter`, `check_historical_gate` |

`symm.LieSymm.main` is a namespaced compatibility facade. Do not add
`_snapshot` to `sys.path`, import its scripts directly, or execute its historical
runner/validator/release scripts. Those scripts contain historical output and
workspace assumptions. Their bytes are retained for audit, not exposed as
portable commands. The private `_loader.load_module` is not a public execution
or sandbox API.

Existing APIs remain usable at their original paths, for example
`from symm.sym_engine import Engine, PDE`, `symm.symmetry_engine`,
`symm.reductor`, `symm.generic`, `symm.solvers`, `symm.selection`, and
`symm.research_demos`. Their existing dependencies and mathematical scopes are
unchanged; LieSymm is a separate sibling package.

## Provenance and limits

`SOURCE_MANIFEST.json` pins **398 byte-identical files / 28,933,176 bytes**:
root sources and proof/review inputs, case/test sources, and only the evidence
referenced by the three frozen gates. It also records the original release
manifest hash. Exploratory run trees are excluded. Historical JSON may contain
absolute source/log paths as inert provenance; supported gate checks resolve
their relative hash keys inside the packaged snapshot.

The Python source bytes are unmodified. Execution imports use a **new adapter**:
each loaded module has its own `__import__` binding that maps sibling imports
to a private package namespace. The adapter never adds the snapshot to
`sys.path`, registers a global import hook, changes global builtins, or creates
bare `main`/`models` aliases. Python execution compiles the copied source bytes;
this is not a claim that the import semantics are byte-identical to the old
script environment.

The one runtime function replacement is `gatekeeper.check_hashes`: it resolves
both Windows and POSIX receipt separators, rejects path escape, and performs
the same SHA-256 byte comparison. No gate or review hashes are rewritten.
Missing/changed evidence fails the gate. `PORT_MANIFEST.json` separately pins
the new adapter/API/test bytes. Its integrity result is not a fresh scientific
review; the new validation receipts and independent reviewer address that.

`proved_for_declared_regular_chart` retains its historical meaning only for
the exact registered equations and guards. Positive-depth/speed charts,
parameter strata, denominators, singular branches, and local smoothness
assumptions remain essential. In particular:

- The scalar printed P, corrected M, and full Eulerian models are distinct.
- Verifying generators is not by itself a proof of maximal classification.
- Reducing independent variables does not automatically reduce ODE order.
- Data compatibility and initial-data stabilizers are additional checks.
- A finite nonclassical registry is not unrestricted nonclassical classification.
- No global solution, arbitrary IBVP, E/P/M equivalence, ML advantage, or new
  mathematical novelty follows from packaging this implementation.

The historical `subalgebra_classification` convenience field can still say
`bracket_verified_optimal_system_not_proved`; consult the separate subalgebra
certificate/status, not a maximal point-algebra status, for optimality claims.
Old failed project audits remain failed qualifications inside the preserved
gates. A passing historical gate does not relabel them as passing.
