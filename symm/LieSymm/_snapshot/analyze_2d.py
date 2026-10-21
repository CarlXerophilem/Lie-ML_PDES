"""Numbered 2D general-symm frontend, retaining the correct mixed-order shell.

The frozen 1D engine supplies jets and prolongation.  This frontend does not
differentiate a second-order Exner equation inside J^2: B_tx, B_ty and B_tt
remain free.  The three first-order water equations contribute nine first
differential consequences.  Integration is a separate reviewed operation.
"""
import time
import os
import sys
import sympy as sp
from main import (JetSpace, arbitrary_generator, characteristic,
                  prolongation_coefficients, point_action)


class MixedShell:
    def __init__(self, space, equations):
        self.space=space
        self.equations=tuple(equations)
        self.order=space.order(equations)
        if len(space.x)!=3 or len(space.u)!=4 or len(equations)!=4:
            raise ValueError('Mixed shell requires three coordinates and four equations/fields')
        if self.order not in (1,2) or any(space.order((row,))!=1 for row in equations[:3]):
            raise ValueError('Unsupported mixed orders: water rows must have order one, bed order at most two')
        leaders=[space.jet(a,space.unit(0)) for a in range(4)]
        matrix,rhs=sp.linear_eq_to_matrix(equations,leaders)
        determinant=sp.factor(matrix.det())
        if determinant==0:
            raise ValueError('Time matrix is singular; a separate chart is required')
        self.divisors=[determinant]
        self.rhs=tuple(matrix.inv()*rhs)
        if any(value.has(*leaders) for value in self.rhs):
            raise ValueError('Unresolved leading time derivatives')
        self.rules=dict(zip(leaders,self.rhs))
        if self.order==2:
            # Spatial water consequences first, then their time consequences.
            for axis in (1,2,0):
                for a in range(3):
                    index=tuple(int(i==0)+int(i==axis) for i in range(3))
                    self.rules[space.jet(a,index)]=sp.expand(space.D(self.rhs[a],axis).xreplace(self.rules))
        self.rules_used={str(key):value for key,value in self.rules.items()}

    def reduce(self, expression):
        return sp.expand(expression.xreplace(self.rules))


def split_free_jets(space, expression, shell):
    # The determining identity is polynomial in free jets already. Global
    # common-denominator expansion needlessly multiplies symbolic radial powers.
    # Keep exact field/parameter expressions as coefficients of that polynomial.
    jets=sorted((symbol for symbol in expression.free_symbols & space.reverse.keys()
                 if any(space.reverse[symbol][1]) and symbol not in shell.rules),key=str)
    polynomial=sp.Poly(expression,*jets,domain='EX') if jets else None
    terms=polynomial.terms() if polynomial is not None else [((),expression)]
    records=[{'powers':powers,'coefficient':sp.factor_terms(coefficient)}
             for powers,coefficient in terms if coefficient!=0]
    return {'status':'complete_jet_split','jets':jets,'terms':records,
            'equations':list(dict.fromkeys(item['coefficient'] for item in records)),
            'denominator':sp.S.One,
            'coefficient_denominators':list(dict.fromkeys(
                sp.denom(term) for row in records for term in sp.Add.make_args(sp.expand(row['coefficient']))
                if sp.denom(term)!=1)),
            'denominator_note':'No common multiplier or parameter division; coefficients retained on the original regular chart'}


def analyze(independent_variables,dependent_fields,equations,parameters,
            branch_conditions,data_case=None):
    started=time.perf_counter()
    timings={}
    last=started
    def mark(label):
        nonlocal last
        now=time.perf_counter()
        timings[label]=now-last
        last=now
        if os.environ.get('SVE_PROFILE')=='1':
            print('PROFILE',label,round(timings[label],3),'seconds',file=sys.stderr,flush=True)
    J=JetSpace(independent_variables,dependent_fields)
    if len(J.x)!=3 or len(J.u)!=4:
        raise ValueError('This frontend is for three coordinates and four fields')
    equations=tuple(sp.expand(sp.sympify(e).subs(branch_conditions.get('substitutions',{}),simultaneous=True))
                    for e in equations)
    xi,eta=arbitrary_generator(J)
    mark('model_and_arbitrary_generator')
    shell=MixedShell(J,equations)
    mark('mixed_shell')
    coefficients=prolongation_coefficients(J,xi,eta,shell.order)
    mark('prolongation_coefficients')
    actions=[point_action(J,e,xi,eta,shell.order,coefficients=coefficients) for e in equations]
    mark('point_actions')
    restricted=[shell.reduce(e) for e in actions]
    mark('shell_restriction')
    splits=[]
    for index,equation in enumerate(restricted):
        splits.append(split_free_jets(J,equation,shell))
        mark('free_jet_split_'+str(index))
    report={'model_id':branch_conditions.get('model_id','user_system'),
            'coordinates':J.x,'fields':J.u,'parameters':parameters,
            'branch_conditions':branch_conditions,'equations':equations,'order':shell.order,
            'arbitrary_generator':{'xi':xi,'eta':eta},'characteristic':characteristic(J,xi,eta),
            'prolonged_equations':actions,'on_shell_equations':restricted,
            'determining_splits':splits,
            'determining_equations':list(dict.fromkeys(e for split in splits for e in split['equations'])),
            'normal_form_rhs':shell.rhs,'normal_form_divisors':shell.divisors,
            'differential_consequences':shell.rules_used,'shell_constraint_count':len(shell.rules),
            'shell_note':'J2: differentiate only water rows; keep B_tx,B_ty,B_tt free' if shell.order==2 else 'J1 evolution shell',
            'data_case':data_case,'data_status':'not_run','reduction_status':'not_run',
            'subalgebra_classification':'not_run','generator_verification':'not_run'}
    from classification_2d import integrate_sve_2d
    report['integration']=integrate_sve_2d(report)
    mark('integrate_and_verify')
    report['classification_status']=report['integration']['status']
    if 'candidate_checks' in report['integration']:
        report['generator_verification']='verified'
    report['elapsed_seconds']=time.perf_counter()-started
    report['phase_seconds']=timings
    return report
