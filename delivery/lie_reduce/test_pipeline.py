import unittest
import sympy as sp
from .models import scalar,euler
from .reduce import reduce
from .strata import rank_locus
from .algebra import add
from .task import to_task


class PipelineTests(unittest.TestCase):
    def test_unrelated_heat_equation(self):
        from .jets import JetSpace
        from .spec import PDESpec
        from .determining import symmetries
        from .run import span_equal
        t,x,u=sp.symbols('t x u')
        j=JetSpace((t,x),(u,),2)
        spec=PDESpec('heat',j,(j.jet(0,1,0)-j.jet(0,0,2),),(j.jet(0,1,0),))
        result=symmetries(spec,2)
        solution=(sp.S.Zero,sp.S.Zero,x**2+2*t)
        self.assertTrue(span_equal(result['basis'],result['basis']+[solution],(t,x,u)))

    def test_adjoint_and_annular(self):
        from .algebra import adjoint_matrix
        from .annular import derive
        spec,b=scalar('P',3);e=sp.Symbol('epsilon',real=True)
        basis=list(b.values());A=adjoint_matrix(b['Y4'],basis,spec.jets.independent+spec.jets.dependent,e)
        self.assertEqual(A,sp.diag(sp.exp(-e),sp.exp(-e),sp.exp(-e),1,1))
        result=derive()
        self.assertEqual(result['flux_identity_remainders'],(0,0,0))
        self.assertEqual(result['reduction'].checks['base_orbit_rank'],2)

    def test_prolongation_independent_frozen(self):
        from .frozen import reproduce_sve2026 as old
        for model in ('P','M'):
            spec,_=scalar(model,3);j=spec.jets
            mapping={v:old.JETS[index] for (a,index),v in j.jets.items()}
            mapping.update(dict(zip(j.independent,(old.t,old.s))))
            field=(j.independent[0]*j.dependent[0], j.independent[1]**2, j.dependent[0]**2+j.independent[0]*j.independent[1])
            mapped=tuple(v.xreplace(mapping) for v in field)
            new=j.prolong(field); expected=old.prolongation(*mapped)
            for (a,index),value in new.items():
                self.assertEqual(sp.expand(value.xreplace(mapping)-expected[index]),0)
            eq=spec.equations[0].xreplace(mapping)
            self.assertEqual(sp.expand(j.act(spec.equations[0],field).xreplace(mapping)-old.act(eq,*mapped)),0)

    def test_table32_against_independent_pullbacks(self):
        from .frozen import reproduce_sve2026 as old
        F,P,C,H,z,g,kappa=old.F,old.P,old.C,old.H,old.z,old.g,old.kappa
        rows={}
        gamma,c=sp.symbols('gamma c',real=True);t,s=old.t,old.s;fun=sp.Function('F')
        for model in ('P','M'):
            for m in (2,3):
                equation=old.master(m)
                if model=='M':equation-=old.total(old.p*(old.q*old.a-g*old.c/old.q**2)/old.q,1)
                for kind,graph,section,weight in (
                    ('common',t*fun(s/t),{s:z*t},t**2),
                    ('tilted',gamma*t+fun(s-c*t),{s:z+c*t},1),
                    ('affine',gamma*s+fun(t),{t:z},1),
                    ('cubic',fun(s*t**2),{s:z/t**2},t)):
                    if kind=='cubic' and m!=3:continue
                    mapping={v:sp.diff(graph,t,i,s,j).subs(section).doit().xreplace(
                        {sp.diff(fun(z),z,n):v for n,v in enumerate((F,P,C,H))}) for (i,j),v in old.JETS.items()}
                    rows[f'{model}_{kind}_m{m}']={'residual':str(sp.factor(weight*equation.xreplace(mapping)))}
        env=dict(F=F,P=P,C=C,H=H,z=z,g=g,kappa=kappa,c=sp.Symbol('c',real=True),gamma=sp.Symbol('gamma',real=True))
        for model in ('P','M'):
            for m in (2,3):
                spec,b=scalar(model,m);c,gamma=env['c'],env['gamma']
                cases={'common':b['Y4'],'tilted':add((1,b['Y1']),(c,b['Y3']),(gamma,b['Y2'])),
                       'affine':add((1,b['Y3']),(gamma,b['Y2']))}
                if m==3:cases['cubic']=b['Y5']
                for kind,X in cases.items():
                    key=f'{model}_{kind}_m{m}'
                    if key not in rows:continue
                    red=reduce(spec,X);self.assertEqual(red.status,'verified',red.reason)
                    fun=red.graph.profiles[0];zz=red.graph.z
                    new=red.equations[0].xreplace({sp.diff(fun,zz,n):v for n,v in enumerate((F,P,C,H))}).subs(zz,z)
                    old=sp.sympify(rows[key]['residual'],locals=env)
                    self.assertEqual(sp.cancel(new-old),0,key)
                    if model=='M' and kind in ('common','tilted'):
                        self.assertEqual(red.first_integrals[0]['status'],'verified')

    def test_multi_parameter_rank_intersection(self):
        a,b=sp.symbols('a b')
        result=rank_locus(sp.Matrix([[a,b]]),(a,b))
        self.assertEqual(set(result['generators']),{a,b})

    def test_vector_cubic_simple_wave(self):
        spec,b=euler(3);red=reduce(spec,b['X5']);self.assertEqual(red.status,'verified')
        z=red.graph.z;g,k=sp.symbols('g kappa',positive=True)
        U=2*z/3;H=(1-4*g*k)*z**2/(9*g);B=4*k*z**2/9
        mapping=dict(zip(red.graph.profiles,(H,U,B)))
        self.assertTrue(all(sp.simplify(eq.subs(mapping).doit())==0 for eq in red.equations))

    def test_invalid_generator_and_task(self):
        spec,b=scalar('M',2)
        self.assertEqual(reduce(spec,b['Y2']).status,'no invariant graph')
        self.assertEqual(reduce(spec,(0,0,spec.jets.independent[0])).status,'no invariant graph')
        red=reduce(spec,b['Y4'])
        with self.assertRaises(ValueError):to_task(red,(1,0,0),(0,1))
        task=to_task(red,(1,1,0),(0,sp.Rational(1,64)))
        self.assertEqual(task['status'],'local_regular_task')


if __name__=='__main__':unittest.main()
