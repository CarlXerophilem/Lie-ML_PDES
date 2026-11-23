"""A readable child frontend for each complete symbolic 2D parameter cell."""
import argparse
import json
from pathlib import Path
from main import json_ready,print_derivation
from analyze_2d import analyze
from models_2d import branch_model_2d,recover_one_dimension

HERE=Path(__file__).resolve().parent


def run_case(name,output,trace='full'):
    output=Path(output).resolve()
    if not output.is_relative_to(HERE) or output==HERE or output.exists():
        raise ValueError('Use a NEW output directory inside this cycle')
    from gatekeeper import check_gate
    if not check_gate(1)['passed']:
        raise ValueError('Current stage-1 gate is required')
    report=analyze(**branch_model_2d(name))
    if report['integration']['status']=='failed' or 'basis' not in report['integration']:
        raise AssertionError(report['integration'])
    from reductions_2d import plane_wave,rotating_radial,rotation_scaling_time_ode
    from algebra_2d import representative_subalgebras
    from data_experiments_2d import run_data_controls
    report['subalgebras']=representative_subalgebras(name,basis=report['integration']['basis'])
    report['subalgebras']['author_declaration_review_status']=report['subalgebras']['algebra_source_review_status']
    report['subalgebras']['source_classification_review_gate']=report['integration']['review_gate']
    report['subalgebras']['algebra_source_review_status']=(
        'reviewed_exact_version' if report['integration']['review_gate']['passed'] else 'pending_current_classification_review')
    report['subalgebra_classification']=report['subalgebras']['optimality_status']
    report['reductions']={'plane_wave':plane_wave(name),'radial':rotating_radial(name),
                          'rotation_scaling':rotation_scaling_time_ode(name)}
    if name=='slope_only_f0':
        report['reductions']['rotation_scaling_n2']=rotation_scaling_time_ode(name,diffusion_exponent=2)
    report['one_dimensional_restriction']=recover_one_dimension(name)
    report['data_experiments']=run_data_controls(name)
    if (report['subalgebras']['status']!='verified_representatives'
            or report['reductions']['plane_wave']['status']!='verified_ode_reduction'
            or report['reductions']['radial']['status']!='verified_pde_reduction'
            or report['data_experiments']['status']!='verified_specified_data_controls'):
        raise AssertionError('A declared algebra, reduction or data control failed')
    if any(row['status'] not in ('verified_ode_reduction','verified_pde_reduction','generator_not_admitted')
           for row in report['reductions'].values()):
        raise AssertionError('Unresolved reduced-equation reconstruction')
    report['reduction_status']='verified_specified_reductions'
    report['data_status']=report['data_experiments']['status']
    report['equivalence']={'full_groupoid_status':'unresolved',
        'primitive_conservative':'(h,u,v,B)->(h,h*u,h*v,B), Jacobian h^2>0',
        'reflection':('(y,v,f)->(-y,-v,-f); f=0 is preserved' if
                      report['data_experiments']['signed_coriolis_reflection']['fixed_parameter_symmetry'] else
                      '(y,v,f)->(-y,-v,-f); nonzero fixed f changes sign'),
        'branch_merging':'No unproved equation equivalence removes cells'}
    if trace=='full':
        print_derivation(report)
        for title,key in [('8b. Actual subalgebra representatives','subalgebras'),
                          ('9. Invariants, projection rank and exact pullback','reductions'),
                          ('10. Specified initial graphs and fluxes','data_experiments'),
                          ('11. One-dimensional restriction and Coriolis control','one_dimensional_restriction')]:
            print('\n'+title)
            print(json.dumps(json_ready(report[key]),indent=2))
    output.mkdir(parents=True)
    (output/'derivation.json').write_text(json.dumps(json_ready(report),indent=2),encoding='utf-8')
    print(name,report['classification_status'],len(report['determining_equations']),
          'determining equations; dimension',report['integration']['dimension'],flush=True)
    return report


def case_cli(name):
    parser=argparse.ArgumentParser(description=f'General-symm derivation: {name}')
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--trace',choices=['full','summary'],default='full')
    args=parser.parse_args()
    run_case(name,args.out,args.trace)
