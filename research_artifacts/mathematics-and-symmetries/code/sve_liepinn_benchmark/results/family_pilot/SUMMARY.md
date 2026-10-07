# Measured benchmark results

Pilot measurements on the recorded CPU, not paper reproduction or a general speed/accuracy claim.
Final checkpoints are fixed in advance. Ranges preserve every seed. The translated case is a structural equivariance check and is excluded from aggregate test errors.

| Group | Architecture | Loss | Parameters | Evolution error: median [min, max] | Training compute: median seconds | Matched runs |
|---|---|---|---:|---:|---:|---:|
| family | mlp | vanilla | 2628 | 0.1528 [0.134, 0.1618] | 3.014 | 0/3 |
| family | mlp | lie | 2628 | 0.151 [0.1308, 0.1591] | 5.269 | 0/3 |
| family | mlp | reweighted | 2628 | 0.151 [0.1308, 0.1591] | 3.197 | 0/3 |
| family | mlp | cosine | 2628 | 0.1528 [0.134, 0.1618] | 7.710 | 0/3 |
| family | mlp | conservation | 2628 | 0.204 [0.1918, 0.2051] | 3.597 | 0/3 |
| family | modified | vanilla | 2596 | 0.1327 [0.1158, 0.1608] | 4.097 | 0/3 |
| family | modified | lie | 2596 | 0.1303 [0.1151, 0.1602] | 6.213 | 0/3 |
| family | modified | reweighted | 2596 | 0.1303 [0.1151, 0.1602] | 3.948 | 0/3 |
| family | modified | cosine | 2596 | 0.1327 [0.1158, 0.1608] | 8.374 | 0/3 |
| family | modified | conservation | 2596 | 0.1524 [0.1235, 0.1737] | 4.487 | 0/3 |
| family | deeponet | vanilla | 2641 | 0.155 [0.1431, 0.1627] | 3.120 | 0/3 |
| family | deeponet | lie | 2641 | 0.1521 [0.1416, 0.166] | 5.474 | 0/3 |
| family | deeponet | reweighted | 2641 | 0.1521 [0.1416, 0.166] | 3.228 | 0/3 |
| family | deeponet | cosine | 2641 | 0.1549 [0.1431, 0.1627] | 7.611 | 0/3 |
| family | deeponet | conservation | 2641 | 0.1675 [0.163, 0.1776] | 3.661 | 0/3 |

Accuracy matching uses the stricter **maximum per-field evolution error**, not the aggregate error displayed above.
No cost advantage is asserted when that threshold is unmet. A single-PDE numerical trajectory is cached for repeated field queries.
Symbolic computation, numerical reference construction, training compute, monitoring, total wall time, and inference are logged separately.
The supplied-generator symbolic audit is not a maximal symmetry classification.

GIF exemplar: mlp/lie, seed 2, test_m2.95_a0.03; selected by median error for display only.
