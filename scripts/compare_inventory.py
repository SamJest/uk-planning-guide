"""Produce before/after changes and a per-page review backlog without migrations."""
import csv
import json
from pathlib import Path
from inventory import save

ROOT=Path(__file__).resolve().parents[1]

def load(path):
    with path.open() as stream: return {r['url']:r for r in csv.DictReader(stream)}

def main():
    before=load(ROOT/'reports/baseline/pages.csv')
    after=load(ROOT/'reports/after/pages.csv')
    fields=['url','change','before_canonical','after_canonical','before_hash','after_hash']
    changes=[]
    for url in sorted(before.keys()|after.keys()):
        b,a=before.get(url,{}),after.get(url,{})
        if b != a:
            changes.append(dict(url=url,change='added' if not b else 'removed' if not a else 'modified',before_canonical=b.get('canonical'),after_canonical=a.get('canonical'),before_hash=b.get('main_hash'),after_hash=a.get('main_hash')))
    save(ROOT/'reports/url_diff.csv',changes,fields)
    backlog=[]
    for r in after.values():
        backlog.append(dict(from_url=r['url'],to_url=r['canonical'] if r['canonical']!=r['url'] else '',page_family=r['page_type'],intent_key='UNRESOLVED:'+r['url'],current_status='static_file_not_HTTP_verified',current_canonical=r['canonical'],is_in_sitemap=r['in_sitemap'],traffic_clicks='protected_sample' if r['protected']=='1' else 'unknown_not_zero',traffic_impressions='see_gsc_sample',backlinks_known='unknown',distinct_information='not_yet_independently_reviewed',evidence_status=r['evidence_status'],proposed_action=r['disposition'],confidence='low',risk='protected' if r['protected']=='1' else 'unassessed',reason=r['findings'] or 'claim_and_intent_review_required',reviewer='',approved_at='',actual_http_result='NOT_RUN_PROXY_403',implemented_at=''))
    save(ROOT/'reports/review_backlog.csv',backlog,list(backlog[0]))
    print(json.dumps(dict(before=len(before),after=len(after),added=len(after.keys()-before.keys()),removed=len(before.keys()-after.keys()),changed_rows=len(changes)),indent=2))

if __name__=='__main__': main()
