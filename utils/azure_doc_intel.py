import os
import sys
import json
import logging
from openai import AzureOpenAI

# Add project root to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import OPENAI_ENDPOINT, OPENAI_KEY, API_VERSION, DEPLOYMENT_NAME

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AzureOpenAISummarizer:
    """
    Azure OpenAI-based summarizer for legal documents.
    """

    def __init__(self):
        """Initialize Azure OpenAI client."""
        self.client = AzureOpenAI(
            azure_endpoint=OPENAI_ENDPOINT,
            api_key=OPENAI_KEY,
            api_version=API_VERSION,
        )

    def summarize_text(self, text: str, max_tokens: int = 500) -> dict:
        """
        Summarizes legal document text into a structured JSON format.

        Args:
            text (str): The extracted text from the document.
            max_tokens (int): Maximum token limit for response.

        Returns:
            dict: Structured JSON containing key details of the document.
        """
        try:
            logging.info("Sending request to Azure OpenAI for summarization...")
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
            logging.info("Summary successfully generated.")

            # Validate if output is JSON
            try:
                summary_json = json.loads(structured_summary)
                return summary_json
            except json.JSONDecodeError:
                logging.error("Invalid JSON format received from OpenAI.")
                return {"error": "Failed to parse response as JSON."}

        except Exception as e:
            logging.error(f"❌ Error summarizing text: {e}")
            return {"error": str(e)}

    def summarize_multiple_documents(self, documents: list) -> list:
        """
        Processes multiple documents and returns a list of structured summaries.

        Args:
            documents (list): List of text documents.

        Returns:
            list: List of structured summaries.
        """
        summaries = []
        for idx, doc in enumerate(documents):
            logging.info(f"Processing document {idx + 1}/{len(documents)}...")
            summary = self.summarize_text(doc)
            summaries.append(summary)
        return summaries


if __name__ == "__main__":
    summarizer = AzureOpenAISummarizer()

    # Sample multiple documents
    sample_documents = [
        "This is a sample contract agreement that outlines the terms and conditions between two parties...",
        "Another legal notice demanding repayment under specified conditions..."
    ]

    summaries = summarizer.summarize_multiple_documents(sample_documents)

    if summaries:
        print("\n✅ Summarized JSON Output:\n", json.dumps(summaries, indent=4))
