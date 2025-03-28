import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Document Intelligence
FORM_RECOGNIZER_ENDPOINT = os.getenv("FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("FORM_RECOGNIZER_KEY")

# Azure OpenAI
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_KEY = os.getenv("OPENAI_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION", "2024-05-01-preview")  # Default version





'''
import streamlit as st

# Azure Document Intelligence
FORM_RECOGNIZER_ENDPOINT = st.secrets["FORM_RECOGNIZER_ENDPOINT"]
FORM_RECOGNIZER_KEY = st.secrets["FORM_RECOGNIZER_KEY"]

# Azure OpenAI
OPENAI_ENDPOINT = st.secrets["OPENAI_ENDPOINT"]
OPENAI_KEY = st.secrets["OPENAI_KEY"]
DEPLOYMENT_NAME = st.secrets["DEPLOYMENT_NAME"]
API_VERSION = st.secrets["API_VERSION"]
'''