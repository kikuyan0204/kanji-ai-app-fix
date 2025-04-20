import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from supabase import create_client, Client
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="幹事アシストAI", layout="centered")

# --- CSS（ダークモード完全対応＋selectbox白ボックス除去） ---
st.markdown("""
<style>
body, .main, .block-container {
    background-color: #f9f9f9;
    color: #333;
    font-family: 'Hiragino Kaku Gothic ProN', 'Helvetica Neue', sans-serif;
}
.stForm {
    background: #fff;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    margin-top: 1.5rem;
}
.stButton>button {
    background-color: #ff6f61;
    color: white;
    font-weight: bold;
    border: none;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-size: 16px;
    width: 100%;
}
.stButton>button:hover {
    background-color: #e95c50;
}
.sidebar .sidebar-content::before {
    content: "🛍️ 幹事アシスト";
    font-size: 1.4rem;
    font-weight: bold;
    color: #ff6f61;
    display: block;
    margin-bottom: 1.5rem;
}
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

/* ===== ダークモード対応（selectbox白背景除去） ===== */
@media (prefers-color-scheme: dark) {
    body, .main, .block-container {
        background-color: #1e1e1e !important;
        color: #f0f0f0 !important;
    }
    .stForm, .chat-container, .bubble {
        background-color: #2c2c2c !important;
        color: #f0f0f0 !important;
    }
    .user-bubble {
        background-color: #3cba54;
        color: white;
    }
    .ai-bubble {
        background-color: #555;
        color: white;
    }
    .stTextInput > div > input,
    .stDateInput input,
    .stSelectbox div,
    textarea {
        background-color: #333 !important;
        color: #f0f0f0 !important;
        border-color: #666 !important;
    }
    .stButton>button {
        background-color: #ff6f61 !important;
        color: white !important;
    }
    .stButton>button:hover {
        background-color: #e95c50 !important;
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }

    [data-baseweb="select"] > div {
        background-color: #333 !important;
        color: #fff !important;
        border-color: #666 !important;
    }
    [data-baseweb="select"] svg {
        fill: #ffffff !important;
    }
    [data-baseweb="select"] .css-1dimb5e-singleValue,
    [data-baseweb="select"] .css-1n6sfyn-ValueContainer {
        background-color: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- 認証とセッション ---
if "user" not in st.session_state:
    st.session_state.user = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# --- サイドバー ---
if st.session_state.user:
    with st.sidebar:
        if st.button("ログアウト"):
            st.session_state.user = None
            st.rerun()

# --- 認証画面 ---
if st.session_state.user is None:
    mode = st.session_state.auth_mode
    st.title("幹事アシストAI")
    st.subheader("ログインまたは新規登録して始めましょう")

    with st.form("auth_form"):
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        submit_btn = st.form_submit_button("ログイン" if mode == "login" else "新規登録")

    if submit_btn:
        try:
            if mode == "login":
                auth_response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                st.session_state.user = auth_response.user
                st.success("ログインに成功しました！")
                st.rerun()
            else:
                auth_response = supabase.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "emailRedirectTo": "http://localhost:8501"
                    }
                })
                st.success("ユーザー登録が完了しました。メールの認証リンクをクリックしてからログインしてください。")
                st.session_state.auth_mode = "login"
        except Exception as e:
            st.error(f"{'ログイン' if mode == 'login' else '新規登録'}に失敗しました: {e}")

    if mode == "login":
        if st.button("新規登録はこちら"):
            st.session_state.auth_mode = "signup"
            st.rerun()
    else:
        if st.button("すでにアカウントをお持ちの方はこちら"):
            st.session_state.auth_mode = "login"
            st.rerun()

# --- メイン画面（ログイン後） ---
else:
    st.title("幹事アシストAI")
    st.subheader("イベント幹事のあなたに、AIが寄り添います。")

    st.markdown("### イベントを作成")
    # ✅ 固定選択肢：白い文字入力ボックス完全消去！
    event_type = st.selectbox("イベントの種類を選んでください", ["飲み会", "ゴルフコンペ"])

    if st.button("AIアシスタントに相談する"):
        if event_type == "飲み会":
            switch_page("飲み会検索")
        else:
            switch_page("ゴルフ場検索")

    st.markdown("---")
    st.markdown("### AI幹事に相談する")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form("chat_form"):
        user_input = st.text_input("AIに質問してみよう（例：結婚式の余興のおすすめは？）", key="main_chat_input")
        submitted = st.form_submit_button("送信")

    if submitted and user_input:
        from utils.ai import ask_bedrock
        st.session_state.chat_history.append(("user", user_input))
        with st.spinner("AIが考え中..."):
            reply = ask_bedrock(user_input)
        st.session_state.chat_history.append(("ai", reply))

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for role, msg in st.session_state.chat_history:
        bubble_class = "user-bubble" if role == "user" else "ai-bubble"
        st.markdown(f'<div class="bubble {bubble_class}">{msg}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
