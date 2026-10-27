"""Check every generated HTML link/asset and sitemap member in a static release."""
import sys
import re
import os
import json
from pathlib import Path
from html import unescape
from urllib.parse import urlsplit, unquote, urljoin
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.production_content import content_errors

def audit(root):
    root = Path(root).resolve()
    files = {str((Path(folder)/name).relative_to(root)).replace('\\','/') for folder,_,names in os.walk(root) for name in names if '.git' not in Path(folder).parts}
    html_files = sorted(p for p in files if p.endswith('.html'))
    refs = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']',re.I)
    def resolve(url):
        rel = unquote(urlsplit(url).path).lstrip('/')
        if not rel or rel.endswith('/'): rel += 'index.html'
        if rel in files: return rel
        if rel+'/index.html' in files: return rel+'/index.html'
        return None
    def check(rel):
        html = (root/rel).read_text(encoding='utf-8')
        errors = []
        base = 'https://ukplanningguide.co.uk/'+rel
        for ref in set(refs.findall(html)):
            ref = unescape(ref)
            if not ref or ref.startswith(('#','mailto:','tel:','data:','javascript:')): continue
            url = urljoin(base,ref)
            if urlsplit(url).netloc not in ('ukplanningguide.co.uk','www.ukplanningguide.co.uk'): continue
            if not resolve(url): errors.append({'page':rel,'target':ref})
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"',html)
        return errors, {'canonical': canonical[1] if canonical else None,
                        'noindex': bool(re.search(r'<meta name="robots" content="[^"]*noindex',html)),
                        'content_errors': content_errors(html, '/'+rel)}
    failures = []
    metadata = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i,(errors,details) in enumerate(pool.map(check,html_files),1):
            metadata[html_files[i-1]] = details
            failures.extend(errors)
            if i % 5000 == 0: print(f'Link check {i}/{len(html_files)}',flush=True)
    sitemap_errors = []
    for rel in files:
        if rel.endswith('.xml') and 'sitemap' in rel:
            doc = ET.parse(root/rel)
            if not doc.getroot().tag.endswith('urlset'): continue
            for node in doc.findall('{*}url/{*}loc'):
                target = resolve(node.text)
                if not target: sitemap_errors.append({'sitemap':rel,'url':node.text,'error':'missing'})
                else:
                    details = metadata[target]
                    canonical = details['canonical']
                    if details['noindex']: error='noindex'
                    elif canonical and canonical.rstrip('/') != node.text.rstrip('/'): error='noncanonical'
                    else: continue
                    sitemap_errors.append({'sitemap':rel,'url':node.text,'error':error})
    content_failures = [{'page':p, 'errors':d['content_errors']} for p,d in metadata.items() if d['content_errors']]
    report = {'html_count':len(html_files),'broken_links':failures,'sitemap_errors':sitemap_errors,'content_errors':content_failures}
    print(json.dumps({'html_count':len(html_files),'broken_link_count':len(failures),'sitemap_error_count':len(sitemap_errors),'content_error_count':len(content_failures)}))
    return report

if __name__ == '__main__':
    report = audit(sys.argv[1])
    Path(sys.argv[2]).write_text(json.dumps(report,indent=2),encoding='utf-8')
    sys.exit(bool(report['broken_links'] or report['sitemap_errors'] or report['content_errors']))
