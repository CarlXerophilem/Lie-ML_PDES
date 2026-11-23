"""Reproduce historical defects without executing either historical CLI."""
import ast
import hashlib
import json
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def audit():
    original = ROOT/'research_artifacts/SVE-reproduced-20261012/main.py'
    template = original.with_name('gemini-code-1792476737954.py')
    scalar = ROOT/'build/sve-autonomous-20261019/recovery/package/main.py'
    syntax = {}
    for name,path in [('eulerian_2022',original),('style_template',template),('scalar_2026',scalar)]:
        try:
            ast.parse(path.read_text(encoding='utf-8-sig'))
            syntax[name] = {'parseable':True}
        except SyntaxError as error:
            syntax[name] = {'parseable':False,'line':error.lineno,'error':error.msg}
        syntax[name]['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    tree = ast.parse(original.read_text(encoding='utf-8-sig'))
    selected = [node for node in tree.body if isinstance(node,(ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef))]
    namespace = {}
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(original),'exec'),namespace)
    residual = namespace['prolong_and_act'](namespace['X5_correct'],namespace['eqs_m3'])[-1]
    witness = sp.simplify(residual.subs({namespace['m']:2,namespace['u']:2,
                                       namespace['zeta']:1,namespace['u_x']:1}))
    if witness != -6:
        raise AssertionError('Historical mixed-shell defect changed')
    from main import JetSpace, verify_generator
    from models import branch_model
    fixed = branch_model('grass_cubic')
    t,x = fixed['independent_variables']; h,u,B = fixed['dependent_fields']
    corrected = verify_generator(JetSpace((t,x),(h,u,B)),fixed['equations'],(t,0),(-2*h,-u,-2*B))
    printed = verify_generator(JetSpace((t,x),(h,u,B)),fixed['equations'],(t,0),(-h,-2*u,-2*B))
    if not corrected['verified'] or printed['verified']:
        raise AssertionError('Parent repair control failed')
    return {'syntax':syntax,'historical_mixed_shell_residual':str(residual),
            'mixed_shell_witness':str(witness),'repaired_cubic_verified':corrected['verified'],
            'printed_wrong_generator_rejected':not printed['verified'],
            'source_categories':{'eulerian_2022':'full three-field 1D system',
                                 'scalar_2026':'printed scalar P; not full-system equivalence'},
            'historical_files_changed':False}


if __name__ == '__main__':
    result = audit()
    (HERE/'parent_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
