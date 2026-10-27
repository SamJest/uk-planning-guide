"""Date only the genuinely edited correction cohort; never date source research."""
import re
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from components.project_checklists import CHECKLISTS
from data.loaders import load_councils

ROOT=Path(__file__).resolve().parents[1]
paths=[ROOT/slug/'index.html' for slug in CHECKLISTS]
for county,councils in load_councils().items():
    for council in councils:
        path=ROOT/'hmos'/county/council['town_slug']/'article-4/index.html'
        if path.exists(): paths.append(path)
urls=set()
for path in paths:
    content=path.read_text()
    content=re.sub(r'("dateModified"\s*:\s*")[^"]+(" )',r'\g<1>2026-10-27\2',content)
    content=re.sub(r'("dateModified"\s*:\s*")[^"]+(")',r'\g<1>2026-10-27\2',content)
    content=re.sub(r'(<strong>Content updated</strong> )[^<]+',r'\g<1>27 October 2026',content)
    content=re.sub(r'(<div class=[\"\x27]last-updated[\"\x27]>)[^<]+',r'\g<1>Editorial content updated 27 October 2026; local verification unchanged',content)
    path.write_text(content)
    urls.add('https://ukplanningguide.co.uk/'+path.relative_to(ROOT).as_posix()[:-10])
entries=0
for path in (ROOT/'sitemaps').glob('*.xml'):
    content=path.read_text()
    def update(match):
        global entries
        block=match[0]
        location=re.search(r'<loc>(.*?)</loc>',block)
        if location and location[1] in urls:
            entries+=1
            if '<lastmod>' in block:
                return re.sub(r'<lastmod>.*?</lastmod>','<lastmod>2026-10-27</lastmod>',block)
            return block.replace('</url>','<lastmod>2026-10-27</lastmod></url>')
        return block
    updated=re.sub(r'<url>.*?</url>',update,content,flags=re.S)
    if content!=updated: path.write_text(updated)
print(f'Editorial dates refreshed on {len(paths)} pages and {entries} sitemap records; no source-check dates altered')
