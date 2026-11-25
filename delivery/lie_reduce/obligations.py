"""43 proof obligations: evidence is not promoted to a global completeness claim."""
TITLES=[
'Equation class and parameter domain','Smoothness / analytic branch','Regular equation submanifold',
'Explicit principal chart','Local solvability / differential compatibility','Equivalent equation presentations',
'Declared coefficient class','Free-jet splitting and exclusions','Complete determining-system solution',
'All parameter strata','Full prolongation sufficiency','Point-symmetry scope',
'Lie closure and Jacobi','Connected adjoint action','Optimal-system coverage and inequivalence',
'Chart-preserving equivalence','Projectability','Constant orbit/base rank','Transverse section',
'Independent complete local invariants','Invariant-surface identities','Bidirectional residual equivalence',
'Reduced differential-algebraic compatibility','First-integral identities','Inherited normalizer symmetries',
'Classification of leading-coefficient zeros','Compatible critical point','Holomorphic desingularization',
'BB normal form','All-order nonresonance','Hyperbolic saddle with nonvertical directions',
'Explicit complex contraction disk','Laurent balance, recurrence and convergence','Regular Picard bounds',
'Invertible physical lift','Closed bed one-form and periods','All original physical balances',
'Physical admissibility','Invariant initial/boundary data','Exact arithmetic','Decidable identity checks',
'Explicit failures','Manuscript and source regressions']


def ledger(report):
    rows=[{'id':i,'condition':title,'status':'not_checked','evidence':[],
           'reason':'No machine evidence in this run establishes the full condition.'}
          for i,title in enumerate(TITLES,1)]
    def setrow(i,status,evidence,reason):
        rows[i-1].update(status=status,evidence=evidence,reason=reason)
    setrow(1,'declared',['models.py','runs[*].principal_chart'],'Model dimensions, orders and chart inequalities are explicit; parameter ranges are scoped.')
    setrow(2,'conditional',['models.py'],'Fixed integer exponents yield rational analytic PDEs where denominators are nonzero; no arbitrary smooth input theorem is automated.')
    setrow(3,'partial',['runs[*].principal_chart'],'Principal Jacobian is checked on shell; unresolved nonvanishing conditions remain explicit.')
    setrow(4,'partial',['runs[*].principal_chart'],'A unique simple principal branch is checked; this is not a PDE existence theorem.')
    setrow(5,'not_checked',[],'No general involutive completion or analytic Cauchy theorem hypotheses checker.')
    setrow(6,'partial',['source_formula_audit','presentation_and_fixed_graph_checks'],'P and M remain separate. Explicit square-free rational-presentation equivalence is checked, including all retained factors and original denominator exclusions; no arbitrary elimination claim.')
    setrow(7,'scoped',['runs[*].discovery'],'Degree-two point coefficient search; unrestricted claims rely on separate proofs.')
    setrow(8,'conditional',['runs[*].discovery','runs[*].principal_chart'],'Algebraic splitting on a regular principal chart; full formal integrability is not established.')
    setrow(9,'scoped',['runs[*].discovery','frozen_PM'],'Exact finite ansatz kernel and frozen P/M proof replay; no general Janet solver.')
    setrow(10,'partial',['coverage'],'m=1,2,3,4 replayed; frozen all-real-m proof is separate; no multivariate CAD stratification.')
    sufficient=all(v['discovery']['status']=='completed' and v['discovery']['value'].get('full_prolongation_verified') for v in report['runs'])
    setrow(11,'machine_checked' if sufficient else 'failed',['runs[*].discovery'],'Every computed finite-class generator is substituted into the full prolongation.')
    setrow(12,'declared',['scope'],'Point symmetries only; contact, generalized and nonclassical symmetries excluded.')
    algebra=all(v['algebra']['status']=='completed' for v in report['runs'])
    setrow(13,'machine_checked' if algebra else 'failed',['runs[*].algebra'],'Closure and Jacobi checked at each instantiated stratum.')
    setrow(14,'partial',['algebra.py','test_pipeline.py'],'Adjoint matrix construction and scaling regression; no discrete group classification.')
    setrow(15,'source_proof_only',['draft/dissertation_wku_compact.tex Appendix B'],'Catalogue input is not an automatic optimality proof; E2 two-dimensional system absent.')
    for i,reason in [(16,'Individual graph conditions are retained; conjugacy is not assumed to preserve the chart.'),
                     (17,'Rank-one projectability is tested; explicit polar E2 action is supplied.'),
                     (18,'Ranks require nonzero section minors; unresolved conditions restrict the local chart.'),
                     (19,'Section inverse and transverse determinant checked; no global single-intersection claim.'),
                     (20,'Local section recovers arbitrary profile data; no global invariant-coordinate theorem.'),
                     (22,'Identity and nonzero-weight evidence are separate; conditional factors are not universal equivalence.')]:
        setrow(i,'conditional',['runs[*].reductions[*].value.checks'],reason)
    setrow(21,'scoped',['runs[*].reductions','E2'],'Passing reductions satisfy vector invariant-surface identities; exclusions are retained.')
    setrow(23,'partial',['E2'],'Three exact annular first integrals checked; no arbitrary DAE completion.')
    setrow(24,'scoped',['runs[*].reductions[*].value.first_integrals','E2'],'Constructed fluxes must differentiate to the residual; not every equation has an integral.')
    critical=report.get('critical_certificate',{})
    passed=critical.get('status')=='completed'
    for i in (27,28,29,30,31,32):
        setrow(i,'scoped_machine_checked' if passed else 'failed',['critical_certificate'],
               'Only the c=-7 annular saddle, with two computed slopes; not a classification of all singularities.')
    setrow(35,'conditional',['models.py','task_exports'],'Material invertibility requires phi_s>0; polar chart requires r>0; no global inverse proof.')
    setrow(36,'source_proof_only',['draft/dissertation_wku_compact.tex'],'Local bed reconstruction theorem not a global period computation.')
    setrow(37,'partial',['E2','source_formula_audit'],'Four E2 quotient balances and source pullbacks checked; no claim of five balances for E1/E2.')
    setrow(38,'partial',['runs[*].reductions','critical_certificate'],'Positive-chart conditions and saddle disk guards; no added bed-thickness or Froude assumptions.')
    setrow(39,'not_applicable',[],'No user-prescribed physical initial/boundary value problem is solved in this stage.')
    setrow(40,'scoped_machine_checked',['identities.py','critical_certificate'],'Exact symbolic/rational proof paths; floating quantities in timings/diagnostics are not proofs.')
    setrow(41,'partial',['identities.py'],'Conservative rational/algebraic normal forms and unknown status; legacy graph simplification remains chart-conditioned.')
    setrow(42,'machine_checked',['runs'],'Timed stages retain explicit failure/unknown conditions; no inference of completeness from successful execution.')
    setrow(43,'partial',['frozen_PM','source_formula_audit','tests.log'],'Finite-stratum/table regressions and exact source witnesses; not an independent reproof of all manuscript theorems.')
    return {'conditions':rows,'complete':False,
            'claim':'Checked local symbolic reductions within declared charts and a finite point-coefficient search; a separate explicit certificate for the selected annular saddle.',
            'global_invariant_solution_enumeration':False,
            'reason':'Neither all parameter strata, optimality, global chart coverage nor all ODE solution germs have been machine established.'}


def write_ledger(record,out):
    lines=['# Evidence for the 43 proof obligations','',record['claim'],'',
           '**No global completeness claim.** A successfully executed check is not an independently verified theorem hypothesis outside its stated scope.','',
           '| # | Condition | Status | Evidence / limit |','|---|---|---|---|']
    for row in record['conditions']:
        lines.append(f"| {row['id']} | {row['condition']} | {row['status']} | {row['reason']} Evidence: {', '.join(row['evidence']) or 'none'} |")
    (out/'OBLIGATIONS.md').write_text('\n'.join(lines)+'\n')
