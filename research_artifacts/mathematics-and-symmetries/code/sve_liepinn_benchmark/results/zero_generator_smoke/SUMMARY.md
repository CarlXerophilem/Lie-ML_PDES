# Measured benchmark results

Pilot measurements on the recorded CPU, not paper reproduction or a general speed/accuracy claim.
Final checkpoints are fixed in advance. Ranges preserve every seed. The translated case is a structural equivariance check and is excluded from aggregate test errors.

| Group | Architecture | Loss | Parameters | Evolution error: median [min, max] | Training compute: median seconds | Matched runs |
|---|---|---|---:|---:|---:|---:|
| flat | mlp | vanilla | 2628 | 1.873 [1.873, 1.873] | 0.034 | 0/1 |
| flat | mlp | lie | 2628 | 1.873 [1.873, 1.873] | 0.049 | 0/1 |

Accuracy matching uses the stricter **maximum per-field evolution error**, not the aggregate error displayed above.
No cost advantage is asserted when that threshold is unmet. A single-PDE numerical trajectory is cached for repeated field queries.
Symbolic computation, numerical reference construction, training compute, monitoring, total wall time, and inference are logged separately.
The supplied-generator symbolic audit is not a maximal symmetry classification.

GIF exemplar: mlp/lie, seed 0, flat; selected by median error for display only.
