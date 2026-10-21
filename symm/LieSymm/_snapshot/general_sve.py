"""Public dimensional dispatcher with the approved equation-first interface.

The immutable stage-1 main.py remains its verified implementation. 2D uses
the same jets/prolongation engine and a separately verified mixed-order shell.
Unknown PDE fingerprints retain unresolved integration, never a guessed basis.
"""


def analyze(independent_variables,dependent_fields,equations,parameters,
            branch_conditions,data_case=None):
    coordinates=tuple(independent_variables)
    if len(coordinates)==2:
        from main import analyze as implementation
    elif len(coordinates)==3:
        from gatekeeper import check_gate
        if not check_gate(1)['passed']:
            raise ValueError('The current 1D complete-classification gate is required')
        from analyze_2d import analyze as implementation
    else:
        raise ValueError('This cycle declares only 1+1 and 2+1 dimensional models')
    return implementation(coordinates,dependent_fields,equations,parameters,
                          branch_conditions,data_case)


def main():
    import argparse
    import json
    from pathlib import Path
    from main import json_ready,print_derivation
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dimension',type=int,choices=(1,2),required=True)
    parser.add_argument('--branch',required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    output=args.out.resolve()
    if not output.is_relative_to(root) or output==root or output.exists():
        parser.error('Use a NEW output directory inside this cycle')
    if args.dimension==1:
        from models import branch_model as model
    else:
        from models_2d import branch_model_2d as model
    report=analyze(**model(args.branch))
    print_derivation(report)
    output.mkdir(parents=True)
    (output/'derivation.json').write_text(json.dumps(json_ready(report),indent=2),encoding='utf-8')
    return 1 if report['classification_status']=='failed' else 0


if __name__=='__main__':
    raise SystemExit(main())
