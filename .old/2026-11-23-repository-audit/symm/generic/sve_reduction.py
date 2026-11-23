"""Run: python -B -m symm.generic.sve_reduction [--m 4]."""

import argparse
import json
from dataclasses import replace

import sympy as sp

from .core import DifferentialSystem, JetSpace, PointGenerator
from .jets import total_derivative
from .problem import DataCondition, PDEProblem
from .chart_reduction import ReductionChart, reduce_in_chart


def sve_scaling_case(m=3):
    """Printed master equation; beta=m*kappa, kappa=A_g*xi_sed fixed."""
    t,s = sp.symbols("t s",positive=True)
    g,kappa = sp.symbols("g kappa",positive=True)
    phi,F = sp.symbols("phi F")
    sigma,rho = sp.symbols("sigma rho",positive=True)
    m = sp.sympify(m)
    if m.free_symbols:
        raise ValueError("the worked example requires a fixed numeric exponent")
    space = JetSpace((t,s),(phi,),3)
    j = space.jet_symbol
    pt,ps = j(0,(1,0)),j(0,(0,1))
    H = ps*j(0,(2,0))-g*j(0,(0,2))/ps**2
    C = pt**(m-1)*j(0,(1,1))/ps
    equation = total_derivative(space,H,0)-g*m*kappa*total_derivative(space,C,1)
    problem = PDEProblem(DifferentialSystem(space,(equation,),inequations=(ps,),name="printed-lagrangian-SVE"),
                         parameters=(g,kappa),domain=(sp.Gt(t,0,evaluate=False),sp.Gt(s,0,evaluate=False),ps>0,pt>0))
    generator = PointGenerator((t,-2*s),(0,))
    chart = ReductionChart(JetSpace((sigma,),(F,),3),(s*t**2,),rho,t,
                           (rho,sigma/rho**2),(F,),(1/t,))
    return problem,generator,chart,((-1,),)


def sve_data_family_case():
    """Cubic chart with a strictly invariant three-jet data family at sigma=1."""
    problem, generator, chart, multipliers = sve_scaling_case(3)
    t, s = problem.system.jet_space.independent_variables
    phi = problem.system.jet_space.dependent_fields[0]
    g, kappa = problem.parameters
    eta = sp.Symbol("eta_ic", real=True)
    ps = problem.system.jet_space.jet_symbol(0, (0, 1))
    pss = problem.system.jet_space.jet_symbol(0, (0, 2))
    k = (27*g/(1-12*g*kappa))**sp.Rational(1, 3)
    data = DataCondition(
        "sigma-one-three-jet",
        s*t**2-1,
        (phi-k, ps/t**2-k/3, pss/t**4+2*k*(1+eta)/9),
    )
    problem = replace(
        problem,
        parameters=(g, kappa, eta),
        domain=(*problem.domain, sp.Gt(1-12*g*kappa, 0, evaluate=False)),
        data=(data,),
    )
    return problem, generator, chart, multipliers


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m",type=int,default=3)
    args = parser.parse_args(argv)
    problem,generator,chart,matrix = sve_scaling_case(args.m)
    result = reduce_in_chart(problem,generator,chart,symmetry_multipliers=matrix)
    summary = {"model":problem.system.name,"m":args.m,"beta":"m*kappa",
               "source_dimensions":{"p":problem.system.p,"q":problem.system.q,"r":problem.system.r,"order":3},
               "jet_structure":problem.jet_structure,"status":result.certificate.status,
               "checks":dict(result.certificate.checks),"scope":result.certificate.message,
               "data_status":result.data_status}
    if result.reduced_system:
        summary.update(reduced_equations=list(map(str,result.reduced_system.equations)),
                       reduced_dimension=result.reduced_system.jet_space.p,
                       pulled_domain=list(map(str,result.pulled_domain)),
                       regularity_conditions=list(map(str,result.regularity_conditions)),
                       reconstruction="phi(t,s) = F(s*t**2)",
                       identity="E_3[T(F)] = R_0[F](s*t**2)/t")
    else:
        summary["failed_identity_residuals"] = list(map(str,result.certificate.residuals))
    print(json.dumps(summary,indent=2))
    return 0 if result.reduced_system else 2


if __name__ == "__main__":
    raise SystemExit(main())
