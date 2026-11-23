#!/usr/bin/env bash
set -euo pipefail
upstream_commit=178c4142598ea9cd6398a6180773becea48a17a2
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
checkout="$(realpath "${1:?Usage: bash delivery/run_klausen_original.sh UPSTREAM_CHECKOUT [LOG_DIR]}")"
target="$(realpath -m "${2:-$root/build/delivery/klausen}")"
mkdir -p "$target"
cd "$checkout"

if [[ "$(git rev-parse HEAD)" != "$upstream_commit" ]] ||
   ! git diff --quiet HEAD --; then
    printf 'Use a clean checkout of the pinned upstream revision %s\n' "$upstream_commit" >&2
    exit 1
fi

export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MPLBACKEND=Agg
for case in heat wave; do
    raw="$target/klausen_${case}_original.txt"
    python -u main.py "configs/${case}_1d.yaml" | tee "$raw"
    saved=$(sed -n 's/.*Model saved to //p' "$raw" | tail -1)
    [[ -n "$saved" ]]
    shopt -s nullglob
    files=("$saved"/model_*.npz)
    [[ "${#files[@]}" == 1 ]]
    python "$root/delivery/verify_klausen.py" "$case" "${files[0]}" > "$target/klausen_${case}_independent.txt"
done
