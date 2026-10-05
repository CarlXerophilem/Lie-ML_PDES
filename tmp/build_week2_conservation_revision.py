from pathlib import Path
import re

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(r"D:\MATHs\math 4890 LieML")
OUTPUT = ROOT / "draft" / "interim report week 2.docx"

BLACK = "000000"
MUTED = "536170"
HEADER = "243B53"
PALE = "EDF3F7"
BORDER = "D9D9D9"


def set_run(run, *, size=9.8, bold=False, italic=False, color=BLACK, font="Aptos"):
    run.font.name = font
    rpr = run._element.get_or_add_rPr()
    rpr.rFonts.set(qn("w:ascii"), font)
    rpr.rFonts.set(qn("w:hAnsi"), font)
    rpr.rFonts.set(qn("w:eastAsia"), font)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    node = tcpr.find(qn("w:shd"))
    if node is None:
        node = OxmlElement("w:shd")
        tcpr.append(node)
    node.set(qn("w:fill"), fill)


def margins(cell, value=95):
    tcpr = cell._tc.get_or_add_tcPr()
    tc_mar = tcpr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tcpr.append(tc_mar)
    for tag in ("top", "start", "bottom", "end"):
        node = tc_mar.find(qn(f"w:{tag}"))
        if node is None:
            node = OxmlElement(f"w:{tag}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def borders(table):
    tblpr = table._tbl.tblPr
    node = tblpr.find(qn("w:tblBorders"))
    if node is None:
        node = OxmlElement("w:tblBorders")
        tblpr.append(node)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        item = node.find(qn(f"w:{edge}"))
        if item is None:
            item = OxmlElement(f"w:{edge}")
            node.append(item)
        item.set(qn("w:val"), "single")
        item.set(qn("w:sz"), "4")
        item.set(qn("w:color"), BORDER)
        item.set(qn("w:space"), "0")


def repeat_header(row):
    trpr = row._tr.get_or_add_trPr()
    item = OxmlElement("w:tblHeader")
    item.set(qn("w:val"), "true")
    trpr.append(item)


def width(cell, inches):
    cell.width = Inches(inches)
    tcpr = cell._tc.get_or_add_tcPr()
    tcw = tcpr.find(qn("w:tcW"))
    if tcw is None:
        tcw = OxmlElement("w:tcW")
        tcpr.append(tcw)
    tcw.set(qn("w:w"), str(int(inches * 1440)))
    tcw.set(qn("w:type"), "dxa")


def style_table(table, widths, *, font_size=7.8, cell_margin=95):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    borders(table)
    repeat_header(table.rows[0])
    for ri, row in enumerate(table.rows):
        for ci, cell in enumerate(row.cells):
            width(cell, widths[ci])
            margins(cell, cell_margin)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if ri == 0:
                shade(cell, HEADER)
            elif ri % 2 == 0:
                shade(cell, PALE)
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_before = Pt(0)
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.paragraph_format.line_spacing = 1.0
                for run in paragraph.runs:
                    set_run(
                        run,
                        size=font_size,
                        bold=(ri == 0),
                        color=("FFFFFF" if ri == 0 else BLACK),
                    )


def add_heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.add_run(text)
    p.paragraph_format.keep_with_next = True
    return p


def add_body(doc, text, lead=None, *, after=3):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.04
    if lead:
        set_run(p.add_run(lead), bold=True)
    set_run(p.add_run(text))
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Inches(0.23)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    set_run(p.add_run(text), size=9.5)
    return p


def math_run(text):
    run = OxmlElement("m:r")
    value = OxmlElement("m:t")
    value.text = text
    run.append(value)
    return run


def add_math(doc, parts, *, after=4):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(after)
    omp = OxmlElement("m:oMathPara")
    omppr = OxmlElement("m:oMathParaPr")
    jc = OxmlElement("m:jc")
    jc.set(qn("m:val"), "center")
    omppr.append(jc)
    omp.append(omppr)
    om = OxmlElement("m:oMath")
    for part in parts:
        if isinstance(part, tuple) and part[0] == "sub":
            node = OxmlElement("m:sSub")
            base = OxmlElement("m:e")
            base.append(math_run(part[1]))
            sub = OxmlElement("m:sub")
            sub.append(math_run(part[2]))
            node.append(base)
            node.append(sub)
            om.append(node)
        elif isinstance(part, tuple) and part[0] == "sup":
            node = OxmlElement("m:sSup")
            base = OxmlElement("m:e")
            base.append(math_run(part[1]))
            sup = OxmlElement("m:sup")
            sup.append(math_run(part[2]))
            node.append(base)
            node.append(sup)
            om.append(node)
        else:
            om.append(math_run(part))
    omp.append(om)
    p._p.append(omp)
    return p


def add_page_field(paragraph):
    run = paragraph.add_run()
    for kind, value in (("begin", None), (None, " PAGE "), ("separate", None), (None, "1"), ("end", None)):
        if kind:
            node = OxmlElement("w:fldChar")
            node.set(qn("w:fldCharType"), kind)
        else:
            node = OxmlElement("w:instrText" if value == " PAGE " else "w:t")
            if value == " PAGE ":
                node.set(qn("xml:space"), "preserve")
            node.text = value
        run._r.append(node)
    set_run(run, size=8.2, color=MUTED)


def configure(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    normal.font.size = Pt(9.8)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    for name, size, before, after in (
        ("Title", 20, 0, 2),
        ("Subtitle", 10.5, 0, 7),
        ("Heading 1", 13, 8, 3),
        ("Heading 2", 10.5, 5, 2),
    ):
        style = doc.styles[name]
        style.font.name = "Aptos Display" if name != "Subtitle" else "Aptos"
        style._element.rPr.rFonts.set(qn("w:ascii"), style.font.name)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), style.font.name)
        style.font.size = Pt(size)
        style.font.bold = name != "Subtitle"
        style.font.italic = False
        style.font.color.rgb = RGBColor.from_string(BLACK if name != "Subtitle" else MUTED)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True


def build():
    doc = Document()
    configure(doc)
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.58)
    section.bottom_margin = Inches(0.58)
    section.left_margin = Inches(0.68)
    section.right_margin = Inches(0.68)
    section.header_distance = Inches(0.25)
    section.footer_distance = Inches(0.25)

    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run(header.add_run("MATH 4890  |  LieML"), size=8.2, color=MUTED)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(footer.add_run("Week 2  |  Conservation-aware revision  |  "), size=8.2, color=MUTED)
    add_page_field(footer)

    title = doc.add_paragraph(style="Title")
    title.add_run("Interim Research Report - Week 2")
    subtitle = doc.add_paragraph(style="Subtitle")
    subtitle.add_run("Conservation-aware Lie-space revision")
    meta = doc.add_paragraph()
    meta.paragraph_format.space_after = Pt(5)
    set_run(meta.add_run("Yihong Xiao  |  Student ID 1308225  |  Supervisor Puneet Rana  |  October 1, 2026"), size=8.7, color=MUTED)

    add_heading(doc, "1. Overall Summary & Status")
    add_body(
        doc,
        "Week 1 left ML placement, admissible subalgebras, and data compatibility unresolved. The project is now narrowed to smooth, continuous, nonlinear balance-law systems with one fixed time axis, one or two spatial dimensions, optional differential constraints, declared branch guards, data, and boundary fluxes. Fractional operators, shocks, and solution/profile learning are outside the v1 core. The printed scalar Lagrangian SVE equation remains a historical anchor, not the target class.",
        lead="Scope decision. ",
    )
    add_math(
        doc,
        [
            ("sub", "D", "t"), " ", ("sub", "ρ", "a"), "(U) + Σᵢ₌₁ᵈ ",
            ("sub", "D", "xᵢ"), " Jₐⁱ",
            "(U⁽ⁿ⁾; λ) = ", ("sub", "S", "a"), ",   d ∈ {1,2},   ",
            ("sub", "C", "ℓ"), "(U⁽ⁿ⁾) = 0",
        ],
    )

    add_heading(doc, "2. Completed Mathematical Checks")
    add_bullet(doc, "Fixed m = 3: X5 = t∂t - 2s∂s, σ = st², Q = -tφt + 2sφs = 0, and E3[F(st²)] = t⁻¹R0[F] were rechecked. The focused suite passed 39 tests.")
    add_bullet(doc, "Published-form contradiction: for the paper's stated power law at g = 1, β = 0.1, σ = 1, printed Eq. (25) evaluates to -13.297080414695, while the Eq. (7)-derived R0 simplifies exactly to zero. This is a reproducible source conflict, not a multiplier difference.")
    add_bullet(doc, "Boundary: these checks certify a supplied generator on a regular local scalar chart; they do not prove generic-m maximal classification or physical equivalence to the full Eulerian SVE system.")

    add_heading(doc, "3. Revised Core Algorithm")
    add_math(doc, ["conservation-aware PDE → exact determining operator → statistical Lie-space proposal → exact recovery/closure → certified conservative reduction"])
    task_table = doc.add_table(rows=1, cols=4)
    for cell, value in zip(task_table.rows[0].cells, ("Task", "Input", "Loss / gate", "Output")):
        cell.text = value
    rows = [
        (
            "Symmetry-algebra estimator",
            "Conservation AST, parameters, guards, normalized ansatz basis",
            "Determining residual, projector/rank, basis covariance, closure, calibration",
            "pθ(k,P|E), P in Gr(k,N), confidence",
        ),
        (
            "Reduction-subalgebra selector",
            "Exact g, structure constants, orbit ranks, data/flux features",
            "Closure, projected rank, data/flux compatibility, reduced cost",
            "pθ(h|g,E,D): adjoint-class ranking",
        ),
    ]
    for values in rows:
        cells = task_table.add_row().cells
        for cell, value in zip(cells, values):
            cell.text = value
    style_table(task_table, [1.35, 2.15, 2.25, 1.4], font_size=7.5)

    add_body(
        doc,
        "The estimator predicts a variable nullity and a Grassmann projector, never a basis-dependent generator list. Its normalized objective includes determining residual, idempotence, symmetry, rank calibration, equivalence covariance, bracket closure, and OOD calibration. Exact nullspace recovery and cokernel checks decide validity. If near-m = 3 learning is retained, it predicts the Grassmann tangent and obstruction probability, not a solution correction.",
        lead="Statistical object. ",
        after=2,
    )
    add_math(
        doc,
        [
            ("sub", "A", "0"), "Ṗ + ", ("sub", "A", "1"),
            ("sub", "P", "0"), " ≈ 0,    Ṗ", ("sub", "P", "0"),
            " + ", ("sub", "P", "0"), "Ṗ = Ṗ",
        ],
        after=2,
    )
    add_math(
        doc,
        [
            "L = ‖", ("sub", "A", "E"), "P‖", ("sub", "F", "2"), "/(‖",
            ("sub", "A", "E"), "‖", ("sub", "F", "2"), "+ε) + α‖P²-P‖",
            ("sub", "F", "2"), " + β‖P-Pᵀ‖", ("sub", "F", "2"),
            " + γ", ("sub", "L", "rank"), " + η", ("sub", "L", "equiv"),
            " + κ", ("sub", "L", "bracket"), " + ζ", ("sub", "L", "cal"),
        ],
        after=2,
    )
    add_body(
        doc,
        "Canonicalization fixes time direction and permits only transformations preserving units, field roles, conservation blocks, constraint blocks, and boundary-flux semantics. A reduction certificate must add conservation_status and verify density/flux/source/constraint pullback, coordinate-Jacobian weight, and boundary flux. Conservation form is not a Noether or variational claim.",
        lead="Semantic gates. ",
        after=2,
    )

    add_heading(doc, "4. Six-Hour Bounded Experiment Plan")
    plan = doc.add_table(rows=1, cols=3)
    for cell, value in zip(plan.rows[0].cells, ("Time", "Experiment / artifact", "Fail-closed acceptance")):
        cell.text = value
    plan_rows = [
        ("0:00-0:40", "Freeze target schema; attach m = 3 and Eq. (25) receipts", "Exact identities and hashes recorded"),
        ("0:40-1:30", "1+1 two-field nonlinear conservation system", "Kernel and conservative pullback agree with exact baseline"),
        ("1:30-2:30", "2+1 smooth system with a differential constraint", "Constraint, orbit rank, and flux gates all pass"),
        ("2:30-3:20", "Parameter-induced algebra/orbit-rank jump", "Exceptional stratum recalled; no projector smearing"),
        ("3:20-4:40", "Eulerian multi-field SVE conservation benchmark", "Smooth-branch density, flux, source, and boundary terms traced"),
        ("4:40-6:00", "Covariance/OOD tests; exact fallback; evidence table", "Same final kernel; every failure remains explicit"),
    ]
    for values in plan_rows:
        cells = plan.add_row().cells
        for cell, value in zip(cells, values):
            cell.text = value
    # Keep the complete six-hour matrix on page 1 so the decision and
    # supervisor fields remain a coherent second page.
    style_table(plan, [1.0, 3.25, 2.9], font_size=7.5, cell_margin=60)

    decision_heading = add_heading(doc, "5. Decision & Nonclaims")
    decision_heading.paragraph_format.page_break_before = True
    add_body(
        doc,
        "Profile/operator ML is now a downstream consumer, not the contribution. Structural ML proceeds only if the exact baselines show repeated-query cost worth amortizing. This report claims neither shock handling, fractional symmetry, Noether currents, generic SVE classification, nor ML speedup. A six-hour overrun, unmatched kernel, failed conservation gate, or missed exceptional stratum stops the route and is reported as a negative result.",
    )
    add_heading(doc, "5.1 Supervisor Feedback & Guidance", 2)
    for _ in range(4):
        line = doc.add_paragraph()
        line.paragraph_format.space_before = Pt(4)
        line.paragraph_format.space_after = Pt(4)
        set_run(line.add_run("________________________________________________________________________________"), size=8.8, color=MUTED)
    review = doc.add_paragraph()
    review.paragraph_format.space_before = Pt(7)
    set_run(review.add_run("Supervisor: Puneet Rana    "), bold=True, size=9.2)
    set_run(review.add_run("Signature: ____________________    Date: ____________________"), size=9.2)

    doc.core_properties.title = "Interim Research Report - Week 2"
    doc.core_properties.subject = "Conservation-aware Lie-space project revision"
    doc.core_properties.author = "Yihong Xiao"
    doc.save(OUTPUT)

    reopened = Document(OUTPUT)
    prose = []
    prose.extend(p.text for p in reopened.paragraphs)
    prose.extend(cell.text for table in reopened.tables for row in table.rows for cell in row.cells)
    word_count = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", "\n".join(prose)))
    if word_count > 600:
        raise RuntimeError(f"Word count {word_count} exceeds 600")
    print(f"OUTPUT={OUTPUT}")
    print(f"WORD_COUNT={word_count}")


if __name__ == "__main__":
    build()
