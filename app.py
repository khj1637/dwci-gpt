# app.py
import streamlit as st
import openai

# 페이지 설정
st.set_page_config(
    page_title="나만의 GPT-4 챗봇",
    page_icon="🤖",
    layout="centered"
)

st.title("🧠 나만의 GPT-4 챗봇")

# 🔑 OpenAI API Key (Streamlit Cloud에서는 secrets 사용)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 🔄 대화 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 유용하고 친절한 AI 어시스턴트입니다."}
    ]

# 📝 사용자 입력 받기
user_input = st.chat_input("메시지를 입력하세요.")
if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": user_input})

    # GPT 응답 생성
    with st.spinner("GPT가 생각 중입니다..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message["content"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")

# 💬 채팅 출력
for message in st.session_state.messages[1:]:  # system 메시지는 생략
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
