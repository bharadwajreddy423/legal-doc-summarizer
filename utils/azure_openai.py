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

    def __init__(self, endpoint, api_key, deployment_name, api_version="2024-05-01-preview"):
        """Initialize Azure OpenAI client with authentication details."""
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        self.deployment_name = deployment_name

    def summarize_text(self, text: str, max_tokens: int = 500) -> dict:
        """Summarizes legal document text into a structured JSON format."""
        try:
            if not text or not isinstance(text, str):
                return {"error": "No valid text provided for summarization."}

            logging.info("Sending request to Azure OpenAI for summarization...")

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an AI that extracts structured summaries from legal documents. "
                                                  "Your response must be valid JSON with no extra text."},
                    {"role": "user", "content": f"Extract a structured summary from this legal document:\n{text}\n\n"
                                                 "Respond in JSON format with:\n"
                                                 "{ \"document_title\": \"\", \"key_clauses\": [], "
                                                 "\"obligations\": {}, \"limitations\": [], \"key_takeaways\": [] }"}
                ],
                max_tokens=max_tokens,
                temperature=0.5
            )

            structured_summary = response.choices[0].message.content.strip()

            if not structured_summary:
                return {"error": "Received an empty response from OpenAI."}

            try:
                return json.loads(structured_summary)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON received: {structured_summary}")
                return {"error": "JSON parsing error", "raw_response": structured_summary}

        except Exception as e:
            logging.error(f"❌ Error summarizing text: {e}")
            return {"error": str(e)}
