import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="마케팅 타겟 최적화 대시보드",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #F8FAFC;
    margin-bottom: 10px;
}
.subtitle {
    font-size: 17px;
    color: #CBD5E1;
    margin-bottom: 30px;
}
.section-title {
    font-size: 30px;
    font-weight: 750;
    color: #F8FAFC;
    margin-top: 30px;
    margin-bottom: 15px;
}
.description {
    font-size: 17px;
    color: #E5E7EB;
    margin-bottom: 20px;
}
[data-testid="stMetricValue"] {
    color: #A5B4FC;
    font-size: 34px;
}
[data-testid="stMetricLabel"] {
    color: #E5E7EB;
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

# -----------------------------
# Title
# -----------------------------
st.markdown(
    '<div class="main-title">마케팅 타겟 최적화 대시보드</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Uplift Modeling 기반 고객 추천 및 비용 시뮬레이션 시스템</div>',
    unsafe_allow_html=True
)

# -----------------------------
# CSV Upload
# -----------------------------
uploaded_file = st.file_uploader("모델 결과 CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("모델 결과 CSV 파일을 업로드해주세요.")
    st.stop()

# -----------------------------
# Required columns check
# -----------------------------
required_cols = [
    "customer_id",
    "uplift_score",
    "segment",
    "recommendation"
]

missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"CSV 파일에 필요한 컬럼이 없습니다: {missing_cols}")
    st.stop()

# -----------------------------
# Data
# -----------------------------
recommended_df = df[df["recommendation"] == "Send"]

# -----------------------------
# KPI Summary
# -----------------------------
st.markdown(
    '<div class="section-title">핵심 요약</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("전체 고객 수", f"{len(df):,}")
col2.metric("추천 고객 수", f"{len(recommended_df):,}")
col3.metric("추천 비율", f"{round(len(recommended_df) / len(df) * 100, 1)}%")
col4.metric("평균 Uplift", round(df["uplift_score"].mean(), 3))

st.divider()

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "고객 결과",
    "타겟팅 분석",
    "비용 시뮬레이션",
    "SHAP 설명"
])

# -----------------------------
# Tab 1: Customer Results
# -----------------------------
with tab1:
    st.markdown(
        '<div class="section-title">고객 결과 테이블</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">모델이 계산한 고객별 uplift 점수와 마케팅 추천 결과를 확인합니다.</div>',
        unsafe_allow_html=True
    )

    show_cols = [
        "customer_id",
        "uplift_score",
        "segment",
        "recommendation"
    ]

    st.dataframe(df[show_cols], use_container_width=True)

    st.markdown(
        '<div class="section-title">추천 고객 리스트</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">마케팅 발송이 추천된 고객만 따로 보여줍니다.</div>',
        unsafe_allow_html=True
    )

    st.dataframe(recommended_df[show_cols], use_container_width=True)

# -----------------------------
# Tab 2: Targeting Analysis
# -----------------------------
with tab2:
    st.markdown(
        '<div class="section-title">세그먼트 분포</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">고객이 Persuadable, Sure Thing, Sleeping Dog, Lost Cause 중 어떤 그룹에 속하는지 보여줍니다.</div>',
        unsafe_allow_html=True
    )

    segment_counts = df["segment"].value_counts()
    st.bar_chart(segment_counts)

    st.markdown(
        '<div class="section-title">Top 10% / 15% / 20% / 30% 타겟팅 비교</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">uplift 점수가 높은 고객부터 선택했을 때 평균 효과를 비교합니다.</div>',
        unsafe_allow_html=True
    )

    sorted_df = df.sort_values(by="uplift_score", ascending=False)

    top_rates = [0.10, 0.15, 0.20, 0.30]
    comparison_rows = []

    for rate in top_rates:
        top_df = sorted_df.head(max(1, int(len(df) * rate)))

        comparison_rows.append({
            "타겟 그룹": f"Top {int(rate * 100)}%",
            "고객 수": len(top_df),
            "평균 Uplift": round(top_df["uplift_score"].mean(), 3)
        })

    comparison_df = pd.DataFrame(comparison_rows)

    st.dataframe(comparison_df, use_container_width=True)
    st.line_chart(comparison_df.set_index("타겟 그룹")["평균 Uplift"])

# -----------------------------
# Tab 3: Cost Simulation
# -----------------------------
with tab3:
    st.markdown(
        '<div class="section-title">비용 시뮬레이션</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">추천 고객에게만 마케팅을 보냈을 때의 예상 매출, 비용, 순이익을 계산합니다.</div>',
        unsafe_allow_html=True
    )

    col_a, col_b = st.columns(2)

    with col_a:
        email_cost = st.number_input(
            "고객 1명당 이메일 발송 비용",
            value=10,
            min_value=0
        )

    with col_b:
        conversion_profit = st.number_input(
            "고객 1명 전환 시 기대 수익",
            value=5000,
            min_value=0
        )

    recommended_count = len(recommended_df)

    estimated_revenue = recommended_count * conversion_profit
    estimated_cost = recommended_count * email_cost
    estimated_profit = estimated_revenue - estimated_cost

    col1, col2, col3 = st.columns(3)

    col1.metric("예상 매출", f"{estimated_revenue:,}원")
    col2.metric("예상 비용", f"{estimated_cost:,}원")
    col3.metric("예상 순이익", f"{estimated_profit:,}원")

    st.divider()

    st.markdown(
        '<div class="section-title">시스템 파이프라인</div>',
        unsafe_allow_html=True
    )

    st.info(
        "고객 CSV 입력 → 데이터 전처리 → Uplift 모델링 → 성능 평가 → 추천 결과 출력 → 비용 시뮬레이션"
    )

# -----------------------------
# Tab 4: SHAP Explanation
# -----------------------------
with tab4:
    st.markdown(
        '<div class="section-title">SHAP 기반 Top-3 요인 설명</div>',
        unsafe_allow_html=True
    )

    shap_cols = [
        "top_factor_1",
        "top_factor_2",
        "top_factor_3"
    ]

    if all(col in df.columns for col in shap_cols):
        st.markdown(
            '<div class="description">각 고객의 uplift 점수에 영향을 준 주요 요인 Top-3를 확인합니다.</div>',
            unsafe_allow_html=True
        )

        factor_map = {
            "history": "구매 이력",
            "recency": "최근 구매 시점",
            "mens": "남성 상품 관심도",
            "womens": "여성 상품 관심도",
            "channel": "마케팅 채널",
            "newbie": "신규 고객 여부",
            "zip_code": "지역 정보",
            "history_segment": "고객 구매 패턴",
            "history_segment_enc": "고객 구매 패턴",
            "treatment": "이메일 수신 여부",
            "spend": "구매 금액"
        }

        selected_customer = st.selectbox(
            "고객 ID 선택",
            df["customer_id"]
        )

        selected_row = df[df["customer_id"] == selected_customer].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Uplift 점수", round(selected_row["uplift_score"], 3))
            st.metric("추천 여부", selected_row["recommendation"])

        with col2:
            f1 = selected_row["top_factor_1"]
            f2 = selected_row["top_factor_2"]
            f3 = selected_row["top_factor_3"]

            st.write("Top 요인 1:", factor_map.get(f1, f1))
            st.write("Top 요인 2:", factor_map.get(f2, f2))
            st.write("Top 요인 3:", factor_map.get(f3, f3))

    else:
        st.info(
            "⏳ SHAP 해석은 최종발표에서 추가 예정입니다. "
            "현재는 uplift 점수와 세그먼트 기반 추천 결과를 확인할 수 있습니다."
        )

        st.write(
            "SHAP(Shapley Additive exPlanations)을 통해 "
            "각 고객의 uplift 점수에 가장 큰 영향을 준 변수 Top-3를 분석할 예정입니다."
        )