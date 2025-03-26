import streamlit as st

# Azure Document Intelligence
FORM_RECOGNIZER_ENDPOINT = st.secrets["FORM_RECOGNIZER_ENDPOINT"]
FORM_RECOGNIZER_KEY = st.secrets["FORM_RECOGNIZER_KEY"]

# Azure OpenAI
OPENAI_ENDPOINT = st.secrets["OPENAI_ENDPOINT"]
OPENAI_KEY = st.secrets["OPENAI_KEY"]
DEPLOYMENT_NAME = st.secrets["DEPLOYMENT_NAME"]
API_VERSION = st.secrets["API_VERSION"]
