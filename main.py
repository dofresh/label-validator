# main.py
import streamlit as st
from classes.assistant import CrossValidationAssistant
from classes.ui import CrossValidationUI

def main():
    st.title("다중 AI 기반 한글 표시사항 교차검증 시스템")
    st.markdown("""
    이 시스템은 여러 항목의 한글 표시사항(Excel 파일의 여러 시트)과 최종 결과물(PDF 파일)을 교차검증하여,
    디자인된 박스의 표시 내용은 의미상 동일하더라도 실제 문자가 다를 경우 AI를 통해 차이를 분석하고,
    별도로 한글 표시사항의 오타나 인간의 실수를 검증하여 수정안을 제안합니다.
    """)

    assistant = CrossValidationAssistant()
    ui = CrossValidationUI(assistant)

    excel_file, pdf_files = ui.render_file_upload()
    if not excel_file or not pdf_files:
        st.info("모든 파일을 업로드하세요.")
        return

    sheet_names, mapping, pdf_file_dict = ui.render_sheet_pdf_mapping(excel_file, pdf_files)
    if sheet_names:
        ui.render_results(excel_file, sheet_names, mapping, pdf_file_dict)
        ui.render_label_validation(excel_file, sheet_names)

if __name__ == "__main__":
    main()
