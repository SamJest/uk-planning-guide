#!/usr/bin/env python3
"""Owner-initiated, rate-limited live crawl of UKPlanningGuide.
Run: pip install -r requirements.txt
     python full_site_crawler.py --site https://ukplanningguide.co.uk --output full_crawl
This requires working internet/DNS and is NOT the same as Google's indexing report.
"""
import argparse, csv, gzip, hashlib, json, re, threading, time
from collections import Counter, defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree as ET
import requests
from bs4 import BeautifulSoup

USER_AGENT = 'UKPlanningGuideOwnerAudit/1.0 (owner-initiated SEO quality check)'
HEADERS = {'User-Agent': USER_AGENT, 'Accept': 'text/html,application/xml,text/xml,*/*'}
EXCLUDE_EXT = ('.jpg','.jpeg','.png','.webp','.svg','.gif','.avif','.ico','.css','.js','.pdf','.zip','.csv','.xlsx','.woff','.woff2','.ttf','.mp4','.mp3','.xml','.txt','.json')
FETCH_LOCK = threading.Lock()
LAST_REQUEST = [0.0]
RPS = [2.0]

def permitted_host(url, host):
    x=urlsplit(url)
    return x.scheme in ('http','https') and x.hostname and x.hostname.lower().removeprefix('www.') == host.removeprefix('www.')

def norm(url):
    s=urlsplit(url)
    if not s.scheme or not s.netloc: return ''
    path=re.sub('/+', '/', s.path or '/')
    if re.search(r'/index\.html?$',path,re.I):path=re.sub(r'index\.html?$', '',path,flags=re.I)
    # Tracking/parameter variants are reported separately, not crawled infinitely.
    return urlunsplit((s.scheme.lower(),s.netloc.lower(),path,'',''))

def throttle():
    with FETCH_LOCK:
        now=time.monotonic()
        pause=max(0.0, LAST_REQUEST[0]+1/max(0.1,RPS[0])-now)
        if pause:time.sleep(pause)
        LAST_REQUEST[0]=time.monotonic()

def fetch(url, timeout=18):
    throttle()
    try:
        res=requests.get(url,headers=HEADERS,timeout=timeout,allow_redirects=True)
        return res,None
    except Exception as ex:
        return None,str(ex)[:260]

def get_xml_links(raw):
    if raw[:2]==b'\x1f\x8b':raw=gzip.decompress(raw)
    root=ET.fromstring(raw)
    tag=root.tag.rsplit('}',1)[-1]
    urls=[el.text.strip() for el in root.iter() if el.tag.rsplit('}',1)[-1]=='loc' and el.text]
    return tag,urls

def read_sitemaps(site, host, robots_txt):
    declared=re.findall(r'^\s*Sitemap\s*:\s*(\S+)',robots_txt,flags=re.I|re.M)
    roots=declared or [urljoin(site,'/sitemap.xml'),urljoin(site,'/sitemap_index.xml'),urljoin(site,'/sitemap-index.xml')]
    seen=set(); urls=set(); history=[]
    def walk(u,depth=0):
        if u in seen or depth>5 or len(seen)>500 or not permitted_host(u,host): return
        seen.add(u)
        response,error=fetch(u)
        if error or response is None:
            history.append([u,'error',0,error or '']);return
        if response.status_code!=200:
            history.append([u,'http',response.status_code,'']);return
        try:
            tag,items=get_xml_links(response.content)
            history.append([u,tag,response.status_code,len(items)])
            if tag=='sitemapindex':
                for item in items:walk(item,depth+1)
            elif tag=='urlset':
                urls.update(norm(item) for item in items if permitted_host(item,host))
        except Exception as e:history.append([u,'parse_error',response.status_code,str(e)[:120]])
    for u in roots:walk(u)
    return urls,history

def simhash(body):
    words=re.findall(r"[a-z0-9']+", body.lower())
    # A few hundred meaningful terms suffice for high-confidence duplicate candidates.
    pieces=[' '.join(words[i:i+3]) for i in range(len(words)-2)]
    weight=[0]*64
    for gram,n in Counter(pieces).items():
        h=int.from_bytes(hashlib.blake2b(gram.encode('utf-8'),digest_size=8).digest(),'big')
        freq=min(5,n)
        for j in range(64):weight[j]+=freq if (h>>j)&1 else -freq
    return sum(1<<j for j,x in enumerate(weight) if x>=0)

def parse_page(url, host, rp):
    row={'url':url,'requested_url':url,'status':'','final_url':'','canonical':'','title':'','description':'',
         'h1':'','h1_count':0,'words':0,'noindex':0,'nofollow':0,'robots_blocked':0,
         'in_sitemap':0,'body_hash':'','simhash':'','internal_links':0,'error':''}
    if rp and not rp.can_fetch(USER_AGENT,url):row['robots_blocked']=1;row['status']='blocked';return row,[],[]
    res,error=fetch(url)
    if error or res is None:row['status']='error';row['error']=error;return row,[],[]
    row['status']=res.status_code;row['final_url']=res.url
    if 'text/html' not in res.headers.get('Content-Type','').lower():return row,[],[]
    soup=BeautifulSoup(res.content,'html.parser')
    title=soup.find('title')
    row['title']=title.get_text(' ',strip=True) if title else ''
    desc=soup.find('meta',attrs={'name':re.compile('^description$',re.I)})
    row['description']=desc.get('content','').strip() if desc else ''
    canonical=soup.find('link',rel=lambda r:bool(r) and 'canonical' in (r if isinstance(r,list) else [r]))
    row['canonical']=urljoin(res.url,canonical.get('href','')) if canonical and canonical.get('href') else ''
    h1=soup.select('h1');row['h1_count']=len(h1);row['h1']=' | '.join(x.get_text(' ',strip=True) for x in h1[:3])
    meta=' '.join(x.get('content','') for x in soup.find_all('meta') if x.get('name','').lower() in ('robots','googlebot'))
    meta+=' '+res.headers.get('X-Robots-Tag','')
    row['noindex']=int('noindex' in meta.lower());row['nofollow']=int('nofollow' in meta.lower())
    internal=[];parameter_urls=[]
    for a in soup.find_all('a',href=True):
        raw=a['href'];dest=urljoin(res.url,raw);ds=urlsplit(dest)
        if not permitted_host(dest,host) or any(ds.path.lower().endswith(ext) for ext in EXCLUDE_EXT):continue
        if ds.query:parameter_urls.append(dest)
        clean=norm(dest)
        if clean:internal.append(clean)
    row['internal_links']=len(set(internal))
    main=soup.find('main') or soup.find('article') or soup.body or soup
    copy=BeautifulSoup(str(main),'html.parser')
    for x in copy.select('script,style,nav,footer,header,form,aside,button'):x.decompose()
    text=' '.join(copy.stripped_strings)
    text=re.sub(r'\s+',' ',text).strip()
    row['words']=len(re.findall(r'\b\w+\b',text))
    row['body_hash']=hashlib.sha256(text.lower().encode('utf-8')).hexdigest() if text else ''
    row['simhash']=f'{simhash(text):016x}' if row['words']>=50 else ''
    return row,list(set(internal)),list(set(parameter_urls))

def write_csv(path,rows,fields):
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        out=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');out.writeheader();out.writerows(rows)

def main():
    ap=argparse.ArgumentParser(description='Rate-limited site-wide SEO audit')
    ap.add_argument('--site',default='https://ukplanningguide.co.uk')
    ap.add_argument('--output',default='full_crawl')
    ap.add_argument('--max-pages',type=int,default=50000)
    ap.add_argument('--workers',type=int,default=3)
    ap.add_argument('--rps',type=float,default=2.0,help='Maximum overall HTTP requests per second')
    args=ap.parse_args()
    if args.workers<1 or args.workers>8:ap.error('workers must be 1..8')
    RPS[0]=args.rps
    site=norm(args.site);site=site.rstrip('/')+'/'
    host=urlsplit(site).hostname
    folder=Path(args.output);folder.mkdir(parents=True,exist_ok=True)
    robots_res,error=fetch(urljoin(site,'/robots.txt'))
    robots_txt=robots_res.text if robots_res is not None and robots_res.status_code==200 else ''
    rp=RobotFileParser()
    rp.parse(robots_txt.splitlines()) if robots_txt else None
    sitemapped,si_log=read_sitemaps(site,host,robots_txt)
    roots=deque([site,*sorted(sitemapped)])
    pending=set(roots);seen=set();data={};graph=defaultdict(set);parameters=set()
    print('Sitemap pages discovered:',len(sitemapped),'Sitemaps checked:',len(si_log),flush=True)
    while roots and len(seen)<args.max_pages:
        batch=[]
        while roots and len(batch)<args.workers*8 and len(seen)+len(batch)<args.max_pages:
            url=roots.popleft();pending.discard(url)
            if url not in seen and permitted_host(url,host) and not urlsplit(url).path.lower().endswith(EXCLUDE_EXT):
                seen.add(url);batch.append(url)
        if not batch:continue
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            jobs={pool.submit(parse_page,u,host,rp if robots_txt else None):u for u in batch}
            for future in as_completed(jobs):
                try:r,links,params=future.result()
                except Exception as e:print('Parse failure:',jobs[future],e);continue
                data[r['url']]=r;parameters.update(params)
                r['in_sitemap']=int(r['url'] in sitemapped)
                for link in links:
                    graph[link].add(r['url'])
                    if link not in seen and link not in pending:
                        roots.append(link);pending.add(link)
        if len(seen)%1000< len(batch):print(f'{len(seen)} pages crawled; queue={len(roots)}',flush=True)
    for url,r in data.items():r['inlinks']=len(graph.get(url,()))
    rows=sorted(data.values(),key=lambda r:r['url'])
    for r in rows:
        cc=norm(r['canonical']) if r['canonical'] else ''
        r['canonical_issue']= ('missing' if not cc and r['status']==200 else
                               'points_elsewhere' if cc and cc!=r['url'] else
                               'self' if cc==r['url'] else '')
    write_csv(folder/'pages.csv',rows,[*rows[0].keys()] if rows else [])
    write_csv(folder/'sitemaps.csv',({'sitemap_url':x,'result':y,'http_status':z,'entries_or_error':w} for x,y,z,w in si_log),['sitemap_url','result','http_status','entries_or_error'])
    exact=defaultdict(list)
    for r in rows:
        if r['body_hash'] and r['status']==200:exact[r['body_hash']].append(r['url'])
    exact_rows=[{'group':i,'url':u,'group_size':len(us)} for i,us in enumerate((s for s in exact.values() if len(s)>1),1) for u in us]
    write_csv(folder/'exact_duplicates.csv',exact_rows,['group','url','group_size'])
    # 4x16-bit simhash blocking. <=3 differing bits guaranteed to share a block.
    hashes={r['url']:int(r['simhash'],16) for r in rows if r['simhash'] and r['status']==200}
    buckets=defaultdict(list)
    for u,h in hashes.items():
        for b in range(4):buckets[(b,(h>>(b*16))&65535)].append(u)
    suspects=set()
    for members in buckets.values():
        if len(members)>500:continue # common boilerplate; skip excessive ambiguous comparisons
        for i,a in enumerate(members):
            for b in members[i+1:]:
                if a!=b and (hashes[a]^hashes[b]).bit_count()<=3:suspects.add(tuple(sorted((a,b))))
    near=[{'url_a':a,'url_b':b,'distance_bits':(hashes[a]^hashes[b]).bit_count()} for a,b in sorted(suspects)]
    write_csv(folder/'near_duplicate_candidates.csv',near,['url_a','url_b','distance_bits'])
    broken=[{'source':src,'destination':dest,'http_status':data[dest]['status']} for dest,refs in graph.items() if dest in data and ((isinstance(data[dest]['status'],int) and data[dest]['status']>=400) or data[dest]['status']=='error') for src in refs]
    write_csv(folder/'broken_internal_links.csv',broken,['source','destination','http_status'])
    write_csv(folder/'query_parameter_links.csv',({'url':u} for u in sorted(parameters)),['url'])
    stats={'pages_crawled':len(rows),'remaining_queue':len(roots),'sitemap_urls':len(sitemapped),
           'sitemap_status':si_log,'http_status':dict(Counter(str(r['status']) for r in rows)),
           'missing_canonical':sum(r['canonical_issue']=='missing' for r in rows),
           'nonself_canonical':sum(r['canonical_issue']=='points_elsewhere' for r in rows),
           'noindex':sum(r['noindex'] for r in rows),'low_wordcount_under_150':sum(r['words']<150 and r['status']==200 for r in rows),
           'duplicate_groups':len([1 for s in exact.values() if len(s)>1]),'near_duplicate_pairs':len(near),
           'broken_internal_links':len(broken),'sitemap_pages_not_crawled':len(sitemapped-data.keys())}
    (folder/'summary.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in stats.items() if k!='sitemap_status'},indent=2))
    print('Wrote audit files to',folder.resolve())
if __name__=='__main__':main()
