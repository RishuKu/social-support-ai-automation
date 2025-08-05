# agents/recommendation_agent.py

from langchain.tools import tool
import joblib
import numpy as np
import math

# Load model and encoders
model = joblib.load("models/recommendation_model.pkl")
encoders = joblib.load("models/label_encoders.pkl")

# Link dictionary
SUPPORT_LINKS = {
    "Job training program": "https://gov-jobs.example.com/job-training",
    "Resume workshop": "https://gov-jobs.example.com/resume-workshop",
    "Career counseling": "https://gov-jobs.example.com/counseling",
    "Job portal link": "https://gov-jobs.example.com/jobs"
}

@tool
def RecommendationAgent(applicant_data: dict) -> dict:
    """Recommend support programs based on classification model."""
    try:
        # Extract input
        income = applicant_data.get('income', 0.0)
        employment_status = applicant_data.get('employment_status', '')
        family_size = applicant_data.get('family_size', 1)
        education_level = applicant_data.get('education_level', '')
        print(f"income {income}")
        print(f"employment_status {employment_status}")
        print(f"family_size {family_size}")
        print(f"education_level {education_level}")

        # Encode categorical features
        employment_status_encoded = encoders['employment_status'].transform([employment_status])[0]
        education_level_encoded = encoders['education_level'].transform([education_level])[0]

        # Build feature array
        features = np.array([[income, employment_status_encoded, family_size, education_level_encoded]], dtype=float)

        # Predict
        pred = model.predict(features)[0]

        # Decode prediction
        recommendation = encoders['recommendation'].inverse_transform([pred])[0]

        # Validate recommendation
        if isinstance(recommendation, float) and (math.isnan(recommendation) or str(recommendation).lower() == 'nan'):
            return {"recommendations": []}

        if isinstance(recommendation, str) and recommendation.strip().lower() == 'none':
            return {"recommendations": []}

        # Append helpful message + link if available
        link = SUPPORT_LINKS.get(recommendation.strip(), "")
        message = f" Recommended: {recommendation}"

        if link:
            message += f"\n\nYou can explore or apply here: ({link})"

        return {"recommendations": [message]}

    except Exception as e:
        print(f"RecommendationAgent Error: {str(e)}")
        return {"recommendations": [f"Error: {str(e)}"]}
