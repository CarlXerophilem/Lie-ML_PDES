#!/usr/bin/env python3
"""General deterministic symbolic PDE-to-ODE reducer and unparsed AST-to-ML runner.

Accepts any SymPy-compiled ``PDESpec`` from a Python module file (no string parsing,
no preset ODE ansatze, no hardcoded invariant coordinates), discovers point symmetries
on the complete ``JetSpace``, enumerates closed rank-(d-1) subalgebras from basis
combinations, constructs the matrix-exponential orbit quotient, integrates exact
variational balances, eliminates algebraic/cyclic profiles while preserving all
symbolic parameters, and optionally hands the live ``ReducedODE`` AST directly in-memory
to ``_profile_learning.Case.from_reduction``.

Usage examples (run from repository root):
  python delivery/reduce_pde.py --model delivery/lie_reduce/models.py:euler_spec \\
      --output delivery/logs/reduce_E1.json
  python delivery/reduce_pde.py --model delivery/lie_reduce/models.py:planar_e2_spec \\
      --subalgebra "X5 ; X1 + alpha_1*X4" --output delivery/logs/reduce_E2.json
  python delivery/reduce_pde.py --model custom_model.py --ml --output delivery/logs/custom.json
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys

os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')

import sympy as sp

from lie_reduce import PDESpec, serial, timed
from lie_reduce.determining import smooth_symmetries
from lie_reduce.hidden import strata
from lie_reduce.models import (
    discover_and_enumerate,
    euler_spec,
    exchange_spec,
    planar_e2_spec,
    polar_e2_spec,
    scalar_spec,
)
from lie_reduce.reduce import reduce


BUILTIN_MODELS = {
    'E1': lambda: euler_spec(),
    'P': lambda: scalar_spec('P'),
    'M': lambda: scalar_spec('M'),
    'E2_planar': lambda: planar_e2_spec(),
    'E2_polar': lambda: polar_e2_spec(),
    'E_exch': lambda: exchange_spec(),
}


def load_pde_spec(target: str) -> PDESpec:
    """Load a SymPy-compiled PDESpec from '<file.py>[:<attr_or_callable>]' or built-in name."""
    if target in BUILTIN_MODELS:
        return BUILTIN_MODELS[target]()

    file_part, sep, attr_part = target.partition(':')
    mod_path = Path(file_part).expanduser().resolve()
    if not mod_path.is_file():
        raise FileNotFoundError(
            f"Model target '{target}' is neither a built-in name ({', '.join(BUILTIN_MODELS)}) "
            f"nor an existing Python file '{mod_path}'."
        )

    spec_loader = None
    # If the file lives inside a Python package (contains __init__.py), import via package dotted name
    pkg_parts = [mod_path.stem]
    cur_dir = mod_path.parent
    while (cur_dir / '__init__.py').is_file():
        pkg_parts.append(cur_dir.name)
        cur_dir = cur_dir.parent
    if len(pkg_parts) > 1:
        if str(cur_dir) not in sys.path:
            sys.path.insert(0, str(cur_dir))
        module = importlib.import_module('.'.join(reversed(pkg_parts)))
    else:
        if str(mod_path.parent) not in sys.path:
            sys.path.insert(0, str(mod_path.parent))
        spec_loader = importlib.util.spec_from_file_location(f'_user_pde_{mod_path.stem}', mod_path)
        if spec_loader is None or spec_loader.loader is None:
            raise ImportError(f'Could not create module loader for {mod_path}')
        module = importlib.util.module_from_spec(spec_loader)
        spec_loader.loader.exec_module(module)

    if sep and attr_part:
        if not hasattr(module, attr_part):
            raise AttributeError(f"Module '{mod_path}' has no attribute '{attr_part}'")
        obj = getattr(module, attr_part)
        candidate = obj() if callable(obj) else obj
        if not isinstance(candidate, PDESpec):
            raise TypeError(f"'{target}' resolved to {type(candidate).__name__}, expected PDESpec")
        return candidate

    for name in ('SPEC', 'spec', 'PDE_SPEC', 'get_spec', 'build_spec'):
        if hasattr(module, name):
            obj = getattr(module, name)
            candidate = obj() if callable(obj) else obj
            if isinstance(candidate, PDESpec):
                return candidate

    found_specs = [v for v in vars(module).values() if isinstance(v, PDESpec)]
    if len(found_specs) == 1:
        return found_specs[0]
    if len(found_specs) > 1:
        raise ValueError(
            f"Module '{mod_path}' defines multiple PDESpec objects; disambiguate with '{file_part}:<attr_name>'."
        )
    raise ValueError(
        f"Module '{mod_path}' did not expose a PDESpec (define SPEC = PDESpec(...) or pass '{file_part}:<callable>')."
    )


def _detect_exponent_symbol(spec: PDESpec, explicit_name: str | None):
    if explicit_name:
        for p in spec.parameters:
            if str(p) == explicit_name:
                return p
        return sp.Symbol(explicit_name, real=True)
    for eq in spec.equations:
        for pw in eq.atoms(sp.Pow):
            for sym in pw.exp.free_symbols:
                if sym in spec.parameters:
                    return sym
    return None


def _run_ml_handoff(spec: PDESpec, reduction):
    """Compile verified scalar ReducedODE AST directly in-memory and evaluate ML benchmarks."""
    try:
        from _profile_learning import Case, Settings, compare
    except ImportError as exc:
        return {"status": "failed", "reason": f"Install lie-reduce[regular] for --ml: {exc}"}

    ode_expr = reduction.reduced_equations[0]
    f_target = reduction.target_profile or reduction.graph.profiles[0]
    z_sym = reduction.graph.z
    orders = [d.derivative_count for d in ode_expr.atoms(sp.Derivative) if d.expr == f_target]
    order = int(max(orders, default=0))
    if order < 1 or order > 3:
        return {'status': 'skipped', 'reason': f'ML layer supports scalar ODE orders 1..3, got order {order}'}

    p_sym = sp.Symbol('p_trace', real=True)
    param_vals = {}
    for idx_s, sym in enumerate(reduction.preserved_parameters):
        nm = str(sym)
        if nm.startswith('alpha_') and nm[-1].isdigit():
            param_vals[sym] = -sp.Rational(3, 2) - sp.Rational(idx_s, 5)
        elif nm.startswith('C'):
            param_vals[sym] = sp.Rational(1, 2)
        elif nm == 'm':
            param_vals[sym] = sp.Integer(2)
        else:
            param_vals[sym] = sp.Integer(1) + sp.Rational(idx_s, 5)

    trace_exprs = (p_sym,) + tuple(sp.Rational(1, 10) for _ in range(order - 1))
    ml_case = Case.from_reduction(
        spec.name,
        reduction,
        left=0.2,
        trace_interval=(0.8, 1.1),
        trace_exprs=trace_exprs,
        parameter_symbol=p_sym,
        parameter_values=param_vals,
    )
    settings = Settings(seed=27, width=5, chebyshev_degree=20, taylor_degree=22,
                        train_coordinates=20, test_coordinates=201, max_nfev=100)
    record = compare(ml_case, settings)
    return {
        'status': 'completed',
        'handoff_mode': record['handoff_mode'],
        'numeric_parameter_slice': {str(k): str(v) for k, v in param_vals.items()},
        'selection': record['selection'],
        'metrics': record['metrics'],
    }


def run_pipeline(args) -> dict:
    spec = load_pde_spec(args.model)
    exp_sym = _detect_exponent_symbol(spec, args.exponent)

    _, basis, subalgebras = discover_and_enumerate(
        spec,
        degree=args.degree,
        exponent=exp_sym,
        max_combo_terms=args.max_combo_terms,
    )

    strata_report = None
    if args.strata and exp_sym is not None:
        strata_report = strata(spec, exp_sym, args.degree, exponent=True)

    smooth_report = None
    if args.smooth_check:
        sm = smooth_symmetries(spec, exponent=exp_sym)
        smooth_report = {
            'smooth_to_affine_proved': sm.get('smooth_to_affine_proved'),
            'generic_dimension': len(sm.get('basis', ())),
        }

    candidates = (
        [s for s in subalgebras if s['id'] == args.subalgebra]
        if args.subalgebra
        else list(subalgebras)
    )
    if args.subalgebra and not candidates:
        available = [s['id'] for s in subalgebras]
        raise ValueError(f"Subalgebra '{args.subalgebra}' not found in enumerated list: {available}")

    reductions = []
    verified_scalar = None
    for sub in candidates:
        stage = timed(lambda g=sub['generators']: reduce(spec, g), args.stage_seconds)
        red = stage['value']
        if red is None:
            reductions.append({
                'subalgebra_id': sub['id'],
                'generators': sub['generators'],
                'status': stage['status'],
                'reason': stage['reason'],
                'wall_seconds': round(stage['wall_seconds'], 4),
            })
            continue
        entry = {
            'subalgebra_id': sub['id'],
            'generators': sub['generators'],
            'status': red.status,
            'reason': red.reason,
            'wall_seconds': round(stage['wall_seconds'], 4),
            'quotient_coordinate': str(red.graph.z) if red.graph is not None else None,
            'target_profile': str(red.target_profile) if red.target_profile is not None else None,
            'preserved_parameters': [str(p) for p in red.preserved_parameters],
            'first_integrals': red.first_integrals,
            'eliminated_profiles': {str(k): str(v) for k, v in red.eliminated.items()},
            'reduced_equations': [str(e) + ' = 0' for e in red.reduced_equations],
            'integrated_ode': str(red.integrated_ode) + ' = 0' if red.integrated_ode is not None else None,
            'reconstructed_lifts': [str(l) for l in red.reconstructed_lifts],
            'checks': red.checks,
        }
        reductions.append(entry)
        if verified_scalar is None and red.status == 'verified' and len(red.reduced_equations) == 1:
            ode_cand = red.reduced_equations[0]
            f_cand = red.target_profile or red.graph.profiles[0]
            ord_cand = max((d.derivative_count for d in ode_cand.atoms(sp.Derivative) if d.expr == f_cand), default=0)
            if 1 <= ord_cand <= 3:
                verified_scalar = (sub['id'], red)

    ml_report = None
    if args.ml:
        if verified_scalar is None:
            ml_report = {'status': 'skipped', 'reason': 'no verified single-scalar ODE quotient found'}
        else:
            sub_id, red_obj = verified_scalar
            ml_report = {'subalgebra_id': sub_id, **_run_ml_handoff(spec, red_obj)}

    verified_count = sum(1 for r in reductions if r['status'] == 'verified')
    scalar_ode_count = sum(
        1 for r in reductions if r['status'] == 'verified' and len(r.get('reduced_equations', ())) == 1
    )

    return {
        'model': {
            'target': args.model,
            'name': spec.name,
            'independent_variables': [str(x) for x in spec.jets.independent],
            'dependent_variables': [str(u) for u in spec.jets.dependent],
            'jet_order': spec.jets.order,
            'equations_count': len(spec.equations),
            'symbolic_parameters': [str(p) for p in spec.parameters],
            'detected_symbolic_exponent': str(exp_sym) if exp_sym is not None else None,
            'domain_conditions': list(spec.conditions),
        },
        'discovery': {
            'search_degree': args.degree,
            'basis_dimension': len(basis),
            'basis': {k: [str(c) for c in v] for k, v in basis.items()},
            'enumerated_rank_d_minus_1_subalgebras': len(subalgebras),
            'smooth_classification': smooth_report,
            'parameter_strata': strata_report,
        },
        'reductions': reductions,
        'ml_handoff': ml_report,
        'summary': {
            'evaluated_subalgebras': len(reductions),
            'verified_quotients': verified_count,
            'scalar_ode_quotients': scalar_ode_count,
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'positional_model',
        nargs='?',
        default=None,
        help='Optional positional path to Python file exporting SymPy PDESpec or built-in model name.',
    )
    parser.add_argument(
        'positional_output',
        nargs='?',
        default=None,
        help='Optional positional path to write JSON experiment log.',
    )
    parser.add_argument(
        '--model',
        '--pde',
        dest='model',
        default=None,
        help="Path to Python file exporting SymPy PDESpec ('path/to/file.py[:callable_or_attr]') or built-in name (E1, P, M, E2_planar, E2_polar, E_exch).",
    )
    parser.add_argument(
        '--output',
        '--log',
        dest='output',
        default=None,
        help='Path to write JSON experiment log (prints to stdout if omitted).',
    )
    parser.add_argument(
        '--subalgebra',
        default=None,
        help='Optional specific enumerated subalgebra ID to reduce (reduces all enumerated subalgebras if omitted).',
    )
    parser.add_argument('--degree', type=int, default=1, help='Polynomial degree in point-symmetry ansatz (default: 1).')
    parser.add_argument('--exponent', default=None, help='Optional symbolic exponent parameter name (auto-detected if omitted).')
    parser.add_argument('--max-combo-terms', type=int, default=2, help='Max basis generators per linear combination (default: 2).')
    parser.add_argument('--stage-seconds', type=float, default=20.0, help='Per-subalgebra symbolic timeout in seconds (default: 20); 0 disables the timer.')
    parser.add_argument('--strata', action='store_true', help='Also compute exact symbolic parameter/exponent jump strata.')
    parser.add_argument('--smooth-check', action='store_true', help='Also run Spencer second-partial smooth-to-affine check.')
    parser.add_argument('--ml', action='store_true', help='Pass first verified scalar ReducedODE AST directly in-memory to ML comparison.')

    args = parser.parse_args(argv)
    args.model = args.model or args.positional_model
    args.output = args.output or args.positional_output
    if not args.model:
        parser.error('a model target is required via --model <path-to-model.py[:spec]> (or positional argument)')
    report = serial(run_pipeline(args))
    rendered = json.dumps(report, indent=2, default=str)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered + '\n', encoding='utf-8')
        s = report['summary']
        print(
            f"[{report['model']['name']}] basis={report['discovery']['basis_dimension']} "
            f"subalgebras={s['evaluated_subalgebras']} verified={s['verified_quotients']} "
            f"scalar_odes={s['scalar_ode_quotients']} -> {out_path}"
        )
    else:
        print(rendered)
    return 0 if report['summary']['verified_quotients'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
