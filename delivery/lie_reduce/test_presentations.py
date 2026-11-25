"""Negative controls for equation multiplicity and vertical fixed graphs."""
import unittest
import sympy as sp
from .jets import JetSpace
from .spec import PDESpec
from .presentation import square_free_presentation
from .fixed import vertical_fixed_graphs
from .determining import symmetries
from .run import span_equal


class PresentationTests(unittest.TestCase):
    def setUp(self):
        self.t,self.x,self.u=sp.symbols('t x u',real=True)
        self.j=JetSpace((self.t,self.x),(self.u,),1)
        self.ut=self.j.jet(0,1,0);self.ux=self.j.jet(0,0,1)

    def spec(self,eq,**kwargs):return PDESpec('test',self.j,(eq,),(self.ut,),**kwargs)

    def test_repeated_root_explicitly_normalized(self):
        original=self.spec(self.ut**2)
        with self.assertRaises(ValueError):original.shell()
        certificate=square_free_presentation(original)
        normalized=certificate['normalized_spec']
        self.assertEqual(normalized.equations,(self.ut,))
        self.assertEqual(original.equations,(self.ut**2,))
        left=symmetries(normalized,1)['basis'];right=symmetries(self.spec(self.ut),1)['basis']
        self.assertTrue(span_equal(left,right,self.j.independent+self.j.dependent))

    def test_union_is_not_silently_discarded(self):
        record=square_free_presentation(self.spec(self.ut**2*self.ux**3))
        self.assertEqual(len(record['components']),2)
        self.assertEqual(set(c['spec'].equations[0] for c in record['components']),{self.ut,self.ux})
        statuses=[c['principal_chart']['status'] for c in record['components']]
        self.assertIn('unavailable',statuses)  # ux=0 is not a solved ut chart.
        self.assertEqual(sp.expand(record['normalized_spec'].equations[0]),self.ut*self.ux)

    def test_denominator_and_parameter_loci_preserved(self):
        a=sp.Symbol('a',real=True)
        record=square_free_presentation(self.spec(a*self.ut**2/self.u))
        self.assertIn(self.u,record['domain_exclusions'])
        self.assertEqual(len(record['components']),2) # a=0 may not be thrown away.
        record=square_free_presentation(self.spec(a*self.ut**2/self.u,positive=(a,self.u)))
        self.assertEqual(record['normalized_spec'].equations,(self.ut,))
        self.assertIn(self.u,record['normalized_spec'].domain_exclusions)
        invalid=self.spec(self.ut,domain_exclusions=(self.ut,))
        with self.assertRaisesRegex(ValueError,'excluded'):invalid.shell()

    def test_not_a_real_radical_or_branch_selector(self):
        record=square_free_presentation(self.spec(self.ut**2+self.ux**2))
        self.assertEqual(record['normalized_spec'].equations,(self.ut**2+self.ux**2,))
        self.assertEqual(record['components'][0]['principal_chart']['status'],'unavailable')
        capped=square_free_presentation(self.spec(self.ut*self.ux),max_components=1)
        self.assertEqual(capped['component_enumeration'],'not_computed')

    def test_fixed_solution_and_positive_chart_exclusion(self):
        r=vertical_fixed_graphs(self.spec(self.ut),(0,0,self.u))
        self.assertEqual(r['branches'][0]['status'],'verified_fixed_solution')
        self.assertFalse(r['is_ODE_reduction'])
        p=vertical_fixed_graphs(self.spec(self.ut,positive=(self.u,)),(0,0,self.u))
        self.assertEqual(p['status'],'no invariant graph')
        self.assertEqual(vertical_fixed_graphs(self.spec(self.ut),(0,0,1))['status'],'no invariant graph')

    def test_nonsymmetry_is_not_promoted(self):
        r=vertical_fixed_graphs(self.spec(self.ut-1),(0,0,self.u))
        self.assertEqual(r['status'],'rejected')

    def test_two_fixed_branches_and_partial_fixed_pde(self):
        r=vertical_fixed_graphs(self.spec(self.ut),(0,0,self.u*(self.u-1)))
        self.assertEqual(len(r['branches']),2)
        self.assertTrue(all(v['status']=='verified_fixed_solution' for v in r['branches']))
        v=sp.Symbol('v',real=True);j=JetSpace((self.t,self.x),(self.u,v),1)
        spec=PDESpec('vector',j,(j.jet(0,1,0),j.jet(1,1,0)),(j.jet(0,1,0),j.jet(1,1,0)))
        result=vertical_fixed_graphs(spec,(0,0,self.u,0))
        self.assertEqual(result['branches'][0]['status'],'constrained_PDE')
        self.assertEqual(result['independent_variables_remaining'],2)

    def test_parameter_degeneracy_is_not_silently_empty(self):
        a=sp.Symbol('a',real=True)
        r=vertical_fixed_graphs(self.spec(self.ut),(0,0,a))
        self.assertEqual(r['status'],'undetermined')
        self.assertEqual(vertical_fixed_graphs(self.spec(self.ut),(0,0,self.t))['status'],'rejected')


if __name__=='__main__':unittest.main()
