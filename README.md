
# Social Support Application Automation

This project is an AI-driven solution designed to automate the eligibility screening, validation, and recommendation process for social support applications. It uses a multi-agent LangGraph workflow, integrates with LangSmith for observability, and offers a user-friendly Streamlit frontend.

---

## Key Features

- Multimodal document ingestion (PDFs, images, tables)
- AI-powered Extraction, Validation, Eligibility & Recommendation agents
- LangGraph-based orchestration
- LangSmith for traceability and debugging
- Streamlit frontend for document upload and live interaction

---

##  Project Structure

```
.
social-support-ai-automation/
├── agents/
│   ├── eligibility_agent/
│   │   ├── main.py
│   │  │   │
│   ├── extraction_agent/
│   │   ├── bank_statement_extractor.py
│   │   ├── id_image_extractor.py
│   │   ├── resume_extractor.py
│   │   ├── main.py
│   │   ├── test_extraction.py
│   │   │
│   ├── recommendation_agent/
│   │   ├── main.py
│   │   ├── recommendation_agent.py
│   │
│   └── validation_agent/
│       ├── main.py
├── backend\api
│   └── main.py
├── data\sample_docs
│   └── bank_statement_ws.xlsx
    └── emirates_id_sample.png
    └── john_doe_resume.pdf
├── frontend/
│   └── main.py
├── models/
│   └── recommendation_model.py
├── orchestrator/
│   └── main.py
    └── agents.py
├── test/
│   
├── utils/
│   │
└── README.md
└── requirements.txt
```

---

##  Run Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/RishuKu/social-support-ai-automation.git
cd social-support-ai-automation
```

### 2. Set up Virtual Environment

```In terminal 
.\venv\Scripts\activate   
pip install -r requirements.txt
```

### 3. Environment Variables

Set the following environment variables in a `.env` file or in your terminal:

```env
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_PROJECT=your_project_name
LANGCHAIN_TRACING_V2=true
```
### 4. Start the ollama

```In terminal 
ollama run tinyllama
```
(Optional:  ensure `ollama` is running locally)_

### 5. Start the Streamlit App

```In terminal 
streamlit run frontend/main.py
```

---

##  Test Flow

1. Upload a document set (Resume, Emirates ID, Bank Statement)-->These sample documents are attached in folder data\sample_docs.
2. Watch the AI agents extract, validate, check eligibility, and recommend support
3. Trace and debug flows using LangSmith

---

##  Requirements

- Python 3.10+
- streamlit, langchain, langgraph, langsmith, llama-index, pandas, scikit-learn, pdf2image, etc.

---


