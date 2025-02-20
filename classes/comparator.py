# classes/comparator.py
import difflib
from langchain.schema import SystemMessage, HumanMessage

class AIComparator:
    def __init__(self, llm):
        self.llm = llm

    def ai_compare_texts(self, excel_text, pdf_text, max_chars=1500):
        excel_snippet = excel_text[:max_chars]
        pdf_snippet = pdf_text[:max_chars]
        prompt = f"""아래 두 텍스트의 의미가 동일한지 판단해줘.

[Excel 텍스트]:
{excel_snippet}

[PDF 텍스트]:
{pdf_snippet}

두 텍스트의 의미가 동일하면 "동일"이라고 응답하고, 그렇지 않다면 "다름"이라고 응답한 후 주요 차이점을 간략히 설명해줘.
"""
        try:
            response = self.llm.invoke(
                [
                    SystemMessage(content="너는 한글 텍스트 비교 전문가야."),
                    HumanMessage(content=prompt)
                ]
            )
            result = response.content
            return result
        except Exception as e:
            return f"AI 비교 중 오류 발생: {str(e)}"

    def diff_texts(self, excel_text, pdf_text):
        diff = "\n".join(difflib.unified_diff(
            excel_text.splitlines(),
            pdf_text.splitlines(),
            fromfile='Excel',
            tofile='PDF',
            lineterm=''
        ))
        return diff
