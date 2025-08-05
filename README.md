
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
├── agents/
│   ├── extraction_agent.py
│   ├── validation_agent.py
│   ├── eligibility_agent.py
│   └── recommendation_agent.py
├── orchestrator/
│   └── main.py
├── frontend/
│   └── main.py
├── models/
│   └── recommendation_model.py
├── utils/
│   ├── document_utils.py
│   ├── validation_rules.py
│   └── image_processing.py
└── README.md
```

---

##  Run Instructions

### 1. Clone the Repo

```bash
git clone <your-private-repo-url>
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


