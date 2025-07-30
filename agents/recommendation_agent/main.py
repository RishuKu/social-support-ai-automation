# agents/recommendation_agent/main.py

def recommend_enablement(applicant_data: dict) -> list:
    if applicant_data["employment_status"] == "unemployed":
        return ["Job training program", "Resume workshop", "Gov job portal link"]
    else:
        return ["No enablement needed"]

if __name__ == "__main__":
    sample = {
        "employment_status": "unemployed"
    }
    print(recommend_enablement(sample))
