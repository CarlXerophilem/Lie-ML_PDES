# Manuscript and defense workflow

The [compact dissertation](dissertation_wku_compact.pdf) is the manuscript of record. The [Madrid defense](defense_wku_madrid.pdf) presents the mathematical argument and the controlled numerical evidence. Both include their editable [manuscript source](dissertation_wku_compact.tex) and [slide source](defense_wku_madrid.tex).

## From model to claim

~~~mermaid
flowchart TD
    A["Declare equations, closure and admissible chart"] --> B["Verify the point action on the equation"]
    B --> C{"Orbit rank, transversality and data compatible?"}
    C -->|Yes| D{"Reduced leading coefficient regular?"}
    C -->|No| E["Record the excluded chart or data"]
    D -->|Yes| F["Solve the reduced initial-value problem"]
    D -->|No| G["Check compatibility and construct the local branch"]
    F --> H["Reconstruct fields and check the original balances"]
    G --> H
    H --> I["Report the theorem and its hypotheses"]
~~~

The published scalar reproduction supplies a separate audit of source formulas. The material route uses the invertible particle map and the closed-bed form. Agreement of a numerical profile at selected samples is evidence at those samples.

## From verification to manuscript and slides

~~~mermaid
flowchart TD
    A["Exact identities and convergence proofs"] --> D["Compact dissertation"]
    B["Matched traces and independent residuals"] --> E["Numerical evidence table"]
    E --> D
    D --> F["Madrid defense"]
    G["Contribution and approximation diagrams"] --> F
    H["Unresolved checks and comparisons"] --> I["Future work"]
~~~

- [Contribution workflow](figures/final-delivery/contribution_workflow.pdf) and [classical and learned comparison](figures/final-delivery/ml_workflow.pdf) are the formula-driven vector figures used in the defense alongside the dedicated `Overall workflow: jet-space PDE to certified profile` slide in [defense_wku_madrid.tex](defense_wku_madrid.tex). See their [contribution source](figures/final-delivery/contribution_workflow.tex) and [comparison source](figures/final-delivery/ml_workflow.tex).
- The figures for the material-coordinate geometry and the rotating basin are defined in the LaTeX sources.
- The [`@delivery` user manual](../delivery/README.md) documents how the general symbolic reducer (`python delivery/reduce_pde.py --model <path-to-model-file/sympy-compiled-PDEs> --output <path-to-experiment-log>`) works, where experiment logs live (`delivery/logs/`), and the mathematical/computational boundaries of each stage.
- The [verification dossier](../delivery/VERIFICATION.md) connects the manuscript claims to calculations and contains the reproducible build entry point (`bash delivery/build_pdfs.sh`).
