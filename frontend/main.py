import streamlit as st
import os
import requests
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from orchestrator.main import run_workflow
from models.prompts import build_prompt

# App setup
st.set_page_config(page_title="Social Support AI", layout="wide")
st.title("🧾 Social Support Application Automation")

# --- Section 1: File Upload ---
st.header("📄 Upload Application Documents")

def save_file(file, folder="data/sample_docs"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, file.name)
    with open(path, "wb") as f:
        f.write(file.read())
    return path

# Store session state for re-uploaded file
if "corrected_bank_statement_path" not in st.session_state:
    st.session_state.corrected_bank_statement_path = None

# File Upload
emirates_id = st.file_uploader("Upload Emirates ID (Image format)", type=["jpg", "jpeg", "png"])
resume = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
bank_statement = st.file_uploader("Upload Bank Statement (Excel only)", type=["xlsx"])

# --- Function to Run Workflow and Handle Validation ---
def process_application(resume_path, bank_statement_path, emirates_id_path):
    with st.spinner("🔄 Processing your application..."):
        result = run_workflow(resume_path, bank_statement_path, emirates_id_path)

    validation_block = result.get("validation_result", {}).get("valid", {})
    is_valid = validation_block.get("valid", True)

    if not is_valid:
        st.error(" Validation failed. Please address the following issues:")

        issues = validation_block.get("issues", [])
        guidance = validation_block.get("guidance", [])

        if issues:
            st.write("### ❗ Issues:")
            for issue in issues:
                st.markdown(f"- {issue}")

        if guidance:
            st.write("### 💡 How to Fix:")
            for g in guidance:
                st.markdown(f" {g}")

        st.write("Would you like to re-upload the **corrected bank statement**?")
        wants_fix = st.radio("Choose an option:", ["Yes", "No"], key="fix_option")

        if wants_fix == "Yes":
            corrected_doc = st.file_uploader("Upload Corrected Bank Statement", type=["xlsx"], key="reupload")
            if corrected_doc:
                corrected_path = save_file(corrected_doc)
                st.session_state.corrected_bank_statement_path = corrected_path
                st.success(" Corrected file uploaded. Re-processing...")
                # Call again with new corrected path
                process_application(resume_path, corrected_path, emirates_id_path)
                return
        else:
            st.info(" You can fix the issue later and try again.")
        st.stop()

    # If validation passed, show results
    st.success("✅ Validation passed!")
    st.subheader("📊 Automated Decision Result:")
    st.json(result)

# --- When all files are uploaded, run process ---
if emirates_id and resume and bank_statement:
    st.success("All files uploaded successfully! ")

    emirates_id_path = save_file(emirates_id)
    resume_path = save_file(resume)

    # Use reuploaded bank statement if available
    bank_statement_path = (
        st.session_state.corrected_bank_statement_path
        if st.session_state.corrected_bank_statement_path
        else save_file(bank_statement)
    )

    process_application(resume_path, bank_statement_path, emirates_id_path)

elif any([emirates_id, resume, bank_statement]):
    st.warning(" Please upload all 3 required documents to continue.")

# --- Section 2: Chat with TinyLLaMA ---
st.header("💬 Chat with AI Assistant")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask a question (e.g., eligibility, required documents, recommendations):")

if user_input:
    st.session_state.chat_history.append({"user": user_input})
    full_prompt = build_prompt(user_input)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "tinyllama", "prompt": full_prompt, "stream": False}
        )
        response_json = response.json()
        answer = response_json.get("response", "TinyLLaMA responded, but no answer was found.")
    except Exception as e:
        answer = f" Failed to connect to TinyLLaMA: {str(e)}"

    st.session_state.chat_history.append({"bot": answer})

# Display chat history
for chat in st.session_state.chat_history:
    if "user" in chat:
        st.markdown(f"👤 **You**: {chat['user']}")
    if "bot" in chat:
        st.markdown(f"🤖 **AI Assistant**: {chat['bot']}")
