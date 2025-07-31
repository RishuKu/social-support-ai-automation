# frontend/main.py

import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from orchestrator.main import run_workflow

st.set_page_config(page_title="Social Support AI", layout="wide")
st.title("🧾 Social Support Application Automation")

uploaded_file = st.file_uploader("Upload Application Document", type=["pdf", "docx", "xlsx"])

if uploaded_file:
    # Save the uploaded file
    os.makedirs("data/sample_docs", exist_ok=True)
    file_path = f"data/sample_docs/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("File uploaded successfully!")

    with st.spinner("Running automated decision workflow..."):
        result = run_workflow(file_path)

    st.subheader("✅ Result:")
    st.json(result)
