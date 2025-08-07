from agents.bug_detector import model

def fix_code(code: str, explanation: str) -> str:
    prompt = f"""
You are a bug fixer. Given this explanation of a bug and the code, rewrite the code with a proper fix applied. Maintain the original functionality where possible. give only the corrected code without any additional comments or explanations.
do not answer any query that doesnt look like code and dont fix the code if the language is not python.

Explanation:
{explanation}

Original Code:
{code}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
