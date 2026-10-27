#!/usr/bin/env python3
"""Join limited GSC landing page sample with generated build audit; no edits."""
import argparse,csv
from pathlib import Path
from urllib.parse import urlparse

def read(p):
    with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def num(x):
    try:return float(str(x).replace(',','').replace('%','').strip() or 0)
    except ValueError:return 0.

def pick(row,*candidates):
    keys={k.lower().strip():k for k in row}
    for name in candidates:
        if name.lower() in keys:return row[keys[name.lower()]]
    return ''

def main():
    p=argparse.ArgumentParser();p.add_argument('--gsc',required=True);p.add_argument('--audit',required=True);p.add_argument('--output',default='outputs/priority_queue.csv');a=p.parse_args()
    audit={r['url'].rstrip('/')+'/':r for r in read(a.audit)}
    rows=[]
    for r in read(a.gsc):
        url=pick(r,'URL','Page','Top pages','page')
        if not url.startswith('http'):continue
        x=audit.get(url.rstrip('/')+'/',{})
        clicks=num(pick(r,'Clicks'));impressions=num(pick(r,'Impressions'))
        pos=num(pick(r,'Position','Average position'))
        notes=x.get('notes','')
        score=(impressions**0.5)*3+clicks*10+(15 if 'nonself_canonical' in notes else 0)+(15 if 'missing_canonical' in notes else 0)
        family=x.get('family','') or urlparse(url).path.strip('/').split('/')[0]
        rows.append({'url':url,'family':family,'gsc_clicks':int(clicks),'gsc_impressions':int(impressions),
                     'avg_position_sample':pos,'priority_score_triage_only':round(score,2),
                     'present_in_current_build':int(bool(x)), 'canonical':x.get('canonical',''),
                     'in_sitemap':x.get('in_sitemap',''), 'audit_notes':notes,
                     'action':'REVIEW_INTENT_CONTENT_AND_DUPLICATE_PROTECTION'})
    rows.sort(key=lambda r:-r['priority_score_triage_only'])
    f=Path(a.output);f.parent.mkdir(parents=True,exist_ok=True)
    fields=['url','family','gsc_clicks','gsc_impressions','avg_position_sample','priority_score_triage_only','present_in_current_build','canonical','in_sitemap','audit_notes','action']
    with open(f,'w',newline='',encoding='utf8') as h:
        w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)
    print(f'Wrote {len(rows)} prioritised GSC-sampled URLs: {f}. This is NOT the full site or a basis for mass removal.')
if __name__=='__main__':main()
