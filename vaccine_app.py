import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(layout="wide")
st.title("💉 予防接種スケジュール（Google共有版・無料）")

# ===== Google認証 =====
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

gc = gspread.authorize(credentials)

# ===== スプレッドシートを開く =====
sheet_url = "https://docs.google.com/spreadsheets/d/1_5KXhHhLSLZv2FazFV7S1hTS6YY-JjDwEs0uzFpniqM/edit?gid=0"
spreadsheet = gc.open_by_url(sheet_url)
worksheet = spreadsheet.get_worksheet(0)

# ===== データ読み込み =====
data = worksheet.get_all_records()
df = pd.DataFrame(data)
st.dataframe(df)

# ===== 追加フォーム =====
st.subheader("🧑‍⚕️ 新しい患者データを追加")
name = st.text_input("患者名")
vaccine = st.text_input("ワクチン名")
date = st.date_input("最終接種日")
dose = st.number_input("接種回数", min_value=1, max_value=4, step=1)

if st.button("追加"):
    worksheet.append_row([name, vaccine, str(date), dose])
    st.success("✅ 登録しました！ ページを更新して反映を確認してください。")
