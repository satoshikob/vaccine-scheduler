import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(layout="wide")

st.title("💉 予防接種スケジュール表示アプリ")

# モード切り替え
mode = st.sidebar.radio("モードを選択", ["標準スケジュール", "個別スケジュール"])

# === 標準スケジュールモード ===
if mode == "標準スケジュール":
    years = st.number_input("年齢（歳）", min_value=0, max_value=100, step=1, value=0)
    months = st.number_input("月齢（追加の月）", min_value=0, max_value=11, step=1, value=0)
    age_in_months = years * 12 + months
    st.write(f"入力された年齢: {years}歳{months}か月（= {age_in_months}か月）")

    st.write("---")

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

    notes = {
        "HBV": ["接種間隔：①②は4週以上、①③は20週以上"],
        "ロタリックス": [
            "生後6週以降に開始",
            "1価（ロタリックス）：2回、各回4週以上空け、生後24週までに完了",
            "5価（ロタテック）：3回、各回4週以上空け、生後32週までに完了",
            "初回は遅くとも生後14週6日までに開始"
        ],
        "肺炎球菌": [
            "2〜6か月開始：初回3回（27日以上空ける）＋12〜15か月で追加1回（3→4は60日以上）",
            "7〜11か月開始：2回（27日以上空ける）＋1歳以降に追加1回",
            "12〜23か月開始：2回（最短60日空ける）",
            "2〜4歳開始：1回のみ"
        ],
        "五種混合": [
            "初回3回：20〜56日間隔（標準は27日以上）",
            "追加1回：初回終了後6か月以上空ける（標準は12〜18か月の間）"
        ],
        "BCG": ["標準：生後5〜8か月の間に1回"],
        "MR": [
            "第1期：1歳〜2歳未満に1回",
            "第2期：5〜7歳未満（就学前1年間）に1回",
            "麻疹流行地・曝露後には生後6か月以降で接種可（ただし規定回数には数えない）"
        ],
        "水痘": ["1-3歳：①②は3ヶ月以上空ける", "3歳以上：①②は4週以上空ける"],
        "おたふく": ["1歳で1回、5〜7歳未満で2回目", "①②は4週以上空ける"],
        "日本脳炎": [
            "第1期：3歳で①②（1〜4週間隔）、6か月以上空けて③",
            "第2期：9〜13歳で1回",
            "特例対象（1995/4/2-2007/4/1）は20歳未満まで定期接種可"
        ],
        "DT": ["11〜13歳で1回"],
        "HPV": [
            "通常はシルガード（9価）を使用",
            "定期対象：小6〜高1女子",
            "①～②は2ヶ月以上空ける（最低1ヶ月）",
            "①～③は6ヶ月以上空ける（最低3ヶ月）",
            "キャッチアップ：1997/4/2〜2008/4/1生まれの女性は2026年3月末まで定期接種可"
        ]
    }

    closest_age = max([m for m in schedule.keys() if m <= age_in_months], default=None)

    col1, col2 = st.columns([2,3])

    with col1:
        st.subheader("📅 標準スケジュール")
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
        st.subheader("💡 ワクチン注釈リスト")
        if closest_age is not None:
            vaccines = schedule[closest_age]
            for v in vaccines:
                for key, val in notes.items():
                    if key in v:
                        st.markdown(f"**{key}**:")
                        for line in val:
                            st.write(f"- {line}")

# === 個別スケジュールモード ===
else:
    st.subheader("👤 個別スケジュール計算")

    st.write("患者ごとに、各ワクチンの最終接種日と回数を入力してください。次回の推奨日を自動計算します。")

    vaccine_rules = {
        "HBV": {1: 28, 2: 140},  # 日数
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

    data = []

    for v in vaccine_list:
        st.markdown(f"### 💉 {v}")
        last_date = st.date_input(f"最終接種日 ({v})", date.today())
        count = st.number_input(f"これまでの接種回数 ({v})", min_value=0, max_value=3, value=0, step=1)

        if count in vaccine_rules[v]:
            interval = vaccine_rules[v][count]
            next_date = last_date + timedelta(days=interval)
            data.append([v, last_date, count, next_date])
        else:
            data.append([v, last_date, count, "完了 or 該当なし"])

    df = pd.DataFrame(data, columns=["ワクチン名", "最終接種日", "接種回数", "次回推奨日"])
    st.table(df)

st.write("---")
st.caption("vaccine for allのサイトを元に作成。個別スケジュールは参考値であり、実際の接種間隔は医師の判断を優先してください。")
