"""Fail objective pilot errors; sitewide debt remains a separate blocking report."""
import csv
import gzip
import json
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from lxml import html
from repair_pilot import ROOT, PILOT

def rows(path):
    opener=gzip.open if path.suffix=='.gz' else open
    with opener(path,'rt',newline='') as stream: return list(csv.DictReader(stream))

def main():
    errors=[]
    for key in PILOT:
        url='https://ukplanningguide.co.uk/'+key+'/'
        doc=html.parse(str(ROOT/key/'index.html'))
        if doc.xpath('//link[@rel="canonical"]/@href') != [url]:
            errors.append(key+': canonical contradiction')
        for href in doc.xpath('//a/@href|//script/@src|//img/@src|//link/@href'):
            target=urlsplit(urljoin(url,href))
            if target.netloc=='ukplanningguide.co.uk' and not (ROOT/unquote(target.path).lstrip('/')).exists():
                errors.append(key+': missing '+target.path)
    baseline=ROOT/'reports/baseline/pages.csv.gz'
    if baseline.exists():
        protected=[r for r in rows(baseline) if r['protected']=='1']
        for row in protected:
            path=urlsplit(row['url']).path.lstrip('/')
            if not (ROOT/path/'index.html').exists(): errors.append('Protected route removed: '+row['url'])
    if errors: raise SystemExit('\n'.join(errors))
    print('PASS: pilot canonicals, local links/assets and protected route presence. Not a sitewide release approval.')

if __name__=='__main__': main()
