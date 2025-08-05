# extraction_agent/main.py

from agents.extraction_agent.resume_extractor import extract_from_resume
from agents.extraction_agent.bank_statement_extractor import extract_from_bank_statement
from agents.extraction_agent.id_image_extractor import extract_name_from_emirates_id

def extract_applicant_info(input_data: dict) -> dict:
    resume_path = input_data.get("resume_path")
    bank_statement_path = input_data.get("bank_statement_path")
    emirates_id_path = input_data.get("emirates_id_path")

    extracted_data = {}

    if resume_path:
        extracted_data.update(extract_from_resume(resume_path))

    if bank_statement_path:
        extracted_data.update(extract_from_bank_statement(bank_statement_path))

    if emirates_id_path:
        extracted_data.update(extract_name_from_emirates_id(emirates_id_path))

    return extracted_data
