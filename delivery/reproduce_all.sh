#!/usr/bin/env bash
# Current dissertation symbolic reproduction only. Never replaces tracked receipts.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
out="${1:-build/reproduction}"
mkdir -p "$out"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
for script in symbolic_sv2022 symbolic_sve2026 symbolic_new_model2026 verify_planar; do
    printf 'Checking %s ...\n' "$script"
    python3 "delivery/$script.py" > "$out/$script.json"
done
python3 delivery/reproduce_sve2026.py --order 6 --output "$out/source_reproduction.json"
printf 'Current symbolic reproduction completed: %s\n' "$out"
