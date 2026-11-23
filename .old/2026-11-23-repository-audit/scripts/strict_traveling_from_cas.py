"""Select a traveling line inside solved CAS algebras, then solve characteristics.

Only coefficients in the returned algebra are selected. No profile or invariant
is supplied. This is a selected-subalgebra certificate, not source-wide closure.
"""
from pathlib import Path
import sys
import json
import hashlib
import argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import sympy as sp
from scripts.run_strict_lie import model,atomic_json
from symm.LieSymm.core import json_ready
from symm.LieSymm.strict import parse_liepde_output,_reduce_names,reduce_from_analysis
from scripts.revalidate_strict_receipts import revalidate_receipt


def traveling_chains_from_receipt(definition, original):
    report=revalidate_receipt(definition,original)
    coords=(*definition['independent_variables'],*definition['dependent_fields'])
    if len(definition['independent_variables'])!=2 or len(definition['dependent_fields'])!=1:
        raise ValueError('This supplementary selector is scalar 1+1 only')
    rows=[]
    for index,check in enumerate(report['independent_checks']):
        if not check.get('verified'):continue
        translations=[v for v in check['basis'] if v[2]==0 and not any(c.has(*coords) for c in v[:2])]
        matrix=sp.Matrix([v[:2] for v in translations]).T
        target=sp.Matrix((1,-1))
        if not translations:
            rows.append(dict(branch=index,status='no_traveling_line_in_returned_span'));continue
        try:weights,undetermined=matrix.gauss_jordan_solve(target)
        except ValueError:
            rows.append(dict(branch=index,status='no_traveling_line_in_returned_span'));continue
        weights=weights.subs({c:0 for c in undetermined})
        vector=tuple(sp.simplify(sum(weights[k]*translations[k][a] for k in range(len(translations)))) for a in range(3))
        membership=matrix*weights-target
        if any(sp.simplify(v)!=0 for v in membership):raise ValueError('Failed algebra-membership certificate')
        guards=list(check.get('guard_checks',[]))
        for weight in weights:
            denominator=sp.denom(sp.factor(weight))
            if denominator!=1:
                guards.append(dict(guard=str(sp.Ne(denominator,0)),condition=sp.Ne(denominator,0),
                                   status='conditional',origin='subalgebra_membership'))
        derived={**report,'independent_checks':[{**check,'basis':[vector],'guard_checks':guards}]}
        rows.append(dict(branch=index,input_sha256=report['input_sha256'],
                         parameter_substitutions=check.get('parameter_substitutions',{}),
                         translation_basis=translations,combination_weights=list(weights),
                         membership_residual=list(membership),reduction=reduce_from_analysis(derived),
                         source_domain='m>=1; m=0 is an extra out-of-source-domain control'))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=ROOT/'build/final-20261027/revalidated-reviewed')
    parser.add_argument('--out',type=Path,default=ROOT/'build/final-20261027/selected-reviewed')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for case in ('P:general','P:1','P:3'):
        receipt=args.source/(case.replace(':','--')+'-60.json')
        for row in traveling_chains_from_receipt(model(case),json.loads(receipt.read_text(encoding='utf-8'))):
            row.update(case=case,source_receipt_sha256=hashlib.sha256(receipt.read_bytes()).hexdigest())
            rows.append(row)
    atomic_json(args.out/'scalar-traveling-from-cas.json',json_ready(dict(status='partial',cases=rows,
        execution_kind='historical_output_revalidation',script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())))
    print('derived traveling chains',len(rows),'strict closure remains incomplete')


if __name__=='__main__':
    main()
