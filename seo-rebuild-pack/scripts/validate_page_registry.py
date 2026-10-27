#!/usr/bin/env python3
"""Generator-level URL/intent registry gate. Supply one row per proposed generated route.

This program is designed to be called BEFORE emitting final HTML and sitemap.
It doesn't infer legal intent; generator must construct stable semantic `intent_key`.
"""
import argparse,csv,sys
from collections import defaultdict
from urllib.parse import urlparse

KEEP={'KEEP_ENRICH','KEEP_DISTINCT'}
ALLOWED=KEEP|{'MERGE_REDIRECT','LEGACY_CANONICAL_TEMP','RETIRE_404_410','RESEARCH_BEFORE_DECISION','NONINDEX_UTILITY'}
LOCAL_HINTS=('council_project','hmo_article4','local_article4','local_conservation','local_search')

def run(rows):
    issues=[];byurl=defaultdict(list);intent=defaultdict(list);total=0
    for lineno,r in enumerate(rows,2):
        total+=1
        u=r.get('url','').strip(); key=r.get('intent_key','').strip().lower();d=r.get('disposition','').strip()
        canon=r.get('canonical','').strip()
        idx=r.get('indexable','').strip().lower() in ('1','true','yes')
        sitemap=r.get('in_sitemap','').strip().lower() in ('1','true','yes')
        page_type=r.get('page_type','').strip().lower()
        local_count=r.get('verified_local_source_count','0').strip()
        if not u.startswith('https://') or not urlparse(u).hostname:issues.append(f'line {lineno}: invalid URL')
        if not key:issues.append(f'line {lineno}: missing semantic intent key')
        if d not in ALLOWED:issues.append(f'line {lineno}: invalid disposition {d}')
        byurl[u].append(lineno)
        if d in KEEP and idx:intent[key].append(u)
        if idx and d not in KEEP:issues.append(f'line {lineno}: indexable but disposition {d}')
        if sitemap and (not idx or d not in KEEP or canon!=u):issues.append(f'line {lineno}: sitemap contains noncanonical/nonindexable route')
        if idx and canon!=u:issues.append(f'line {lineno}: kept indexable page is not self-canonical')
        if d in ('MERGE_REDIRECT','RETIRE_404_410') and sitemap:issues.append(f'line {lineno}: retired URL emitted into sitemap')
        if d in KEEP and idx and page_type in LOCAL_HINTS:
            try: verified=int(local_count)
            except ValueError: verified=-1
            if verified < 1 and r.get('approved_distinct_utility','').strip().lower() not in ('1','true','yes'):
                issues.append(f'line {lineno}: local page lacks verified distinguishing evidence (research or consolidate); exception needs explicit approval')
    for u,ls in byurl.items():
        if len(ls)>1:issues.append(f'URL generated more than once {u} at lines {ls}')
    for k,urls in intent.items():
        if len(urls)>1:issues.append(f'new duplicate intent {k}: {urls[:8]}')
    return issues,{'routes':total,'distinct_kept_indexable_intents':len(intent),'duplicate_intent_groups':sum(len(x)>1 for x in intent.values())}

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);x=p.parse_args()
    with open(x.input,encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    errors,summary=run(rows)
    print(summary)
    for e in errors:print('FAIL:',e)
    if errors:sys.exit(1)
    print('PASS: unique new canonical intent routes. Registry field accuracy requires independent editorial review.')
if __name__=='__main__':main()
