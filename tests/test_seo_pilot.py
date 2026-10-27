import importlib.util
import unittest
from pathlib import Path
from lxml import html

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('repair',ROOT/'scripts/repair_pilot.py')
repair=importlib.util.module_from_spec(spec)
spec.loader.exec_module(repair)

class PilotTests(unittest.TestCase):
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
        import subprocess
        for key in repair.PILOT:
            path=key+'/index.html'
            old=html.fromstring(subprocess.check_output(['git','show','bb01d67fc58f21400dffbf449604ee05d561abbc:'+path],cwd=ROOT))
            new=html.parse(str(ROOT/path))
            for query in ('//script/@src','//form/@action','//link[@rel="canonical"]/@href'):
                self.assertEqual(old.xpath(query),new.xpath(query))
    def test_nations_do_not_inherit_thresholds(self):
        for nation in ('england','wales','scotland','northern-ireland'):
            for project in ('hmos','garden-rooms','driveways','fences-and-walls','solar-panels'):
                for topic in ('planning-permission','maximum-height','article-4'):
                    output=repair.render(nation,'Research required','No property determination has been made.',[f'Confirm {project} and {topic} with the authority.'])
                    self.assertNotRegex(output,r'\d+\s*(?:m²|metres|meters)')
                    self.assertIn('data-jurisdiction="'+nation+'"',output)

if __name__=='__main__': unittest.main()
