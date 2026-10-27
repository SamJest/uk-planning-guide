#!/usr/bin/env python3
"""Fail on structurally unsupported official verification claims; no internet requests."""
import argparse,json,sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REQUIRED=('claim_id','jurisdiction','topic','claim','evidence_status')
JURIS={'england','wales','scotland','northern-ireland','uk','not-applicable'}
STATUS={'verified_primary','verified_secondary','unverified','superseded'}


def validate(data):
    issues=[]; ids=set()
    if not isinstance(data,list):return ['Top-level JSON must be a list of claim records']
    for i,r in enumerate(data,1):
        if not isinstance(r,dict):issues.append(f'[{i}] Not a JSON object');continue
        for k in REQUIRED:
            if not isinstance(r.get(k),str) or not r[k].strip():issues.append(f'[{i}] Missing {k}')
        if r.get('claim_id') in ids:issues.append(f'[{i}] Duplicate claim ID {r.get("claim_id")}')
        ids.add(r.get('claim_id'))
        if r.get('jurisdiction') not in JURIS:issues.append(f'[{i}] Illegal jurisdiction')
        if r.get('evidence_status') not in STATUS:issues.append(f'[{i}] Illegal evidence_status')
        if r.get('evidence_status') in ('verified_primary','verified_secondary'):
            for k in ('source_url','source_title','source_publisher','source_location','verified_at'):
                if not r.get(k):issues.append(f'[{i}] Verified claim lacks {k}')
            if r.get('source_url'):
                u=urlparse(r['source_url'])
                if u.scheme!='https' or not u.netloc:issues.append(f'[{i}] Source URL must be HTTPS with hostname')
        for k in ('source_published','source_effective','verified_at'):
            if r.get(k):
                try:date.fromisoformat(r[k])
                except (ValueError,TypeError):issues.append(f'[{i}] Invalid ISO date {k}')
    return issues

def main():
    a=argparse.ArgumentParser();a.add_argument('--input',required=True);x=a.parse_args()
    try:data=json.loads(Path(x.input).read_text(encoding='utf8'))
    except Exception as ex:print(f'Unable to read JSON: {ex}');sys.exit(2)
    errors=validate(data)
    if errors:
        for err in errors:print('FAIL:',err)
        sys.exit(1)
    print(f'PASS: {len(data)} evidence records schema/required-provenance checks. NOTE: this cannot verify claim truth.')
if __name__=='__main__':main()
