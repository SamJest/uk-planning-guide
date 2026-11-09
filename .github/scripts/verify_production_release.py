"""Verify an exact production patch without regenerating or dropping the corpus."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urljoin, urlsplit, unquote
import xml.etree.ElementTree as ET
from lxml import html

ROOT=Path(__file__).resolve().parents[2]
BASE_URL='https://ukplanningguide.co.uk'
MANIFEST=ROOT/'.github/releases/2026-11-09.json'
QUERIES=['//script[@src]/@src','//form/@action','//link[@rel="canonical"]/@href','//meta[@name="robots"]/@content']

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def blobs(revision,paths):
    paths=sorted(set(paths))
    request=''.join(revision+':'+path+'\n' for path in paths).encode()
    result=subprocess.run(['git','cat-file','--batch'],input=request,capture_output=True,cwd=ROOT,check=True)
    stream=io.BytesIO(result.stdout);output={}
    for path in paths:
        header=stream.readline().split()
        assert len(header)==3 and header[1]==b'blob', 'Missing baseline object: '+path
        output[path]=stream.read(int(header[2]))
        assert stream.read(1)==b'\n'
    return output
def sha(raw):return hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()
def contracts(before,after):
    old,new=html.fromstring(before),html.fromstring(after)
    for query in QUERIES:
        if old.xpath(query)!=new.xpath(query):raise ValueError('Preservation failed: '+query)
    if len(old.xpath('//h1'))!=len(new.xpath('//h1')):raise ValueError('H1 count changed')

def self_test():
    original=b'<html><head><link rel="canonical" href="https://ukplanningguide.co.uk/a/"><script src="/app.js"></script></head><body><h1>A</h1><form action="/submit"></form></body></html>'
    contracts(original,original.replace(b'<h1>A',b'<h1>Improved A'))
    for before,after in [(b'/app.js',b'/other.js'),(b'/submit',b'/elsewhere'),(b'https://ukplanningguide.co.uk/a/',b'https://ukplanningguide.co.uk/b/')]:
        try:contracts(original,original.replace(before,after))
        except ValueError:continue
        raise AssertionError('A deliberate contract mutation passed')

def main(source,index=False):
    self_test()
    release=json.loads(MANIFEST.read_text(encoding='utf-8'))
    base=release['production_base']
    source=Path(source).resolve()
    sys.path.insert(0,str(source))
    from components.project_checklists import render_checklist
    assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()==release['tested_source_sha']
    before=set(git('ls-tree','-r','--name-only',base).decode().splitlines())
    after=set(git('ls-files').decode().splitlines())
    diff_args=['diff','--name-only',base]+(['--cached'] if index else ['HEAD'])
    changed=set(git(*diff_args).decode().splitlines())
    declared={c['path']:c for c in release['changes']}
    assert changed==set(declared)|set(release['metadata_files']), 'Unexpected or missing change outside the exact release manifest'
    old_html={p for p in before if p.endswith('.html')};new_html={p for p in after if p.endswith('.html')}
    assert old_html==new_html and len(new_html)==release['html_after']==release['html_before']==35220
    assert not before-after, 'Production file deleted'
    xml_paths={p for p in before if p=='sitemap.xml' or p.startswith('sitemaps/') and p.endswith('.xml')}
    baseline_blobs=blobs(base,(set(declared)&before)|xml_paths|{'index.html'})
    changed_docs={}
    print(f'Checking {len(declared)} exact file changes against production and tested source...',flush=True)
    for path,record in declared.items():
        old=baseline_blobs[path] if path in before else None
        new=(ROOT/path).read_bytes()
        assert (sha(old) if old is not None else None)==record['before_sha256'], 'Baseline hash mismatch: '+path
        assert sha(new)==record['after_sha256'], 'Candidate hash mismatch: '+path
        expected=source/path if record['kind']=='recovered-reviewed-content' else source/'artifacts/phase-0-canary-site'/path
        expected_bytes=expected.read_bytes().replace(b'\r\n',b'\n')
        if record['kind']=='source-checked-canary-with-preserved-checklist':
            assert path in {'garden-rooms/index.html','england/projects/garden-rooms/index.html'}
            expected_bytes=expected_bytes.replace(b'</h1>',b'</h1>'+render_checklist('garden-rooms').encode(),1)
            assert new.count(b'id="project-evidence-checklist"')==1
        assert sha(expected_bytes)==record['after_sha256'], 'Published bytes differ from the tested source: '+path
        if path.endswith('.html'):
            assert old is not None
            contracts(old,new)
            changed_docs[path]=html.fromstring(new)
    # Every changed internal destination must exist in the retained full site.
    directories={str(Path(p).parent).replace('\\','/') for p in after}
    for path,doc in changed_docs.items():
        url=BASE_URL+'/'+path.removesuffix('index.html')
        for href in doc.xpath('//a/@href|//script/@src|//img/@src|//link/@href'):
            target=urlsplit(urljoin(url,href))
            if target.scheme not in {'https','http'} or target.netloc!='ukplanningguide.co.uk':continue
            target_path=unquote(target.path).strip('/')
            assert target_path in after or target_path in directories or not target_path, f'Broken changed link: {path} -> {href}'
    def metadata(path):
        doc=html.parse(str(ROOT/path))
        # Plain strings release each parsed document; lxml smart strings would
        # otherwise retain tens of thousands of complete DOM trees in memory.
        return BASE_URL+'/'+path.removesuffix('index.html'),[str(v) for v in doc.xpath('//link[@rel="canonical"]/@href')],' '.join(doc.xpath('//meta[@name="robots" or @name="googlebot"]/@content')).lower()
    with ThreadPoolExecutor(max_workers=4) as pool:
        emitted={}
        for count,(url,canonical,robots) in enumerate(pool.map(metadata,sorted(new_html)),1):
            emitted[url]=(canonical,robots)
            if count%5000==0:print(f'Validated metadata {count}/{len(new_html)}',flush=True)
    def sitemap_set(files,baseline=False):
        result=set()
        for p in sorted(files):
            if not (p=='sitemap.xml' or p.startswith('sitemaps/') and p.endswith('.xml')):continue
            doc=ET.fromstring(baseline_blobs[p] if baseline else (ROOT/p).read_bytes())
            if doc.tag.rsplit('}',1)[-1]!='urlset':continue
            for node in doc.findall('.//{*}url/{*}loc'):
                value=(node.text or '').strip()
                assert value not in result,'Duplicate sitemap URL: '+value
                result.add(value)
        return result
    old_urls=sitemap_set(before,True);new_urls=sitemap_set(after)
    assert old_urls==new_urls and len(new_urls)==release['sitemap_urls_after']==35195
    for url in new_urls:
        assert url in emitted and emitted[url][0]==[url] and 'noindex' not in emitted[url][1], 'Invalid full-site sitemap target: '+url
    protected=json.loads((ROOT/'.github/releases/protected-urls.json').read_text(encoding='utf-8'))
    assert len(protected)==len(set(protected))==975
    assert sum(url in emitted for url in protected)==954
    assert all(BASE_URL+urlsplit(url).path.rstrip('/')+'/' in emitted for url in protected)
    assert (ROOT/'index.html').read_bytes().replace(b'\r\n',b'\n')==baseline_blobs['index.html'], 'Unapproved homepage refresh'
    report={'status':'passed','production_base':base,'tested_source_sha':release['tested_source_sha'],'changed_public_files':len(declared),'changed_html':len(changed_docs),'html_before':len(old_html),'html_after':len(new_html),'sitemap_urls':len(new_urls),'protected_sample':975,'existing_url_deletions':0,'canonical_script_form_robots_changes':0,'new_downloads':release['new_urls']}
    (ROOT/'release-qa-result.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--index',action='store_true')
    args=parser.parse_args();main(args.source,args.index)
