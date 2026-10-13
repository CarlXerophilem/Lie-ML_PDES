import sympy as sp


def test_physical_pullback_and_printed_compatibility_are_distinct():
    from main import build_model_report
    r=build_model_report()
    assert r['checks']['mass_pullback_zero']
    assert r['checks']['printed_compatibility_zero']
    assert r['checks']['physical_compatibility_zero']
    assert not r['physical_equals_printed']


def test_source_inventory_has_every_number_and_required_key():
    from main import equation_inventory, REQUIRED_KEYS
    rows=equation_inventory()
    assert [r['equation'] for r in rows]==list(range(1,35))
    assert len(REQUIRED_KEYS)==10
    assert REQUIRED_KEYS[-1]=='[Numeric solutions to the ODEs]'


def test_final_coverage_retains_refuted_and_missing_claims():
    from main import build_coverage
    evidence={'reductions':{'source_witnesses':{
        'eq25':{'status':'refuted_as_printed','source':'p.7 eq25','witness':'437/25'}}}}
    r=build_coverage(evidence)
    assert len(r['equations'])==34
    assert r['equations'][24]['status']=='refuted_as_printed'
    assert r['equations'][23]['status']=='unresolved'
    assert r['inventory_complete'] is True
    assert r['all_printed_claims_reproduced'] is False
