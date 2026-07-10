import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from proposed_method import METHOD_SPEC, run_method, score_case, load_examples
from value_add import run_demo


class ProposedMethodTest(unittest.TestCase):
    def test_unique_method_runs(self):
        result = run_method()
        self.assertEqual(result["algorithm_id"], 'P109-Srikumar-Nlp')
        self.assertEqual(result["algorithm_name"], 'SrikumarEvidenceNlpRepairLoop')
        self.assertEqual(result["project_family"], 'language')
        self.assertTrue(result["top_cases"])

    def test_score_case_outputs_priority(self):
        row = load_examples()[0]
        scored = score_case(row)
        self.assertIn("priority_score", scored)
        self.assertGreaterEqual(scored["priority_score"], 0.0)

    def test_value_add_report_includes_unique_method(self):
        report = run_demo()
        self.assertEqual(report["proposed_method"]["algorithm_id"], 'P109-Srikumar-Nlp')


if __name__ == "__main__":
    unittest.main()
