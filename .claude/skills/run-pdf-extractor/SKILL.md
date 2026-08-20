---
name: run-pdf-extractor
description: Build, run, and drive the pdf2md PDF→Markdown app for the LieML project. Use when asked to run, start, test, smoke-test, or screenshot the PDF extractor / pdf2md, convert reference PDFs in ref/ to Markdown, batch-convert a folder of PDFs, rasterize PDF pages, or extract figure bounding boxes from papers.
---

# run-pdf-extractor

Drives **`pdf2md`**, the PDF→Markdown app at `pdf2md/pdf2md.py`. It's a **CLI
tool** — run with `python` directly; exercised end-to-end by `smoke.sh`.
Two stages (per `plan.txt`):

1. **Local (CPU, no API key)** — rasterize each page to PNG, compute figure
   bounding boxes `B=[x0,y0,x1,y1]`, pull the text layer. Always runs; offline.
2. **Remote (`--api`)** — ship page PNG + bbox metadata to a vision LLM
   (DeepSeek / OpenAI / GLM) over the OpenAI-compatible SDK. Skipped unless
   `--api` **and** a provider key are set.

> Paths below are relative to the unit root: `D:/MATHs/math 4890 LieML`.
> The driver graduated into the app folder: `pdf2md/pdf2md.py`
> (deps: `pdf2md/requirements.txt`, docs: `pdf2md/README.md`).

## Prerequisites

`pymupdf` + `openai` (already present in this environment). From clean:

```bash
pip install -r pdf2md/requirements.txt
```

Verify deps + which provider keys are set:

```bash
python pdf2md/pdf2md.py --probe
```

## Run (agent path) — FIRST

One-shot smoke test (probe + 2-page conversion + asserts artifacts):

```bash
bash .claude/skills/run-pdf-extractor/smoke.sh
```

**Convert every PDF in `ref/`** to Markdown (the main job — ~85s, ~460 MB):

```bash
python pdf2md/pdf2md.py ref pdf2md/output --dpi 150
```

Fast text-only batch (skips rasters, ~13x faster, no PNGs):

```bash
python pdf2md/pdf2md.py ref pdf2md/output --no-png
```

Single file:

```bash
python pdf2md/pdf2md.py "ref/Generalized Lie Symmetries in Physics-Informed Neural Operators.pdf" pdf2md/output --max-pages 3
```

High-fidelity remote stage (needs a key, e.g. `export DEEPSEEK_API_KEY=...`):

```bash
python pdf2md/pdf2md.py ref pdf2md/output --api --provider deepseek --model deepseek-vl
```

Output layout under `pdf2md/output/`:
- `<stem>/document.md` — stitched Markdown (text + figure placeholders)
- `<stem>/manifest.json` — per-page summary
- `<stem>/pages/page-NNN.png` — rasterized pages (omitted with `--no-png`)
- `<stem>/pages/page-NNN.bbox.json` — `{page,size,images:[{bbox,…}],text}`
- `index.md` — table of every converted document

Read a rendered page to eyeball it (`Read pdf2md/output/<stem>/pages/page-001.png`),
or inspect bboxes (**utf-8 — Windows default gbk will crash**):

```bash
python -c "import json;d=json.load(open('pdf2md/output/Sophus Lie, the mathematician/pages/page-001.bbox.json',encoding='utf-8'));print(len(d['images']),'figures')"
```

### Options

| flag | meaning | default |
|---|---|---|
| `--no-png` | skip rasterization (text+bbox only, fast) | off |
| `--max-pages N` | cap pages per document (0 = all) | 0 |
| `--pages A-B` | 1-based inclusive range | all |
| `--dpi N` | raster DPI | 150 |
| `--api` | run remote vision stage | off |
| `--provider` | `deepseek` \| `openai` \| `glm` | deepseek |
| `--model` | model id override | provider default |
| `--probe` | print deps/keys and exit | — |

## Gotchas

- **No `python3` on this box** — the binary is `python` (Python 3.14);
  `python3` returns "command not found".
- **Console is gbk:** non-ASCII in `print()` raises `UnicodeEncodeError`
  (hit this with a `✓`). The app uses ASCII status (`[ok]`). Same codec bites
  when *reading* the utf-8 output JSON with bare `open()` — pass
  `encoding='utf-8'`.
- **Scanned PDFs look empty in Markdown.** `visual_complex_analysis.pdf`
  (612 pp) yields ~134 KB of text but 1658 figures — it's a scanned book, so
  the local Markdown is mostly `![figure](…)` placeholders. Run `--api` on
  those to transcribe the page images.
- **`--api` silently degrades** to local when the provider key is unset (by
  design). Run `--probe` first to confirm a key is visible.
- **`deepseek-chat` is text-only** — the `deepseek` default model id is a
  placeholder; pass `--model` with a real vision model id (e.g. `deepseek-vl`).
- **Disk:** the full `ref/` raster run is ~460 MB. Use `--no-png` while
  iterating; bound big books with `--max-pages`.

## Troubleshooting

| symptom | fix |
|---|---|
| `python3: command not found` | use `python` |
| `UnicodeEncodeError: 'gbk'` on print | non-ASCII in output; already ASCII in app — avoid unicode in your own prints |
| `UnicodeDecodeError: 'gbk'` reading `.json` | add `encoding='utf-8'` to `open()` |
| `--api` produced local-looking output | key unset; check `--probe`, `export <PROVIDER>_API_KEY=...` |
| `error: no such file/dir` | quote paths with spaces; paths are relative to unit root |
| `error: no PDFs found` | point `INPUT` at a `.pdf` or a dir containing `*.pdf` |

## Files

- `pdf2md/pdf2md.py` — the app/driver (local raster/bbox/text + optional API stage).
- `pdf2md/requirements.txt`, `pdf2md/README.md` — deps and app docs.
- `.claude/skills/run-pdf-extractor/smoke.sh` — offline end-to-end smoke test.
