import pprint
from langgraph.graph import StateGraph, END
from orchestrator.agents import (
    ExtractionAgent,
    ValidationAgent,
    EligibilityAgent,
    RecommendationAgent,
)

# Define the state schema
state_schema = dict

# Node 1: Extract data
def node_extract(state):
    pprint.pprint({" Step": "Extraction", "input_state": state})
    path = state["document_path"]
    output = ExtractionAgent.invoke(path)
    return {
        "applicant_data": output,
        "extracted_data": output
    }

# Node 2: Validate extracted data
def node_validate(state):
    pprint.pprint({"Step": "Validation", "input_state": state})
    data = state["applicant_data"]
    output = ValidationAgent.invoke({"applicant_data": data})
    return {
        "validation_result": output,
        "applicant_data": data,
        "extracted_data": state.get("extracted_data")  # retain
    }

# Branching decision
def should_continue(state):
    result = state["validation_result"]
    pprint.pprint({" Step": "Validation Check", "validation_result": result})

    valid_result = result.get("valid", {})
    if isinstance(valid_result, dict):
        return "eligible" if valid_result.get("valid", False) else "end"
    elif isinstance(valid_result, bool):
        return "eligible" if valid_result else "end"
    else:
        return "end"

# Node 3: Eligibility check
def node_eligibility(state):
    pprint.pprint({" Step": "Eligibility", "input_state": state})
    data = state["applicant_data"]
    output = EligibilityAgent.invoke({"applicant_data": data})
    return {
        "eligibility_result": output,
        "applicant_data": data,
        "validation_result": state.get("validation_result"),
        "extracted_data": state.get("extracted_data")
    }

# Node 4: Recommendation generation
def node_recommend(state):
    pprint.pprint({"Step": "Recommendation", "input_state": state})
    data = state["applicant_data"]
    output = RecommendationAgent.invoke({"applicant_data": data})
    return {
        "recommendations": output,
        "eligibility_result": state.get("eligibility_result"),
        "validation_result": state.get("validation_result"),
        "applicant_data": data,
        "extracted_data": state.get("extracted_data")
    }

# Build LangGraph
def build_graph():
    graph = StateGraph(state_schema)

    graph.add_node("extract", node_extract)
    graph.add_node("validate", node_validate)
    graph.add_node("eligible", node_eligibility)
    graph.add_node("recommend", node_recommend)
    graph.add_node("end", lambda state: state)

    graph.set_entry_point("extract")
    graph.add_edge("extract", "validate")
    graph.add_conditional_edges("validate", should_continue, {
        "eligible": "eligible",
        "end": "end"
    })
    graph.add_edge("eligible", "recommend")
    graph.add_edge("recommend", "end")

    return graph.compile()

# Entry point
def run_workflow(document_path: str) -> dict:
    print("\n Starting workflow for document:", document_path)
    workflow = build_graph()
    final_state = workflow.invoke({"document_path": document_path})
    print("\n Final state of workflow:")
    pprint.pprint(final_state)

    return {
        "decision": final_state.get("eligibility_result", "Validation Failed"),
        "recommendations": final_state.get("recommendations", []),
        "validation_result": final_state.get("validation_result", {}),
        "extracted_data": final_state.get("applicant_data", {})
    }
