# agents/extraction_agent/main.py

def extract_applicant_info(document_path: str) -> dict:
    # TODO: Replace with OCR or PDF parsing
    print(f"Extracting data from {document_path}")
    return {
        "name": "John Doe",
        "income": 3000,
        "family_size": 4,
        "employment_status": "unemployed"
    }

if __name__ == "__main__":
    result = extract_applicant_info("data/sample_docs/sample_id.pdf")
    print(result)
