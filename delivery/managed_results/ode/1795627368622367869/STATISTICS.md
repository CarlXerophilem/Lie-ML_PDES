# Managed ODE pilot diagnostics

1025 evaluation coordinates. Profile error is in q for N3; the physical field error is in H. These are sampled reference differences, not true-error or continuous bounds; differences below reference uncertainty must not be used to rank methods.

| Task | Method | Profile/reference difference | Physical/reference difference | Residual max | Admissible on samples |
|---|---|---:|---:|---:|---|
| N1 | chebyshev | 3.189e-05 | 3.189e-05 | 4.470e-03 | True |
| N1 | lnn | 1.226e-01 | 1.226e-01 | 1.841e-01 | True |
| N1 | pinn | 9.646e-02 | 9.646e-02 | 4.863e-01 | True |
| N1 | prefix | 8.829e-03 | 8.829e-03 | 3.169e-02 | True |
| N1 | taylor | 4.875e-03 | 4.875e-03 | 5.256e-02 | True |
| N2 | chebyshev | 1.443e-15 | 1.443e-15 | 7.212e-12 | True |
| N2 | lnn | 3.812e-01 | 3.812e-01 | 4.945e+00 | True |
| N2 | pinn | 4.966e-01 | 4.966e-01 | 1.210e+01 | True |
| N2 | prefix | 1.142e-02 | 1.142e-02 | 2.455e+01 | True |
| N2 | taylor | 1.332e-15 | 1.332e-15 | 4.279e-12 | True |
| N3minus | chebyshev | 2.032e-14 | 3.742e-20 | 3.199e-13 | True |
| N3minus | lnn | 8.346e-01 | 1.978e-06 | 1.768e+00 | True |
| N3minus | pinn | 9.564e-01 | 2.442e-06 | 2.023e+00 | True |
| N3minus | prefix | 1.553e-02 | 5.925e-08 | 8.617e-02 | True |
| N3minus | taylor | 4.201e-13 | 1.603e-18 | 4.556e-12 | True |
| N3plus | chebyshev | 1.557e-13 | 1.838e-19 | 6.176e-13 | True |
| N3plus | lnn | 2.776e+00 | 4.522e-06 | 6.566e+00 | True |
| N3plus | pinn | 2.244e+00 | 8.560e-06 | 9.839e+00 | True |
| N3plus | prefix | 1.512e-02 | 5.767e-08 | 8.829e-02 | True |
| N3plus | taylor | 4.471e-12 | 1.706e-17 | 5.015e-11 | True |
