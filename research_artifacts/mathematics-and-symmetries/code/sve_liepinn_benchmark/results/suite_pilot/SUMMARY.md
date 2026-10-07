# Measured benchmark results

Pilot measurements on the recorded CPU, not paper reproduction or a general speed/accuracy claim.
Final checkpoints are fixed in advance. Ranges preserve every seed. The translated case is a structural equivariance check and is excluded from aggregate test errors.

| Group | Architecture | Loss | Parameters | Evolution error: median [min, max] | Training compute: median seconds | Matched runs |
|---|---|---|---:|---:|---:|---:|
| flat | mlp | vanilla | 2628 | 0.144 [0.1204, 0.1543] | 2.959 | 0/3 |
| flat | mlp | lie | 2628 | 0.1421 [0.1212, 0.1619] | 4.450 | 0/3 |
| flat | mlp | reweighted | 2628 | 0.1421 [0.1212, 0.1619] | 3.053 | 0/3 |
| topography | mlp | vanilla | 2628 | 0.1077 [0.08947, 0.1346] | 2.934 | 0/3 |
| topography | mlp | lie | 2628 | 0.1096 [0.09015, 0.1435] | 4.381 | 0/3 |
| topography | mlp | reweighted | 2628 | 0.1096 [0.09015, 0.1435] | 3.008 | 0/3 |
| rotation_drag | mlp | vanilla | 2628 | 0.04676 [0.03671, 0.04839] | 3.062 | 0/3 |
| rotation_drag | mlp | lie | 2628 | 0.0486 [0.03924, 0.05361] | 4.565 | 0/3 |
| rotation_drag | mlp | reweighted | 2628 | 0.0486 [0.03924, 0.05361] | 3.256 | 0/3 |
| sve_m2.9 | mlp | vanilla | 2628 | 0.1036 [0.09983, 0.1326] | 3.113 | 0/3 |
| sve_m2.9 | mlp | lie | 2628 | 0.09632 [0.09588, 0.1243] | 5.359 | 0/3 |
| sve_m2.9 | mlp | reweighted | 2628 | 0.09632 [0.09588, 0.1243] | 3.111 | 0/3 |
| sve_m3 | mlp | vanilla | 2628 | 0.1114 [0.09625, 0.1133] | 3.044 | 0/3 |
| sve_m3 | mlp | lie | 2628 | 0.1212 [0.1031, 0.1219] | 5.416 | 0/3 |
| sve_m3 | mlp | reweighted | 2628 | 0.1212 [0.1031, 0.1219] | 3.128 | 0/3 |
| sve_m3.1 | mlp | vanilla | 2628 | 0.1144 [0.0957, 0.1207] | 3.131 | 0/3 |
| sve_m3.1 | mlp | lie | 2628 | 0.1076 [0.09143, 0.1156] | 5.343 | 0/3 |
| sve_m3.1 | mlp | reweighted | 2628 | 0.1076 [0.09143, 0.1156] | 3.165 | 0/3 |
| sve_m4 | mlp | vanilla | 2628 | 0.123 [0.1109, 0.1684] | 2.984 | 0/3 |
| sve_m4 | mlp | lie | 2628 | 0.1126 [0.1081, 0.1593] | 5.235 | 0/3 |
| sve_m4 | mlp | reweighted | 2628 | 0.1126 [0.1081, 0.1593] | 3.180 | 0/3 |

Accuracy matching uses the stricter **maximum per-field evolution error**, not the aggregate error displayed above.
No cost advantage is asserted when that threshold is unmet. A single-PDE numerical trajectory is cached for repeated field queries.
Symbolic computation, numerical reference construction, training compute, monitoring, total wall time, and inference are logged separately.
The supplied-generator symbolic audit is not a maximal symmetry classification.

GIF exemplar: mlp/lie, seed 2, flat; selected by median error for display only.
