#!/usr/bin/env python3
"""Compare before/after static audit pages.csv; surface all changed routes for approval."""
import argparse,csv,json
from pathlib import Path

def load(p):
    with open(p,encoding='utf-8-sig',newline='') as f:return {r['url']:r for r in csv.DictReader(f)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--output',default='outputs/build_comparison');a=p.parse_args()
    b=load(a.before);n=load(a.after);dst=Path(a.output);dst.mkdir(parents=True,exist_ok=True)
    changes=[]
    for url in sorted(set(b)|set(n)):
        o=b.get(url,{});z=n.get(url,{})
        status=('REMOVED_NEEDS_MIGRATION_REVIEW' if not z else 'ADDED_NEEDS_UNIQUENESS_REVIEW' if not o else 'CHANGED' if any(o.get(k)!=z.get(k) for k in ('canonical_normalised','title','h1','main_hash','indexable_by_meta','in_sitemap')) else 'UNCHANGED')
        if status=='UNCHANGED':continue
        changes.append({'url':url,'change':status,'before_canonical':o.get('canonical_normalised',''),
                        'after_canonical':z.get('canonical_normalised',''),
                        'before_indexable':o.get('indexable_by_meta',''),'after_indexable':z.get('indexable_by_meta',''),
                        'before_sitemap':o.get('in_sitemap',''),'after_sitemap':z.get('in_sitemap',''),
                        'before_family':o.get('family',''),'after_family':z.get('family',''),
                        'manual_review_required':int(status.startswith(('REMOVED','ADDED')) or o.get('canonical_normalised','')!=z.get('canonical_normalised',''))})
    keys=['url','change','before_canonical','after_canonical','before_indexable','after_indexable','before_sitemap','after_sitemap','before_family','after_family','manual_review_required']
    with (dst/'changed_urls.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(changes)
    s={'before_count':len(b),'after_count':len(n),'removed':sum(x['change'].startswith('REMOVED') for x in changes),
       'added':sum(x['change'].startswith('ADDED') for x in changes),
       'modified':sum(x['change']=='CHANGED' for x in changes),'review_required':sum(x['manual_review_required'] for x in changes)}
    (dst/'summary.json').write_text(json.dumps(s,indent=2)+'\n')
    print(json.dumps(s,indent=2))
if __name__=='__main__':main()
