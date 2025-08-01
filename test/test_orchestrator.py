# test_orchestrator.py
from orchestrator.main import run_workflow

result = run_workflow("sample_docs/Nagarro Resume Template.docx")
print("Final Output:", result)
