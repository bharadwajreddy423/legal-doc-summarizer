from utils.azure_doc_intel import AzureDocumentIntelligence
from utils.azure_openai import AzureOpenAISummarizer

# Initialize Clients
doc_intel = AzureDocumentIntelligence()
summarizer = AzureOpenAISummarizer()

# Path to the sample legal document
sample_doc_path = "data/sample_demandnotice.pdf"

# Step 1: Extract Text from the Document
extracted_data = doc_intel.analyze_document(sample_doc_path)

if extracted_data:
    print("\n✅ Extracted Document Text:\n", extracted_data["text"])

    # Step 2: Summarize Extracted Text
    summary = summarizer.summarize_text(extracted_data["text"])

    if summary:
        print("\n📄 **Summarized Legal Document:**\n", summary)
