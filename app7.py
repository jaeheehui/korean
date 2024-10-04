import streamlit as st
import openai
import pandas as pd

# OpenAI API 키 설정
openai.api_key ="your_key"  # 여기에 실제 API 키를 입력하세요


# Excel 파일 읽기 (Vocabulary, Grammar 열이 있는 Excel 파일 경로)
excel_data = excel_data = pd.read_excel("study_data.xlsx")

# Streamlit 웹 페이지 구성
st.title("GPT 기반 한국어 쓰기 과제 도구")

# 사용자 입력
user_input = st.text_area("쓰기 과제를 입력하세요:")

# 피드백 생성 버튼
if st.button("검사 받기"):
    if user_input:
        # Excel 데이터를 GPT 프롬프트에 추가
        vocab_data = excel_data['어휘'].dropna().tolist()  # Vocabulary 열에서 어휘 불러오기
        grammar_data = excel_data['문법'].dropna().tolist()  # Grammar 열에서 문법 불러오기

        # GPT 프롬프트 구성 (주제 관련 부분 제거)
        prompt = (
            f"너는 한국어 교사 역할을 맡고 있다. 학습자가 작성한 글에서 오직 문법적 오류만 수정하라. "
            f"문맥이나 내용은 고치지 말고, 학습자가 작성한 원래 내용에 충실하게 문법적 오류만 수정해라. "
            f"엑셀에서 제공한 문법을 쓸 수 있는 부분에만 문법을 적용하라. "
            f"동일한 표현을 반복해서 사용하지 말고, 자연스럽게 어휘와 문법을 활용해라. "
            f"엑셀에서 제공된 문법 항목은 최소 2회 이상 사용해야 한다. "
            f"수정된 부분만 빨간색으로 표시하여 모범 답안을 작성해라.\n\n"
            f"사용할 어휘: {', '.join(vocab_data)}\n"
            f"사용할 문법: {', '.join(grammar_data)}\n\n"
            f"학습자가 작성한 글:\n{user_input}\n\n"
            f"문법적 오류만 고쳐서 모범 답안을 작성해라. 엑셀에서 사용한 어휘와 문법 부분은 빨간색으로 표시해라."
        )

        # GPT API 호출 (최신 방식 사용)
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0125:personal:lev3grammar:AEVA4SJm",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # GPT 피드백 출력
        feedback = response['choices'][0]['message']['content'].strip()

        # Streamlit에서 HTML로 출력하기 (unsafe_allow_html=True 옵션을 사용하여 HTML 태그를 허용)
        styled_feedback = feedback.replace("<span style='color:red'>", "<mark style='background-color:red; color:white'>").replace("</span>", "</mark>")
        st.markdown(styled_feedback, unsafe_allow_html=True)
    else:
        st.write("과제를 먼저 입력하세요.")
