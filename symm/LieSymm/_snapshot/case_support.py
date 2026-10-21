"""A thin per-branch command line around the shared, readable derivation."""
import argparse
import json
from pathlib import Path
import sympy as sp
from main import analyze, json_ready, print_derivation
from models import branch_model

HERE=Path(__file__).resolve().parent


def run_case(name, output, trace='full'):
    output=Path(output).resolve()
    if not output.is_relative_to(HERE) or output == HERE or output.exists():
        raise ValueError('Use a NEW output directory inside this cycle')
    report=analyze(**branch_model(name))
    if report['integration']['status'] == 'failed':
        raise AssertionError(report['integration'])
    from reductions import traveling_reduction, scaling_reduction
    from data_experiments import uniform_flow, constant_slope_flow, initial_data_stabilizer, lake_control
    model=branch_model(name)
    basis=report['integration']['basis']
    report['traveling_reduction']=traveling_reduction(model,basis)
    report['scaling_reductions']=[]
    coordinates=model['independent_variables']+model['dependent_fields']
    for vector in basis:
        weights=[sp.diff(value,coordinate) for value,coordinate in zip(vector,coordinates)]
        if all(sp.simplify(value-weight*coordinate)==0 for value,weight,coordinate in zip(vector,weights,coordinates)):
            reduction=scaling_reduction(model,basis,vector)
            if reduction.get('available_conditional_chart')=='time':
                reduction=scaling_reduction(model,basis,vector,chart='time')
                report['scaling_reductions'].append(reduction)
                from models import n
                reduction=scaling_reduction(model,basis,vector,chart='space',substitutions={n:2})
            report['scaling_reductions'].append(reduction)
    x=model['independent_variables'][1]
    report['data_experiments']={
        'uniform_flow':uniform_flow(name),
        'constant_slope_flow':constant_slope_flow(name),
        'initial_profiles':{key:initial_data_stabilizer(name,(2,3,bed))
            for key,bed in [('flat',sp.S.One),('linear',1+x),('quadratic',1+x**2)]},
        'fixed_endpoints':initial_data_stabilizer(name,(2,3,1),endpoints=(0,1)),
        'zero_speed_control':lake_control(name,bed=x**2,level=3),
    }
    report['data_status']='specified_controls_verified_with_recorded_chart_exclusions'
    from subalgebras import classify_subalgebra_lines
    from models import n
    options={'parameter':n,'domain':sp.Interval(0,4)} if name=='slope_only' else {}
    report['subalgebras']=classify_subalgebra_lines(coordinates,basis,**options)
    report['subalgebra_classification']=report['subalgebras'].get('optimality_status','unresolved')
    if report['subalgebras']['status']!='certified_line_orbit_classification':
        raise AssertionError('Declared branch subalgebra representatives were not constructed')
    if (report['traveling_reduction']['status']!='verified_reduction'
            or any(value['status']!='verified_reduction' for value in report['scaling_reductions'])):
        raise AssertionError('Declared reduction failed its exact reconstruction')
    data=report['data_experiments']
    if (data['uniform_flow']['status']!='verified_exact_solution'
            or data['constant_slope_flow']['status']!='verified_exact_solution'
            or any(value['status']!='verified_initial_data_stabilizer' for value in data['initial_profiles'].values())):
        raise AssertionError('Declared exact-flow or initial-data control failed')
    report['equivalence']={'proof':'EQUIVALENCE.md','full_groupoid_status':'unresolved',
        'negative_velocity_chart':'covered by exact (x,u)->(-x,-u) reflection of signed flux',
        'primitive_conservative':'q=h*u, invertible when h>0'}
    report['reduction_status']=report['traveling_reduction'].get('status','unresolved')
    if trace == 'full':
        print_derivation(report)
        print('\n8b. Subalgebra representative families from the actual adjoint action')
        print(json.dumps(json_ready(report['subalgebras']),indent=2))
        print('\n9. Characteristic integration and original-equation pullback')
        print(json.dumps(json_ready(report['traveling_reduction']),indent=2))
        print('\n10. Diagonal scaling charts and exact reconstruction')
        print(json.dumps(json_ready(report['scaling_reductions']),indent=2))
        print('\n11. Initial graph, domain and flux experiments')
        print(json.dumps(json_ready(report['data_experiments']),indent=2))
    output.mkdir(parents=True)
    (output/'derivation.json').write_text(json.dumps(json_ready(report),indent=2),encoding='utf-8')
    print(name,report['classification_status'],len(report['determining_equations']),
          'determining equations; dimension',report['integration'].get('dimension'))
    return report


def case_cli(name):
    parser=argparse.ArgumentParser(description=f'Full general-symm derivation for {name}')
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--trace',choices=['full','summary'],default='full')
    args=parser.parse_args()
    run_case(name,args.out,args.trace)
