<!-- Math rendering: GitHub MathJax / KaTeX compatible LaTeX. Use $...$ or standalone $$ blocks; no custom macros or injected scripts. -->

# Historical experiments

These scripts are preserved for provenance, not presented as the current dissertation's validation or recommended solver. No failure has been converted into a pass.

- `verify_klausen.py` and `run_klausen_original.sh`: independent historical heat/wave comparison against the pinned original LieSolver repository. They require a local, clean upstream checkout and independently generated checkpoints.
- `legacy/`: previous per-model Lie and ML experiments, the seeded multi-dimensional regression suite, and the exact exchange-profile defect demonstration. Their original receipts remain in `delivery/logs/`.
- `reproduce_legacy.sh`: opt-in historical replay; writes fresh reports beneath `build/legacy-reproduction/`, not the published receipts. This can be much slower than the current symbolic reproduction.

Run the maintained route instead:

```bash
python -m pip install -e .
lie-reduce --model E1 --subalgebra X1
bash delivery/reproduce_all.sh
```

For full pre-cleanup contents, consult the [compact archive index](../.old/CoT.json). The original files remain in the pinned Git snapshot.
