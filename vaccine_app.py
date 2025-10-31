import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(layout="wide")

st.title("💉 予防接種スケジュール表示アプリ")

mode = st.sidebar.radio("モードを選択", ["標準スケジュール", "個別スケジュール"])

# === 標準スケジュール ===
if mode == "標準スケジュール":
    years = st.number_input("年齢（歳）", min_value=0, max_value=100, step=1, value=0)
    months = st.number_input("月齢（追加の月）", min_value=0, max_value=11, step=1, value=0)
    age_in_months = years * 12 + months
    st.write(f"入力された年齢: {years}歳{months}か月（= {age_in_months}か月）")

    schedule = {
        2: ["HBV①", "ロタリックス①", "肺炎球菌①", "五種混合①"],
        3: ["HBV②", "ロタリックス②", "肺炎球菌②", "五種混合②"],
        4: ["肺炎球菌③", "五種混合③"],
        6: ["BCG"],
        7: ["HBV③"],
        12: ["肺炎球菌④", "五種混合④", "MR①", "水痘①", "おたふく①"],
        15: ["水痘②"],
        36: ["日本脳炎１期①②（１週間空けて２回）"],
        42: ["日本脳炎１期③"],
        60: ["MR②", "おたふく②"],
        108: ["日本脳炎２期"],
        132: ["DT"],
        144: ["HPV"]
    }

    closest_age = max([m for m in schedule.keys() if m <= age_in_months], default=None)

    if closest_age:
        st.subheader("📅 標準スケジュール")
        vaccines = schedule[closest_age]
        years_show = closest_age // 12
        months_show = closest_age % 12
        st.markdown(f"**{years_show}歳{months_show}か月（{closest_age}か月）時点の推奨接種:**")
        for v in vaccines:
            st.write(f"- {v}")
    else:
        st.info("この年齢に近いスケジュールはまだ登録されていません。")

# === 個別スケジュール ===
else:
    st.subheader("👤 個別スケジュール管理")

    if "patients" not in st.session_state:
        st.session_state["patients"] = {}

    # --- 患者の追加 ---
    new_patient = st.text_input("新しい患者名を入力")
    if st.button("患者を追加"):
        if new_patient and new_patient not in st.session_state["patients"]:
            st.session_state["patients"][new_patient] = []
            st.success(f"{new_patient} さんを追加しました。")
        else:
            st.warning("すでに登録済みか、名前が空欄です。")

    # --- 患者の選択 ---
    if st.session_state["patients"]:
        selected_patient = st.selectbox("患者を選択", list(st.session_state["patients"].keys()))

        # --- 患者削除 ---
        if st.button("選択中の患者を削除"):
            del st.session_state["patients"][selected_patient]
            st.success("削除しました。ページを再読み込みしてください。")

        vaccine_rules = {
            "HBV": {1: 28, 2: 140},
            "五種混合": {3: 180},
            "肺炎球菌": {3: 60},
            "ロタリックス": {1: 28},
            "MR": {1: 180},
            "水痘": {1: 84},
            "おたふく": {1: 28},
            "日本脳炎": {2: 180, 3: 180},
            "DT": {},
            "HPV": {1: 60, 2: 180}
        }

        vaccine_list = list(vaccine_rules.keys())

        st.markdown(f"### 💉 {selected_patient} さんの接種情報")

        for v in vaccine_list:
            last_date = st.date_input(f"最終接種日 ({v})", date.today(), key=f"{selected_patient}_{v}_date")
            count = st.number_input(f"接種回数 ({v})", min_value=0, max_value=3, value=0, step=1, key=f"{selected_patient}_{v}_count")

            if count in vaccine_rules[v]:
                interval = vaccine_rules[v][count]
                next_date = last_date + timedelta(days=interval)
                result = next_date
            else:
                result = "完了 or 該当なし"

            st.write(f"➡️ 次回推奨日: {result}")

            # 保存ボタン
            if st.button(f"{v} の記録を保存", key=f"{selected_patient}_{v}_save"):
                record = {"ワクチン": v, "最終接種日": str(last_date), "接種回数": count, "次回推奨日": str(result)}
                st.session_state["patients"][selected_patient].append(record)
                st.success(f"{v} の記録を保存しました。")

        # --- 現在のデータを一覧表示 ---
        st.markdown("---")
        st.markdown("#### 📋 現在の記録一覧")
        data = st.session_state["patients"][selected_patient]
        if data:
            df = pd.DataFrame(data)
            st.table(df)
        else:
            st.info("まだ記録がありません。")

st.caption("※ データはセッション中に保持されます。ページを閉じると消えます。将来的にCookieまたはクラウド保存に対応予定。")
