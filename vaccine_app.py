import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💉 予防接種スケジュール表示アプリ")

# 年齢入力（歳と月齢を分ける）
years = st.number_input("年齢（歳）", min_value=0, max_value=100, step=1, value=0)
months = st.number_input("月齢（追加の月）", min_value=0, max_value=11, step=1, value=0)

# 総月齢を計算
age_in_months = years * 12 + months
st.write(f"入力された年齢: {years}歳{months}か月（= {age_in_months}か月）")

st.write("---")

# スケジュール定義
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

# 注釈データ（医療者向け詳細版、箇条書き形式）
notes = {
    "HBV": "- B型肝炎\n- ①②は4週以上\n- ①③は20週以上",
    "ロタリックス": "- ロタウイルス（1価）\n- 生後6週以降に開始\n- 2回、各回4週以上空け、生後24週までに完了\n- 初回は遅くとも生後14週6日までに開始",
    "ロタテック": "- ロタウイルス（5価）\n- 3回、各回4週以上空け、生後32週までに完了\n- 初回は遅くとも生後14週6日までに開始",
    "肺炎球菌": "- 肺炎球菌（PCV15・20）\n- 2〜6か月開始＝初回3回（27日以上空け）＋12〜15か月で追加1回（3→4は60日以上）\n- 7〜11か月開始＝2回（27日以上空け）＋1歳以降に追加1回\n- 12〜23か月開始＝2回（最短60日空け）\n- 2〜4歳開始＝1回のみ",
    "五種混合": "- 五種混合（DPT-IPV-Hib）\n- 初回3回（20〜56日間隔、標準は27日以上）\n- 追加1回（初回終了後6か月以上、標準は12〜18か月）",
    "BCG": "- BCG\n- 生後5〜8か月の間に1回",
    "MR": "- MR（麻しん・風しん）\n- 第1期＝1歳〜2歳未満に1回\n- 第2期＝5〜7歳未満（就学前1年間）に1回\n- 麻疹流行地・曝露後は生後6か月以降で接種可（規定回数には含めない）",
    "水痘": "- 水痘\n- 1〜3歳＝①②は3か月以上空ける\n- 3歳以上＝①②は4週以上空ける",
    "おたふく": "- おたふくかぜ\n- 1歳で1回、5〜7歳未満で2回目\n- ①②は4週以上空ける",
    "日本脳炎": "- 日本脳炎\n- 第1期＝3歳で①②（1〜4週間隔）、6か月以上空けて③\n- 第2期＝9〜13歳で1回\n- 特例対象（1995/4/2〜2007/4/1生まれ）は20歳未満まで定期接種可",
    "DT": "- DT（二種混合）\n- 11〜13歳で1回",
    "HPV": "- HPV（ヒトパピローマウイルス）\n- 現在はシルガード9（9価）が主流\n- 定期対象＝小6〜高1女子\n- ①〜②は2か月以上（最低1か月）\n- ①〜③は6か月以上（最低3か月）\n- キャッチアップ＝1997/4/2〜2008/4/1生まれの女性は2026年3月末まで定期接種可"
}

# 近い月齢を探す
closest_age = max([m for m in schedule.keys() if m <= age_in_months], default=None)

col1, col2 = st.columns([2,3])

with col1:
    st.subheader("📅 標準的なスケジュール")
    if closest_age is not None:
        vaccines = schedule[closest_age]
        years_show = closest_age // 12
        months_show = closest_age % 12
        st.markdown(f"**{years_show}歳{months_show}か月（{closest_age}か月）時点の推奨接種**:")
        for v in vaccines:
            st.write(f"- {v}")
    else:
        st.info("この年齢に近いスケジュールはまだ登録されていません。")

with col2:
    st.subheader("💡 ワクチン注釈リスト（医療者向け詳細版）")
    if closest_age is not None:
        vaccines = schedule[closest_age]
        for v in vaccines:
            for key, val in notes.items():
                if key in v:
                    st.markdown(f"**{key}**:\n{val}")

# グラフ形式のタイムライン
st.write("---")
st.subheader("📊 接種タイムライン（グラフ表示）")

ages = []
vaccine_labels = []

for age, vaccines in schedule.items():
    for v in vaccines:
        ages.append(age)
        vaccine_labels.append(v)

plt.figure(figsize=(10,6))
plt.scatter(ages, vaccine_labels, marker="o")
plt.xlabel("月齢")
plt.ylabel("ワクチン")
plt.title("予防接種タイムライン")
plt.grid(True, linestyle="--", alpha=0.6)
st.pyplot(plt)

st.write("---")
st.caption("※厚生労働省推奨の標準的スケジュールをもとに作成（医療者向け詳細版）。実際の接種は最新のガイドラインに従い、必ず医師の判断を仰いでください。")