# frontend/main.py

import streamlit as st
import os
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from orchestrator.main import run_workflow

# App setup
st.set_page_config(page_title="Social Support AI", layout="wide")
st.title("🧾 Social Support Application Automation")

# --- Section 1: File Upload ---
st.header("📄 Upload Application Document")

uploaded_file = st.file_uploader("Upload PDF, DOCX, or XLSX file", type=["pdf", "docx", "xlsx"])

if uploaded_file:
    # Save uploaded file locally
    os.makedirs("data/sample_docs", exist_ok=True)
    file_path = f"data/sample_docs/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ File uploaded successfully!")

    # Run main workflow
    with st.spinner("🔍 Processing..."):
        result = run_workflow(file_path)

    st.subheader("🧠 Automated Decision Result:")
    st.json(result)

# --- Section 2: Chat with Ollama ---
st.header("💬 Chat with AI Assistant")

# Session state to store chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input from user
user_input = st.text_input("Ask a question (e.g., eligibility criteria, required documents):")

if user_input:
    st.session_state.chat_history.append({"user": user_input})

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": user_input, "stream": False}
        )
        print("Ollama Response:", response.json())  # 👈 Debug line
        if "response" in response.json():
            answer = response.json()["response"]
        else:
            answer = "⚠️ Ollama responded but no answer was found."
    except Exception as e:
        answer = f"Failed to connect to Ollama: {str(e)}"

    st.session_state.chat_history.append({"bot": answer})

# Display conversation
for chat in st.session_state.chat_history:
    if "user" in chat:
        st.markdown(f"👤 **You**: {chat['user']}")
    if "bot" in chat:
        st.markdown(f"🤖 **AI Assistant**: {chat['bot']}")
