"""Check the two compiled 2027 write-ups and their stored evidence, not novelty."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from statistics import median
import subprocess
import sys

import fitz

from verify_bounds import verify


SUPPORT = Path(__file__).resolve().parent
DRAFT = SUPPORT.parent
ROOT = DRAFT.parent
TITLE = "Lie-Symmetry Reduction and Taylor-PINN Approximation of a Lagrangian Shallow-Water Equation"
REFERENCE_HASH = "2b853b7ecf58820105384d8931dcd1f989fd0a1cb2ea7553430f4cd55e8cc5f5"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(relative):
    return json.loads((SUPPORT / relative).read_text(encoding="utf-8"))


def check_pdf(stem, expected_pages, tex_points, bibliography_keys):
    source = (DRAFT / f"{stem}.tex").read_text(encoding="utf-8")
    aux = (DRAFT / f"{stem}.aux").read_text(encoding="utf-8")
    log = (DRAFT / f"{stem}.log").read_text(encoding="utf-8", errors="replace")
    cited = {key for group in re.findall(r"\\citation\{([^}]+)\}", aux) for key in group.split(",")}
    resolved = set(re.findall(r"\\bibcite\{([^}]+)\}", aux))
    local_keys = set(re.findall(r"\\bibitem\{([^}]+)\}", source))
    warnings = [line for line in log.splitlines() if re.search(r"Warning|Overfull|Underfull|Missing character|^!", line)]
    body_sizes, baseline_gaps, outside, texts = [], [], [], []
    with fitz.open(DRAFT / f"{stem}.pdf") as document:
        pages = len(document)
        title = document.metadata.get("title")
        for page in document:
            texts.append(page.get_text())
            baselines = set()
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    body_line = False
                    for span in line["spans"]:
                        value = span["text"].strip()
                        x0, y0, x1, y1 = span["bbox"]
                        # TeX puts page numbers below the one-inch body margin.
                        footer = value == str(page.number + 1) and y0 > page.rect.height - 72
                        # TeX textheight ends at a baseline; allow 3.5 pt for glyph descent.
                        if value and not footer and (x0 < 71 or x1 > page.rect.width - 71 or y0 < 71 or span["origin"][1] > page.rect.height - 71 or y1 > page.rect.height - 68.5):
                            outside.append({"page": page.number + 1, "text": value, "bbox": list(span["bbox"])})
                        if "TimesNewRoman" in span["font"] and "Bold" not in span["font"] and "Italic" not in span["font"] and len(value) >= 25:
                            body_sizes.append(span["size"])
                            body_line = True
                    if body_line:
                        baselines.add(round(line["spans"][0]["origin"][1], 3))
            ordered = sorted(baselines)
            baseline_gaps.extend(b - a for a, b in zip(ordered, ordered[1:]) if b - a > 1)
    text = "\n".join(texts)
    body_size = median(body_sizes) if body_sizes else None
    gap = median(baseline_gaps) if baseline_gaps else None
    checks = {
        "expected_page_count": pages == expected_pages,
        "fixed_title": title == TITLE,
        "planned_2027_scope_visible": "2027" in texts[0] and "eight-week" in texts[0].lower(),
        "shared_bibliography": "\\input{proposal_support/references_2027.tex}" in source,
        "all_citations_resolved": cited == resolved == bibliography_keys | local_keys,
        "no_unresolved_markers": "??" not in text,
        "one_references_heading": len(re.findall(r"^References$", text, re.MULTILINE)) == 1,
        "times_new_roman_body_size": body_size is not None and abs(body_size - tex_points * 72 / 72.27) < 0.03,
        "no_text_outside_tex_body_allowance": not outside,
        "clean_latex_log": not warnings,
        "current_pilot_only": "\\input{proposal_support/lagrange_evidence/pilot_values.tex}" in source and "\\input{proposal_support/evidence/" not in source,
    }
    if stem == "proposal":
        headings = re.findall(r"\\section\{([^}]+)\}", source)
        expected = ["Research Problem", "Objectives", "Methodology", "Expected Outcomes"]
        checks["requested_heading_structure"] = headings == expected and all(name in text for name in expected)
        checks["double_spaced_body"] = "\\doublespacing" in source and gap is not None and abs(gap - 24 * 72 / 72.27) < 0.08
    return {"checks": checks, "pages": pages, "cited_keys": sorted(cited), "body_font_size_pdf_points": body_size, "median_body_baseline_pdf_points": gap, "latex_warnings": warnings, "out_of_bounds": outside}


def check_evidence():
    classical = read_json("lagrange_evidence/report.json")
    neural = read_json("feasibility_20260912/report.json")
    bounds = read_json("feasibility_20260912/bounds.json")
    live_bounds = verify()
    coefficient_hash = sha(SUPPORT / "verify_lagrange.py")
    rows = []
    for case in neural["cases"]:
        values = [case["before"]["max_profile_error"], case["after"]["max_profile_error"], case["after"]["max_normalized_defect"]]
        fields = []
        for value in values:
            mantissa, exponent = f"{value:.2e}".split("e")
            fields.append(f"${mantissa}\\times10^{{{int(exponent)}}}$")
        rows.append(" & ".join([str(case["order"]), *fields, f"{case['training_seconds']:.2f}"]) + r" \\")
    expected_table = "\n".join(rows) + "\n"
    source_pdf = next((ROOT / "ref/main").glob("*mathematics-14-00433-v3.pdf"))
    archive = SUPPORT / "archive/before_2027_submit_writeup"
    old_qa = read_json("lagrange_evidence/publication_check.json")
    checks = {
        "reference_pdf_matches_verified_publisher_hash": sha(source_pdf) == REFERENCE_HASH,
        "classical_source_matches": classical["source_sha256"] == coefficient_hash,
        "neural_source_matches": neural["source_sha256"] == sha(SUPPORT / "pinn_feasibility.py") and neural["coefficient_source_sha256"] == coefficient_hash,
        "exact_bound_reproduced": live_bounds == bounds and all(live_bounds["checks"].values()),
        "classical_checks_passed": classical["all_checks_passed"] and all(classical["symbolic"]["checks"].values()) and all(classical["numerical"]["checks"].values()),
        "neural_smoke_completed": neural["status"] == "feasibility-only" and all(case["status"] == "completed" for case in neural["cases"]),
        "neural_table_matches_report": (SUPPORT / "feasibility_20260912/table.tex").read_text(encoding="utf-8") == expected_table,
        "certification_not_overstated": not neural["interval_certified"] and not neural["formal_2027_study_completed"] and not bounds["neural_uniform_residual_validated"] and not bounds["perturbed_trajectory_containment_certified"],
        "historical_qa_matches_archived_proposal": old_qa["tex_sha256"] == sha(archive / "proposal.tex") and old_qa["pdf_sha256"] == sha(archive / "proposal.pdf"),
    }
    return {"checks": checks, "exact_bounds": live_bounds, "neural_status": neural["status"], "reference_pdf_sha256": sha(source_pdf)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON report; stdout only by default")
    args = parser.parse_args()
    bibliography = SUPPORT / "references_2027.tex"
    keys = set(re.findall(r"\\bibitem\{([^}]+)\}", bibliography.read_text(encoding="utf-8")))
    # The standard 11pt article class defines normalsize as 10.95 TeX points.
    documents = {stem: check_pdf(stem, pages, points, keys) for stem, pages, points in [("proposal", 6, 12), ("draft", 14, 10.95)]}
    evidence = check_evidence()
    test = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", str(SUPPORT), "-p", "test_*.py", "-v"], cwd=ROOT, capture_output=True, text=True, timeout=120)
    test_log = test.stdout + test.stderr
    count = re.search(r"Ran (\d+) tests?", test_log)
    test_count = int(count.group(1)) if count else 0
    paths = [bibliography, DRAFT / "research_record.md", SUPPORT / "README.md", SUPPORT / "submission_source_audit.md", SUPPORT / "sve2d_source_audit.md", Path(__file__)]
    paths += sorted(SUPPORT.glob("test_*.py"))
    paths += [SUPPORT / name for name in ["verify_lagrange.py", "verify_bounds.py", "pinn_feasibility.py", "lagrange_evidence/report.json", "lagrange_evidence/pilot_values.tex", "feasibility_20260912/report.json", "feasibility_20260912/table.tex", "feasibility_20260912/bounds.json"]]
    paths += [DRAFT / f"{stem}.{suffix}" for stem in documents for suffix in ("tex", "pdf", "log", "aux")]
    checks = {"all_document_checks": all(all(doc["checks"].values()) for doc in documents.values()), "all_evidence_checks": all(evidence["checks"].values()), "tests_passed": test.returncode == 0 and test_count >= 37}
    report = {
        "schema": "lieml.2027-publication-check.v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Current proposal and pre-study manuscript; not peer review, novelty validation or a trained-network interval certificate",
        "supersedes": ["archive/before_sve2d_20260913/publication_check_2027.json (pre-Appendix-C manuscript)", "lagrange_evidence/publication_check.json (retained for the archived preceding proposal)"],
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "documents": documents,
        "evidence": evidence,
        "tests": {"returncode": test.returncode, "count": test_count, "output": test_log},
        "sha256": {path.relative_to(ROOT).as_posix(): sha(path) for path in paths},
        "limits": ["Web-source evidence is recorded in submission_source_audit.md; this check does not repeat network retrieval.", "PDF checks use one-inch body margins with 1 pt coordinate tolerance and 3.5 pt bottom glyph descent; page-number footers are excluded. They do not replace visual or mathematical review.", "The stored neural smoke is hash-checked, not rerun; timing is historical and machine-dependent."],
    }
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)
    if not report["all_checks_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
