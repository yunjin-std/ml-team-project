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
    df = pd.read_csv("uplift_result.csv")

# 필요한 컬럼 자동 생성
if "recommendation" not in df.columns:
    df["recommendation"] = df["uplift_score"].apply(
        lambda x: "Send" if x > 0 else "Do not send"
    )

if "segment" not in df.columns:
    def classify_segment(score):
        if score > 0.05:
            return "Persuadable"
        elif score > 0:
            return "Sure Thing"
        elif score > -0.05:
            return "Sleeping Dog"
        else:
            return "Lost Cause"

    df["segment"] = df["uplift_score"].apply(classify_segment)

if "top_factor_1" not in df.columns:
    df["top_factor_1"] = "history"

if "top_factor_2" not in df.columns:
    df["top_factor_2"] = "mens"

if "top_factor_3" not in df.columns:
    df["top_factor_3"] = "recency"

recommended_df = df[df["recommendation"] == "Send"]

st.markdown('<div class="section-title">핵심 요약</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric("전체 고객 수", len(df))
col2.metric("추천 고객 수", len(recommended_df))
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

    show_columns = [
        "customer_id",
        "uplift_score",
        "segment",
        "recommendation",
        "top_factor_1",
        "top_factor_2",
        "top_factor_3"
    ]

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

    segment_counts = df["segment"].value_counts()
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
            len(top10),
            len(top15),
            len(top20),
            len(top30)
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
        email_cost = st.number_input("고객 1명당 이메일 발송 비용", value=10)

    with col_b:
        conversion_profit = st.number_input("고객 1명 전환 시 기대 수익", value=5000)

    recommended_count = len(recommended_df)

    estimated_revenue = recommended_count * conversion_profit
    estimated_cost = recommended_count * email_cost
    estimated_profit = estimated_revenue - estimated_cost

    col1, col2, col3 = st.columns(3)

    col1.metric("예상 매출", f"{estimated_revenue:,}원")
    col2.metric("예상 비용", f"{estimated_cost:,}원")
    col3.metric("예상 순이익", f"{estimated_profit:,}원")

with tab4:
    st.markdown('<div class="section-title">SHAP 기반 Top-3 요인 설명</div>', unsafe_allow_html=True)
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