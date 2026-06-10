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
    Matches freelancer skills against job descriptions with high accuracy,
    supporting multi-word skills and technical symbols (e.g., C++, C#, .NET).
    """

    def __init__(self, freelancer_skills: List[str],
                 skills_db_path: str = "data/skills.json"):
        """
        Initialize the SkillMatcher with freelancer skills and a database path.
        """
        if not isinstance(freelancer_skills, list):
            logging.error("Freelancer skills must be provided as a list.")
            raise ValueError("Freelancer skills must be a list.")

        self.freelancer_skills = set(
            str(skill).strip().lower() for skill in freelancer_skills
        )
        # Store as a sorted list to match longer phrases first
        self.common_tech_skills = sorted(list(self._load_skills_db(skills_db_path)), key=len, reverse=True)

    def _load_skills_db(self, path: str) -> Set[str]:
        """Loads the common skills database from a JSON file."""
        try:
            if not os.path.exists(path):
                logging.warning(f"Skills database not found at {path}.")
                return set()

            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                skills = data.get("common_tech_skills", [])
                return set(skill.lower() for skill in skills)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Failed to load or parse skills database: {e}")
            return set()

    def analyze_job(self, job_description: str) -> Dict[str, List[str]]:
        """
        Analyzes the job description using phrase matching.
        Uses a 'consumption' approach to avoid matching sub-skills (e.g., matching 'Tailwind' if 'Tailwind CSS' is present).
        """
        try:
            if not job_description:
                return {"matched": [], "missing": [], "required_all": []}

            # We use a temporary string and replace matches with placeholders to avoid double-matching
            desc_temp = job_description.lower()
            found_skills = set()

            for skill in self.common_tech_skills:
                escaped_skill = re.escape(skill)
                pattern = r'\b' + escaped_skill + r'(?!\w)'
                if re.search(pattern, desc_temp):
                    found_skills.add(skill)
                    # Replace found skill with a neutral placeholder to 'consume' it
                    desc_temp = re.sub(pattern, " [SKILL_MATCH] ", desc_temp)

            # Match against freelancer's own skills
            matched_skills = found_skills.intersection(self.freelancer_skills)

            # Identify gaps
            missing_skills = found_skills.difference(self.freelancer_skills)

            return {
                "matched": sorted(list(matched_skills)),
                "missing": sorted(list(missing_skills)),
                "required_all": sorted(list(found_skills))
            }
        except Exception as e:
            logging.exception("An unexpected error occurred during analysis.")
            return {
                "error": "Internal analysis error",
                "matched": [],
                "missing": [],
                "required_all": []
            }


if __name__ == "__main__":
    example_skills = ["Python", "C++", "Machine Learning"]
    example_job = "Seeking a C++ developer with Machine Learning and React experience."

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "../data/skills.json")

    matcher = SkillMatcher(example_skills, skills_db_path=data_path)
    report = matcher.analyze_job(example_job)
    print(f"Match Report: {json.dumps(report, indent=4)}")
