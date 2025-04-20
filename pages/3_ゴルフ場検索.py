# ゴルフ場検索
import streamlit as st
from dotenv import load_dotenv
from utils.gora import search_golf_courses
from streamlit_extras.switch_page_button import switch_page

# --- 認証チェックをここで追加 ---
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("このページを閲覧するにはログインが必要です。")
    switch_page("main")


load_dotenv()

st.set_page_config(page_title="ゴルフ場検索", layout="centered")

# --- CSS（白ボックス削除＋ダークモード対応） ---
st.markdown("""
    <style>
        .title-text {
            text-align: center;
            font-size: 2em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 1rem;
        }
        .form-section {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            max-width: 600px;
            margin: auto;
        }
        .search-button button {
            background-color: #ff6f61;
            color: white;
            font-weight: bold;
            border: none;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-size: 16px;
            width: 100%;
            transition: background-color 0.3s ease;
        }
        .search-button button:hover {
            background-color: #e95c50;
        }
        .result-card {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 14px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
            padding: 1rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
            transition: transform 0.2s ease;
            margin-bottom: 1rem;
        }
        .result-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
        }
        .result-image {
            display: block !important;
            width: 100% !important;
            height: 180px !important;
            object-fit: cover !important;
            border-radius: 8px !important;
            margin-bottom: 0.75rem;
        }
        .golf-name {
            font-size: 1.1rem;
            font-weight: 600;
            min-height: 3.5rem;
            margin: 0.5rem 0;
        }
        .weather-button button {
            background-color: #ff6f61 !important;
            color: white !important;
            font-weight: bold;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 14px;
            width: 100%;
            transition: background-color 0.3s ease;
        }
        .weather-button button:hover {
            background-color: #e95c50 !important;
        }
        @media screen and (max-width: 768px) {
            .form-section {
                padding: 1rem;
                margin: 0 0.5rem;
                max-width: 100% !important;
            }
            .golf-name {
                font-size: 1rem !important;
            }
        }
        @media (prefers-color-scheme: dark) {
            body, .main, .block-container {
                background-color: #1e1e1e !important;
                color: #f0f0f0 !important;
            }
            .form-section, .result-card {
                background-color: #2c2c2c !important;
                color: #f0f0f0 !important;
                border-color: #444 !important;
            }
            .stTextInput > div > input,
            .stDateInput input,
            .stSelectbox div,
            textarea {
                background-color: #333 !important;
                color: #f0f0f0 !important;
                border-color: #666 !important;
            }
            .stButton button {
                background-color: #ff6f61 !important;
                color: white !important;
            }
            .stButton button:hover {
                background-color: #e95c50 !important;
            }
            .title-text {
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

# --- タイトル ---
st.markdown("<div class='title-text'>ゴルフ場を検索</div>", unsafe_allow_html=True)

if "courses" not in st.session_state:
    st.session_state["courses"] = None

# --- 入力フォーム ---
st.markdown("<div class='form-section'>", unsafe_allow_html=True)

with st.form("golf_form"):
    area = st.selectbox("都道府県を選択", [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
        "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
        "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
        "岐阜県", "静岡県", "愛知県", "三重県",
        "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
        "鳥取県", "島根県", "岡山県", "広島県", "山口県",
        "徳島県", "香川県", "愛媛県", "高知県",
        "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
    ])
    fee = st.selectbox("最大料金（円）", [None, 5000, 8000, 10000, 15000, 20000])
    style = st.selectbox("プレースタイル", [None, "セルフ", "キャディ付き"])
    submitted = st.form_submit_button("ゴルフ場を検索")

st.markdown("</div>", unsafe_allow_html=True)

# --- 検索処理 ---
if submitted:
    courses = search_golf_courses(area=area, fee=fee, style=style)
    if courses:
        st.session_state["courses"] = courses
    else:
        st.warning("条件に一致するゴルフ場が見つかりませんでした。")
        st.session_state["courses"] = None

# --- 検索結果表示 ---
if st.session_state["courses"]:
    st.subheader("検索結果")
    cols = st.columns(3)

    for idx, c in enumerate(st.session_state["courses"]):
        item = c["Item"]
        image_url = item.get("golfCourseImageUrl", "")
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                <div class='result-card'>
                    <img src="{image_url}" class="result-image" />
                    <div class='golf-name'>{item["golfCourseName"]}</div>
                    <a href="{item["golfCourseDetailUrl"]}" target="_blank">楽天GORAで詳細を見る</a>
                """, unsafe_allow_html=True)

                if st.button("プレー当日・プレー終了時の天候と渋滞情報", key=f"route_{idx}"):
                    st.session_state["selected_course"] = {
                        "name": item["golfCourseName"],
                        "lat": item["latitude"],
                        "lon": item["longitude"]
                    }
                    switch_page("天気予報・渋滞情報")

                st.markdown("</div>", unsafe_allow_html=True)