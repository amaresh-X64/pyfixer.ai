from langgraph_flow import run_bug_buster
from colorama import init, Fore

init(autoreset=True)

def clean_response(text: str) -> str:
    return (
        text.replace("```python", "")
            .replace("```", "")
            .replace("**", "")
            .strip()
    )

def print_agent_section(agent_name: str, icon: str, color: str, raw_text: str):
    print(color + f"\n{icon} {agent_name.upper()}")
    print(color + "-" * 80)
    print(clean_response(raw_text))
    print(color + "-" * 80)

if __name__ == "__main__":
    with open("examples/buggy_code_example.py") as f:
        code = f.read()

    result = run_bug_buster(code)

    print_agent_section("Bug Detector Agent", "🕵️", Fore.YELLOW, result["bug_info"])
    print_agent_section("Explainer Agent", "🔍", Fore.GREEN, result["explanation"])
    print_agent_section("Fixer Agent", "🔧", Fore.MAGENTA, result["fixed_code"])
    print_agent_section("Test Agent", "🧪", Fore.BLUE, result["test_result"])
