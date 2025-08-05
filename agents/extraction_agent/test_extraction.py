import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent.parent

# Add to Python path
sys.path.append(str(project_root))

from agents.extraction_agent.main import extract_applicant_info

if __name__ == "__main__":
    # Use absolute paths
    sample_input = {
        "emirates_id_path": str(project_root / "data" / "sample_docs" / "emirates_id_sample.png"),
        "resume_path": str(project_root / "data" / "sample_docs" / "john_doe_resume.pdf"),
        "bank_statement_path": str(project_root / "data" / "sample_docs" / "bank_statement.xlsx")
    }
    
    # Verify files exist
    for path in sample_input.values():
        if not os.path.exists(path):
            print(f"File not found: {path}")
    
    result = extract_applicant_info(sample_input)
    print(result)