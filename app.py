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
        """Summarizes legal document text into a structured format."""
        try:
            if not text.strip():
                return {"error": "No text extracted from the document."}

            logging.info("Sending request to Azure OpenAI for summarization...")
            response = self.client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are an AI that extracts structured summaries from legal documents. "
                                                  "Ensure the response is in the requested format."},
                    {"role": "user", "content": f"Extract a structured summary from this legal document:\n{text}\n\n"
                                                 "Format the response as follows:\n\n"
                                                 "Title: <document_title>\n"
                                                 "Key Clauses:\n"
                                                 "1. <Clause 1 description>\n"
                                                 "2. <Clause 2 description>\n\n"
                                                 "Obligations:\n"
                                                 "- <Party A>: <Obligation>\n"
                                                 "- <Party B>: <Obligation>\n\n"
                                                 "Limitations:\n"
                                                 "- <Limitation 1>\n"
                                                 "- <Limitation 2>\n\n"
                                                 "Key Takeaways:\n"
                                                 "- <Key Takeaway 1>\n"
                                                 "- <Key Takeaway 2>\n\n"
                                                 "Return only the formatted text. Do not include JSON or extra text."}
                ],
                max_tokens=max_tokens,
                temperature=0.5
            )

            structured_summary = response.choices[0].message.content.strip()

            # Debugging: Print raw response from OpenAI
            logging.info(f"🔍 OpenAI Raw Response:\n{structured_summary}")

            if not structured_summary:
                return {"error": "Received an empty response from OpenAI."}

            return {"summary": structured_summary}

        except Exception as e:
            logging.error(f"❌ Error summarizing text: {e}")
            return {"error": str(e)}


# Function to extract text from different file types
def extract_text(uploaded_file):
    """
    Extract text from an uploaded PDF, DOCX, or TXT file.

    Args:
        uploaded_file: Streamlit file uploader object.

    Returns:
        str: Extracted text from the file.
    """
    try:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        # Handle PDFs
        if file_extension == "pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.read())
                temp_pdf_path = temp_pdf.name

            # Open the PDF and extract text
            doc = fitz.open(temp_pdf_path)
            extracted_text = "\n".join([page.get_text("text") for page in doc])
            doc.close()  # Ensure the file is closed before deletion

            # Now, remove the temporary file safely
            os.remove(temp_pdf_path)
            return extracted_text

        # Handle DOCX files
        elif file_extension == "docx":
            doc = docx.Document(uploaded_file)
            extracted_text = "\n".join([para.text for para in doc.paragraphs])
            return extracted_text

        # Handle TXT files
        elif file_extension == "txt":
            return uploaded_file.read().decode("utf-8")

        else:
            return f"Unsupported file format: {file_extension}"

    except Exception as e:
        return f"Error extracting text: {str(e)}"


# Function to truncate text if too long
def truncate_text(text, max_words=3000):
    """Truncates text to ensure it fits within OpenAI's limits."""
    words = text.split()
    return " ".join(words[:max_words]) if len(words) > max_words else text


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
            truncated_text = truncate_text(extracted_text)  # Ensure text is within OpenAI's limit
            summary = summarizer.summarize_text(truncated_text)
            summaries.append({"file_name": file.name, "summary": summary})

    st.success("✅ Summarization Complete!")

    # Display summaries
    for doc_summary in summaries:
        st.subheader(f"📄 {doc_summary['file_name']}")

        summary_data = doc_summary["summary"]
        if "error" in summary_data:
            st.error(summary_data["error"])
        else:
            st.markdown(f"### 📌 **Legal Document Summary**\n\n{summary_data['summary']}")
