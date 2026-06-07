import unittest
import os
import json
from core.matcher import SkillMatcher

class TestSkillMatcher(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = "tests/test_skills.json"
        test_data = {
            "common_tech_skills": ["python", "react", "machine learning", "c++", "node.js"]
        }
        with open(cls.test_db_path, 'w') as f:
            json.dump(test_data, f)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def setUp(self):
        self.freelancer_skills = ["Python", "C++", "Machine Learning"]
        self.matcher = SkillMatcher(self.freelancer_skills, skills_db_path=self.test_db_path)

    def test_multi_word_match(self):
        job_desc = "Looking for someone with Machine Learning skills."
        result = self.matcher.analyze_job(job_desc)
        self.assertIn("machine learning", result["matched"])

    def test_symbols_match(self):
        job_desc = "Requirements: C++ developer."
        result = self.matcher.analyze_job(job_desc)
        self.assertIn("c++", result["matched"])

    def test_dot_symbols_match(self):
        job_desc = "Need Node.js experience."
        result = self.matcher.analyze_job(job_desc)
        self.assertIn("node.js", result["required_all"])

    def test_missing_skills(self):
        job_desc = "Python and React."
        result = self.matcher.analyze_job(job_desc)
        self.assertIn("python", result["matched"])
        self.assertIn("react", result["missing"])

    def test_empty_job_desc(self):
        result = self.matcher.analyze_job("")
        self.assertEqual(result["matched"], [])

if __name__ == '__main__':
    unittest.main()
