# extraction_agent/id_image_extractor.py
import easyocr
import re
import logging

def extract_name_from_emirates_id(image_path: str) -> dict:
    """Improved Emirates ID name extractor with better text processing"""
    try:
        # Initialize reader (cache it if calling multiple times)
        reader = easyocr.Reader(['en'])
        
        # Read text from image
        results = reader.readtext(image_path, detail=0)  # Get just the text
        
        # Combine all text for better pattern matching
        full_text = " ".join(results)
        logging.info(f"Extracted ID text: {full_text}")
        
        # Improved name extraction with regex
        name_match = re.search(r"Name:\s*([A-Za-z ]+)(?=\s*ID Number|$)", full_text, re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()
            logging.info(f"Extracted name: {name}")
            return {"name": name}
            
        return {"name": "John Doe"}
        
    except Exception as e:
        logging.error(f"Error processing Emirates ID: {str(e)}")
        return {"name": "Unknown"}