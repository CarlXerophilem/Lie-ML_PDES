import ast
import copy
import json
from pathlib import Path
import unittest
import sympy as sp
from lie_pde_reducer import reduction,verifier
from ode_methods.task import Task
from ode_methods.classical import taylor,chebyshev,analytic

ROOT=Path(__file__).resolve().parent


class IsolationTests(unittest.TestCase):
    def test_checker_has_no_solver_import(self):
        for path in ('independent_verifier.py','symbolic_input.py'):
            tree=ast.parse((ROOT/path).read_text())
            imports=[]
            for node in ast.walk(tree):
                if isinstance(node,ast.Import):imports.extend(v.name for v in node.names)
                if isinstance(node,ast.ImportFrom):imports.append(node.module or '')
            self.assertTrue(all(not any(bad in name for bad in ('lie_reduce','ode_methods','torch','numpy','scipy')) for name in imports),imports)
        for path in (ROOT/'ode_methods').glob('*.py'):
            self.assertNotIn('independent_verifier',path.read_text())

    def test_pde_tampering_detected(self):
        record=reduction('E1',2,'bed_drift');paper=(ROOT/'paper_contracts/E1.json').read_text()
        self.assertEqual(record['verification']['status'],'verified_local_identities')
        altered=copy.deepcopy(record['solver_output']);altered['equations'][2]='0'
        self.assertEqual(verifier(altered,paper)['status'],'not_verified')
        wrong_model=copy.deepcopy(record['solver_output']);wrong_model['model']='M'
        self.assertEqual(verifier(wrong_model,paper)['status'],'verification_error')
        source=json.loads(paper);source['equations'][2]+='+1'
        self.assertEqual(verifier(record['solver_output'],json.dumps(source))['status'],'not_verified')

    def test_unsafe_expression_rejected(self):
        from symbolic_input import Expressions
        with self.assertRaises(ValueError):Expressions().read('__import__("os").getcwd()')

    def test_independent_generator_sufficiency(self):
        paper=(ROOT/'paper_contracts/E1.json').read_text()
        record={'kind':'point_generators','model':'E1','parameter_bindings':{'m':'2'},
                'generators':[['1','0','0','0','0'],['t','x','0','0','0']]}
        self.assertEqual(verifier(record,paper)['status'],'verified_generators_on_regular_chart')
        record['generators']=[['0','0','0','1','0']]
        self.assertEqual(verifier(record,paper)['status'],'not_verified')
        record['model']='M'
        self.assertEqual(verifier(record,paper)['status'],'verification_error')
        record.update(model='E1',generators=[])
        self.assertEqual(verifier(record,paper)['status'],'verification_error')

    def test_independent_principal_regularity(self):
        paper={'schema':'paper-pde-v1','source_anchor':'fixture','source_excerpt':'u_t squared = 0',
               'model':'degenerate','independent':['t','x'],'dependent':['u'],'parameters':[],
               'equations':['Derivative(u(t,x),t)**2'],'principal':['Derivative(u(t,x),t)']}
        output={'kind':'point_generators','model':'degenerate','generators':[['1','0','0']]}
        result=verifier(output,paper)
        self.assertEqual(result['status'],'verification_error')
        self.assertIn('singular',result['reason'])

    def test_exact_and_approximate_candidates(self):
        task=Task({'id':'N1','operator':'regular','initial':'1','interval':['0','1'],'residual':'5*y*dy/2+1'})
        paper={'schema':'paper-ode-v1','source_anchor':'fixture','source_excerpt':'2UU_x+1=0',
               'symbols':['s','y','dy'],'coordinate':'s','value_symbol':'y','derivative_symbol':'dy',
               'residual':task.data['residual'],'trace_coordinate':'0','trace_value':'1'}
        self.assertEqual(verifier(analytic(task),paper)['status'],'exact_implicit_solution')
        self.assertEqual(verifier(taylor(task,6),paper)['status'],'approximation')
        record=chebyshev(task,16)
        self.assertEqual(record['status'],'residual_tolerance')
        self.assertLess(record['collocation_residual_max'],1e-10)
        self.assertEqual(verifier({'representation':'analytic','expression':'-sqrt(1-4*s/5)'},paper)['status'],'not_verified')

    def test_nonautonomous_symbolic_path(self):
        task=Task({'id':'linear_fixture','operator':'regular','initial':'1','interval':['0','1'],'residual':'dy-s*y'})
        candidate=analytic(task)
        self.assertEqual(candidate['representation'],'analytic')
        paper={'schema':'paper-ode-v1','source_anchor':'fixture','source_excerpt':"y'=s*y; y(0)=1",
               'symbols':['s','y','dy'],'coordinate':'s','value_symbol':'y','derivative_symbol':'dy',
               'residual':'dy-s*y','trace_coordinate':'0','trace_value':'1'}
        self.assertEqual(verifier(candidate,paper)['status'],'exact_solution')
        equilibrium=Task({'id':'equilibrium','operator':'regular','initial':'0','interval':['0','1'],'residual':'dy-y'})
        self.assertEqual(analytic(equilibrium)['expression'],'0')

    def test_lobatto_trace_is_not_moved(self):
        task=Task({'id':'BB_fixture','operator':'BB','initial':'0','interval':['-1','1'],'residual':'s*dy+y-3*s**2'})
        with self.assertRaisesRegex(ValueError,'Lobatto node'):chebyshev(task,7)
        candidate=chebyshev(task,8)
        coeff=list(map(float,candidate['coefficients']))
        self.assertAlmostEqual(coeff[2],1.,places=11)
        self.assertLess(max(abs(v) for i,v in enumerate(coeff) if i!=2),1e-11)

    def test_candidate_denominator_and_network_derivative(self):
        paper={'schema':'paper-ode-v1','source_anchor':'fixture','source_excerpt':'y_prime/y=0',
               'symbols':['s','y','dy'],'coordinate':'s','value_symbol':'y','derivative_symbol':'dy',
               'residual':'dy/y','residual_numerator':'dy','residual_denominator':'y','trace_coordinate':'0','trace_value':'0'}
        self.assertEqual(verifier({'representation':'polynomial','coefficients':['0']},paper)['status'],'inadmissible')
        altered=copy.deepcopy(paper);altered['residual_numerator']='0'
        self.assertEqual(verifier({'representation':'polynomial','coefficients':['1']},altered)['status'],'verification_error')
        paper.update(residual='dy',residual_denominator='1',trace_value='1')
        candidate={'representation':'network','layers':[{'kind':'linear','weight':[[0]],'bias':[1]}],
                   'verification_points':['0'],'autograd_probes':[{'coordinate':'0','value':1,'derivative':99}]}
        self.assertEqual(verifier(candidate,paper)['status'],'derivative_mismatch')
        candidate['autograd_probes']=[]
        self.assertEqual(verifier(candidate,paper)['status'],'verification_error')

    def test_model_parameter_counts(self):
        import torch
        from ode_methods.neural import Network
        torch.set_default_dtype(torch.float64)
        self.assertEqual(sum(p.numel() for p in Network().parameters()),12673)
        liquid=Network(liquid=True)
        self.assertEqual(sum(p.numel() for p in liquid.parameters()),29569)
        self.assertTrue(all(torch.all(a==.5) for a in liquid.alpha))

    def test_training_input_allowlist(self):
        from spinn_ode_solver import training_task
        task=training_task({'id':'test','operator':'regular','initial':'1','interval':['0','1'],
                           'residual':'dy-y','exact_solution':'exp(s)','reference_values':[1,2],
                           'singularity':'oracle','paper_contract':{'answer':'hidden'}})
        self.assertEqual(set(task.data),{'id','operator','initial','interval','residual'})


if __name__=='__main__':unittest.main()
