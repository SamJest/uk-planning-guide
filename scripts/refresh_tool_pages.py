"""Regenerate tool pages and their existing aliases inside an isolated candidate."""
import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
output = Path(sys.argv[1]).resolve()
output.relative_to((ROOT/'artifacts/builds').resolve())
os.environ.update(UKPG_BUILD_MODE='full',UKPG_OUTPUT_DIR=str(output))
from generators.planning_tools import generate_tools
from generators.upgrade_pages import _canonical_alias_html, _apply_static_redirect_bridges
from utils.route_contracts import route_contract_for_legacy_path
generate_tools()
changed = set()
for page in (output/'tools').glob('*/index.html'):
    route = '/' + page.relative_to(output).parent.as_posix() + '/'
    changed.add(route)
    contract = route_contract_for_legacy_path(route)
    if contract and contract.canonical_path != route:
        target = output/contract.canonical_path.strip('/')/'index.html'
        if target.exists(): target.write_text(_canonical_alias_html(page,contract),encoding='utf-8')
_apply_static_redirect_bridges(only_paths=changed)
print(f'Regenerated {len(changed)} tool routes and their existing aliases.')
