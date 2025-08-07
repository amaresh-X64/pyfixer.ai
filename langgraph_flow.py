from typing import TypedDict
from langgraph.graph import StateGraph
from agents.bug_detector import detect_bug
from agents.explainer import explain_bug
from agents.fixer import fix_code
from agents.tester import test_code

class BugBusterState(TypedDict):
    code: str
    bug_info: str
    explanation: str
    fixed_code: str
    test_result: str

def run_bug_buster(code: str):
    def detector(state: BugBusterState) -> BugBusterState:
        bug = detect_bug(state["code"])
        return {"code": state["code"], "bug_info": bug}

    def explainer(state: BugBusterState) -> BugBusterState:
        explanation = explain_bug(state["code"], state["bug_info"])
        return {**state, "explanation": explanation}

    def fixer(state: BugBusterState) -> BugBusterState:
        fixed = fix_code(state["code"], state["explanation"])
        return {**state, "fixed_code": fixed}

    def tester(state: BugBusterState) -> BugBusterState:
        test_result = test_code(state["fixed_code"])
        return {**state, "test_result": test_result}

    builder = StateGraph(BugBusterState)
    builder.add_node("Detector", detector)
    builder.add_node("Explainer", explainer)
    builder.add_node("Fixer", fixer)
    builder.add_node("Tester", tester)

    builder.set_entry_point("Detector")
    builder.add_edge("Detector", "Explainer")
    builder.add_edge("Explainer", "Fixer")
    builder.add_edge("Fixer", "Tester")
    builder.set_finish_point("Tester")

    graph = builder.compile()
    result = graph.invoke({"code": code})
    return result
