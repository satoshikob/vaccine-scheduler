import streamlit as st
import pandas as pd
import gspread

st.set_page_config(layout="wide")
st.title("💉 予防接種スケジュール（Google共有版・無料）")

# GoogleスプレッドシートURL（あなたの共有リンク）
sheet_url = "https://docs.google.com/spreadsheets/d/1_5KXhHhLSLZv2FazFV7S1hTS6YY-JjDwEs0uzFpniqM/edit?gid=0"
gc = gspread.oauth()

# シートを開く（ワークシート名を確認して必要なら変更）
sh = gc.open_by_url(sheet_url)
worksheet = sh.get_worksheet(0)

# 既存データを取得
data = worksheet.get_all_records()
df = pd.DataFrame(data)
st.subheader("📋 登録済みデータ")
if not df.empty:
    st.dataframe(df)
else:
    st.info("まだデータがありません。")

# 新規登録フォーム
st.subheader("🧑‍⚕️ 新しい患者データを追加")
name = st.text_input("患者名")
vaccine = st.text_input("ワクチン名")
date = st.date_input("最終接種日")
dose = st.number_input("接種回数", min_value=1, max_value=4, step=1)

if st.button("追加"):
    worksheet.append_row([name, vaccine, str(date), dose])
    st.success("✅ 登録しました！ ページを更新して反映を確認してください。")
