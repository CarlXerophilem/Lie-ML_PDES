#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build="$(realpath -m "${1:-$root/build/delivery}")"
mkdir -p "$build/figures" "$build/draft"
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1795392000}"
export FORCE_SOURCE_DATE=1
if ! command -v pdflatex >/dev/null 2>&1 && [ -d "$HOME/.local/share/.TinyTeX/bin/x86_64-linux" ]; then
    export PATH="$HOME/.local/share/.TinyTeX/bin/x86_64-linux:$PATH"
fi

cd "$root/draft/figures/final-delivery"
for name in contribution_workflow ml_workflow; do
    pdflatex -halt-on-error -interaction=nonstopmode -output-directory="$build/figures" "$name.tex" > "$build/figures/$name.txt"
    cp "$build/figures/$name.pdf" "$name.pdf"
done

cd "$root/draft"
for name in dissertation_wku_compact defense_wku_madrid; do
    for pass in 1 2 3; do
        pdflatex -halt-on-error -interaction=nonstopmode -output-directory="$build/draft" "$name.tex" > "$build/draft/$name-$pass.txt"
    done
    cp "$build/draft/$name.pdf" "$name.pdf"
done

cd "$root"
sha256sum draft/dissertation_wku_compact.pdf draft/defense_wku_madrid.pdf draft/figures/final-delivery/*.pdf
