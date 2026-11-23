"""Inventory every declared case and retained failure without promoting a pass."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.run_strict_lie import cases


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reports',type=Path,default=ROOT/'build/final-20261027/revalidated-release')
    parser.add_argument('--selected',type=Path,default=ROOT/'build/final-20261027/selected-release')
    parser.add_argument('--out',type=Path,default=ROOT/'research_artifacts/sve-final-20261027/data')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    rows=[];categories=Counter();failed=[];families=Counter()
    for key in cases():
        path=args.reports/(key.replace(':','--')+'-60.json')
        row={'case':key,'original_cas_status':'timeout','terminal_match':False,
             'verified_families':0,'excluded_families':0,'selected_chains':0,
             'projection_ranks':'','reduction_categories':'','unparsed_reduction_guards':0,
             'determining_completeness':'unproved','data_status':'not_checked','strict_pass':False}
        if path.exists():
            r=json.loads(path.read_text())
            checks=r.get('independent_checks',[])
            families.update(c['status'] for c in checks)
            chains=r.get('translation_reduction',{}).get('chains',[])
            row.update(original_cas_status=r['cas']['status'],
                       terminal_match=r.get('branch_correspondence',{}).get('matched',False),
                       verified_families=sum(c.get('verified',False) for c in checks),
                       excluded_families=sum(c['status']=='excluded-by-input-guards' for c in checks),
                       selected_chains=len(chains),
                       projection_ranks=';'.join(str(c.get('projection_rank','')) for c in chains),
                       reduction_categories=';'.join(c['category'] for c in chains),
                       unparsed_reduction_guards=sum(g['status']=='unparsed' for c in chains for g in c.get('guard_checks',[])),
                       report_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            categories.update(c['category'] for c in chains)
            for i,c in enumerate(chains):
                if c.get('reconstruction_identity_verified') is False or c.get('Q_zero') is False:
                    failed.append({'case':key,'chain':i,'category':c['category']})
        rows.append(row)
    scalar=[]
    original=args.selected
    for exponent,suffix in [('general','-general'),('1','-1'),('3','')]:
        p=original/('scalar-nine-characteristic-chains'+suffix+'.json')
        r=json.loads(p.read_text())
        for i,c in enumerate(r['cases']):
            scalar.append({'exponent':exponent,'source_subsection':i+1,
                           'category':c.get('category'),'positive_velocity_guard':c.get('positive_velocity_guard'),
                           'Q':c.get('Q'),'reconstruction_residual':c.get('reconstruction_residual')})
    retry_path=args.out/'remote-summary.json'
    retry=json.loads(retry_path.read_text()) if retry_path.exists() else None
    for row in rows:
        row['latest_returned_family']=row['verified_families']>0
        row['latest_scope']='Initial returned charts; completeness unproved'
        if row['case']=='E1:grass_generic' and retry:
            generic=next(v for v in retry['jobs'] if v['name']=='direct-generic')
            row['latest_returned_family']=generic.get('returned_family_verified',False)
            row['latest_scope']='Native direct-CRACK chart: 1<=m<=4, m not in {1,2,3}; m1,m2 incomplete'
    analysis={'strict_pass':False,'total_inputs':len(rows),'coverage_scope':'Initial campaign counts; latest chart status recorded separately per row',
              'latest_inputs_with_verified_returned_chart':sum(r['latest_returned_family'] for r in rows),
              'returned_inputs':sum(r['original_cas_status']=='returned-solved' for r in rows),
              'matched_inputs':sum(r['terminal_match'] for r in rows),
              'verified_families':sum(r['verified_families'] for r in rows),
              'excluded_families':sum(r['excluded_families'] for r in rows),
              'family_categories':dict(families),'selected_chain_categories':dict(categories),
              'failed_defined_chain_identities':failed,'coverage':rows,'scalar_selected_chains':scalar,
              'open_gates':['necessary-and-sufficient determining solutions and exceptional strata',
                            'scope-complete source and declared-branch reductions',
                            'same-IBVP stabilizers and invariant-trace compatibility when data are supplied'],
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.out/'delivery-analysis.json').write_text(json.dumps(analysis,indent=2)+'\n',encoding='utf-8')
    with (args.out/'coverage.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(dict.fromkeys(k for row in rows for k in row)))
        writer.writeheader();writer.writerows(rows)
    print(json.dumps({k:v for k,v in analysis.items() if k not in ['coverage','scalar_selected_chains']},indent=2))


if __name__=='__main__':main()
