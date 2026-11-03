import importlib.util
import subprocess
import unittest
from unittest.mock import patch
from pathlib import Path
from lxml import html
from components.project_checklists import CHECKLISTS, download_text, render_checklist

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('repair',ROOT/'scripts/repair_pilot.py')
repair=importlib.util.module_from_spec(spec)
spec.loader.exec_module(repair)

BASELINE = 'bb01d67fc58f21400dffbf449604ee05d561abbc'
PRESERVED_QUERIES = (
    '//script/@src', '//form/@action', '//link[@rel="canonical"]/@href',
)


def baseline_page(path):
    # An unavailable historical commit is a checkout defect, never a new route.
    commit = subprocess.run(
        ['git', 'cat-file', '-e', BASELINE + '^{commit}'], cwd=ROOT,
        capture_output=True,
    )
    if commit.returncode:
        raise RuntimeError('Production baseline unavailable; fetch history (checkout fetch-depth: 0).')
    return html.fromstring(subprocess.check_output(
        ['git', 'show', BASELINE + ':' + path], cwd=ROOT,
    ))


class PilotTests(unittest.TestCase):
    def assert_preserved(self, old, new):
        for query in PRESERVED_QUERIES:
            self.assertEqual(old.xpath(query), new.xpath(query), query)

    def test_missing_history_is_an_error_not_a_new_route(self):
        with patch.object(subprocess, 'run', return_value=subprocess.CompletedProcess([], 1)):
            with self.assertRaisesRegex(RuntimeError, 'fetch history'):
                baseline_page('planning-permission/flintshire/index.html')

    def test_recovered_project_guides_and_downloads_match_source(self):
        for slug in CHECKLISTS:
            with self.subTest(slug=slug):
                raw = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
                self.assertIn(render_checklist(slug), raw)
                self.assertEqual(len(html.fromstring(raw).xpath(
                    '//*[@id="project-evidence-checklist"]')), 1)
                self.assertEqual(
                    (ROOT / 'downloads' / (slug + '-survey.txt')).read_text(encoding='utf-8'),
                    download_text(slug),
                )

    def test_repair_idempotence_and_contract(self):
        for key,data in repair.PILOT.items():
            with self.subTest(key=key):
                raw=(ROOT/key/'index.html').read_text()
                self.assertEqual(raw,repair.repaired(raw,key,data))
                doc=html.fromstring(raw)
                panels=doc.xpath('//*[@id="intent-research-pilot"]')
                self.assertEqual(len(panels),1)
                self.assertEqual(panels[0].get('data-evidence-status'),'unverified')
                self.assertEqual(panels[0].get('data-jurisdiction'),data[0])
                self.assertEqual(len(doc.xpath('//h1')),1)
                self.assertNotIn('The live issue is usually conservation areas.',raw)
                self.assertNotIn('Last reviewed 5 April 2026',raw)
    def test_repair_preserves_scripts_forms_and_canonical(self):
        # All five routes, including Flintshire, exist at the real main baseline.
        # Do not silently drop paths when git show fails in a shallow checkout.
        for key in repair.PILOT:
            with self.subTest(key=key):
                path=key+'/index.html'
                self.assert_preserved(baseline_page(path), html.parse(str(ROOT/path)))

    def test_preservation_detects_script_form_and_canonical_mutations(self):
        fixture = ('<html><head><link rel="canonical" href="https://example.test/new/">'
                   '<script src="/assets/app.js"></script></head><body>'
                   '<form action="/submit"></form></body></html>')
        for selector, attribute in (
            ('//script', 'src'), ('//form', 'action'),
            ('//link[@rel="canonical"]', 'href'),
        ):
            for mutation in ('change', 'remove', 'add'):
                with self.subTest(selector=selector, mutation=mutation):
                    old, new = html.fromstring(fixture), html.fromstring(fixture)
                    node = new.xpath(selector)[0]
                    if mutation == 'change':
                        node.set(attribute, '/unexpected')
                    elif mutation == 'remove':
                        node.getparent().remove(node)
                    else:
                        node.getparent().append(html.fromstring(html.tostring(node)))
                    with self.assertRaises(AssertionError):
                        self.assert_preserved(old, new)

    def test_new_route_repair_contract_without_historical_comparison(self):
        # Synthetic, deliberately new route: no Git fallback or publication.
        key = 'planning-permission/new-route-fixture'
        raw = ('<html><head><link rel="canonical" href="https://example.test/new/">'
               '<script src="/assets/app.js"></script></head><body><h1>New route</h1>\n'
               '<form action="/submit"></form></body></html>')
        data = ('wales', 'Research required', 'Local coverage remains unverified.',
                ['Ask the authority to confirm the proposed work.'])
        output = repair.repaired(raw, key, data)
        doc = html.fromstring(output)
        self.assert_preserved(html.fromstring(raw), doc)
        self.assertEqual(output, repair.repaired(output, key, data))
        self.assertEqual(len(doc.xpath('//h1')), 1)
        panels = doc.xpath('//*[@id="intent-research-pilot"]')
        self.assertEqual(len(panels), 1)
        self.assertEqual(panels[0].get('data-jurisdiction'), 'wales')
        self.assertEqual(panels[0].get('data-evidence-status'), 'unverified')
    def test_nations_do_not_inherit_thresholds(self):
        for nation in ('england','wales','scotland','northern-ireland'):
            for project in ('hmos','garden-rooms','driveways','fences-and-walls','solar-panels'):
                for topic in ('planning-permission','maximum-height','article-4'):
                    output=repair.render(nation,'Research required','No property determination has been made.',[f'Confirm {project} and {topic} with the authority.'])
                    self.assertNotRegex(output,r'\d+\s*(?:m²|metres|meters)')
                    self.assertIn('data-jurisdiction="'+nation+'"',output)

if __name__=='__main__': unittest.main()
