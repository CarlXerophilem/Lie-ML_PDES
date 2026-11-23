"""Declared 1D model cells. A cell can carry a continuous parameter modulus."""
import sympy as sp
from main import JetSpace

t, x = sp.symbols('t x', real=True)
h, u = sp.symbols('h u', positive=True)
B = sp.Symbol('B', real=True)
g = sp.Symbol('g', positive=True)
K, G = sp.symbols('K G', nonnegative=True)
m, n = sp.symbols('m n', real=True)

BRANCHES = {
    'grass_generic': {'K': True, 'G': False, 'm': m, 'n': None,
                     'guards': ['K>0', '1<=m<=4', 'm!=3']},
    'grass_cubic': {'K': True, 'G': False, 'm': 3, 'n': None, 'guards': ['K>0']},
    'slope_attachment_generic': {'K': True, 'G': True, 'm': m, 'n': m-1,
                               'guards': ['K>0', 'G>0', '1<=m<=4', 'm!=3']},
    'slope_attachment_cubic': {'K': True, 'G': True, 'm': 3, 'n': 2,
                             'guards': ['K>0', 'G>0']},
    'slope_source_generic': {'K': True, 'G': True, 'm': m, 'n': m,
                           'guards': ['K>0', 'G>0', '1<=m<=4', 'm!=3']},
    'slope_source_cubic': {'K': True, 'G': True, 'm': 3, 'n': 3,
                         'guards': ['K>0', 'G>0']},
    'slope_only': {'K': False, 'G': True, 'm': None, 'n': n,
                  'guards': ['G>0', '0<=n<=4']},
    'zero_transport': {'K': False, 'G': False, 'm': None, 'n': None, 'guards': []},
}


def branch_model(name):
    cell = BRANCHES[name]
    jets = JetSpace((t, x), (h, u, B))
    ht, ut, Bt = (jets.jet(i, (1, 0)) for i in range(3))
    hx, ux, Bx = (jets.jet(i, (0, 1)) for i in range(3))
    transport = K * u ** cell['m'] if cell['K'] else sp.S.Zero
    if cell['G']:
        transport -= G * u ** cell['n'] * Bx
    equations = (ht + u*hx + h*ux, ut + u*ux + g*(hx+Bx), Bt + jets.D(transport, 1))
    parameters = (g,) + ((K,) if cell['K'] else ()) + ((G,) if cell['G'] else ())
    parameters += tuple(sorted(set().union(*(e.free_symbols for e in equations)) & {m, n}, key=str))
    return dict(independent_variables=(t, x), dependent_fields=(h, u, B),
                equations=equations, parameters=parameters,
                branch_conditions={'model_id': name, 'guards': ['h>0', 'u>0', 'g>0'] + cell['guards'],
                                   'substitutions': {}, 'registry_status': 'awaiting_necessity_review'},
                data_case=None)
