from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.shared import Pt


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "draft" / "interim report format.docx"
OUTPUT = ROOT / "draft" / "interim report week 2.docx"


def replace(paragraph, text, *, bold=False, size=11):
    ppr = deepcopy(paragraph._p.pPr) if paragraph._p.pPr is not None else None
    for child in list(paragraph._p):
        paragraph._p.remove(child)
    if ppr is not None:
        paragraph._p.insert(0, ppr)
    run = paragraph.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)


document = Document(SOURCE)
p = document.paragraphs

replace(p[0], "Student name: Yihong Xiao")
replace(p[1], "Student ID: 1308225")

for index in (4, 10, 20, 29, 33):
    replace(p[index], p[index].text, bold=True, size=12)

replace(
    p[5],
    "Overall Progress: Completed the first runnable three-layer baseline: "
    "ML-only literature experiments, a pure Lie-symmetry reduction, and a "
    "certificate-gated Lie-ML prototype for the printed Lagrangian SVE equation.",
)
replace(
    p[6],
    "Summary: The project has moved from deciding where machine learning belongs "
    "to a falsifiable implementation. Lie analysis first reduces the verified "
    "m=3 branch to an ODE; neural models then approximate only the reduced profile; "
    "the reconstructed field is checked in the original PDE. The prototype improves "
    "some profile/residual measures, but a conventional ODE solve is still much faster "
    "for one IVP, so no ML speedup is claimed.",
)

replace(p[11], "Task 1: Completed the pure Lie baseline.", bold=True)
replace(
    p[12],
    "The Python demo verifies X5 = t*d_t - 2*s*d_s at m=3, integrates its group "
    "flow, derives sigma = s*t^2, checks the invariant-surface condition, derives "
    "the third-order reduced ODE, and verifies the lifting identity and exact "
    "power-law control. Reusing the same supplied identity at m=4 is retained as "
    "an unsupported negative control rather than being interpreted as no symmetry.",
)

replace(p[14], "Task 2: Reproduced two ML-only literature directions.", bold=True)
replace(
    p[15],
    "The logistic MLP-PINN/PIKAN benchmark ran ten seeds and 10,000 Adam iterations. "
    "PIKAN reproduced the reported direction, but the absolute numerical result did "
    "not match the paper and several MLP seeds converged to wrong low-residual branches. "
    "The bounded Duffing experiment used three seeds at T=1 and T=3: TM-PINN was most "
    "accurate at T=1 but became highly unstable at T=3. All seeds and failures were kept.",
)

replace(p[17], "Task 3: Completed the certificate-gated SVE fusion prototype.", bold=True)
replace(
    p[18],
    "DOP853 and Radau agreed within 3.3e-13. Across three seeds, P2 + z^3 N had "
    "the lowest median profile error (2.67e-6), while P4 + z^5 N had the lowest "
    "raw residual (5.35e-2). Direct and lifted residuals agreed within 2e-14. "
    "A 92/197/377-evaluation DOP853 tolerance ladder ended at about 0.003 s; "
    "neural training took roughly 3.6-4.2 s per seed.",
)

replace(p[22], "Challenge:", bold=True)
replace(
    p[23],
    "The current prototype explains where ML can be inserted, but it does not yet "
    "show a cost advantage. One reduced IVP is too cheap for amortized learning to "
    "win. The next meaningful test requires repeated parameter queries. PIKAN also "
    "cannot be transferred directly to the third-order SVE residual until a "
    "higher-order spline passes a third-derivative smoothness and stability gate.",
)

replace(p[25], "Action Plan:", bold=True)
replace(
    p[26],
    "Day 1 - Freeze the run manifest, rerun regression tests, and audit every reported number.\n"
    "Day 2 - Define a justified repeated-query parameter family with matched DOP853 cost accounting.\n"
    "Day 3 - Analyze persistence or obstruction for m = 3 + delta before training on perturbed parameters.\n"
    "Day 4 - Run the smallest matched-cost comparison, update the manuscript, and report negative results unchanged.",
)

replace(
    p[30],
    "1. Decide whether repeated parameter queries provide a real use case for amortized ML.\n"
    "2. Keep eta_ic (initial-curvature perturbation) separate from delta = m - 3.\n"
    "3. Add a smoothness gate before any KAN transfer to the third-order residual.\n"
    "4. Continue the symmetry-persistence analysis before expanding the neural architecture.",
)

replace(p[41], "Supervisor Name: Puneet Rana")
replace(p[42], "Signature: _______________________________")
replace(p[43], "Date: ___________________________________")

# Keep two feedback lines, but remove five template spacers that otherwise
# push the signature block onto a mostly empty third page in Microsoft Word.
for index in (40, 39, 38, 37, 36):
    paragraph = p[index]
    paragraph._element.getparent().remove(paragraph._element)

document.core_properties.title = "MATH 4890 Interim Report Week 2"
document.core_properties.subject = "Lie symmetry reduction and machine-learning baselines"
document.save(OUTPUT)
print(OUTPUT)
