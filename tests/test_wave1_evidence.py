"""Negative evidence fixtures never establish planning rights or public routes."""
from copy import deepcopy
import json
import unittest
from core.paths import ROOT
from utils.claim_evidence import (validate_record_evidence, validate_source_propositions,
                                 validate_evidence_migration)
from utils.content_contracts import ContractError, load_page_records
from utils.source_registry import source_registry_by_id, validate_page_source_links
from utils.trust_status import trust_status


class Wave1EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.records = deepcopy(list(load_page_records()))
        self.registry = deepcopy(source_registry_by_id())
        self.page = next(p for p in self.records if p['route_path'] == '/wales/projects/dropped-kerbs/cardiff/')
        self.claim = next(c for c in self.page['claims'] if c['evidence_status'] == 'verified')
        ref = self.claim['evidence_refs'][0]
        self.source = self.registry[ref['source_id']]
        self.prop = next(p for p in self.source['propositions'] if p['proposition_id'] == ref['proposition_id'])

    def reject(self):
        with self.assertRaises(ContractError):
            validate_record_evidence(self.page, self.registry)

    def test_actual_primary_cohort_and_existing_local_floors(self):
        validate_page_source_links()
        cohort = [p for p in self.records if p.get('evidence_version') == 1]
        self.assertEqual(len(cohort), 5)
        self.assertEqual({p['jurisdiction'] for p in cohort}, {'england', 'wales', 'scotland'})
        for page in cohort:
            validate_record_evidence(page, self.registry)

    def test_wrong_nation_and_uk_fallback(self):
        for nation in ['england', 'scotland', 'northern-ireland', 'uk']:
            with self.subTest(nation=nation):
                self.source['jurisdiction'] = self.prop['scope']['jurisdiction'] = nation
                self.reject()

    def test_wrong_project(self):
        self.prop['scope']['project_ids'] = ['garden-rooms']
        self.reject()

    def test_wrong_rule(self):
        self.prop['scope']['rule_ids'] = ['article-4']
        self.reject()

    def test_wrong_authority(self):
        self.source['authority_id'] = self.prop['scope']['authority_id'] = 'swansea'
        self.reject()

    def test_missing_source_and_proposition(self):
        ref = self.claim['evidence_refs'][0]
        self.registry.pop(ref['source_id'])
        self.reject()
        self.registry = deepcopy(source_registry_by_id())
        ref['proposition_id'] = 'absent-proposition'
        self.reject()

    def test_edited_text_cannot_inherit_evidence(self):
        self.claim['text'] += ' A 4 metre driveway is automatically permitted.'
        self.reject()

    def test_unavailable_source_or_unverified_proposition(self):
        self.source['status'] = 'unavailable'
        self.reject()
        self.source['status'] = 'active'
        self.prop['verification_status'] = 'unverified'
        self.reject()

    def test_no_invented_future_dates_or_professional_reviewer(self):
        for field, value in [('checked_at', '2999-01-01'), ('checked_at', '2026-02-30'),
                             ('checked_by', 'chartered-planner')]:
            before = self.prop[field]
            self.prop[field] = value
            self.reject()
            self.prop[field] = before
        self.page['reviewer_name'] = 'Invented reviewer'
        self.reject()

    def test_historical_count_must_retain_date(self):
        source = next(s for s in self.registry.values() if any(p['kind'] == 'historical_context' for p in s.get('propositions', [])))
        prop = next(p for p in source['propositions'] if p['kind'] == 'historical_context')
        prop['text'] = 'The council has 25 conservation areas.'
        with self.assertRaises(ContractError):
            validate_source_propositions(source)

    def test_article4_cannot_claim_property_applicability_from_general_guidance(self):
        self.prop['kind'] = self.claim['kind'] = 'article4_applicability'
        self.reject()

    def test_unresolved_site_question_stays_unknown(self):
        claim = next(c for c in self.page['claims'] if c['evidence_status'] == 'unverified')
        claim['text'] = 'A 4 metre driveway is allowed.'
        self.reject()

    def test_northern_ireland_unsupported_fixture_has_no_english_answer(self):
        fixture = deepcopy(self.page)
        fixture.update(route_path='/northern-ireland/projects/dropped-kerbs/test-only/',
                       jurisdiction='northern-ireland', jurisdiction_support='unsupported',
                       index_status='noindex', verified_at=None, source_ids=[], unique_local_facts=[])
        fixture['claims'] = [dict(claim_id='unknown', text='Planning rights are not verified for this unsupported jurisdiction.',
                                 source_ids=[], kind='unresolved_check', evidence_status='unverified', evidence_refs=[])]
        validate_record_evidence(fixture, self.registry)
        fixture['claims'] = [deepcopy(self.claim)]
        with self.assertRaises(ContractError):
            validate_record_evidence(fixture, self.registry)

    def test_legacy_date_does_not_verify_claims(self):
        legacy = next(p for p in self.records if p.get('confidence') == 'high' and p.get('evidence_version') != 1)
        self.assertEqual(trust_status(legacy).verification, 'historical')
        self.assertEqual(trust_status(legacy).confidence, 'not assessed')

    def test_changed_or_new_legacy_record_requires_migration(self):
        validate_evidence_migration(self.records)
        legacy = next(p for p in self.records if p.get('evidence_version') != 1)
        legacy['content_updated_at'] = '2026-11-07'
        with self.assertRaises(ContractError):
            validate_evidence_migration(self.records)
        legacy['route_path'] = '/test-only-new-route/'
        with self.assertRaises(ContractError):
            validate_evidence_migration(self.records)

    def test_capture_digest_is_required_and_official_host_cannot_be_spoofed(self):
        self.prop['capture_sha256'] = 'not-a-hash'
        self.reject()
        self.prop['capture_sha256'] = 'a' * 64
        self.source['url'] = 'https://gov.wales.example.com/fake'
        self.reject()

    def test_alias_date_gate_still_rejects_missing_canonical_content_date(self):
        import shutil
        import tempfile
        from pathlib import Path
        from utils.phase0_validation import validate_phase0_canary
        source = ROOT / 'artifacts/phase-0-canary-site'
        self.assertTrue(source.is_dir(), 'Build the canary before running all gates')
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'site'
            shutil.copytree(source, output)
            page = output / 'councils/colchester/index.html'
            updated = next(p['content_updated_at'] for p in self.records if p['route_path'] == '/england/councils/colchester/')
            page.write_text(page.read_text(encoding='utf-8').replace(updated, '1999-01-01'), encoding='utf-8')
            errors = validate_phase0_canary(output, baseline_dir=ROOT)['errors']
            self.assertTrue(any(e['route'] == '/councils/colchester/' and e['code'] == 'date-mismatch' for e in errors))


if __name__ == '__main__':
    unittest.main()
