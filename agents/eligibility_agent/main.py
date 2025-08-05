# agents/eligibility_agent/main.py

from sklearn.linear_model import LogisticRegression
import numpy as np
from langsmith import traceable  #  add this

@traceable(name="EligibilityAgent")  # new decorator for Langsmith

def mock_predict_eligibility(applicant_data: dict) -> str:
    # TODO: Replace with actual ML model later
    income = applicant_data["income"]
    score = 1 if income < 5000 else 0
    return "Approved" if score == 1 else "Soft Decline"

if __name__ == "__main__":
    sample = {
        "income": 3000,
        "family_size": 4
    }
    print(mock_predict_eligibility(sample))
