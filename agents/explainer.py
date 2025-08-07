from agents.bug_detector import model

def explain_bug(code: str, bug_info: str) -> str:
    prompt = f"""
You are a bug explainer. Based on the following buggy code and identified bug info, explain clearly what the buggy code is doing and why it causes a problem.

Bug info:
{bug_info}

Code:
{code}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
