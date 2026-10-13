# Standalone script layout

`main.py` contains ordinary Python source in one editable file, including
convergence checks, reconstructed fields and static scientific plots.
It does not import any local implementation package. Run `python main.py
--help` from any working directory. The script resolves its default output
directory relative to its own location.

Edit `DEFAULT_RTOL`, `DEFAULT_ATOL`, and `DEFAULT_TRACE` near the imports, or
override them with `--rtol`, `--atol`, and `--trace`. The numerical model
constants `G`, `KAPPA`, `CASES`, `EXPONENTS` and per-case initial jets and
intervals in `NUMERICAL_CASE_SETTINGS` are beside those top-level defaults.
The symbolic jet variables and `master` are in Core. The independent source
checks, corrected reductions, Fehlberg solver, numerical checks, evidence
coverage, and report writer each have labeled sections.

The source locator searches the script directory and its ancestors for the
two `ref/` PDFs. `--repo-root PATH` explicitly selects a repository when the
script has been copied elsewhere. Missing PDFs or PyMuPDF are recorded in
`source_manifest.json` as unavailable; no source extraction is fabricated.
The symbolic and numerical computations can still run, but their source
verification status must be read separately from their execution status.
`run.complete_audit` is false if either primary PDF could not be checked.
`code_manifest.json` hashes the executed script, not unused historical files.

`_reductions_step` constructs human-readable symbolic trace rows;
`_rkf45_step` is the integrator's internal numerical step. Those two former
`_step` helpers have different purposes and were renamed to avoid a global
namespace collision. All former `j.<symbol>` core aliases now refer directly
to the named top-level core symbols/functions. Other original public
functions retain their names so tests can exercise them directly.

The historical modules and original entrypoint are archived in
`archive/release-before-animation.zip`. The retired runtime directory was
removed after exact symbolic/numerical parity checks. Tests now import the
actual `main.py` definitions. A copied-script run without the local package
or PDFs also completed all 21 numerical and convergence cases.

The subsequent computation-only revision removes the HTML template, viewer
data packaging and HTML command-line options. It adds live source-Table-2,
original-master pullback and source-witness gates. See `COMPUTATION.md` for
the exact distinction between authored inputs and computed results.
