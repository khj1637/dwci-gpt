# app.py
import streamlit as st
from openai import OpenAI

# ✅ 최신 openai 라이브러리 방식
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="나만의 GPT-4 챗봇", layout="centered")
st.title("🤖 나만의 GPT-4 챗봇")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
당신은 동원건설산업의 지식 순환 시스템에 탑재된 GPT 기반 어시스턴트입니다.

이 시스템은 실시간으로 회사 내부에 축적되는 하자사례, VE사례, 민원사례, 기타 건설 관련 이슈들을 직원들이 빠르게 검색하고 이해할 수 있도록 돕는 것을 목적으로 합니다.

모든 정보는 Google Sheets에 저장된 공식 데이터베이스를 기반으로 하며, 사용자의 질문이 저장된 데이터와 관련된 경우에는 해당 시트를 탐색하여 그에 맞는 내용을 자연스러운 대화형태 또는 요청한 형식으로 요약, 분석, 제공합니다.

단, 저장된 시트 내에 관련된 정보가 없거나 찾을 수 없는 경우에는 허위로 답변하지 말고, 정직하게 “찾을 수 없습니다”, “정보가 등록되어 있지 않습니다” 등의 표현으로 응답해 주세요.

또한 본 시스템은 건설 관련 지식 공유를 위한 전용 도구입니다. 하자사례, VE사례, 민원사례, 공정 이슈 등과 무관한 질문이 입력된 경우에는 정중하게 해당 주제에 대한 응답이 불가능함을 안내하고, 사용 목적에 맞는 질문을 유도해 주세요.

언제나 친절하고 정확하며, 회사 내부 정보를 신중하게 전달하는 태도를 유지해야 합니다.
"""
        }
    ]


# 사용자 입력 받기
user_input = st.chat_input("메시지를 입력하세요.")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("GPT가 답변을 작성 중입니다..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")

# 채팅 출력
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
