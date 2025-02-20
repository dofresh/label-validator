# classes/extractor.py
import pandas as pd
import pdfplumber
import streamlit as st

class ExcelExtractor:
    @staticmethod
    def extract_sheet_text(excel_file, sheet_name):
        try:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            texts = []
            for col in df.columns:
                texts.extend(df[col].dropna().astype(str).tolist())
            return "\n".join(texts)
        except Exception as e:
            st.error(f"[{sheet_name}] 시트 처리 중 오류: {str(e)}")
            return ""

class PDFExtractor:
    @staticmethod
    def extract_text(pdf_file):
        text = ""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            st.error(f"[{pdf_file.name}] PDF 처리 중 오류: {str(e)}")
        return text
