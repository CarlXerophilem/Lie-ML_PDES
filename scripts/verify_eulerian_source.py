"""Post-discovery audit of the printed 2022 cubic generator (equation 25)."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import sympy as sp
from scripts.run_strict_lie import model
from symm.LieSymm.core import JetSpace, point_action, prolongation_coefficients, json_ready
from symm.LieSymm.strict import StrictMixedShell, input_fingerprint


def audit():
    definition=model('E1:grass_cubic')
    j=JetSpace(definition['independent_variables'],definition['dependent_fields'])
    t,x=j.x;h,u,B=j.u
    shell=StrictMixedShell(j,definition['equations'])
    rows={}
    for label,eta in [('printed_equation_25',(-h,-2*u,-2*B)),
                      ('corrected_comparison',(-2*h,-u,-2*B))]:
        coeff=prolongation_coefficients(j,(t,0),eta,1,'recursive')
        residual=[sp.factor(shell.reduce(point_action(j,e,(t,0),eta,coefficients=coeff)))
                  for e in definition['equations']]
        rows[label]={'xi':(t,0),'eta':eta,'original_PDE_tangency_residual':residual,
                     'admitted':all(v==0 for v in residual)}
    assert not rows['printed_equation_25']['admitted']
    assert rows['corrected_comparison']['admitted']
    return {'scope':'Post-solve source comparison, not a determining-system solve',
            'source_DOI':'10.3390/sym14081679','source_equation':25,
            'input_sha256':input_fingerprint(**definition),'cases':rows}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists():parser.error('Select a new output; preserve previous receipts')
    result=audit();result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(json_ready(result),indent=2)+'\n',encoding='utf-8')
    print('Printed generator rejected; corrected comparison admitted.')
