"""Offline dossier, emission and migration-safety gate; does not crawl or publish."""
import csv
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from utils.content_contracts import load_page_records
from utils.intent_registry import review_registry
from utils.url_review import validate_normalization, validate_review_only
from utils.url_registry import url_registry
from utils.sitemap_integrity import validate_targets


def check():
    folder=ROOT/'reports/wave-2'
    def read(name): return json.loads((folder/name).read_text(encoding='utf-8'))
    assert read('intent-registry.json') == review_registry(load_page_records()), 'Intent export is stale'
    expected=json.loads((ROOT/'reports/WAVE_0_EVIDENCE.json').read_text(encoding='utf-8'))['protected_nonexact_unchanged']
    cards=read('protected-url-decisions.json')
    assert [c['url'] for c in cards] == expected and len(cards)==21
    with (ROOT/'seo-rebuild-pack/data/gsc/search_console_1000_pages_ranked.csv').open(encoding='utf-8-sig') as stream:
        sample={r['URL']:r for r in csv.DictReader(stream)}
    pages=list(cards)
    for card in cards:
        validate_normalization(card)
        assert card['sample_metrics']=={'clicks':float(sample[card['url']]['Clicks']),'impressions':float(sample[card['url']]['Impressions'])}
    pairs=read('overlap-decisions.json')
    assert len(pairs)==6
    for card in pairs:
        validate_review_only(card)
        assert card['cohort_6_12_months']=='unknown' and card['rollback_map']['to_url'] is None
        pages.extend([card['source'],card['target']])
    for page in pages:
        disk=ROOT/urlsplit(page['normalized_static_url']).path.strip('/')/'index.html'
        assert disk.is_file() and hashlib.sha256(disk.read_bytes().replace(b'\r\n',b'\n')).hexdigest()==page['static_lf_sha256'], 'Reviewed public page changed'
    bridge=url_registry()['/councils/colchester/']
    assert bridge['delivery_mode']=='legacy_200_bridge' and bridge['planned_status_code']==301
    output=ROOT/'artifacts/phase-0-canary-site'
    import xml.etree.ElementTree as ET
    urls=[]
    for shard in sorted((output/'sitemaps').glob('*.xml')):
        urls.extend((n.text or '').strip() for n in ET.parse(shard).findall('.//{*}url/{*}loc'))
    validate_targets(urls,output,'https://ukplanningguide.co.uk')
    print(f'PASS: 24 typed records; 21 historical HTTP normalization observations; 6 review-only pairs; {len(urls)} emitted sitemap targets; no migration authorized.')


if __name__=='__main__':check()
