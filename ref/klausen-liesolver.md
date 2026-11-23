# Klausen LieSolver

René P. Klausen, Ivan Timofeev, Johannes Frank, Jonas Naujoks, Thomas Wiegand, Sebastian Lapuschkin, and Wojciech Samek. *LieSolver: A PDE-constrained solver for IBVPs using Lie symmetries*. [arXiv:2510.25731](https://arxiv.org/abs/2510.25731).

The [pinned implementation](https://github.com/oduwancheekee/liesolver/tree/178c4142598ea9cd6398a6180773becea48a17a2) constructs bricks by Lie transformations of known solutions of linear homogeneous PDEs and fits coefficients against the initial and boundary data. The replay uses its original one-dimensional heat and wave configurations. The [independent verification](../delivery/VERIFICATION.md#original-klausen-comparison) compares with separate analytic solution formulas.

The SVE work uses verified invariant solutions as references for parameter continuation, with validity of each chart checked separately. Linear superposition of solution bricks is the mechanism in the original algorithm and does not transfer to nonlinear SVE.
