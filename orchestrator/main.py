# orchestrator/main.py

import pprint
import os
from langgraph.graph import StateGraph
from langsmith import traceable
from orchestrator.agents import (
    ExtractionAgent,
    ValidationAgent,
    EligibilityAgent,
)
from agents.recommendation_agent.recommendation_agent import RecommendationAgent
from dotenv import load_dotenv
load_dotenv()

# === LangSmith API ENV VARS ===
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "SocialSupportAI"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Define the state schema
state_schema = dict
@traceable(name="SocialSupportAI")
def node_extract(state):
    pprint.pprint({"Step": "Extraction", "input_state": state})
    
    resume_path = state.get("resume_path")
    bank_statement_path = state.get("bank_statement_path")
    emirates_id_path = state.get("emirates_id_path")

    input_payload = {
        "resume_path": resume_path,
        "bank_statement_path": bank_statement_path,
        "emirates_id_path": emirates_id_path,
    }

    output = ExtractionAgent.invoke(input_payload)
    return {
        "applicant_data": output,
        "extracted_data": output
    }

def node_validate(state):
    pprint.pprint({"Step": "Validation", "input_state": state})
    data = state["applicant_data"]
    output = ValidationAgent.invoke({"applicant_data": data})
    return {
        "validation_result": output,
        "applicant_data": data,
        "extracted_data": state.get("extracted_data")
    }

def should_continue(state):
    result = state["validation_result"]
    pprint.pprint({"Step": "Validation Check", "validation_result": result})

    valid = result.get("valid", False)
    return "eligible" if valid else "end"

def node_eligibility(state):
    pprint.pprint({"Step": "Eligibility", "input_state": state})
    data = state["applicant_data"]
    output = EligibilityAgent.invoke({"applicant_data": data})
    return {
        "eligibility_result": output,
        "validation_result": state.get("validation_result"),
        "extracted_data": state.get("extracted_data"),
        "applicant_data": data
    }

def node_recommend(state):
    pprint.pprint({"Step": "Recommendation", "input_state": state})
    data = state["applicant_data"]
    output = RecommendationAgent.invoke({"applicant_data": data})
    return {
        "recommendations": output,
        "eligibility_result": state.get("eligibility_result"),
        "validation_result": state.get("validation_result"),
        "extracted_data": state.get("extracted_data"),
        "applicant_data": data
    }

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

def run_workflow(resume_path: str, bank_statement_path: str, emirates_id_path: str) -> dict:
    print("\n📄 Starting workflow with multimodal input")
    workflow = build_graph()
    final_state = workflow.invoke({
        "resume_path": resume_path,
        "bank_statement_path": bank_statement_path,
        "emirates_id_path": emirates_id_path
    })
    print("\n✅ Final state of workflow:")
    pprint.pprint(final_state)

    return {
        "decision": final_state.get("eligibility_result", "Validation Failed"),
        "recommendations": final_state.get("recommendations", []),
        "validation_result": final_state.get("validation_result", {}),
        "extracted_data": final_state.get("applicant_data", {})
    }
