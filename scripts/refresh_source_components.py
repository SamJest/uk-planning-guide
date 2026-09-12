"""Incremental regeneration of source components after a completed full build.

Uses the production component and local-page generators, never bespoke page copy.
Only isolated artifacts/builds candidates can be updated with this command.
"""
import os
from pathlib import Path
import sys
import re
import json
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main(output, components_only=False):
    output = Path(output).resolve()
    output.relative_to((ROOT / 'artifacts/builds').resolve())
    os.environ['UKPG_BUILD_MODE'] = 'full'
    os.environ['UKPG_OUTPUT_DIR'] = str(output)
    from generators.scenario_pages import generate_scenario_pages
    from generators.council_pages import generate_council_pages
    from generators.upgrade_pages import _canonical_alias_html, _apply_static_redirect_bridges
    from utils.route_contracts import route_contract_for_legacy_path
    from data.scenario_data import SCENARIOS
    from components.official_sources import build_official_sources_block
    from components.page_authority import infer_page_context
    from utils.production_content import assert_publishable
    from utils.build_provenance import source_fingerprint
    if components_only and not (output / 'BUILD-MANIFEST.json').is_file():
        raise ValueError('A completed candidate build is required before refreshing components only')
    if not components_only:
        generate_scenario_pages()
        generate_council_pages()
    source_prefixes = {'councils'} | {item['slug'] for item in SCENARIOS}
    regenerated = set()
    html_pages = [Path(folder) / name for folder, _, names in os.walk(output)
                  for name in names if name.endswith('.html')]
    for page in ([] if components_only else html_pages):
        relative = page.relative_to(output)
        if relative.parts[0] not in source_prefixes:
            continue
        route = '/' + relative.parent.as_posix().strip('/') + '/'
        regenerated.add(route)
        contract = route_contract_for_legacy_path(route)
        if contract and contract.canonical_path != route:
            target = output / contract.canonical_path.strip('/') / 'index.html'
            if target.exists():
                target.write_text(_canonical_alias_html(page, contract), encoding='utf-8')
    if not components_only:
        _apply_static_redirect_bridges(only_paths=regenerated)
    block = re.compile(r'<section class="official-sources"[^>]*>.*?</section>', re.S)
    def refresh_page(page):
        html = page.read_text(encoding='utf-8')
        if '</html>' not in html[-1000:].lower():
            raise ValueError(f'Incomplete generated page; regenerate before continuing: {page}')
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        context = infer_page_context(canonical[1]) if canonical else {}
        def replace(match):
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', match[0].split('>', 1)[0]))
            return build_official_sources_block(
                page_family=attrs['data-official-sources-family'],
                authority_slug=attrs.get('data-official-sources-authority', ''),
                country_slug=context.get('country_slug', ''),
                project_slug=context.get('project_slug', ''),
                scenario_slug=context.get('scenario_slug', ''),
                section_id=attrs.get('id', 'official-sources'),
                max_links=int(attrs.get('data-official-sources-count', 5)),
            ).strip()
        updated = block.sub(replace, html)
        assert_publishable(updated, '/' + page.relative_to(output).as_posix())
        if updated != html:
            temporary = page.with_suffix('.html.source-refresh.tmp')
            temporary.write_text(updated, encoding='utf-8')
            temporary.replace(page)
            return 1
        return 0
    scanned = changed = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(refresh_page, html_pages):
            changed += result
            scanned += 1
            if scanned % 1000 == 0:
                print(f'Checked {scanned}/{len(html_pages)} pages; refreshed {changed}', flush=True)
    report = {'scanned': scanned, 'changed': changed, 'content_qa': 'passed',
              'source_fingerprint': source_fingerprint(ROOT)}
    (ROOT / 'artifacts/repair-source-refresh.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main(sys.argv[1], components_only='--components-only' in sys.argv[2:])
