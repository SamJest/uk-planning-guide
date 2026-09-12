import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from data.loaders import load_rule
from utils.data_loader import load_national_rules
from utils.jurisdiction_rules import _module, validate_rule_module, verified_local_layer
from utils.production_content import content_errors, audit_output
from utils.trust_status import trust_status, validate_trust_status
from core.render import _render_contract_trust_strip


class JurisdictionTests(unittest.TestCase):
    def test_all_extension_variants_are_isolated(self):
        for nation, town in [('england', 'somerset'), ('wales', 'cardiff'), ('scotland', 'aberdeen-city')]:
            county = 'somerset' if nation == 'england' else nation
            for project in ('house-extensions', 'single-storey-extensions', 'two-storey-extensions', 'rear-extensions', 'side-extensions', 'wraparound-extensions'):
                with self.subTest(nation=nation, project=project):
                    local = load_rule(project, county, town)
                    national = load_national_rules(project, nation)
                    self.assertEqual(local['jurisdiction'], nation)
                    self.assertEqual(national['jurisdiction'], nation)
                    text = json.dumps([local, national])
                    self.assertFalse(content_errors(text, f'/{project}/{nation}/{town}/'))
                    self.assertIn({'england': '7m', 'wales': '10.5m', 'scotland': '10m'}[nation], text)

    def test_missing_module_never_uses_england(self):
        for nation in ('wales', 'scotland', 'northern-ireland'):
            module = load_national_rules('not-a-published-project', nation)
            self.assertEqual(module['availability'], 'unavailable')
            self.assertEqual(module['rules'], {})
        with tempfile.TemporaryDirectory() as tmp:
            _module.cache_clear()
            with patch('utils.jurisdiction_rules.DATA_FOLDER', Path(tmp)):
                self.assertEqual(load_national_rules('house-extensions', 'wales')['availability'], 'unavailable')
            _module.cache_clear()

    def test_missing_or_wrong_jurisdiction_fails(self):
        for record in ({}, {'jurisdiction': 'england'}):
            with self.assertRaises(ValueError):
                validate_rule_module(record, 'wales')
        with self.assertRaises(ValueError):
            load_national_rules('house-extensions', '')
        with self.assertRaises(ValueError):
            load_rule('house-extensions', 'unknown-county', 'test')

    def test_all_published_gb_projects_have_dated_official_guidance(self):
        from data.loaders import load_projects
        for nation in ('wales', 'scotland'):
            for project in load_projects():
                with self.subTest(nation=nation, project=project['slug']):
                    module = load_national_rules(project['slug'], nation)
                    self.assertNotEqual(module.get('availability'), 'unavailable')
                    self.assertTrue(module['rules'])
                    self.assertTrue(module['official_sources'][0]['checked_at'])

    def test_unverified_local_text_cannot_override_baseline(self):
        self.assertEqual(verified_local_layer({'rules': {'depth_rules': '8m'}}, 'wales'), {})
        with self.assertRaises(ValueError):
            verified_local_layer({'jurisdiction': 'england', 'source_url': 'https://example.gov.uk/', 'checked_at': '2026-09-11'}, 'wales')


class ContentQATests(unittest.TestCase):
    def test_national_source_links_are_not_local_facts(self):
        from components.official_sources import build_official_sources_block
        html = build_official_sources_block(page_family='project', authority_slug='cardiff', country_slug='wales', project_slug='house-extensions')
        self.assertNotIn('data-local-fact=', html)
        self.assertNotIn('shows how Cardiff explains', html)
        self.assertIn('data-source-link=', html)
    def test_instruction_patterns_and_input_placeholder(self):
        for phrase in ('Keep this block', 'TODO', 'FIXME:', 'replace this', 'insert here', 'placeholder', 'placeholder text', 'for the project-specific objections'):
            self.assertTrue(content_errors(f'<p>{phrase}</p>'))
        self.assertFalse(content_errors('<input placeholder="Enter dimensions"><p>A placeholder in your own sketch can show the proposed position.</p>'))
        self.assertFalse(content_errors('<h3>What it does not replace</h3><p>This site provides guidance.</p>'))

    def test_leaks_fail_in_both_route_formats(self):
        for nation in ('wales', 'scotland'):
            for path in (f'/{nation}/projects/house-extensions/', f'/house-extensions/{nation}/test/'):
                for text in ("England’s Class A", '8 metres detached and 6 metres other houses with prior approval', '7m from the rear boundary', 'larger home extension'):
                    self.assertTrue(content_errors(f'<p>{text}</p>', path))
        self.assertFalse(content_errors('<p>8m detached with prior approval</p>', '/england/extensions/'))
        self.assertFalse(content_errors('<p>10.5m from the rear boundary; window 1.7m above floor.</p>', '/wales/extensions/'))

    def test_whole_output_including_unsampled_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'index.html').write_text('<p>Fine</p>')
            (root/'hidden.html').write_text('<p>Keep this block</p>')
            with self.assertRaises(ValueError):
                audit_output(root)


class TrustTests(unittest.TestCase):
    def test_all_status_combinations(self):
        for family in ('local_project', 'tool', 'workflow'):
            for verified in (None, '2026-09-11'):
                for confidence in ('low', 'medium', 'high', 'not assessed'):
                    record={'page_family':family, 'verified_at':verified, 'source_ids':['source'] if verified else [], 'confidence':confidence, 'content_updated_at':'2026-09-11'}
                    with self.subTest(record=record):
                        if not verified and confidence=='high':
                            with self.assertRaises(ValueError): validate_trust_status(record)
                        else: validate_trust_status(record)
                        html=_render_contract_trust_strip(record)
                        self.assertFalse(content_errors(html))
                        if family in ('tool','workflow'):
                            self.assertNotIn('<strong>Confidence</strong>',html)
                        if not verified:
                            self.assertNotEqual(trust_status(record).confidence,'high')

    def test_no_independent_reviewer_schema(self):
        from components.page_authority import _person_schema
        from data.authority_profiles import authority_profile
        self.assertIsNone(_person_schema(authority_profile('lead_reviewer'), '/about/'))

    def test_unverified_profiles_do_not_publish_editor_instructions(self):
        from components.page_authority import build_authority_summary_section
        from data.authority_profiles import authority_profile
        profile = authority_profile('lead_author')
        profile['is_placeholder'] = True
        with patch('components.page_authority.authority_profile', return_value=profile):
            html = build_authority_summary_section(section_id='review', title='Editorial process', intro='Source checks')
        self.assertNotIn('Replace the placeholder', html)
        self.assertIn('not yet verified', html)
        self.assertFalse(content_errors(html))

    def test_downloads_are_utility_even_with_legacy_guide_family(self):
        record = {'route_path': '/downloads/', 'page_family': 'national_guide',
                  'verified_at': None, 'source_ids': [], 'confidence': 'not assessed',
                  'content_updated_at': '2026-09-11'}
        self.assertNotIn('<strong>Confidence</strong>', _render_contract_trust_strip(record))
