from agents.bug_detector import model

def test_code(fixed_code: str) -> str:
    prompt = f"""
You are a testing agent. You are given some fixed Python code. Write a test plan or brief test output to confirm if the bug fix is successful. You don't need to run the code.

Code:
{fixed_code}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
