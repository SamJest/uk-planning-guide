#!/usr/bin/env python3
"""Source-independent triage of generated static HTML for likely templating failures.

These are advisory review flags, NOT evidence that the page is wrong or should be deleted.
"""
import argparse,csv,re
from pathlib import Path
from bs4 import BeautifulSoup
from audit_static_build import file_url

PATTERNS = [
 ('unverified_local_placeholder', re.compile(r'no (?:property.specific )?local facts have been verified|not yet verified|no locally verified',re.I)),
 ('moved_html_shell', re.compile(r'this page has moved|we have moved this page',re.I)),
 ('generic_source_checklist', re.compile(r'check the local authority.{0,120}official (?:website|source)',re.I)),
 ('placeholder_lorem',re.compile(r'\blorem ipsum\b|\bTODO\b|\bcoming soon\b',re.I)),
 ('unsupported_absolute',re.compile(r'\bplanning permission (?:is never|always|is always) (?:needed|required)\b',re.I))
]

def inspect(root,base):
    rows=[]
    for fp in sorted(Path(root).rglob('*.html')):
        url=file_url(fp,Path(root),base)
        s=BeautifulSoup(fp.read_bytes(),'html.parser')
        main=s.find('main') or s.find('article') or s.body or s
        for tag in main.select('script,style,nav,footer,form'):tag.decompose()
        txt=' '.join(main.stripped_strings)
        lower=url.lower()
        flags=[]
        for label,reg in PATTERNS:
            if reg.search(txt):flags.append(label)
        # Heuristic only. It is normal for a global height guide to discuss garden rooms in examples;
        # review when a generic route makes a single project its opening main answer.
        front=txt[:700].lower()
        if '/maximum-height/' in lower and 'garden room' in front: flags.append('generic_height_leads_with_garden_room_review')
        if '/planning-permission/' in lower and 'garden room' in front: flags.append('generic_permission_leads_with_garden_room_review')
        if '/hmos/' in lower and '/article-4/' in lower and 'usually conservation areas' in front: flags.append('hmo_article4_conservation_default_review')
        if flags:rows.append({'url':url,'flags':';'.join(sorted(set(flags))),'sample_first_140_characters':txt[:140]})
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--output',default='outputs/content_smells.csv');p.add_argument('--base',default='https://ukplanningguide.co.uk/');x=p.parse_args()
    rows=inspect(x.root,x.base)
    out=Path(x.output);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['url','flags','sample_first_140_characters']);w.writeheader();w.writerows(rows)
    print(f'{len(rows)} pages with candidate content quality flags written to {out}; verify each; do NOT auto delete')
if __name__=='__main__':main()
