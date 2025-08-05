# agents/validation_agent/main.py

def validate_data(applicant_data: dict) -> dict:
    issues = []
    guidance = []

    income = applicant_data.get("income")
    family_size = applicant_data.get("family_size")

    if income is not None and income < 0:
        issues.append("Invalid income (cannot be negative).")
        guidance.append("Please ensure your bank statement is uploaded correctly and income is valid.")

    if family_size is None or family_size <= 0:
        issues.append("Invalid or missing family size.")
        guidance.append("Please ensure your resume includes accurate family size information.")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "guidance": guidance
    }

if __name__ == "__main__":
    sample = {
        "income": -200,
        "family_size": 0,
        "employment_status": "unemployed"
    }
    print(validate_data(sample))
