import google.generativeai as genai
import os
import json

def parse_resume_to_json(text: str):
    """Uses Gemini to parse resume text into structured JSON."""
    api_key = os.getenv("GEMINI_API_KEY") # System fallback or user key
    if not api_key: return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Parse the following resume text into a structured JSON object with:
    - bio_summary (string)
    - skills (array of strings)
    - portfolio (array of objects with title, description, and optional url)

    Resume Text:
    {text}

    Output ONLY valid JSON.
    """

    response = model.generate_content(prompt)
    try:
        # Simple extraction of JSON from response
        content = response.text.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        return json.loads(content)
    except:
        return None

def generate_smart_quiz(skill_name: str, bio: str):
    """Generates a deep MCQ question for a skill."""
    # Similar AI call logic to generate a concept-based MCQ
    pass
