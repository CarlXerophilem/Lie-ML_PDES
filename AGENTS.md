<!-- Math rendering: GitHub MathJax / KaTeX compatible LaTeX. Use $...$ or standalone $$ blocks; no custom macros or injected scripts. -->

# Review and maintenance

Use the [compact dissertation](draft/dissertation_wku_compact.tex) as the manuscript of record. Start with the [project README](README.md), [verification dossier](delivery/VERIFICATION.md), [reference audit](ref/README.md) and [research history](delivery/research_path.md).

- Retain equation definitions and domains. The $E_1$, printed $P$, compatible $M$, annular $E_2$, and rotating-exchange models have distinct claims. Direct comparison and continuation between $P$ and $M$ are deferred.
- State the symmetry search class, orbit rank, transversality, data, nonvanishing denominators and convergence assumptions used. Separate theorem, symbolic check, sampled result and open problem.
- Keep historical runs and their negative controls intact. Keep the compact archive index at `.old/CoT.json`; preserve original files by pinned commit references, not duplicate working-tree archives. Current executable and verification material belongs under `delivery/`; historical experiments belong in `bin/`.
- Use `delivery/build_pdfs.sh` for the two active PDFs and vector workflows. Inspect final logs and render affected pages. Use the targeted symbolic and source checks in the verification dossier when mathematical source or reference paths change.
- Keep manuscripts and their supporting figures in `draft/`, and keep `ref/` flat. Preserve concurrent Git changes with a guarded fast-forward.
