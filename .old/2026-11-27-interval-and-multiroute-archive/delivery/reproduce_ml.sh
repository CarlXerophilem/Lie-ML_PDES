#!/usr/bin/env bash
# Planar E2 ML benchmark (about 7 minutes on 16 cores); writes JSON receipts to logs/planar_ml/.
# Order matters: experiments -> bounds -> neighbourhoods -> continuation -> figure tables in draft/figures/planar/.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
mkdir -p logs/planar_ml
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
status=0
for name in parameter_experiments parameter_bounds verify_parameter_neighborhoods compare_continuation figure_data; do
    start=$(date +%s)
    if python3 "$name.py" > "logs/planar_ml/$name.out" 2> "logs/planar_ml/$name.err"; then
        verdict=passed
    else
        verdict=FAILED; status=1
    fi
    printf '%-32s %-7s %4ss\n' "$name" "$verdict" "$(( $(date +%s) - start ))"
    [ "$verdict" = passed ] || break
done
exit $status
