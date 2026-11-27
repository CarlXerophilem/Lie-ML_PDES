#!/usr/bin/env bash
# Reproduce the Chapter 4 irreducible planar ODE benchmark (Taylor, DOP853, 1D Chebyshev,
# and joint 4D physics-only LNN-PINN surrogate) plus LaTeX figure tables and macros.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="$ROOT/delivery/logs/planar_ml"
mkdir -p "$LOG"

for name in planar_ode_experiments figure_data; do
  echo "==> $name"
  python3 "$ROOT/delivery/$name.py" | tee "$LOG/$name.stdout"
done

echo "Done. Receipts in $LOG"
