#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
source /home/carl/miniforge3/etc/profile.d/conda.sh
conda activate pinn
export PYTHONDONTWRITEBYTECODE=1
export MPLBACKEND=Agg
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
output="${1:-results/fluid-baseline}"
if [[ -e "$output/manifest.json" ]]; then
  echo "Refusing to overwrite existing evidence: $output. Choose a fresh output folder." >&2
  exit 2
fi
mkdir -p "$output"
python -m pip freeze > "$output/pip-freeze.txt"
python -B -m pytest -q -p no:cacheprovider --ignore=symm/test_ml_pde_solver.py \
  --junitxml="$output/pytest.xml" 2>&1 | tee "$output/pytest.txt"
python -B -m symm.fluid_baselines.run --output "$output" 2>&1 | tee "$output/run.log"
