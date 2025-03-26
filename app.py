import streamlit as st
import os
import json
import logging
import tempfile
import fitz  # PyMuPDF for PDF processing
import docx
from openai import AzureOpenAI
from config import OPENAI_ENDPOINT, OPENAI_KEY, API_VERSION, DEPLOYMENT_NAME

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AzureOpenAISummarizer:
    """Azure OpenAI-based summarizer for legal documents."""

    def __init__(self):
        """Initialize Azure OpenAI client."""
        self.client = AzureOpenAI(
            azure_endpoint=OPENAI_ENDPOINT,
            api_key=OPENAI_KEY,
            api_version=API_VERSION,
        )

    def summarize_text(self, text: str, max_tokens: int = 500) -> dict:
        """Summarizes legal document text into a structured JSON format."""
        try:
            response = self.client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are an AI that extracts structured summaries from legal documents."},
                    {"role": "user", "content": f"Extract a structured summary from this legal document:\n{text}\n\n"
                                                 "Format the output as JSON with keys: document_title, key_clauses, "
                                                 "obligations, limitations, key_takeaways."}
                ],
                max_tokens=max_tokens,
                temperature=0.5
            )

            structured_summary = response.choices[0].message.content.strip()
            return json.loads(structured_summary)

        except Exception as e:
            logging.error(f"❌ Error summarizing text: {e}")
            return {"error": str(e)}

# Function to extract text from different file types
def extract_text(file):
    """Extracts text from PDF, DOCX, or TXT files."""
    text = ""
    file_extension = file.name.split(".")[-1].lower()

    if file_extension == "pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file.read())
            temp_pdf_path = temp_pdf.name
        doc = fitz.open(temp_pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        os.remove(temp_pdf_path)

    elif file_extension == "docx":
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])

    elif file_extension == "txt":
        text = str(file.read(), "utf-8")

    return text

# Streamlit UI
st.title("📑 AI-Powered Legal Document Summarizer")
st.write("Upload multiple legal documents (PDF, DOCX, TXT) to generate structured summaries.")

# File uploader
uploaded_files = st.file_uploader("Upload Documents", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_files:
    summarizer = AzureOpenAISummarizer()
    summaries = []

    for file in uploaded_files:
        with st.spinner(f"Processing {file.name}..."):
            extracted_text = extract_text(file)
            if extracted_text:
                summary = summarizer.summarize_text(extracted_text)
                summaries.append({"file_name": file.name, "summary": summary})

    st.success("✅ Summarization Complete!")

    # Display summaries
    for doc_summary in summaries:
        st.subheader(f"📄 {doc_summary['file_name']}")

        summary_data = doc_summary["summary"]
        if "error" in summary_data:
            st.error(summary_data["error"])
        else:
            st.markdown(f"### 📌 **{summary_data['document_title']}**")
            st.markdown("#### 📝 Key Clauses:")
            for clause in summary_data["key_clauses"]:
                st.write(f"- **{clause['clause_number']}.** {clause['description']}")

            st.markdown("#### 📜 Obligations:")
            for obligation in summary_data["obligations"]:
                st.write(f"- **{obligation['party']}**: {obligation['description']}")

            st.markdown("#### ⚠️ Limitations:")
            for limitation in summary_data["limitations"]:
                st.write(f"- {limitation['description']}")

            st.markdown("#### 🔑 Key Takeaways:")
            for takeaway in summary_data["key_takeaways"]:
                st.write(f"- {takeaway['description']}")

