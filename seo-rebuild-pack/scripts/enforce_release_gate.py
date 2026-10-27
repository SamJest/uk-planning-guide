#!/usr/bin/env python3
"""Objective quality gate: no new exact duplicates, sitemap violations, or unreviewed removals.

Run against before/after audit folders after comparing protected traffic URLs.
This is a *minimum* gate, not a substitute for source fact-checking or manual intent review.
"""
import argparse,csv,json,sys
from pathlib import Path

def rows(path):
    with open(path,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def run_gate(before,after):
    b=Path(before);a=Path(after)
    errors=[];warnings=[]
    old={r['url']:r for r in rows(b/'pages.csv')}
    new={r['url']:r for r in rows(a/'pages.csv')}
    old_exact={r['url'] for r in rows(b/'exact_duplicates.csv')}
    new_exact={r['url'] for r in rows(a/'exact_duplicates.csv')}
    added=set(new)-set(old)
    emerging=new_exact-old_exact
    if emerging:
        errors.append(f'{len(emerging)} new URLs involved in exact duplicate indexable content; inspect: {list(sorted(emerging))[:8]}')
    new_viols=rows(a/'sitemap_violations.csv')
    dangerous=[v for v in new_viols if v['issue'] in ('sitemap_noindex','sitemap_non_self_canonical','listed_but_not_built_static_html')]
    if dangerous:errors.append(f'{len(dangerous)} sitemap canonical/robots/missing page conflicts in after build')
    removed=set(old)-set(new)
    if removed:warnings.append(f'{len(removed)} removed routes require checked migration mapping and live HTTP verification before release')
    formerly_indexable_changed=[u for u in old.keys()&new.keys() if old[u]['indexable_by_meta']=='1' and new[u]['indexable_by_meta']!='1']
    if formerly_indexable_changed:errors.append(f'{len(formerly_indexable_changed)} previously indexable URLs became noindex without explicit migration approval')
    newly_nonself=[u for u in added if new[u]['indexable_by_meta']=='1' and new[u]['self_canonical']!='1']
    if newly_nonself:errors.append(f'{len(newly_nonself)} newly emitted indexable pages do not self-canonicalise')
    return errors,warnings,{'old_urls':len(old),'new_urls':len(new),'added':len(added),'removed':len(removed),
                           'new_exact_duplicate_members':len(emerging),'sitemap_violations':len(dangerous)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);x=p.parse_args()
    errs,warns,summary=run_gate(x.before,x.after)
    print(json.dumps(summary,indent=2))
    for w in warns:print('REVIEW:',w)
    for e in errs:print('FAIL:',e)
    if errs:sys.exit(1)
    print('PASS: objective release gates. Manual legal/redirect checks still necessary.')
if __name__=='__main__':main()
