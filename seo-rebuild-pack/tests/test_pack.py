"""Smoke tests: the packaged scripts work without the user's actual repo."""
import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def mod(n):
    sp=importlib.util.spec_from_file_location(n,ROOT/'scripts'/f'{n}.py')
    x=importlib.util.module_from_spec(sp);sp.loader.exec_module(x)
    return x

class PackTests(unittest.TestCase):
    def test_url_normalization(self):
        x=mod('audit_static_build')
        self.assertEqual(x.normalise('https://ukplanningguide.co.uk/foo/index.html'), 'https://ukplanningguide.co.uk/foo/')
        self.assertEqual(x.normalise('https://ukplanningguide.co.uk/foo?x=tracking'), 'https://ukplanningguide.co.uk/foo/')

    def test_evidence_checks(self):
        x=mod('validate_evidence')
        self.assertEqual(x.validate(json.loads((ROOT/'data/templates/evidence_registry_example.json').read_text())),[])
        bad=[{'claim_id':'A','jurisdiction':'england','topic':'rule','claim':'Allowed', 'evidence_status':'verified_primary'}]
        self.assertTrue(any('source_url' in e for e in x.validate(bad)))

    def test_proposed_route_retirement_requires_approval(self):
        x=mod('check_migration_decisions')
        bad=[{'from_url':'https://ukplanningguide.co.uk/foo/', 'to_url':'https://ukplanningguide.co.uk/bar/', 'proposed_action':'MERGE_REDIRECT','reason':'dup','reviewer':'UNREVIEWED','traffic_clicks':'UNKNOWN','backlinks_known':'UNKNOWN','approved_at':''}]
        self.assertGreater(len(x.check(bad)),0)

    def test_generated_build_audits_and_detects_duplication(self):
        x=mod('audit_static_build')
        with tempfile.TemporaryDirectory() as td:
            r=Path(td)/'public';out=Path(td)/'audit'
            p1=r/'england'/'councils'/'colchester'/'index.html'
            p2=r/'councils'/'colchester'/'index.html'
            p1.parent.mkdir(parents=True);p2.parent.mkdir(parents=True)
            maintext='Planning case evidence sources and qualifications. '*35
            def page(can):return f'<html><head><title>Colchester Planning</title><link rel="canonical" href="{can}"></head><body><main><h1>Colchester planning</h1><p>{maintext}</p></main><a href="/england/councils/colchester/">Click</a></body></html>'
            p1.write_text(page('https://ukplanningguide.co.uk/england/councils/colchester/'))
            p2.write_text(page('https://ukplanningguide.co.uk/england/councils/colchester/'))
            (r/'sitemap.xml').write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://ukplanningguide.co.uk/england/councils/colchester/</loc></url><url><loc>https://ukplanningguide.co.uk/councils/colchester/</loc></url></urlset>')
            summary=x.run_audit(r,out,'https://ukplanningguide.co.uk/')
            self.assertEqual(summary['html_emitted'],2)
            self.assertEqual(summary['exact_duplicate_groups'],1)
            self.assertGreater(summary['sitemap_violations'],0)
            y=mod('enforce_release_gate')
            errs,_,_=y.run_gate(out,out)
            self.assertTrue(any('sitemap' in e for e in errs))

if __name__=='__main__':unittest.main()

class RegistryGateTests(unittest.TestCase):
    def test_duplicate_intent_is_failed(self):
        x=mod('validate_page_registry')
        def rec(url):
            return {'url':url,'intent_key':'england|colchester|article4','disposition':'KEEP_ENRICH','canonical':url,'indexable':'1','in_sitemap':'1','page_type':'local_article4','verified_local_source_count':'1','approved_distinct_utility':'0'}
        errors,summary=x.run([rec('https://ukplanningguide.co.uk/article-4/colchester/'),rec('https://ukplanningguide.co.uk/local-search/article4-colchester/')])
        self.assertEqual(summary['duplicate_intent_groups'],1)
        self.assertTrue(any('duplicate intent' in e for e in errors))

    def test_reject_unverified_local_doorway(self):
        x=mod('validate_page_registry')
        row={'url':'https://ukplanningguide.co.uk/local-search/article4-town/','intent_key':'england|town|article4','disposition':'KEEP_DISTINCT','canonical':'https://ukplanningguide.co.uk/local-search/article4-town/','indexable':'1','in_sitemap':'1','page_type':'local_article4','verified_local_source_count':'0','approved_distinct_utility':'0'}
        errors,_=x.run([row]);self.assertTrue(any('verified distinguishing evidence' in e for e in errors))
