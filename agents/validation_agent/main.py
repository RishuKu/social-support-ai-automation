# agents/validation_agent/main.py

def validate_data(applicant_data: dict) -> dict:
    issues = []

    if applicant_data["income"] < 0:
        issues.append("Invalid income")

    if applicant_data["family_size"] <= 0:
        issues.append("Family size must be at least 1")

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }

if __name__ == "__main__":
    sample = {
        "income": 3000,
        "family_size": 4,
        "employment_status": "unemployed"
    }
    print(validate_data(sample))
