import json
from pathlib import Path


def test_report_contains_required_keys_and_does_not_promote_unknown_claims():
    import tempfile
    from main import write_report
    from main import REQUIRED_KEYS
    evidence={'models':{'master':'E=0','checks':{'mass':True}},
              'symmetries':{'classification_status':'unresolved'},
              'algebra':{},'reductions':{},'numerics':{'status':'not_run'},
              'source_manifest':{'equations':[]},'run':{'complete_audit':False}}
    with tempfile.TemporaryDirectory(prefix='sve-report-test-') as directory:
        tmp_path=Path(directory)
        write_report(evidence,tmp_path)
        report=(tmp_path/'REPORT.md').read_text(encoding='utf-8')
        assert all(key in report for key in REQUIRED_KEYS)
        assert 'unresolved' in report
        assert 'not_run' in report
        stored=json.loads((tmp_path/'evidence.json').read_text(encoding='utf-8'))
        assert stored['run']['complete_audit'] is False
