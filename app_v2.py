import streamlit as st
import pandas as pd

st.set_page_config(page_title="마케팅 타겟 최적화 대시보드", layout="wide")

st.markdown("""
<style>

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #EEF2FF;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 20px;
    color: #CBD5E1;
    margin-bottom: 35px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #F8FAFC;
    margin-top: 25px;
    margin-bottom: 15px;
}

.description {
    font-size: 16px;
    color: #D1D5DB;
    margin-bottom: 20px;
}

[data-testid="stMetricValue"] {
    color: #A5B4FC;
    font-size: 34px;
}

[data-testid="stMetricLabel"] {
    color: #E5E7EB;
    font-size: 16px;
}

button[data-baseweb="tab"] {
    background-color: #111827;
    border-radius: 10px;
    padding: 10px 18px;
    color: white;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #4F46E5;
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">마케팅 타겟 최적화 대시보드</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Uplift Modeling 기반 고객 추천 및 비용 시뮬레이션 시스템</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("모델 결과 CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("uplift_prediction_full_v4.csv")

# [수정2] 4분류 segment 자동 생성 — 점수 0은 Sure Thing으로 (기존: Sleeping Dog으로 잘못 분류됨)
if "segment" not in df.columns or df["segment"].iloc[0] in ["Mens E-Mail", "Womens E-Mail", "No E-Mail"]:
    def classify_segment(score):
        if score > 0.01:
            return "Persuadable"
        elif score >= 0:
            return "Sure Thing"
        elif score >= -0.01:
            return "Lost Cause"
        else:
            return "Sleeping Dog"

    # [수정1] 기존 실험그룹 segment가 있으면 experiment_group으로 보존
    if "segment" in df.columns:
        df.rename(columns={"segment": "experiment_group"}, inplace=True)

    df["segment"] = df["uplift_score"].apply(classify_segment)

# 필요한 컬럼 자동 생성
if "recommendation" not in df.columns:
    df["recommendation"] = df["uplift_score"].apply(
        lambda x: "Send" if x > 0 else "Do not send"
    )

# [수정4] top_factor 빈칸이면 임시값 채우지 않음 (SHAP 탭에서 별도 처리)
has_shap = (
    "top_factor_1" in df.columns
    and df["top_factor_1"].notna().any()
)

recommended_df = df[df["recommendation"] == "Send"]

st.markdown('<div class="section-title">핵심 요약</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric("전체 고객 수", f"{len(df):,}")
col2.metric("추천 고객 수", f"{len(recommended_df):,}")
col3.metric("추천 비율", f"{round(len(recommended_df) / len(df) * 100, 1)}%")
col4.metric("평균 Uplift", round(df["uplift_score"].mean(), 3))

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "고객 결과",
    "타겟팅 분석",
    "비용 시뮬레이션",
    "SHAP 설명"
])

with tab1:
    st.markdown('<div class="section-title">고객 결과 테이블</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="description">모델이 계산한 고객별 uplift 점수와 마케팅 추천 결과를 확인합니다.</div>',
        unsafe_allow_html=True
    )

    # [수정5] 테이블에 보여줄 컬럼 — SHAP 데이터 없으면 top_factor 제외
    show_columns = [
        "customer_id",
        "uplift_score",
        "segment",
        "recommendation",
    ]
    if has_shap:
        show_columns += ["top_factor_1", "top_factor_2", "top_factor_3"]

    available_columns = [col for col in show_columns if col in df.columns]
    st.dataframe(df[available_columns], use_container_width=True)

    st.markdown('<div class="section-title">추천 고객 리스트</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="description">마케팅 발송이 추천된 고객만 따로 보여줍니다.</div>',
        unsafe_allow_html=True
    )
    st.dataframe(recommended_df[available_columns], use_container_width=True)

with tab2:
    st.markdown('<div class="section-title">세그먼트 분포</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="description">고객이 Persuadable, Sure Thing, Sleeping Dog, Lost Cause 중 어떤 그룹에 속하는지 보여줍니다.</div>',
        unsafe_allow_html=True
    )

    # [수정6] 세그먼트 순서 고정 (발표자료와 일치)
    segment_order = ["Persuadable", "Sure Thing", "Lost Cause", "Sleeping Dog"]
    segment_counts = df["segment"].value_counts().reindex(segment_order, fill_value=0)
    st.bar_chart(segment_counts)

    st.markdown('<div class="section-title">Top 10% / 15% / 20% / 30% 타겟팅 비교</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="description">uplift 점수가 높은 고객부터 선택했을 때 평균 효과를 비교합니다.</div>',
        unsafe_allow_html=True
    )

    sorted_df = df.sort_values(by="uplift_score", ascending=False)

    top10 = sorted_df.head(max(1, int(len(df) * 0.10)))
    top15 = sorted_df.head(max(1, int(len(df) * 0.15)))
    top20 = sorted_df.head(max(1, int(len(df) * 0.20)))
    top30 = sorted_df.head(max(1, int(len(df) * 0.30)))

    comparison_df = pd.DataFrame({
        "타겟 그룹": ["Top 10%", "Top 15%", "Top 20%", "Top 30%"],
        "고객 수": [
            f"{len(top10):,}",
            f"{len(top15):,}",
            f"{len(top20):,}",
            f"{len(top30):,}"
        ],
        "평균 Uplift": [
            round(top10["uplift_score"].mean(), 3),
            round(top15["uplift_score"].mean(), 3),
            round(top20["uplift_score"].mean(), 3),
            round(top30["uplift_score"].mean(), 3)
        ]
    })

    st.dataframe(comparison_df, use_container_width=True)
    st.line_chart(comparison_df.set_index("타겟 그룹")["평균 Uplift"])

with tab3:
    st.markdown('<div class="section-title">비용 시뮬레이션</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="description">추천 고객에게만 마케팅을 보냈을 때의 예상 매출, 비용, 순이익을 계산합니다.</div>',
        unsafe_allow_html=True
    )

    col_a, col_b = st.columns(2)
    with col_a:
        email_cost = st.slider("이메일 발송 단가 ($)", 0.01, 0.20, 0.05, 0.01)
    with col_b:
        margin = st.slider("마진율 (%)", 5, 60, 30, 5) / 100

    if "treatment" in df.columns and "spend" in df.columns:
        control_avg_spend = df[df["treatment"] == 0]["spend"].mean()
    else:
        control_avg_spend = 0.6528

    sorted_df = df.sort_values("uplift_score", ascending=False)
    results = []
    chart_rows = []

    for pct in range(5, 101, 5):
        n = max(1, int(len(df) * pct / 100))
        target = sorted_df.head(n)

        if "spend" in target.columns and "treatment" in target.columns:
            treated_target = target[target["treatment"] == 1]
            actual_spend = treated_target["spend"].sum()
            n_treated = len(treated_target)
        else:
            actual_spend = 0
            n_treated = n

        counterfactual = n_treated * control_avg_spend
        revenue_lift = actual_spend - counterfactual
        profit_lift = revenue_lift * margin
        cost = n * email_cost
        net_profit = profit_lift - cost
        roi = net_profit / cost if cost > 0 else 0

        results.append({
            "발송 비율": f"{pct}%",
            "발송 수": f"{n:,}",
            "매출 증분": f"${revenue_lift:,.0f}",
            "이익 증분": f"${profit_lift:,.0f}",
            "발송 비용": f"${cost:,.0f}",
            "순이익": f"${net_profit:,.0f}",
            "ROI": f"{roi:.1f}x"
        })
        chart_rows.append({
            "발송 비율(%)": pct,
            "순이익($)": net_profit,
            "ROI(x)": roi,
        })

    sim_df = pd.DataFrame(results)
    chart_df = pd.DataFrame(chart_rows)

    best_idx = chart_df["순이익($)"].idxmax()
    best_pct = chart_df.loc[best_idx, "발송 비율(%)"]
    best_profit = chart_df.loc[best_idx, "순이익($)"]
    best_roi = chart_df.loc[best_idx, "ROI(x)"]
    full_roi = chart_df.loc[chart_df["발송 비율(%)"] == 100, "ROI(x)"].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("최적 발송 비율", f"{best_pct}%")
    col2.metric("최적 순이익", f"${best_profit:,.0f}")
    col3.metric("전체 발송 대비 ROI", f"{best_roi:.1f}x (전체 {full_roi:.1f}x)")

    st.markdown('<div class="section-title">발송 비율별 순이익 곡선</div>', unsafe_allow_html=True)
    st.line_chart(chart_df.set_index("발송 비율(%)")[["순이익($)"]])

    st.markdown('<div class="section-title">시나리오 비교</div>', unsafe_allow_html=True)
    st.dataframe(sim_df, use_container_width=True)

    st.caption(
        f"가정값: 발송 단가 ${email_cost}/건, 마진율 {margin*100:.0f}%, "
        f"Control 평균 spend ${control_avg_spend:.4f}"
    )

with tab4:
    st.markdown('<div class="section-title">SHAP 기반 Top-3 요인 설명</div>', unsafe_allow_html=True)

    # [수정7] SHAP 데이터 없으면 "최종발표 예정" 표시
    if not has_shap:
        st.info("⏳ SHAP 해석은 최종발표에서 추가 예정입니다. 현재는 uplift 점수와 세그먼트 기반 추천 결과를 확인할 수 있습니다.")
        st.markdown(
            '<div class="description">SHAP(SHapley Additive exPlanations)을 통해 각 고객의 uplift 점수에 가장 큰 영향을 준 변수 Top-3를 분석할 예정입니다.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="description">각 고객이 추천된 이유를 Top-3 요인으로 설명합니다.</div>',
            unsafe_allow_html=True
        )

        selected_customer = st.selectbox("고객 ID 선택", df["customer_id"])

        selected_row = df[df["customer_id"] == selected_customer].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Uplift 점수", selected_row["uplift_score"])
            st.metric("추천 여부", selected_row["recommendation"])

        with col2:
            st.write("Top 요인 1:", selected_row["top_factor_1"])
            st.write("Top 요인 2:", selected_row["top_factor_2"])
            st.write("Top 요인 3:", selected_row["top_factor_3"])

st.divider()

st.markdown('<div class="section-title">시스템 파이프라인</div>', unsafe_allow_html=True)

st.info("""
고객 CSV 입력 → 데이터 전처리 → Uplift 모델링 → 성능 평가 → 추천 결과 출력 → 비용 시뮬레이션
""")
