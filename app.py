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
        {"role": "system", "content": "당신은 유용하고 친절한 AI 어시스턴트입니다."}
    ]

# 사용자 입력 받기
user_input = st.chat_input("메시지를 입력하세요.")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("GPT가 답변을 작성 중입니다..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
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
