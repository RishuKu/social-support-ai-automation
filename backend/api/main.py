# backend/api/main.py

from fastapi import FastAPI, UploadFile, File
import shutil
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from orchestrator.main import run_workflow

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Social Support AI API"}

@app.post("/process/")
async def process_file(file: UploadFile = File(...)):
    file_path = f"data/sample_docs/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_workflow(file_path)
    return result
