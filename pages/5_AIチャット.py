import streamlit as st
from streamlit_extras.switch_page_button import switch_page

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("このページを閲覧するにはログインが必要です。")
    switch_page("main")

# AIチャットに相談
import streamlit as st
import sys
import os

# モジュールパスを追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.ai import ask_bedrock

st.set_page_config(page_title="AI幹事チャット", layout="centered")
st.title("AI幹事に質問してみよう")

# CSS: LINE風チャットUIとダークモード対応
st.markdown("""
<style>
.chat-container {
    max-width: 600px;
    margin: 0 auto;
}
.bubble {
    padding: 10px 15px;
    border-radius: 10px;
    margin: 5px 0;
    display: inline-block;
    max-width: 80%;
    word-wrap: break-word;
}
.user-bubble {
    background-color: #DCF8C6;
    color: black;
    margin-left: auto;
    text-align: right;
    border-bottom-right-radius: 0;
}
.ai-bubble {
    background-color: #F1F0F0;
    color: black;
    margin-right: auto;
    text-align: left;
    border-bottom-left-radius: 0;
}
@media (prefers-color-scheme: dark) {
    .user-bubble {
        background-color: #3cba54;
        color: white;
    }
    .ai-bubble {
        background-color: #555;
        color: white;
    }
}
</style>
""", unsafe_allow_html=True)

# チャット履歴をセッションに保持
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# 入力フォーム
with st.form("chat_form"):
    user_input = st.text_input("質問を入力（例：結婚式の余興のおすすめは？）", key="chat_input")
    submitted = st.form_submit_button("送信")

# 送信後の処理
if submitted and user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("AIが考え中..."):
        reply = ask_bedrock(user_input)
    st.session_state.chat_history.append(("ai", reply))

# チャット履歴の表示
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, msg in st.session_state.chat_history:
    bubble_class = "user-bubble" if role == "user" else "ai-bubble"
    st.markdown(f'<div class="bubble {bubble_class}">{msg}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
