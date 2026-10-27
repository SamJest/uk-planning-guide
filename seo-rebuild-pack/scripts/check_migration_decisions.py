#!/usr/bin/env python3
"""Validate duplicate dispositions before migration; requires reviewer for risky changes."""
import argparse,csv,sys
from urllib.parse import urlparse
ACTIONS={'KEEP_ENRICH','KEEP_DISTINCT','MERGE_REDIRECT','LEGACY_CANONICAL_TEMP','RETIRE_404_410','RESEARCH_BEFORE_DECISION','NONINDEX_UTILITY'}
DANGEROUS={'MERGE_REDIRECT','LEGACY_CANONICAL_TEMP','RETIRE_404_410'}

def check(rows):
    errors=[];sources=set();map_to={}
    for i,r in enumerate(rows,2):
        src=r.get('from_url','').strip();dest=r.get('to_url','').strip();action=r.get('proposed_action','')
        if not src.startswith('https://'):errors.append(f'line {i}: invalid from_url')
        if src in sources:errors.append(f'line {i}: duplicate source url')
        sources.add(src)
        if action not in ACTIONS:errors.append(f'line {i}: unknown action {action}')
        if action in {'MERGE_REDIRECT','LEGACY_CANONICAL_TEMP'}:
            if not dest.startswith('https://') or dest==src:errors.append(f'line {i}: invalid destination')
            if dest and urlparse(dest).hostname!=urlparse(src).hostname:errors.append(f'line {i}: cross-domain target needs independent approval')
            map_to[src]=dest
        if action in DANGEROUS:
            if r.get('reviewer','').strip() in ('','UNREVIEWED') or not r.get('approved_at','').strip():errors.append(f'line {i}: destructive change not approved')
            if not r.get('reason','').strip():errors.append(f'line {i}: missing decision reason')
            if r.get('traffic_clicks','') in ('','UNKNOWN') or r.get('backlinks_known','') in ('','UNKNOWN'):errors.append(f'line {i}: traffic/backlinks unassessed')
    for src in map_to:
        seen=set();cur=src
        while cur in map_to:
            if cur in seen:errors.append(f'loop detected beginning at {src}');break
            seen.add(cur);cur=map_to[cur]
        if len(seen)>1:errors.append(f'redirect chain beginning at {src}: must be single-hop')
    return errors

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);x=p.parse_args()
    with open(x.input,encoding='utf-8-sig',newline='') as fh:rows=list(csv.DictReader(fh))
    errors=check(rows)
    if errors:
        for e in errors:print('FAIL:',e)
        sys.exit(1)
    print(f'PASS: {len(rows)} migration decisions pass structural safety checks; real HTTP redirects still require live verification.')
if __name__=='__main__':main()
