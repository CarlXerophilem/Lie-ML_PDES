import numpy as np
import sympy as sp
import torch

from symm.generic.pipeline_certificates import exact_certificates
from symm.solvers.benchmark import original_scaled_residual, diagnostics
from symm.solvers.hybrid_profile import HardProfile
from symm.solvers.loss_measures import parameter_directional_loss, profile_jets, quotient_loss
from symm.solvers.problems import ProfileProblem


def test_exact_certificates_and_cubic_constraint():
    data=exact_certificates()
    assert data['cubic_anchor']['constraint_substitution_remainder']=='0'
    assert all(v=='0' for v in data['coupled_corrected']['checks'].values())
    assert data['coupled_corrected']['maximal_classification'] is False
    assert [r['invariant'] for r in data['boundary_controls']]==[True,False,False]


def test_independent_original_residual_and_measures_on_non_solution():
    z=np.linspace(1,1.5,1001)
    f=2+.5*(z-1)+.05*(z-1)**2+.02*(z-1)**3
    jets=np.array((f,.5+.1*(z-1)+.06*(z-1)**2,.1+.12*(z-1),np.full_like(z,.12)))
    for chart in ('cubic_X5','common_printed','common_corrected'):
        problem=ProfileProblem(chart)
        original=original_scaled_residual(problem,z,jets)
        reduced=problem.residual(z,*jets)
        assert np.max(np.abs(original-reduced)) < 1e-12
        metrics=diagnostics(problem,z,jets,jets)
        assert metrics['measure_pullback_difference'] < 1e-12


def test_parameter_gradient_through_exact_differential_linearization():
    model=HardProfile(ProfileProblem('common_printed'))
    z=torch.linspace(1,1.5,17,dtype=torch.float64,requires_grad=True)
    weights=torch.full_like(z,.5/17)
    parameters=tuple(model.parameters())
    directions=tuple(torch.full_like(p,.01) for p in parameters)
    chain=parameter_directional_loss(model,z,weights,directions)
    loss=quotient_loss(model.problem,z,profile_jets(model(z),z),weights)
    gradients=torch.autograd.grad(loss,parameters)
    direct=sum((g*d).sum() for g,d in zip(gradients,directions))
    assert torch.allclose(chain,direct,atol=1e-11,rtol=1e-9)
