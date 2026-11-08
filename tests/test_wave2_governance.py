from copy import deepcopy
from pathlib import Path
import tempfile
import json
import unittest
from core.paths import ROOT
from utils.content_contracts import ContractError, load_page_records, validate_distinct_intents
from utils.intent_registry import intent_key, review_registry
from utils.sitemap_integrity import validate_targets
from utils.url_review import validate_normalization, validate_review_only
from utils.url_registry import url_registry


class IntentGovernanceTests(unittest.TestCase):
    def record(self, route='/article-4/test/'):
        return dict(route_path=route, canonical_path=route, index_status='index', page_family='local_rule',
                    jurisdiction='england', authority_id='test', project_id=None, rule_id='article-4')

    def test_export_has_six_typed_axes_and_deterministic_order(self):
        records=list(load_page_records())
        exported=review_registry(records)
        self.assertEqual(exported,review_registry(list(reversed(records))))
        self.assertEqual(set(exported[0]['intent']), {'jurisdiction','authority_id','project_id','rule_topic','user_question','role'})

    def test_renaming_url_does_not_evade_semantic_collision(self):
        with self.assertRaisesRegex(ContractError,'Duplicate canonical intent'):
            validate_distinct_intents([self.record(),self.record('/local-search/new-keyword-test/')])

    def test_distinct_nation_authority_project_rule_and_role_are_not_false_merges(self):
        original=self.record()
        for field,value in [('jurisdiction','wales'),('authority_id','other'),('project_id','garden-rooms'),
                            ('rule_id','conservation-areas'),('page_family','authority_profile')]:
            with self.subTest(field=field):
                other=self.record('/different/')
                other[field]=value
                validate_distinct_intents([original,other])

    def test_unknown_or_multi_authority_intent_is_rejected(self):
        for field,value in [('jurisdiction','unknown'),('authority_id','one,two'),('page_family','keyword-variant')]:
            record=self.record(); record[field]=value
            with self.assertRaises(ContractError): intent_key(record)

    def test_legacy_bridge_is_a_retained_route_not_an_extra_indexable_intent(self):
        alias=self.record('/legacy/'); alias['canonical_path']='/article-4/test/'
        validate_distinct_intents([self.record(),alias])
        self.assertEqual(len(review_registry([self.record(),alias])),2)

    def test_functional_pages_are_explicit_and_not_exempt_from_exact_collisions(self):
        tool=self.record('/tools/check/'); tool.update(page_family='tool',authority_id=None,rule_id=None,functional_intent_id='route-check')
        other=deepcopy(tool);other.update(route_path='/tools/export/',canonical_path='/tools/export/')
        with self.assertRaises(ContractError): validate_distinct_intents([tool,other])
        other['functional_intent_id']='project-export'
        validate_distinct_intents([tool,other])
        del other['functional_intent_id']
        with self.assertRaises(ContractError): validate_distinct_intents([tool,other])


class SitemapTargetTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.page=self.root/'guide/index.html'
        self.page.parent.mkdir()
        self.url='https://ukplanningguide.co.uk/guide/'
        self.write()

    def write(self,canonical=None,meta=''):
        self.page.write_text(f'<head><link rel="canonical" href="{canonical or self.url}">{meta}</head><main>Guide</main>',encoding='utf-8')

    def test_valid_existing_self_canonical_target_passes(self):
        validate_targets([self.url],self.root,'https://ukplanningguide.co.uk')

    def test_domain_prefix_spoofing_query_fragment_and_slashless_target_fail(self):
        for url in [self.url.replace('.co.uk','.co.uk.evil'),self.url+'?q=1',self.url+'#part',self.url.rstrip('/')]:
            with self.assertRaises(ValueError):validate_targets([url],self.root,'https://ukplanningguide.co.uk')

    def test_absent_target_and_traversal_fail(self):
        for url in ['https://ukplanningguide.co.uk/missing/','https://ukplanningguide.co.uk/%2e%2e/outside/']:
            with self.assertRaises(ValueError):validate_targets([url],self.root,'https://ukplanningguide.co.uk')

    def test_wrong_or_multiple_canonical_fails(self):
        self.write(canonical='https://ukplanningguide.co.uk/other/')
        with self.assertRaises(ValueError):validate_targets([self.url],self.root,'https://ukplanningguide.co.uk')
        self.write(meta=f'<link rel="canonical" href="{self.url}">')
        with self.assertRaises(ValueError):validate_targets([self.url],self.root,'https://ukplanningguide.co.uk')

    def test_robots_googlebot_noindex_and_none_fail(self):
        for name,content in [('robots','NOINDEX, follow'),('googlebot','noindex'),('robots','none')]:
            self.write(meta=f'<meta name="{name}" content="{content}">')
            with self.assertRaises(ValueError):validate_targets([self.url],self.root,'https://ukplanningguide.co.uk')

    def test_duplicate_sitemap_entry_fails(self):
        with self.assertRaises(ValueError):validate_targets([self.url,self.url],self.root,'https://ukplanningguide.co.uk')


class ReviewOnlyEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.card=json.loads((ROOT/'reports/wave-2/protected-url-decisions.json').read_text(encoding='utf-8'))[0]

    def test_actual_normalization_evidence_passes_without_changing_disposition(self):
        before=deepcopy(self.card)
        validate_normalization(self.card)
        self.assertEqual(self.card,before)

    def test_final_200_or_canonical_hint_is_not_an_http_redirect(self):
        for key,value in [('redirect_count',0),('status',404),('effective_url','https://ukplanningguide.co.uk/other/'),
                          ('body_sha256','0'*64),
                          ('header_chain',['HTTP/1.1 200 OK'])]:
            with self.subTest(key=key):
                card=deepcopy(self.card);card['current_http'][key]=value
                with self.assertRaises(ContractError):validate_normalization(card)

    def test_retirement_approval_and_invented_backlink_evidence_are_rejected(self):
        for key,value in [('outcome','retire-approved'),('actionable_migration',True),('approval','automatic'),('backlinks','none')]:
            card=deepcopy(self.card);card[key]=value
            with self.assertRaises(ContractError):validate_review_only(card)

    def test_existing_bridge_labels_planned_code_without_claiming_live_301(self):
        bridge=url_registry()['/councils/colchester/']
        self.assertEqual(bridge['delivery_mode'],'legacy_200_bridge')
        self.assertEqual(bridge['planned_status_code'],301)
        self.assertNotIn('verified_http_301',bridge.values())
