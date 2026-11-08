"""Offline evidence and URL preservation gate for the bounded Wave 1 cohort."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import subprocess
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lxml import html
from utils.content_contracts import load_page_records, render_record_for_path
from utils.source_registry import validate_page_source_links


def check(output):
    policy = json.loads((ROOT / 'data/canary/wave1-corpus.json').read_text(encoding='utf-8'))
    assert len(policy['qa_corpus']) == 20
    assert len(policy['primary_routes']) == 5
    validate_page_source_links()
    # The full clicked sample is protected, including unresolved URL variants.
    sample_path = 'seo-rebuild-pack/data/gsc/search_console_1000_pages_ranked.csv'
    sample = ROOT / sample_path
    baseline = subprocess.check_output(['git', 'cat-file', '--filters', policy['baseline_sha'] + ':' + sample_path], cwd=ROOT)
    assert sample.read_bytes() == baseline, 'The dated traffic sample changed'
    with sample.open(encoding='utf-8-sig', newline='') as stream:
        clicked = [r['URL'] for r in csv.DictReader(stream) if float(r['Clicks']) > 0]
    unresolved = []
    for url in clicked:
        path = unquote(urlsplit(url).path)
        if not path.endswith('/') or not (ROOT / path.strip('/') / 'index.html').is_file():
            unresolved.append(url)
    prior = json.loads((ROOT / 'reports/WAVE_0_EVIDENCE.json').read_text(encoding='utf-8'))
    assert len(clicked) == 975 and sorted(unresolved) == sorted(prior['protected_nonexact_unchanged']), 'Traffic corpus presence changed'
    excluded = {'templates', 'components', 'tests', 'reports', 'artifacts', 'seo-rebuild-pack', 'backend', 'node_modules'}
    changed = subprocess.check_output(['git', 'diff', '--name-only', policy['baseline_sha']], cwd=ROOT, text=True).splitlines()
    changed += subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
    public_changes = [p for p in changed if Path(p).parts[0] not in excluded and
                      (Path(p).suffix in {'.html', '.xml'} or p.startswith('assets/') or p in {'CNAME', 'robots.txt', '.nojekyll'})]
    assert not public_changes, f'Wave 1 may not mutate the public publishing tree: {public_changes}'
    records = {p['route_path']: p for p in load_page_records()}
    for row in policy['qa_corpus']:
        route = row['route_path']
        public = ROOT / row['public_path'].strip('/') / 'index.html'
        assert hashlib.sha256(public.read_bytes().replace(b'\r\n', b'\n')).hexdigest() == row['public_sha256'], f'Public content changed: {route}'
        doc = html.parse(str(public))
        for key, xpath in [('public_canonical', '//link[@rel="canonical"]/@href'),
                           ('public_script_srcs', '//script[@src]/@src'),
                           ('public_form_actions', '//form/@action')]:
            assert doc.xpath(xpath) == row[key], f'Public {key} changed: {route}'
        record = records[route]
        assert record['canonical_path'] == row['canonical_path'], f'Canonical changed: {route}'
        assert record['index_status'] == row['index_status'], f'Indexation changed: {route}'
        candidate = html.parse(str(output / route.strip('/') / 'index.html'))
        assert candidate.xpath('//link[@rel="canonical"]/@href') == ['https://ukplanningguide.co.uk' + row['canonical_path']]
        robots = ' '.join(candidate.xpath('//meta[@name="robots"]/@content')).lower()
        assert ('noindex' in robots) == (row['index_status'] == 'noindex')
        if route in policy['primary_routes']:
            assert record['evidence_version'] == 1
            for claim in record['claims']:
                matches = candidate.xpath('//li[@data-claim-id=$cid]', cid=claim['claim_id'])
                assert matches and all(m.get('data-evidence-status') == claim['evidence_status'] for m in matches)
                assert all(claim['text'] in ' '.join(m.itertext()) for m in matches)
    print('PASS: 5 evidence canaries; 20 public byte/canonical/script/form and candidate indexation contracts; 19 frozen legacy records; 975 clicked URLs (954 exact, 21 unchanged unresolved); no publishing-tree changes.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/phase-0-canary-site')
    check(parser.parse_args().output.resolve())
