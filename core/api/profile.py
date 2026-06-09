import PyPDF2
import io
import google.generativeai as genai
import os
import json
from typing import List, Dict

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extracts text from a PDF file."""
    text = ""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def parse_profile_with_ai(text: str, api_key: str):
    """Uses LLM to parse text into a structured JSON profile."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Analyze the following text (resume or profile) and extract:
    1. A professional bio summary (bio_summary).
    2. A list of technical skills (skills) as an array of objects: [{{"name": "SkillName", "verified": false, "source": "resume"}}]
    3. A list of portfolio projects (portfolio) as an array: [{{"title": "Project Name", "description": "...", "url": "..."}}]

    Text:
    {text}

    Output ONLY valid JSON.
    """

    response = model.generate_content(prompt)
    try:
        content = response.text.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        return json.loads(content)
    except:
        return None
