# classes/assistant.py
import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings

class CrossValidationAssistant:
    def __init__(self):
        self.api_service = None
        self.api_key = None
        self.llm = None
        self.embeddings = None
        self.setup_credentials()

    def setup_credentials(self):
        st.sidebar.header("API 설정")
        self.api_service = st.sidebar.selectbox("사용할 AI 서비스", ["Google Gemini", "OpenAI GPT"])
        self.api_key = st.sidebar.text_input("API Key", type="password")
        if self.api_key:
            if self.api_service == "Google Gemini":
                os.environ["GOOGLE_API_KEY"] = self.api_key
                self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
                self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            elif self.api_service == "OpenAI GPT":
                os.environ["OPENAI_API_KEY"] = self.api_key
                self.llm = ChatOpenAI(model_name="gpt-4")
                self.embeddings = OpenAIEmbeddings()
