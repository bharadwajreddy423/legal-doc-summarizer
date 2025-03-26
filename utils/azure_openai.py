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

    def summarize_text(self, text: str, max_tokens: int = 700) -> dict:
        """
        Summarizes legal document text into a structured JSON format.

        Args:
            text (str): The extracted text from the document.
            max_tokens (int): Maximum token limit for response.

        Returns:
            dict: Structured JSON containing key details of the document.
        """
        try:
            logging.info("Sending request to Azure OpenAI for structured summarization...")

            response = self.client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are an AI that extracts structured summaries from legal documents. "
                                                  "You must always return output as valid JSON without additional text."},
                    {"role": "user", "content": f"Extract a structured summary from this legal document:\n{text}\n\n"
                                                 "Format the response as valid JSON:\n\n"
                                                 "{\n"
                                                 '  "document_title": "Title of the document",\n'
                                                 '  "key_clauses": [\n'
                                                 '    {"clause_number": 1, "description": "Clause description"}\n'
                                                 '  ],\n'
                                                 '  "obligations": [\n'
                                                 '    {"party": "Party name", "description": "Obligation details"}\n'
                                                 '  ],\n'
                                                 '  "limitations": [\n'
                                                 '    "Limitation 1", "Limitation 2"\n'
                                                 '  ],\n'
                                                 '  "key_takeaways": [\n'
                                                 '    "Takeaway 1", "Takeaway 2"\n'
                                                 '  ]\n'
                                                 "}\n\n"
                                                 "Only return valid JSON. No extra text, explanations, or markdown formatting."}
                ],
                max_tokens=max_tokens,
                temperature=0  # Enforce deterministic output
            )

            structured_summary = response.choices[0].message.content.strip()
            logging.info("Summary successfully generated.")

            # Remove markdown code blocks if present
            structured_summary = structured_summary.replace("```json", "").replace("```", "").strip()

            # Validate and return JSON
            try:
                summary_json = json.loads(structured_summary)
                return summary_json
            except json.JSONDecodeError:
                logging.error("❌ Invalid JSON format received from OpenAI.")
                return {"error": "Failed to parse response as JSON."}

        except Exception as e:
            logging.error(f"❌ Error summarizing text: {e}")
            return {"error": str(e)}


if __name__ == "__main__":
    summarizer = AzureOpenAISummarizer()

    sample_text = "This is a sample contract agreement that outlines the terms and conditions between two parties..."
    summary = summarizer.summarize_text(sample_text)

    if summary:
        print("\n✅ Summarized JSON Output:\n", json.dumps(summary, indent=4))
