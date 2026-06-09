import google.generativeai as genai
import anthropic
import os
from typing import List, Dict

def generate_proposal_with_gemini(
    api_key: str,
    job_description: str,
    profile_data: Dict,
    screening_questions: str = ""
):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    system_prompt = f"""
    أنت محرك ذكاء اصطناعي مخصص لصياغة عروض العمل. يجب عليك الاعتماد حصرياً على المهارات والمشاريع الموجودة في ملف المستخدم المرسل إليك.
    يُمنع منعاً باتاً اختراع، أو افتراض، أو إسقاط أي مهارة أو خبرة لا تظهر صراحة في ملفه.
    إذا تطلبت الوظيفة تقنية لا يملكها المستخدم، ركز على حل المشكلة بالمهارات المتاحة لديه دون الإشارة للتقنية المفقودة.

    بيانات المستخدم:
    {profile_data}
    """

    user_prompt = f"""
    وصف الوظيفة:
    {job_description}

    الأسئلة الإضافية:
    {screening_questions}

    المطلوب:
    1. قسم الـ Hooks: يعرض 3 خيارات لسطور افتتاحية جذابة.
    2. قسم الـ Proposal: عرض عمل مخصص بالكامل أقل من 250 كلمة.
    3. قسم إجابات الأسئلة: صياغة إجابات صادقة ودقيقة.
    """

    response = model.generate_content([system_prompt, user_prompt])
    return response.text

def generate_proposal_with_claude(
    api_key: str,
    job_description: str,
    profile_data: Dict,
    screening_questions: str = ""
):
    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = f"""
    أنت محرك ذكاء اصطناعي مخصص لصياغة عروض العمل. يجب عليك الاعتماد حصرياً على المهارات والمشاريع الموجودة في ملف المستخدم المرسل إليك.
    يُمنع منعاً باتاً اختراع، أو افتراض، أو إسقاط أي مهارة أو خبرة لا تظهر صراحة في ملفه.

    بيانات المستخدم:
    {profile_data}
    """

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"Job: {job_description}\nQuestions: {screening_questions}"
            }
        ]
    )
    return message.content[0].text
