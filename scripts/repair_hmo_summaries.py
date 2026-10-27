"""Render the corrected recovered-generator summary into existing HMO routes only."""
import argparse
import re
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from components.scenario_sections import build_your_situation_summary
from data.loaders import load_councils

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    count=0
    for county,councils in load_councils().items():
        for council in councils:
            path=ROOT/'hmos'/county/council['town_slug']/'article-4/index.html'
            if not path.exists(): continue
            raw=path.read_text()
            summary=build_your_situation_summary('HMO','change-of-use','Article 4',council['town_name'],county,{},'article-4')
            updated,n=re.subn(r'\n<section class="situation-summary" id="scenario-summary"[^>]*>.*?</section>\n',lambda m:summary,raw,count=1,flags=re.S)
            if n!=1: raise SystemExit(f'Missing summary: {path}')
            if raw!=updated:
                count+=1
                if not args.check: path.write_text(updated)
    if args.check and count: raise SystemExit(f'{count} stale summaries')
    print(f'HMO Article 4 summaries updated: {count}')

if __name__=='__main__': main()
