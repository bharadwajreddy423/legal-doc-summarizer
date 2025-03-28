import os
import logging
import tempfile
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

class AzureDocumentIntelligence:
    """Handles document processing using Azure Document Intelligence."""

    def __init__(self, endpoint: str, api_key: str):
        """Initialize the Azure Document Intelligence client."""
        self.client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(api_key))
        logging.info("✅ Azure Document Intelligence client initialized.")

    def analyze_document(self, uploaded_file, model="prebuilt-layout"):
        """Analyze a legal document using Azure Document Intelligence."""
        try:
            if not uploaded_file:
                return {"error": "No file provided for processing."}

            file_extension = uploaded_file.name.split(".")[-1].lower()

            # Create a temporary file to handle document processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            logging.info(f"📄 Processing document: {uploaded_file.name}")

            # Open and analyze the document using Azure Document Intelligence
            with open(temp_file_path, "rb") as document_stream:
                poller = self.client.begin_analyze_document(model, document_stream)
                result = poller.result()

            os.remove(temp_file_path)  # Clean up temp file

            extracted_text = self._parse_analysis_result(result)

            if not extracted_text.strip():
                logging.warning("⚠️ No text was extracted from the document.")
                return {"error": "No text extracted from the document. Ensure the file is readable."}

            return {"file_name": uploaded_file.name, "extracted_data": extracted_text}

        except Exception as e:
            logging.error(f"❌ Error processing document: {e}")
            return {"error": str(e)}

    def _parse_analysis_result(self, result):
        """Extract text content from the Azure Document Intelligence response."""
        try:
            extracted_text = ""

            for page in result.pages:
                if hasattr(page, "lines"):
                    extracted_text += "\n".join([line.content for line in page.lines]) + "\n"

            return extracted_text.strip()

        except Exception as e:
            logging.error(f"❌ Error parsing document results: {e}")
            return ""

