# classes/ui.py (일부)
import streamlit as st
import pandas as pd
from .extractor import ExcelExtractor, PDFExtractor
from .comparator import AIComparator
from .label_validator import LabelValidator
from .local_storage import load_mapping_from_file, save_mapping_to_file

class CrossValidationUI:
    def __init__(self, assistant):
        self.assistant = assistant

    def render_file_upload(self):
        st.sidebar.header("파일 업로드")
        excel_file = st.sidebar.file_uploader("Excel 파일 업로드 (여러 시트 포함)", type=["xlsx"])
        pdf_files = st.sidebar.file_uploader("PDF 파일 업로드 (최종 결과물)", type=["pdf"], accept_multiple_files=True)
        return excel_file, pdf_files

    def render_sheet_pdf_mapping(self, excel_file, pdf_files):
        try:
            xls = pd.ExcelFile(excel_file)
            sheet_names = xls.sheet_names
            st.write("Excel 파일 내 시트 목록:")
            st.write(sheet_names)
        except Exception as e:
            st.error(f"Excel 파일 읽기 오류: {str(e)}")
            return None, None, None

        # PDF 파일들을 이름(확장자 제거) 기준으로 딕셔너리 생성
        pdf_file_dict = {}
        for pdf in pdf_files:
            key = pdf.name.rsplit(".", 1)[0]
            pdf_file_dict[key] = pdf

        # st.session_state를 이용하여 매핑 정보를 자동으로 불러오기
        if "mapping" not in st.session_state:
            st.session_state.mapping = load_mapping_from_file()

        stored_mapping = st.session_state.mapping  # 파일에 저장된 매핑 또는 빈 dict

        st.sidebar.header("시트 - PDF 매핑 설정")
        mapping = {}
        for sheet in sheet_names:
            default_option = "None"
            options = ["None"] + list(pdf_file_dict.keys())
            # 저장된 매핑이 있으면 기본값으로 사용
            if sheet in stored_mapping and stored_mapping[sheet] in options:
                default_option = stored_mapping[sheet]
            elif sheet in pdf_file_dict:
                default_option = sheet
            mapping[sheet] = st.sidebar.selectbox(
                f"'{sheet}' 시트에 매핑할 PDF 파일 선택",
                options=options,
                index=options.index(default_option),
                key=f"map_{sheet}"
            )
        # 변경된 매핑 정보를 세션에 저장하고 파일에도 저장
        st.session_state.mapping = mapping
        save_mapping_to_file(mapping)
        return sheet_names, mapping, pdf_file_dict

    def render_results(self, excel_file, sheet_names, mapping, pdf_file_dict):
        if st.button("교차검증 실행"):
            st.header("교차검증 결과")
            if not self.assistant.llm:
                st.error("먼저 API 키를 입력하여 AI 서비스를 설정하세요.")
                return

            comparator = AIComparator(self.assistant.llm)
            for sheet in sheet_names:
                mapped_pdf_key = mapping[sheet]
                st.subheader(f"시트: {sheet}")
                excel_text = ExcelExtractor.extract_sheet_text(excel_file, sheet)
                if mapped_pdf_key == "None":
                    st.warning(f"'{sheet}' 시트에 매핑된 PDF 파일이 없습니다. 수동으로 매핑해주세요.")
                    continue
                pdf_file = pdf_file_dict.get(mapped_pdf_key)
                if not pdf_file:
                    st.error(f"매핑된 PDF 파일 '{mapped_pdf_key}'을(를) 찾을 수 없습니다.")
                    continue
                pdf_text = PDFExtractor.extract_text(pdf_file)
                if not excel_text:
                    st.error(f"[{sheet}] 시트에서 텍스트를 추출하지 못했습니다.")
                    continue
                if not pdf_text:
                    st.error(f"[{pdf_file.name}] PDF에서 텍스트를 추출하지 못했습니다.")
                    continue

                st.markdown("**AI 기반 의미 비교 결과:**")
                result = comparator.ai_compare_texts(excel_text, pdf_text)
                st.text_area(f"{sheet} vs {pdf_file.name}", result, height=250)

                st.markdown("**문자 단위 차이 (옵션):**")
                diff = comparator.diff_texts(excel_text, pdf_text)
                if diff.strip():
                    st.text_area("Diff 결과", diff, height=250)
                else:
                    st.success("두 텍스트의 차이가 발견되지 않았습니다.")

    def render_label_validation(self, excel_file, sheet_names):
        st.header("한글 표시사항 검증")
        selected_sheet = st.selectbox("검증할 시트 선택", sheet_names)
        if st.button("검증 실행", key="label_validation"):
            excel_text = ExcelExtractor.extract_sheet_text(excel_file, selected_sheet)
            if not excel_text:
                st.error(f"[{selected_sheet}] 시트에서 텍스트를 추출하지 못했습니다.")
            else:
                if not self.assistant.llm:
                    st.error("먼저 API 키를 입력하여 AI 서비스를 설정하세요.")
                    return
                validator = LabelValidator(self.assistant.llm)
                result = validator.validate_label(excel_text)
                st.text_area(f"{selected_sheet} 검증 결과", result, height=300)
