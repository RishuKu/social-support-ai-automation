# extraction_agent/resume_extractor.py
import fitz  # PyMuPDF
import re
import logging

def extract_from_resume(pdf_path: str) -> dict:
    """Extract only family_size and education_level from resume PDF"""
    try:
        # Open PDF and extract text
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        
        # Initialize with defaults
        result = {
            "family_size": 1,  # Minimum valid value
            "education_level": "unknown"
        }
        
        # Extract family size (handles hyphen/space variations)
        family_match = re.search(
            r"Family Size:\s*[-\s]*(\d+)", 
            text, 
            re.IGNORECASE
        )
        if family_match:
            result["family_size"] = max(1, int(family_match.group(1)))
        
        # Extract education level (handles bullet points/hyphens)
        education_match = re.search(
            r"Education Level:\s*[-•\s]*(\w+)", 
            text, 
            re.IGNORECASE
        )
        if education_match:
            # Clean and standardize the value
            edu_level = education_match.group(1).strip().lower()
            
            # Standardize known variations
            if 'high' in edu_level or 'hs' in edu_level:
                result["education_level"] = "high_school"
            else:
                result["education_level"] = edu_level
        
        return result
        
    except Exception as e:
        logging.error(f"Resume extraction error: {str(e)}")
        return {
            "family_size": 1,
            "education_level": "unknown"
        }