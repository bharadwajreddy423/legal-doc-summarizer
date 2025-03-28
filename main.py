import json
from utils.azure_doc_intel import AzureDocumentIntelligence
from utils.azure_openai import AzureOpenAISummarizer
from config import FORM_RECOGNIZER_ENDPOINT, FORM_RECOGNIZER_KEY, OPENAI_ENDPOINT, OPENAI_KEY, DEPLOYMENT_NAME

# ✅ Initialize Clients using values from config.py
doc_intel = AzureDocumentIntelligence(FORM_RECOGNIZER_ENDPOINT, FORM_RECOGNIZER_KEY)
summarizer = AzureOpenAISummarizer(OPENAI_ENDPOINT, OPENAI_KEY, DEPLOYMENT_NAME)

# ✅ Path to the sample legal document
sample_doc_path = "data/sample_demandnotice.pdf"

# ✅ Step 1: Extract Text from the Document
with open(sample_doc_path, "rb") as file:
    extracted_data = doc_intel.analyze_document(file)

if not extracted_data.get("extracted_data"):
    print("\n❌ No text extracted from the document. Please check the file format.")
else:
    extracted_text = extracted_data["extracted_data"]
    print("\n✅ Extracted Document Text:\n", extracted_text)

    # ✅ Step 2: Summarize Extracted Text
    summary = summarizer.summarize_text(extracted_text)

    if "error" in summary:
        print("\n❌ OpenAI Error:", summary["error"])
        print("🔍 Raw OpenAI Response:", summary.get("raw_response", "No response received"))
    else:
        print("\n📄 **Summarized Legal Document:**\n", json.dumps(summary, indent=4))
