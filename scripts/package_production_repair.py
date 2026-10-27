"""Prepare a hash-bound normal-commit release against the exact production base."""
import sys
import os
import json
import hashlib
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from utils.production_content import assert_publishable
from utils.build_provenance import source_fingerprint
from scripts.site_content_qa import audit_rule_data

def main(candidate, release, expected_base):
    candidate,release = Path(candidate).resolve(),Path(release).resolve()
    candidate.relative_to((ROOT/'artifacts/builds').resolve())
    release.relative_to((ROOT/'artifacts').resolve())
    base = subprocess.check_output(['git','-C',str(release),'rev-parse','HEAD'],text=True).strip()
    if base != expected_base: raise ValueError('Production base changed')
    if subprocess.check_output(['git','-C',str(release),'status','--porcelain'],text=True).strip():
        raise ValueError('Release checkout must be clean before packaging')
    audit_rule_data()
    pages_before = subprocess.check_output(['git','-C',str(release),'ls-tree','-r','--name-only','HEAD'],text=True).splitlines()
    paths = [Path(folder)/name for folder,_,names in os.walk(candidate) for name in names if name != 'BUILD-MANIFEST.json' and not name.endswith('.tmp')]
    changes = []
    def copy(source):
        rel = source.relative_to(candidate)
        target = release/rel
        after = source.read_bytes()
        if source.suffix == '.html': assert_publishable(after.decode('utf-8'),'/'+rel.as_posix())
        before = target.read_bytes() if target.is_file() else None
        # GitHub Pages content is LF; avoid an all-corpus line-ending-only diff.
        if source.suffix in ('.html','.css','.js','.json','.xml','.txt','.svg'):
            after = after.replace(b'\r\n',b'\n')
        if before == after: return None
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(after)
        return {'path':rel.as_posix(),'before_sha256':hashlib.sha256(before).hexdigest() if before is not None else None,
                'after_sha256':hashlib.sha256(after).hexdigest()}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i,result in enumerate(pool.map(copy,paths),1):
            if result: changes.append(result)
            if i%5000==0: print(f'Packaged {i}/{len(paths)} files',flush=True)
    candidate_paths = {p.relative_to(candidate).as_posix() for p in paths}
    retained = sorted(p for p in pages_before if p not in candidate_paths)
    for rel in retained:
        if rel.endswith('.html'): assert_publishable((release/rel).read_text(encoding='utf-8'),'/'+rel)
    html_before = sum(p.endswith('.html') for p in pages_before)
    html_after = sum(p.endswith('.html') for p in set(pages_before)|candidate_paths)
    manifest = {'production_base':base,'source_fingerprint':source_fingerprint(ROOT),
        'html_before':html_before,'html_after':html_after,'html_delta':html_after-html_before,
        'changed_files':changes,'retained_production_files':retained,
        'rollback':'Revert the deployment commit with a normal git revert; never reset or force-push.'}
    (ROOT/'artifacts/repair-release-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'changed':len(changes),'html_before':html_before,'html_after':html_after,'retained':retained}),flush=True)

if __name__ == '__main__': main(*sys.argv[1:])
