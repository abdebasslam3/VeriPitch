import re
import logging
import json
import os
from typing import List, Dict, Set

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class SkillMatcher:
    """
    SkillMatcher Class
    Matches freelancer skills against job descriptions with high accuracy.
    Handles technical symbols like .NET, C++, and multi-word phrases.
    """

    def __init__(self, freelancer_skills: List[str],
                 skills_db_path: str = None):
        if not isinstance(freelancer_skills, list):
            logging.error("Freelancer skills must be provided as a list.")
            raise ValueError("Freelancer skills must be a list.")

        self.freelancer_skills = set(
            str(skill).strip().lower() for skill in freelancer_skills
        )

        # استخدام مسار مطلق لضمان العمل في بيئة Serverless (Netlify Functions)
        if skills_db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            skills_db_path = os.path.join(base_dir, "../data/skills.json")

        self.common_tech_skills = self._load_skills_db(skills_db_path)

    def _load_skills_db(self, path: str) -> List[str]:
        try:
            if not os.path.exists(path):
                logging.warning(f"Skills database not found at {path}.")
                return []

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                skills = data.get("common_tech_skills", [])
                # Sort by length descending to match longest phrases first
                return sorted([skill.lower() for skill in skills], key=len, reverse=True)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Failed to load or parse skills database: {e}")
            return []

    def analyze_job(self, job_description: str) -> Dict[str, List[str]]:
        try:
            if not job_description:
                return {"matched": [], "missing": [], "required_all": []}

            desc_lower = job_description.lower()
            found_skills = set()

            for skill in self.common_tech_skills:
                escaped_skill = re.escape(skill)

                # Dynamic Boundary
                start_boundary = r'\b' if skill[0].isalnum() else r'(?<!\w)'
                end_boundary = r'(?!\w)' if skill[-1].isalnum() else r''

                pattern = start_boundary + escaped_skill + end_boundary

                if re.search(pattern, desc_lower):
                    found_skills.add(skill)

            matched_skills = found_skills.intersection(self.freelancer_skills)
            missing_skills = found_skills.difference(self.freelancer_skills)

            return {
                "matched": sorted(list(matched_skills)),
                "missing": sorted(list(missing_skills)),
                "required_all": sorted(list(found_skills))
            }
        except Exception as e:
            logging.exception("An unexpected error occurred during analysis.")
            return {"error": "Internal error", "matched": [], "missing": [], "required_all": []}
