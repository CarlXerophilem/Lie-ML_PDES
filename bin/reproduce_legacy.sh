#!/usr/bin/env bash
# Runs the four Lie and four profile experiments; exits nonzero if any written verifier fails.
set -uo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root/delivery"
out="$(realpath -m "${1:-$root/build/legacy-reproduction}")"
mkdir -p "$out"
status=0
for name in experiment_lie_E1 experiment_lie_P experiment_lie_M experiment_lie_E2 \
            experiment_ml_E1 experiment_ml_P experiment_ml_M experiment_ml_Eexch; do
    start=$(date +%s)
    if python3 "$root/bin/legacy/$name.py" > "$out/$name.json" 2> "$out/$name.err"; then
        verdict=passed
    else
        verdict=FAILED; status=1
    fi
    printf '%-22s %-7s %4ss\n' "$name" "$verdict" "$(( $(date +%s) - start ))"
done
for law in 'kappa*u**3' 'Q(u)'; do
    tag=$(echo "$law" | tr -c 'A-Za-z0-9' '_')
    if python3 -m lie_reduce.bed --flux "$law" > "$out/bed_$tag.json" 2> "$out/bed_$tag.err" &&
       python3 -c "import json,sys;s=json.load(open('$out/bed_$tag.json'))['summary'];sys.exit(s['ode_reductions']==0)"; then
        printf '%-22s %-7s\n' "bed flux $law" passed
    else
        printf '%-22s %-7s\n' "bed flux $law" FAILED; status=1
    fi
done
start=$(date +%s)
if OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 "$root/bin/legacy/check_multid.py" > "$out"/check_multid.json 2> "$out"/check_multid.err; then
    verdict=passed
else
    verdict=FAILED; status=1
fi
printf '%-22s %-7s %4ss\n' "strata + (d+1)D quotient" "$verdict" "$(( $(date +%s) - start ))"
start=$(date +%s)
if python3 verify_planar.py > "$out"/verify_planar.json 2> "$out"/verify_planar.err; then
    verdict=passed
else
    verdict=FAILED; status=1
fi
printf '%-22s %-7s %4ss\n' "planar E2 identities" "$verdict" "$(( $(date +%s) - start ))"
python3 - "$out" <<'EOF'
import json, sys
from pathlib import Path
print('\nprofile method selection (sampled residual rule)')
for m in ('E1','P','M','Eexch'):
    s=json.load(open(Path(sys.argv[1]) / f'experiment_ml_{m}.json'))['record']['selection']
    print(f"{m:6s} selected={s['selected']:10s} admissible={s['admissible']} rejected={s['rejected']}")
EOF
exit $status
