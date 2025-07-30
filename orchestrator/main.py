# orchestrator/main.py

from agents.extraction_agent.main import extract_applicant_info
from agents.validation_agent.main import validate_data
from agents.eligibility_agent.main import mock_predict_eligibility
from agents.recommendation_agent.main import recommend_enablement

def run_workflow(document_path: str):
    data = extract_applicant_info(document_path)
    validation = validate_data(data)

    if not validation["valid"]:
        return {"status": "Validation Failed", "issues": validation["issues"]}

    decision = mock_predict_eligibility(data)
    recommendation = recommend_enablement(data)

    return {
        "decision": decision,
        "recommendations": recommendation
    }

if __name__ == "__main__":
    result = run_workflow("data/sample_docs/sample_id.pdf")
    print(result)
