"""Refresh an already audited full candidate using production generators/components.

The completed canary is copied last for its contracted routes. No live checkout is
written here. The release packager independently compares the resulting corpus
to the exact production base and retains production-only paths.
"""
import os
import sys
import re
import json
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def main():
    output = Path(sys.argv[1]).resolve()
    canary = Path(sys.argv[2]).resolve()
    for folder in (output, canary):
        folder.relative_to((ROOT/'artifacts/builds').resolve())
        if not (folder/'BUILD-MANIFEST.json').is_file(): raise ValueError('Completed build required')
    os.environ.update(UKPG_BUILD_MODE='full', UKPG_OUTPUT_DIR=str(output))
    from generators.site_core import generate_site_core
    from generators.homepage import generate_homepage
    from generators.upgrade_pages import _canonical_alias_html, _apply_static_redirect_bridges, generate_data_asset_pages, generate_monetisation_pages, generate_phase_zero_update
    from utils.route_contracts import route_contract_for_legacy_path
    from components.upgrade_components import build_sticky_action_bar, build_save_export_cta
    from utils.production_content import assert_publishable
    from utils.build_provenance import source_fingerprint
    from scripts.site_content_qa import audit_rule_data
    from data.loaders import load_projects, load_councils
    from html import unescape
    audit_rule_data()
    generate_homepage()
    generate_site_core(countries={'wales','scotland'})
    changed_routes = set()
    councils = load_councils()
    for project in load_projects():
        for nation in ('wales','scotland'):
            for council in councils.get(nation, []):
                route = f"/{project['slug']}/{nation}/{council['town_slug']}/"
                changed_routes.add(route)
                source = output/route.strip('/')/'index.html'
                contract = route_contract_for_legacy_path(route)
                if contract and contract.canonical_path != route:
                    target = output/contract.canonical_path.strip('/')/'index.html'
                    if target.is_file(): target.write_text(_canonical_alias_html(source,contract),encoding='utf-8')
    _apply_static_redirect_bridges(only_paths=changed_routes)
    generate_data_asset_pages()
    generate_monetisation_pages()
    generate_phase_zero_update()
    # Copy the fully tested contracted pages and assets; preserve full sitemaps.
    for folder,_,names in os.walk(canary):
        for name in names:
            source = Path(folder)/name
            rel = source.relative_to(canary)
            if source.suffix == '.html' or rel.parts[0] == 'assets':
                target = output/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(source,target)
    # Production generator refresh for shared UI present across all page families.
    template = (ROOT/'templates/base.html').read_text(encoding='utf-8')
    action = re.compile(r'  function handleRouteAction\(eventName, node\) \{.*?(?=  function safeStorageGet)',re.S)
    new_action = action.search(template)[0]
    email_handler = re.compile(r'  document.querySelectorAll\("form\[data-static-submit[^\n]+.*?(?=  function emitGaEvent)', re.S)
    new_email_handler = email_handler.search(template)[0]
    sticky = re.compile(r'<div class="sticky-action-bar"[^>]*>.*?</div>',re.S)
    cta = re.compile(r'<section class="route-retention-cta"[^>]*>.*?</section>',re.S)
    def refresh_cta(match):
        html = match[0]
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', html.split('>',1)[0]))
        return build_save_export_cta(page_family=attrs.get('data-page-family',''),country=attrs.get('data-country',''),
            project_slug=attrs.get('data-project-slug',''),authority_slug=attrs.get('data-authority-slug','')).strip()
    def refresh(page):
        html = page.read_text(encoding='utf-8')
        if '</html>' not in html[-1000:].lower(): raise ValueError(f'Incomplete page: {page}')
        updated = action.sub(lambda _:new_action, html)
        updated = email_handler.sub(lambda _:new_email_handler, updated)
        updated = sticky.sub(lambda _:build_sticky_action_bar().strip(),updated)
        updated = cta.sub(refresh_cta,updated)
        assert_publishable(updated,'/'+page.relative_to(output).as_posix())
        if updated != html:
            temp = page.with_suffix('.html.repair.tmp')
            temp.write_text(updated,encoding='utf-8')
            temp.replace(page)
        return updated != html
    pages = [Path(folder)/name for folder,_,names in os.walk(output) for name in names if name.endswith('.html')]
    changed = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        for count,result in enumerate(pool.map(refresh,pages),1):
            changed += result
            if count % 2000 == 0: print(f'Checked {count}/{len(pages)} pages',flush=True)
    report = {'scanned':len(pages),'changed':changed,'content_qa':'passed','source_fingerprint':source_fingerprint(ROOT)}
    (ROOT/'artifacts/repair-release-refresh.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report),flush=True)

if __name__ == '__main__': main()
