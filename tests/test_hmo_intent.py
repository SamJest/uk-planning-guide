import unittest
from components.scenario_sections import build_your_situation_summary, _scenario_constraint, _next_step_hint

class HmoIntentTests(unittest.TestCase):
    def test_all_nations_use_evidence_not_risk_guesses(self):
        for nation in ('england','wales','scotland','northern-ireland'):
            result=build_your_situation_summary('HMO','change-of-use','Article 4','Test authority',nation,{'restrictions':{'conservation_area':'Yes'}},'article-4')
            self.assertIn('boundary map',result)
            self.assertIn('Existing lawful use',result)
            self.assertNotIn('Likely risk level',result)
            self.assertNotIn('usually conservation',result)
            self.assertIn('data-evidence-status="unverified"',result)

    def test_topic_beats_unrelated_first_restriction(self):
        rule={'restrictions':{'conservation_area':'Possible conservation designation'}}
        self.assertNotEqual(_scenario_constraint(rule,'article-4'),'conservation areas')
        self.assertIn('direction document',_next_step_hint('change-of-use','article-4',rule))
