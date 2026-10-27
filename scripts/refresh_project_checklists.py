"""Refresh four existing project guides and their text downloads; no new HTML routes."""
import re
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from components.project_checklists import CHECKLISTS, render_checklist, download_text

ROOT=Path(__file__).resolve().parents[1]
for slug in CHECKLISTS:
    path=ROOT/slug/'index.html'
    content=path.read_text()
    content=re.sub(r'\n<section id="project-evidence-checklist".*?</section>\n','',content,flags=re.S)
    content=content.replace('</h1>','</h1>'+render_checklist(slug),1)
    path.write_text(content)
    (ROOT/'downloads'/f'{slug}-survey.txt').write_text(download_text(slug))
print('Refreshed 4 protected project guides and 4 reusable text checklists')
