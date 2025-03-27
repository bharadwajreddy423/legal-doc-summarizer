# 📑 AI-Powered Legal Document Summarizer  

![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-green) ![Azure](https://img.shields.io/badge/Azure-OpenAI-blue)  

## Overview  
This project is a **legal document summarization app** that uses **Azure OpenAI** to generate structured summaries from uploaded legal documents (PDF, DOCX, TXT). Users can upload documents, and the AI extracts **key clauses, obligations, limitations, and key takeaways** in a readable format.  

🔗 **Live App:** [Click here to try it](https://hm7wfwgmuzc6quxxttmbrf.streamlit.app/)  

## Features  
✅ Upload **PDF, DOCX, and TXT** files  
✅ Extract structured summaries using **Azure OpenAI**  
✅ Display results in a **clean format** (not raw JSON)  
✅ Supports multiple file uploads  

## 🛠️ Tech Stack  
- **Azure OpenAI** (GPT-4o model for summarization)  
- **Azure Document Intelligence** (for document processing)  
- **Streamlit** (UI for document upload & results display)  
- **Python** (FastAPI, Pandas, PyMuPDF, python-docx)  

## 📌 Setup Instructions  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/legal-doc-summarization.git
cd legal-doc-summarization
```

### 2️⃣ Create a Virtual Environment & Install Dependencies  
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables  
Since **secrets** are required for Azure services, use **Streamlit secrets** for deployment. For local testing, create a `.env` file:  
```ini
FORM_RECOGNIZER_ENDPOINT="your-form-recognizer-endpoint"
FORM_RECOGNIZER_KEY="your-form-recognizer-key"
OPENAI_ENDPOINT="your-azure-openai-endpoint"
OPENAI_KEY="your-azure-openai-key"
DEPLOYMENT_NAME="your-deployment-name"
API_VERSION="2024-05-01-preview"
```

### 4️⃣ Run the App Locally  
```bash
streamlit run app.py
```

## 📂 Project Structure  
```
📦 legal-doc-summarization
├── 📄 app.py                 # Streamlit app
├── 📄 config.py              # Configuration file (reads Streamlit secrets)
├── 📄 requirements.txt       # Python dependencies
├── 📄 README.md              # Project documentation
└── 📁 utils                  # Helper functions (if any)
```

## Deploying on Streamlit  
1. Push your code to GitHub  
2. Go to **Streamlit Cloud** and deploy using your GitHub repo  
3. Add your Azure **secrets** in the Streamlit deployment settings  

## 🤝 Contributing  
Pull requests are welcome! Feel free to fork the repo and submit changes.  

## 📜 License  
This project is **open-source** under the MIT License.  
