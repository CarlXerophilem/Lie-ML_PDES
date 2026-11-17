# Dissertation in the supplied MATH 4890 template

Prepared 16 November 2026 from the latest saved `dissertation_wku.tex` (version 8), using the uploaded `MATH_4890_dissertation_template.zip`.

## Files and build

- `dissertation_wku.pdf`: compiled dissertation.
- `dissertation_wku.tex`: complete, editable manuscript with embedded bibliography and plot data.
- `main.tex`: optional Overleaf entry point that inputs the manuscript.
- `WKU.png`: university logo from the uploaded template.
- `wku_programme_header.pdf`: vector Chinese programme header, with the template's wording.
- `wku_programme_header.tex`: optional editable source for that header.
- `template_changes.diff` and `preservation_check.json`: formatting changes and checks against the previous source.
- `pdf_check.json`: PDF layout/build checks.
- `verify_coefficients.py` and `symbolic_checks.json`: retained exact coefficient check and its previous results.

Keep the manuscript and assets together. Use pdfLaTeX in a full TeX Live or MiKTeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error dissertation_wku.tex
pdflatex -interaction=nonstopmode -halt-on-error dissertation_wku.tex
pdflatex -interaction=nonstopmode -halt-on-error dissertation_wku.tex
```

Alternatively, run `latexmk -pdf dissertation_wku.tex`. On Overleaf, upload the entire package and set `dissertation_wku.tex` or `main.tex` as the main document. The prebuilt programme header allows ordinary pdfLaTeX compilation without a system Chinese font. Rebuilding only that header requires XeLaTeX and Noto Serif CJK SC.

## Template application

The supplied template determines A4 paper, 12-point text, 1.25-inch side margins, top/bottom/footer geometry, no running header, right-aligned page numbers, uppercase Roman front-matter numbering, Arabic body numbering, logo dimensions, programme header, student fields, declaration wording, and front-matter order. Table cell spacing follows the template. Chapter headings begin at the text area's top, and default paragraph spacing is used.

The front matter is: cover, Author's Declaration, Abstract, Contents, List of Figures, List of Tables, and List of Symbols and Abbreviations. The placeholder abstract, example figure and sample references have been replaced by the existing dissertation content.

The `report` class is retained internally to preserve the dissertation's six chapters, three appendices, and chapter-based theorem/equation numbering. The template's sample chapter titles do not replace the frozen research structure. Short list entries and wrapped displays improve fit at the template's font size and margins; the complete captions and mathematical expressions are preserved.

The recorded submission date remains **11 November 2026**. Declaration name, date and signature lines remain blank. A factual AI-assistance disclosure accompanies the template's declaration; no declaration or signature has been executed on the author's behalf.

## Content preservation

This is a formatting pass. The frozen research questions, model assumptions, mathematical claims, proofs, numerical records and bibliography entries are retained. The entire body is checked after normalization of explicitly listed layout markup. All 17 theorem/proof environments, all 93 existing label numbers, the chapter order and both embedded numerical plot tables are preserved. The abstract is unchanged verbatim.

The analytical supplements already present in the input remain: Propositions 3.A and 3.B on generator continuation, Theorem A.A on analytic SVE crossing branches, and Proposition A.B on critical recursion and tail bounds. This pass adds no new analytical claim and performs no new training or numerical experiment. The retained symbolic verification script may be run separately with SymPy installed.

The attached `dissertation_wku.pdf` could not be opened, so this edition was built from the latest saved LaTeX source. Any edits existing only in that unavailable attachment are not incorporated.
