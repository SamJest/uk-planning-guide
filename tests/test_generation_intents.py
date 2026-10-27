import unittest
from utils.content_contracts import validate_distinct_intents, ContractError

class GenerationIntentTests(unittest.TestCase):
    def record(self,path):
        return dict(route_path=path,canonical_path=path,index_status='index',page_family='local_rule',jurisdiction='england',authority_id='test',project_id=None,rule_id='article-4')
    def test_keyword_variant_of_same_intent_is_rejected(self):
        with self.assertRaises(ContractError):
            validate_distinct_intents([self.record('/article-4/test/'),self.record('/local-search/test-article-4/')])
    def test_different_nation_is_not_merged(self):
        other=self.record('/wales/rules/article-4/test/')
        other['jurisdiction']='wales'
        validate_distinct_intents([self.record('/article-4/test/'),other])
    def test_legacy_alias_is_not_second_indexable_intent(self):
        other=self.record('/legacy/')
        other['canonical_path']='/article-4/test/'
        validate_distinct_intents([self.record('/article-4/test/'),other])
