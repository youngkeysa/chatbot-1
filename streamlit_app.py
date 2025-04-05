import streamlit as st
from openai import OpenAI

# Set Streamlit page config
st.set_page_config(page_title="심리상담 챗봇", page_icon="💬", layout="centered")

# Show title and description.
st.title("💬 심리상담 챗봇")
st.markdown(
    """
    이 챗봇은 당신의 심리적 어려움을 나누고 위로하기 위한 상담 도우미입니다. 💗

    **주의:** 이 챗봇은 전문 의료 상담이 아닌 AI 기반 대화 도우미이며, 심각한 정신적 고통이 있다면 반드시 전문가의 상담을 받으세요.
    
    👉 OpenAI API 키를 입력해야 사용 가능합니다. [API 키 발급 링크](https://platform.openai.com/account/api-keys)
    """
)

# 사용자로부터 OpenAI API 키 입력받기
openai_api_key = st.text_input("🔑 OpenAI API Key 입력", type="password")
if not openai_api_key:
    st.info("API 키를 입력해 주세요. 위 링크에서 발급 가능합니다.", icon="🔐")
    st.stop()

# OpenAI 클라이언트 생성
client = OpenAI(api_key=openai_api_key)

# 대화 저장을 위한 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 공감 능력 있고 따뜻한 심리상담사입니다. 상대방을 위로하고 조언해 주세요."}
    ]

# 기존 메시지 출력
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 사용자 입력 받기
if user_input := st.chat_input("마음 속 이야기를 나눠보세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        

    # GPT 응답 생성
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-o3-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    # 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": response})

