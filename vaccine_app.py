import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import date

# =============================
# Google認証（Secretsに保存済みのJSONを使用）
# =============================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)
client = gspread.authorize(creds)

# =============================
# スプレッドシート設定
# =============================
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1_5KXhHhLSLZv2FazFV7S1hTS6YY-JjDwEs0uzFpniqM/edit"
sheet = client.open_by_url(SPREADSHEET_URL).sheet1

# =============================
# Streamlit UI
# =============================
st.set_page_config(page_title="予防接種スケジュール共有アプリ", page_icon="💉", layout="wide")
st.title("💉 予防接種スケジュール（Google共有版・無料）")

# =============================
# 新規登録フォーム
# =============================
st.header("👩‍⚕️ 新しい患者データを追加")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("患者名")
with col2:
    vaccine = st.text_input("ワクチン名")

col3, col4 = st.columns(2)
with col3:
    last_date = st.date_input("最終接種日", date.today())
with col4:
    doses = st.number_input("接種回数", min_value=0, step=1)

if st.button("💾 保存"):
    today = str(date.today())
