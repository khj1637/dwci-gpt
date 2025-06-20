import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from openai import OpenAI
import json

# ✅ OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["OPENAI"]["OPENAI_API_KEY"])

# ✅ Google Sheets 인증
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDS = Credentials.from_service_account_info(
    st.secrets["GCP_SERVICE_ACCOUNT"], scopes=SCOPES
)
gc = gspread.authorize(CREDS)

# ✅ 시트 열기
sheet_url = "https://docs.google.com/spreadsheets/d/1tHgvGiAttA21K_zdqEJXoMjwi9eGhO3NEyXzZOVRIhM"
sheet = gc.open_by_url(sheet_url)

# ✅ 모든 워크시트 데이터 전체 불러오기
defect_data = sheet.worksheet("defect_cases").get_all_records()
ve_data = sheet.worksheet("ve_cases").get_all_records()
misc_data = sheet.worksheet("misc_cases").get_all_records()

# ✅ Streamlit 설정
st.set_page_config(page_title="동원건설 지식순환 GPT", layout="centered")
st.markdown(
    """
    <h1 style='text-align: center;'>Knowledge Sharing GPT</h1>
    <div style='height: 20px;'></div>  <!-- 공백 한 줄 -->
    <p style='text-align: left; font-size: 0.85rem; color: #555;'>
        버전: v1.0.0<br>
        최종 업데이트: 2025년 6월 17일<br>
        개발자 : 동원건설산업 기술팀 김혁진
    </p>
    """,
    unsafe_allow_html=True
)

# ✅ 사용자 입력
user_input = st.chat_input("하자, VE, 민원 등 궁금한 점을 입력하세요.")
if "messages" not in st.session_state:
    st.session_state.messages = []

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("GPT가 정보를 분석하고 있습니다..."):
        try:
            # ✅ GPT 프롬프트 구성
            system_prompt = """
당신은 동원건설산업의 지식 순환 시스템에 탑재된 GPT 기반 어시스턴트입니다.
이 시스템은 실시간으로 회사 내부에 축적되는 하자사례, VE사례, 민원사례, 기타 건설 관련 이슈들을 직원들이 빠르게 검색하고 이해할 수 있도록 돕는 것을 목적으로 합니다.
모든 정보는 Google Sheets에 저장된 공식 데이터베이스를 기반으로 하며, 사용자의 질문이 저장된 데이터와 관련된 경우에는 해당 시트를 탐색하여 그에 맞는 내용을 자연스러운 대화형태 또는 요청한 형식으로 요약, 분석, 제공합니다.
단, 저장된 시트 내에 관련된 정보가 없거나 찾을 수 없는 경우에는 허위로 답변하지 말고, 정직하게 “찾을 수 없습니다”, “정보가 등록되어 있지 않습니다” 등의 표현으로 응답해 주세요.
또한 본 시스템은 건설 관련 지식 공유를 위한 전용 도구입니다. 하자사례, VE사례, 민원사례, 공정 이슈 등과 무관한 질문이 입력된 경우에는 정중하게 해당 주제에 대한 응답이 불가능함을 안내하고, 사용 목적에 맞는 질문을 유도해 주세요.
언제나 친절하고 정확하며, 회사 내부 정보를 신중하게 전달하는 태도를 유지해야 합니다.
사용자의 질문에 따라 다음 세 가지 워크시트 중 적절한 곳에서 정보를 찾아 요약하거나 응답하세요:

- 하자사례 관련 → defect_cases
- VE사례 관련 → ve_cases
- 민원/기타 이슈 관련 → misc_cases

정보는 아래 [데이터] 항목에서 제공합니다.
반드시 관련된 시트에서만 정보를 사용하세요. 적절한 내용이 없으면 '등록된 정보가 없습니다'라고 정직하게 안내하세요.
친절하고 명확한 말투로 응답하세요.
"""

            # ✅ 전체 데이터 JSON 문자열로 직렬화 (단순화 위해 json.dumps 사용)
            data_context = f"""
[defect_cases]
{json.dumps(defect_data, ensure_ascii=False)}

[ve_cases]
{json.dumps(ve_data, ensure_ascii=False)}

[misc_cases]
{json.dumps(misc_data, ensure_ascii=False)}
"""

            # ✅ GPT 호출
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": f"{user_input}\n\n{data_context.strip()}"}
                ]
            )

            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")

# ✅ 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
