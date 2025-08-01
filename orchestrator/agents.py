# orchestrator/agents.py

from langchain_core.tools import tool
from agents.extraction_agent.main import extract_applicant_info
from agents.validation_agent.main import validate_data
from agents.eligibility_agent.main import mock_predict_eligibility
from agents.recommendation_agent.main import recommend_enablement

@tool
def ExtractionAgent(document_path: str) -> dict:
    """Extract applicant info from uploaded document"""
    return extract_applicant_info(document_path)

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
