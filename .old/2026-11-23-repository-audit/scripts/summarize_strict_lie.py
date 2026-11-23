"""Post-solve algebra audit and readable evidence; never supplies a CAS answer."""
from pathlib import Path
import argparse
import json
import sys
import hashlib

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import sympy as sp
from scripts.run_strict_lie import model,cases,atomic_json
from symm.LieSymm.core import json_ready,lie_bracket
from symm.LieSymm.strict import parse_liepde_output,_reduce_names


def coefficient_matrix(vectors,coordinates):
    columns=[]
    for vector in vectors:
        column={}
        for i,value in enumerate(vector):
            for powers,coefficient in sp.Poly(value,*coordinates,domain='EX').terms():
                if coefficient != 0:
                    column[(i,powers)]=coefficient
        columns.append(column)
    keys=sorted(set().union(*(set(c) for c in columns)))
    return sp.Matrix([[c.get(k,0) for c in columns] for k in keys])


def audit_algebra(definition,raw,checks,*,cas_mode='liepde'):
    coordinates=(*definition['independent_variables'],*definition['dependent_fields'])
    parameters=definition['parameters']
    names=_reduce_names((*coordinates,*parameters))
    parsed=parse_liepde_output(raw,{v:k for k,v in names.items()},_crack_frame=cas_mode=='crack')
    results=[]
    for branch,check in zip(parsed['branches'],checks):
        if not check.get('verified'):
            results.append(dict(status=check['status']));continue
        assigned=branch['assignments']
        substitutions={p:assigned[p] for p in parameters if p in assigned}
        keys=[sp.Symbol('xi_'+names[x]) for x in definition['independent_variables']]
        keys += [sp.Symbol('eta_'+names[u]) for u in definition['dependent_fields']]
        components=[assigned[k].subs(substitutions) for k in keys]
        free=[c for c in branch['free'] if c not in parameters]
        vectors=[tuple(sp.diff(v,c) for v in components) for c in free]
        try:
            matrix=coefficient_matrix(vectors,coordinates)
            pivots=matrix.rref()[1]
            basis=[vectors[i] for i in pivots]
            pivot_rows=matrix[:,list(pivots)].T.rref()[1]
            rank_minor=sp.factor(matrix.extract(pivot_rows,pivots).det())
            brackets={}
            conditions=[sp.denom(sp.factor(v)) for b in basis for v in b]
            for i in range(len(basis)):
                for k in range(i+1,len(basis)):
                    bracket=lie_bracket(coordinates,basis[i],basis[k])
                    system=coefficient_matrix([*basis,bracket],coordinates)
                    solution,free_parameters=system[:,:-1].gauss_jordan_solve(system[:,-1])
                    solution=solution.subs({p:0 for p in free_parameters})
                    remainder=[sp.simplify(v-sum(solution[a]*basis[a][j] for a in range(len(basis))))
                               for j,v in enumerate(bracket)]
                    if any(v != 0 for v in remainder):
                        raise ValueError('Nonzero bracket reconstruction')
                    brackets[f'{i},{k}']=list(solution)
                    conditions += [sp.denom(sp.factor(v)) for v in solution]
            results.append(dict(status='verified_finite_algebra_closure',dimension=len(basis),
                                basis=basis,brackets=brackets,parameter_substitutions=substitutions,
                                basis_rank_guard=sp.Ne(rank_minor,0),basis_rank_minor=rank_minor,
                                nonzero_denominators=list(dict.fromkeys(v for v in conditions if v != 1)),
                                scope='Finite constant-coefficient specialization of returned CAS family; not maximality'))
        except (ValueError,sp.PolynomialError) as exc:
            results.append(dict(status='unresolved_basis_or_brackets',reason=str(exc)))
    return results


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'build/sve-strict-lie-20261026')
    parser.add_argument('--tier',type=int,default=60)
    args=parser.parse_args()
    rows=[];details=['# Strict equation-first derivation record','',
                    '**Acceptance: INCOMPLETE.** Empty CAS residual lists, finite algebra closure and selected translation reductions do not establish exhaustive strata or the nine source-subsection chains.','']
    for key in cases():
        path=args.out/(key.replace(':','--')+f'-{args.tier}.json')
        if not path.exists():
            worker=args.out/(key.replace(':','--')+f'-worker-{args.tier}.json')
            receipt=json.loads(worker.read_text()) if worker.exists() else {}
            rows.append(dict(case=key,status=receipt.get('status','not-run'),strict_pass=False))
            continue
        report=json.loads(path.read_text(encoding='utf-8'))
        row=dict(case=key,status=report['classification_status'],cas=report['cas']['status'],strict_pass=False,
                 report_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        if report.get('cas_solution'):
            row['algebras']=audit_algebra(model(key),report['cas']['stdout'],report.get('independent_checks',[]))
        row['reduction_categories']=[c.get('category') for c in report.get('translation_reduction',{}).get('chains',[])]
        rows.append(row)
        details += [f'## {key}',f"CAS: `{row['cas']}`; strict acceptance remains incomplete.",'',
                    'Input guards: `'+str(report['branch_conditions'].get('guards',[]))+'`','']
        for algebra in row.get('algebras',[]):
            details += ['Algebra: `'+str(json_ready(algebra))+'`','']
        for chain in report.get('translation_reduction',{}).get('chains',[]):
            details += ['Characteristic/reduction certificate:','```json',json.dumps(chain,indent=2),'```','']
        if report.get('transfer_diagnostics'):
            details += ['Custom constitutive-law diagnostics:','```json',json.dumps(report['transfer_diagnostics'],indent=2),'```','']
    artifact=dict(strict_pass=False,cases=rows,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    atomic_json(args.out/f'algebra-coverage-{args.tier}.json',json_ready(artifact))
    (args.out/f'DERIVATIONS-{args.tier}.md').write_text('\n'.join(details),encoding='utf-8')
    print('cases',len(rows),'strict_pass',False)


if __name__=='__main__':
    main()
