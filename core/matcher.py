from typing import List, Dict, Set

class SkillMatcher:
    def __init__(self, freelancer_skills: List[str]):
        """
        تهيئة المطابق بمهارات المستقل.
        """
        self.freelancer_skills = set(skill.lower() for skill in freelancer_skills)

    def analyze_job(self, job_description: str) -> Dict[str, List[str]]:
        """
        تحليل وصف الوظيفة ومطابقته مع مهارات المستقل.
        ملاحظة: هذا نموذج أولي يستخدم مطابقة الكلمات المفتاحية البسيطة.
        في النسخة النهائية، سيتم استخدام LLM و Embeddings.
        """
        # قائمة تجريبية للمهارات التقنية الشائعة للبحث عنها
        common_tech_skills = {
            "python", "javascript", "react", "node.js", "fastapi",
            "postgresql", "mongodb", "docker", "aws", "html", "css",
            "typescript", "next.js", "tailwind", "machine learning", "ai"
        }

        job_words = set(job_description.lower().replace(",", "").replace(".", "").split())

        # استخراج المهارات المطلوبة في الوظيفة بناءً على القائمة المعروفة لدينا
        required_skills = job_words.intersection(common_tech_skills)

        # تحديد المهارات المتطابقة
        matched_skills = required_skills.intersection(self.freelancer_skills)

        # تحديد الفجوات (المهارات المطلوبة ولكنها غير موجودة لدى المستقل)
        missing_skills = required_skills.difference(self.freelancer_skills)

        return {
            "matched": list(matched_skills),
            "missing": list(missing_skills),
            "required_all": list(required_skills)
        }

# تجربة بسيطة للنموذج الأولي
if __name__ == "__main__":
    my_skills = ["Python", "FastAPI", "HTML", "CSS", "PostgreSQL"]
    job_desc = """
    We are looking for a Python developer who knows FastAPI and React.
    Experience with PostgreSQL and Docker is a plus.
    """

    matcher = SkillMatcher(my_skills)
    result = matcher.analyze_job(job_desc)

    print("--- نتيجة مطابقة المهارات ---")
    print(f"المهارات المتوفرة لديك والمتطابقة مع الوظيفة: {result['matched']}")
    print(f"المهارات المطلوبة ولكنها تنقصك (فجوات): {result['missing']}")
    print(f"كافة المهارات التقنية المكتشفة في الوظيفة: {result['required_all']}")
