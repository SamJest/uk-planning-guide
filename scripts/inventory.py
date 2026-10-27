"""Repository-derived static inventory. HTTP and legal verification are separate checks."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from lxml import html, etree

BASE = 'https://ukplanningguide.co.uk'

def route(path):
    value = '/' + path.as_posix()
    return value[:-10] if value.endswith('index.html') else value

def save(path, rows, fields):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)

def audit(root, output, revision=None):
    output.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in root.rglob('*.html') if '.git' not in p.parts and 'seo-rebuild-pack' not in p.parts)
    urls = {BASE + route(p.relative_to(root)) for p in files}
    sitemap = Counter()
    shard_errors = []
    for path in [root / 'sitemap.xml', *sorted((root / 'sitemaps').glob('*.xml'))]:
        doc = etree.parse(str(path))
        if etree.QName(doc.getroot()).localname != 'urlset':
            continue
        locs = doc.xpath('//*[local-name()="url"]/*[local-name()="loc"]/text()')
        sitemap.update(locs)
        if len(locs) > 50000 or path.stat().st_size > 50000000:
            shard_errors.append(str(path))
    protected = {}
    gsc = root / 'seo-rebuild-pack/data/gsc/search_console_1000_pages_ranked.csv'
    with gsc.open(encoding='utf-8-sig') as stream:
        for row in csv.DictReader(stream):
            if float(row['Clicks']) > 0:
                protected[row['URL']] = row
    save(output / 'protected.csv', protected.values(), ['URL','Clicks','Impressions'])
    incoming = Counter()
    rows, broken = [], []
    for i, path in enumerate(files):
        url = BASE + route(path.relative_to(root))
        raw = path.read_bytes()
        if revision:
            import subprocess
            changed = subprocess.check_output(['git','diff','--name-only',revision,'--','*.html'],cwd=root,text=True).splitlines() if i == 0 else changed
            if path.relative_to(root).as_posix() in changed:
                raw = subprocess.check_output(['git','show',revision+':'+path.relative_to(root).as_posix()],cwd=root)
        doc = html.fromstring(raw)
        main = doc.xpath('//main') or doc.xpath('//body') or [doc]
        # Exclude repeated navigation, scripts, styles and forms from main fingerprint.
        content = html.fromstring(etree.tostring(main[0]))
        for node in content.xpath('.//script|.//style|.//nav|.//footer|.//form'):
            node.drop_tree()
        text = ' '.join(content.text_content().split())
        canonical = doc.xpath('//link[contains(concat(" ",@rel," ")," canonical ")]/@href')
        canonical = canonical[0] if len(canonical) == 1 else ''
        robots = ' '.join(doc.xpath('//meta[@name="robots" or @name="googlebot"]/@content')).lower()
        links = set()
        for href in doc.xpath('//a/@href'):
            target = urlsplit(urljoin(url, href))
            if target.netloc == 'ukplanningguide.co.uk':
                dest = BASE + target.path
                links.add(dest)
                incoming[dest] += 1
                disk = root / unquote(target.path).lstrip('/')
                if not disk.exists():
                    broken.append({'source':url,'target':dest})
        parts = urlsplit(url).path.strip('/').split('/')
        nation = next((n for n in ('england','wales','scotland','northern-ireland') if n in parts), 'unknown')
        nation = doc.get('data-jurisdiction', nation)
        family = doc.get('data-page-family', parts[0] or 'home')
        legacy = canonical != url and bool(canonical)
        utility = 'noindex' in robots
        findings = []
        if 'No property-specific local facts have been verified' in text:
            findings.append('missing_local_evidence')
        if 'usually conservation areas' in text and 'article-4' in parts and 'hmos' in parts:
            findings.append('wrong_hmo_constraint_default')
        if legacy: findings.append('nonself_canonical_review')
        if not canonical: findings.append('missing_or_multiple_canonical')
        disposition = 'NONINDEX_UTILITY' if utility else 'LEGACY_CANONICAL_TEMP' if legacy else 'RESEARCH_BEFORE_DECISION'
        rows.append(dict(url=url,page_type=family,nation=nation,authority_id='',authority_hint=parts[-1],project=parts[0],topic=parts[-1],title=' '.join(doc.xpath('//title/text()')),h1=' | '.join(doc.xpath('//h1//text()')),canonical=canonical,indexability='noindex' if utility else 'indexable_by_meta_only',source_ids='|'.join(sorted(set(doc.xpath('//*[@data-source-id]/@data-source-id')))),outgoing=len(links),incoming=0,main_hash=hashlib.sha256(text.encode()).hexdigest(),tokens=len(text.split()),last_genuine_updated_date='',date_note='existing dates not independently verified',disposition=disposition,evidence_status='needs_claim_level_review',findings=';'.join(findings),in_sitemap=sitemap[url],http_status='NOT_CHECKED',protected=int(url in protected)))
        if i % 5000 == 0: print(f'Parsed {i}/{len(files)}', flush=True)
    for row in rows: row['incoming'] = incoming[row['url']]
    save(output/'pages.csv',rows,list(rows[0]))
    save(output/'broken_links.csv',broken,['source','target'])
    violations = [{'url':u,'issue':'missing_html'} for u in sitemap if u not in urls]
    for row in rows:
        if row['in_sitemap'] and (row['canonical'] != row['url'] or row['indexability']=='noindex'):
            violations.append({'url':row['url'],'issue':'noncanonical_or_noindex'})
        if row['in_sitemap'] > 1: violations.append({'url':row['url'],'issue':'repeated_sitemap_entry'})
    save(output/'sitemap_violations.csv',violations,['url','issue'])
    duplicates = []
    for field in ('title','h1','main_hash'):
        groups = defaultdict(list)
        for row in rows: groups[row[field]].append(row['url'])
        for value, members in groups.items():
            if value and len(members)>1:
                duplicates.extend({'signal':field,'value':value,'url':u,'group_size':len(members),'decision':'RESEARCH_BEFORE_DECISION'} for u in members)
    save(output/'duplicate_candidates.csv',duplicates,['signal','value','url','group_size','decision'])
    summary = dict(html_emitted=len(rows),dispositions=dict(Counter(r['disposition'] for r in rows)),families=dict(Counter(r['page_type'] for r in rows)),sitemap_unique_urls=len(sitemap),sitemap_violations=len(violations),oversize_shards=shard_errors,broken_links=len(broken),orphan_candidates=sum(r['incoming']==0 for r in rows),missing_local_evidence=sum('missing_local_evidence' in r['findings'] for r in rows),wrong_hmo_default=sum('wrong_hmo' in r['findings'] for r in rows),protected_urls=len(protected),protected_present=sum(r['protected'] for r in rows),scope='Static files only; candidates are not confirmed duplicates; no independent legal verification')
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path('.'))
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--revision',help='Read modified HTML at this baseline Git revision')
    args=parser.parse_args()
    audit(args.root.resolve(),args.output.resolve(),args.revision)
