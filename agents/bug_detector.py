import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def detect_bug(code: str) -> str:
    prompt = f"""
You are a bug detector. Analyze the following Python code and identify the buggy line(s). Return only:
- Bug description
- Bug line number(s)
- Why it's a bug

Code:
{code}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
