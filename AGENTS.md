# Review and maintenance

Use the [compact dissertation](draft/dissertation_wku_compact.tex) as the manuscript of record. Start with the [project README](README.md), [verification dossier](delivery/VERIFICATION.md), [reference audit](ref/README.md) and [research history](delivery/research_path.md).

- Retain equation definitions and domains. The \(E_1\), printed \(P\), compatible \(M\), annular \(E_2\), and rotating-exchange models have distinct claims. Direct comparison and continuation between \(P\) and \(M\) are deferred.
- State the symmetry search class, orbit rank, transversality, data, nonvanishing denominators and convergence assumptions used. Separate theorem, symbolic check, sampled result and open problem.
- Keep historical runs and their negative controls intact. Archive material under `.old/`. Current executable and verification material belongs under `delivery/`.
- Use `delivery/build_pdfs.sh` for the two active PDFs and vector workflows. Inspect final logs and render affected pages. Use the targeted symbolic and source checks in the verification dossier when mathematical source or reference paths change.
- Keep manuscripts and their supporting figures in `draft/`, and keep `ref/` flat. Preserve concurrent Git changes with a guarded fast-forward.
