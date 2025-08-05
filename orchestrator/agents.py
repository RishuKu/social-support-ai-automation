# orchestrator/agents.py

from langchain_core.tools import tool
from agents.extraction_agent.main import extract_applicant_info
from agents.validation_agent.main import validate_data
from agents.eligibility_agent.main import mock_predict_eligibility
from agents.recommendation_agent.main import recommend_enablement

from langchain.tools import tool

@tool
def ExtractionAgent(
    resume_path: str,
    bank_statement_path: str,
    emirates_id_path: str
) -> dict:
    """
    Extracts structured applicant info from resume, bank statement, and Emirates ID.
    """
    from agents.extraction_agent.main import extract_applicant_info

    return extract_applicant_info({
        "resume_path": resume_path,
        "bank_statement_path": bank_statement_path,
        "emirates_id_path": emirates_id_path
    })



@tool
def ValidationAgent(applicant_data: dict) -> dict:
    """Validate extracted applicant information"""
    is_valid = validate_data(applicant_data)
    return {"valid": is_valid}

@tool
def EligibilityAgent(applicant_data: dict) -> str:
    """Determine if applicant is eligible"""
    return mock_predict_eligibility(applicant_data)

@tool
def RecommendationAgent(applicant_data: dict) -> list:
    """Recommend economic enablement support"""
    return recommend_enablement(applicant_data)
