from langchain.schema import SystemMessage, HumanMessage

class LabelValidator:
    def __init__(self, llm):
        self.llm = llm

    def validate_label(self, text, product_category="일반"):
        # 도메인별 기준 추가: 냉동식품의 경우 -18℃ 이하
        domain_instructions = ""
        if product_category == "냉동":
            domain_instructions = "※ 냉동식품의 경우, 보관 온도는 반드시 -18℃ 이하여야 합니다.\n"

        snippet = text[:1500]
        prompt = f"""아래 한글 표시사항의 텍스트를 분석하여 오타, 문법 오류, 혹은 논리적 모순(예: 냉동식품에 '18도 이하'와 같이 부적절한 보관 온도)이 있는지 확인하고, 문제가 없으면 "문제 없음"이라고 응답해주는데, 순서는 법적으로 문제가 되는 사안을 먼저 그 다음 법적으로 문제가 되지않는 사안을 해주고 구분선을 넣은 다음 수정안을 제시해줘 .

{domain_instructions}
[한글 표시사항]:
{snippet}
"""
        response = self.llm.invoke(
            [
                SystemMessage(content="너는 한글 텍스트 검증 전문가야."),
                HumanMessage(content=prompt)
            ]
        )
        result = response.content
        return result
