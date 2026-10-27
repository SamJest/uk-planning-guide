#!/usr/bin/env python3
"""Non-destructive audit of an ALREADY GENERATED UKPlanningGuide static site.

Requires beautifulsoup4 (see scripts/crawl_requirements.txt).
Does NOT decide which duplicate to delete. Reports candidate groups for review.
"""
import argparse
import csv
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup

EXCLUDED = {'script', 'style', 'nav', 'footer', 'form', 'noscript', 'svg', 'button'}
FIELDS = ['url','relative_path','family','status_assumed','title','h1','h1_count',
          'description','canonical','canonical_normalised','self_canonical',
          'indexable_by_meta','in_sitemap','main_words','main_hash',
          'main_simhash','internal_inlinks','internal_outlinks','intent_hint',
          'notes','meta_last_modified']


def normalise(url):
    """Compare *equivalent* static URLs; don't erase semantically different paths."""
    p = urlparse(url)
    if not p.scheme or not p.netloc:
        return ''
    path = re.sub(r'/+', '/', p.path or '/')
    path = re.sub(r'/index\.html?$', '/', path, flags=re.I)
    if not path.endswith('/') and '.' not in path.rsplit('/', 1)[-1]:
        path += '/'
    return urlunparse((p.scheme.lower(), p.netloc.lower(), path, '', '', ''))


def file_url(path, root, base):
    rel = path.relative_to(root).as_posix()
    if rel == 'index.html': route = '/'
    elif rel.endswith('/index.html'): route = '/' + rel[:-10]
    elif rel.endswith('.html'): route = '/' + rel
    else: route = '/' + rel
    return normalise(urljoin(base, route))


def family(url):
    bits = [x for x in urlparse(url).path.split('/') if x]
    if not bits: return 'home'
    if bits[0] in ('england','wales','scotland','northern-ireland') and len(bits)>1:
        return bits[0] + '/' + bits[1]
    return bits[0]


def simhash(text):
    words = re.findall(r'[a-z0-9]+', text.lower())[:1500]
    if len(words) < 30: return ''
    grams = Counter(' '.join(words[i:i+3]) for i in range(len(words)-2))
    counts=[0]*64
    for token, freq in grams.items():
        v=int.from_bytes(hashlib.blake2b(token.encode('utf8'),digest_size=8).digest(),'big')
        for i in range(64):counts[i] += min(freq,3) * (1 if (v>>i)&1 else -1)
    return f'{sum(1<<i for i,x in enumerate(counts) if x>=0):016x}'


def read_page(fp,root,base):
    url=file_url(fp,root,base)
    soup=BeautifulSoup(fp.read_bytes(), 'html.parser')
    title=soup.title.get_text(' ',strip=True) if soup.title else ''
    hs=soup.find_all('h1')
    h1=' | '.join(h.get_text(' ',strip=True) for h in hs[:4])
    desc=soup.find('meta',attrs={'name':re.compile('^description$',re.I)})
    desc=desc.get('content','').strip() if desc else ''
    can=soup.find('link',rel=lambda r:bool(r) and 'canonical' in (r if isinstance(r,list) else [r]))
    can=urljoin(url,can.get('href','')) if can and can.get('href') else ''
    robots=' '.join(x.get('content','') for x in soup.find_all('meta') if x.get('name','').lower() in ('robots','googlebot'))
    lastmod=soup.find('meta',attrs={'property':re.compile('^(article:modified_time|og:updated_time)$',re.I)})
    lm=lastmod.get('content','') if lastmod else ''
    main=soup.find('main') or soup.find('article') or soup.body or soup
    # Keep headings & other real page content, remove nav/forms/scripts from text.
    copy=BeautifulSoup(str(main),'html.parser')
    for el in copy.find_all(EXCLUDED):el.decompose()
    text=re.sub(r'\s+',' ',copy.get_text(' ',strip=True)).strip()
    words=re.findall(r'\b\w+\b',text)
    links=[]
    for a in soup.find_all('a',href=True):
        href=a.get('href','').strip()
        if href.startswith(('mailto:','tel:','javascript:')) or href.startswith('#'):continue
        full=urljoin(url,href)
        parsed=urlparse(full)
        if parsed.netloc.lower() != urlparse(base).netloc.lower():continue
        clean=normalise(full)
        if clean and not re.search(r'\.(?:jpe?g|png|svg|webp|gif|pdf|zip|csv|json|xml|txt|js|css|woff2?)$',parsed.path,re.I):
            links.append(clean)
    parts=[p for p in urlparse(url).path.split('/') if p]
    intent='|'.join(parts)
    row={
        'url':url,'relative_path':fp.relative_to(root).as_posix(), 'family':family(url),
        'status_assumed':'200_static_file_ONLY_not_live_verified','title':title,'h1':h1,'h1_count':len(hs),
        'description':desc,'canonical':can,'canonical_normalised':normalise(can) if can else '',
        'self_canonical':int(bool(can) and normalise(can)==url),
        'indexable_by_meta':int('noindex' not in robots.lower()),'in_sitemap':0,
        'main_words':len(words),'main_hash':hashlib.sha256(text.lower().encode()).hexdigest() if text else '',
        'main_simhash':simhash(text),'internal_inlinks':0,'internal_outlinks':len(set(links)),
        'intent_hint':intent,'notes':'', 'meta_last_modified':lm
    }
    return row, set(links)


def read_sitemap_files(root, base):
    urls=set(); errors=[]; checked=[]
    # Parse all sitemap XML documents in build, including unlisted shards.
    for f in sorted(root.rglob('*.xml')):
        if 'sitemap' not in f.name.lower():continue
        try:
            raw = f.read_bytes()
            elem=ET.fromstring(raw)
            if elem.tag.rsplit('}',1)[-1]=='urlset':
                checked.append(f.relative_to(root).as_posix())
                for u in elem.iter():
                    if u.tag.rsplit('}',1)[-1]=='loc' and u.text:
                        uu=normalise(u.text.strip())
                        if uu and urlparse(uu).hostname==urlparse(base).hostname:urls.add(uu)
        except Exception as e:errors.append(f'{f}: {e}')
    for f in sorted(root.rglob('*.xml.gz')):
        if 'sitemap' not in f.name.lower():continue
        try:
            elem=ET.fromstring(gzip.decompress(f.read_bytes()))
            if elem.tag.rsplit('}',1)[-1]=='urlset':
                checked.append(f.relative_to(root).as_posix())
                for u in elem.iter():
                    if u.tag.rsplit('}',1)[-1]=='loc' and u.text:
                        uu=normalise(u.text.strip())
                        if uu and urlparse(uu).hostname==urlparse(base).hostname: urls.add(uu)
        except Exception as e:errors.append(f'{f}: {e}')
    return urls,errors,checked


def save_csv(path, rows, columns):
    with path.open('w',newline='',encoding='utf-8-sig') as fh:
        writer=csv.DictWriter(fh,fieldnames=columns,extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def run_audit(root,output,base,max_pages=0):
    root=Path(root).resolve();output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
    if not root.is_dir():raise ValueError(f'No build directory at {root}')
    if output==root or root in output.parents:raise ValueError('Output must not be inside site build directory')
    pages=sorted(root.rglob('*.html'))
    if max_pages:pages=pages[:max_pages]
    rows=[]; graph=defaultdict(set); link_map={}; seen=[]
    for i,fp in enumerate(pages,1):
        try:
            row,links=read_page(fp,root,base)
            rows.append(row);link_map[row['url']]=links
            for l in links:graph[l].add(row['url'])
        except Exception as ex: seen.append({'file':fp.relative_to(root).as_posix(),'error':str(ex)[:250]})
        if i%5000==0:print(f'Processed {i:,} HTML files',flush=True)
    urls={r['url'] for r in rows}
    sitemaps,site_errors,checked=read_sitemap_files(root,base)
    for r in rows:
        r['in_sitemap']=int(r['url'] in sitemaps)
        r['internal_inlinks']=len(graph[r['url']])
        notes=[]
        if not r['title']: notes.append('missing_title')
        if r['h1_count']!=1:notes.append('h1_count_not_one')
        if r['indexable_by_meta'] and not r['canonical']:notes.append('missing_canonical')
        if r['indexable_by_meta'] and r['canonical'] and not r['self_canonical']:notes.append('nonself_canonical')
        if r['indexable_by_meta'] and r['main_words']<120:notes.append('short_main_review')
        if r['indexable_by_meta'] and r['internal_inlinks']==0 and r['url']!=normalise(base):notes.append('orphan_candidate')
        r['notes']=';'.join(notes)
    exact=defaultdict(list);titles=defaultdict(list)
    for r in rows:
        if r['main_hash'] and r['indexable_by_meta']:exact[r['main_hash']].append(r['url'])
        if r['title'] and r['indexable_by_meta']:titles[r['title'].lower()].append(r['url'])
    exact_rows=[{'cluster':i,'cluster_size':len(us),'url':u} for i,us in enumerate((us for us in exact.values() if len(us)>1),1) for u in us]
    title_rows=[{'title':t,'cluster_size':len(us),'url':u} for t,us in titles.items() if len(us)>1 for u in us]
    # LSH candidate generation: 4 × 16-bit exact partitions, then 64-bit Hamming <=3.
    # This is intentionally ONLY a candidate queue, and does not scale to common boilerplate buckets.
    hash_by_url={r['url']:int(r['main_simhash'],16) for r in rows if r['main_simhash'] and r['indexable_by_meta']}
    by_url={r['url']:r for r in rows}
    buckets=defaultdict(list)
    for u,h in hash_by_url.items():
        for b in range(4):buckets[(b,(h>>(b*16))&65535)].append(u)
    candidate=set();skipped=0
    for members in buckets.values():
        if len(members)>250:skipped+=1;continue
        for i,a in enumerate(members):
            for b in members[i+1:]:
                if a==b:continue
                if (hash_by_url[a]^hash_by_url[b]).bit_count()<=3:
                    pair=tuple(sorted((a,b)))
                    candidate.add(pair)
    near=[{'url_a':a,'url_b':b,'distance_bits':(hash_by_url[a]^hash_by_url[b]).bit_count(),
           'family_a':by_url[a]['family'],'family_b':by_url[b]['family'],
           'warning':'candidate_only_DO_NOT_AUTO_MERGE'} for a,b in sorted(candidate)]
    broken=[{'source':src,'destination':dest,'kind':'target_missing_from_built_html_check_route_handling'}
            for src,links in link_map.items() for dest in sorted(links) if dest not in urls]
    sitemap_issues=[]
    for u in sorted(sitemaps-urls):sitemap_issues.append({'url':u,'issue':'listed_but_not_built_static_html'})
    for r in rows:
        if r['in_sitemap'] and not r['indexable_by_meta']:sitemap_issues.append({'url':r['url'],'issue':'sitemap_noindex'})
        if r['in_sitemap'] and not r['self_canonical']:sitemap_issues.append({'url':r['url'],'issue':'sitemap_non_self_canonical'})
        if not r['in_sitemap'] and r['indexable_by_meta'] and r['self_canonical']:
            sitemap_issues.append({'url':r['url'],'issue':'eligible_canonical_missing_sitemap_review'})
    save_csv(output/'pages.csv',rows,FIELDS)
    save_csv(output/'exact_duplicates.csv',exact_rows,['cluster','cluster_size','url'])
    save_csv(output/'repeated_titles.csv',title_rows,['title','cluster_size','url'])
    save_csv(output/'near_duplicate_candidates.csv',near,['url_a','url_b','distance_bits','family_a','family_b','warning'])
    save_csv(output/'broken_internal_links.csv',broken,['source','destination','kind'])
    save_csv(output/'internal_links.csv',({'source':u,'target':l} for u,links in sorted(link_map.items()) for l in sorted(links)),['source','target'])
    save_csv(output/'sitemap_violations.csv',sitemap_issues,['url','issue'])
    save_csv(output/'parse_errors.csv',seen,["file","error"])
    summary={
        'scope':'static build only; no HTTP status tested; near-duplicates are UNREVIEWED candidate pairs',
        'build_root':str(root),'html_emitted':len(rows),'files_failed_parse':len(seen),
        'html_examined':len(pages),'pages_indexable_by_meta':sum(r['indexable_by_meta'] for r in rows),
        'self_canonical_indexable':sum(r['self_canonical'] and r['indexable_by_meta'] for r in rows),
        'in_sitemap':sum(r['in_sitemap'] for r in rows),'sitemap_loc_count':len(sitemaps),
        'sitemap_shards_read':checked,'sitemap_errors':site_errors,
        'sitemap_violations':len(sitemap_issues),'exact_duplicate_groups':sum(len(us)>1 for us in exact.values()),
        'exact_duplicate_url_rows':len(exact_rows),'near_duplicate_candidate_pairs':len(near),
        'candidate_buckets_skipped_too_large':skipped,'repeated_title_rows':len(title_rows),
        'broken_internal_link_candidates':len(broken),
        'notes':'Sitemap discovered only from XML build files; inspect any dynamically produced sitemaps separately. Static links to dynamic route aliases may be falsely flagged.'
    }
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    print(json.dumps(summary,indent=2))
    return summary


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',required=True,help='PATH TO GENERATED HTML folder, not source code')
    ap.add_argument('--output',default='outputs/build_audit')
    ap.add_argument('--base',default='https://ukplanningguide.co.uk/')
    ap.add_argument('--max-pages',default=0,type=int,help='Pilot only: does NOT give full inventory')
    args=ap.parse_args()
    run_audit(args.root,args.output,args.base,args.max_pages)

if __name__=='__main__':main()
