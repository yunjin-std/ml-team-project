# AI_USAGE_LOG.md
## 팀원: 서윤진 | 프로젝트: Uplift Modeling 기반 마케팅 타겟 최적화

| 날짜 | 사용 도구 | 목적 | 입력한 요청 | 받은 결과 | 실제 반영 여부 | 팀원 |
|------|----------|------|------------|----------|--------------|------|
| 6월 5일 | Claude | 코드 작성 | 상위 15% 비용 시뮬레이션 코드 작성 요청 | simulate_top_k() 함수 및 전체 발송 vs 상위 15% 순이익·ROI 비교 코드 생성 | 반영 | 서윤진 |
| 6월 5일 | Claude | 코드 작성 | T-Learner에 SHAP 적용, summary plot 생성, top_factor_1~3 컬럼 채우기 코드 요청 | TreeExplainer 기반 SHAP 계산 코드, summary plot 코드, 개인별 top3 feature 추출 코드 생성 | 반영 | 서윤진 |
| 6월 5일 | Claude | 오류 수정 | SHAP summary_plot ax 인자 오류 수정 요청 | ax 인자 제거, plot_size로 크기 지정하는 방식으로 수정 | 반영 | 서윤진 |
| 6월 5일 | Claude | 오류 수정 | SHAP values shape 불일치 오류(AssertionError) 수정 요청 | shap_values 3차원(n_samples, n_features, n_classes) 처리 로직 제안 → `shap_arr[:, :, 1]` 로 수정 | 반영 | 서윤진 |
| 6월 5일 | Claude | 인사이트 도출 | "어떤 특성의 고객이 마케팅에 잘 반응하는가" 인사이트 코드 요청 | SHAP 기반 마케팅 반응 고객 프로필 출력 코드 생성 (history, recency, mens/womens, newbie 순) | 반영 | 서윤진 |
| 6월 5일 | Claude | 코드 작성 | Lenta 크로스도메인 검증 코드 요청 (T-Learner 동일 파이프라인 적용) | Lenta 전처리, feature 선택, T-Learner 학습, AUUC 계산 및 Hillstrom 비교표 코드 생성 | 반영 | 서윤진 |
| 6월 5일 | Claude | 코드 작성 | Womens 캠페인 T-Learner 모델링 코드 요청 | Mens와 동일 구조로 Womens T-Learner 학습, AUUC 계산, 세그먼트 분류, CSV 저장 코드 생성 | 반영 | 서윤진 |
| 6월 5일 | Claude | 오류 수정 | Womens 비교표 KeyError('segment_type') 수정 요청 | df_womens → result_womens 참조 오류 수정, 컬럼명 자동 판별 로직 추가 | 반영 | 서윤진 |
| 6월 5일 | Claude | 분석 정리 | X-Learner 과적합 원인 분석 요청 | 원인 3가지(모델 복잡도, tau 추정 불안정, propensity 단순화) 및 교훈 정리 코드 생성 | 반영 | 서윤진 |
| 6월 5일 | Claude | 분석 정리 | 상위 15%가 최적인 이유 분석 요청 | 고객 구성 변화, 세그먼트 분포, 비용 시뮬레이션 기반 원인 분석 코드 생성 | 반영 | 서윤진 |
| 6월 5일 | Claude | 분석 정리 | Lenta AUUC가 Hillstrom보다 압도적으로 높은 이유 분석 요청 | AUUC 규모 비례 특성, 도메인 반응률 차이, 정규화 비교 방법 분석 코드 생성 | 반영 | 서윤진 |
| 6월 6일 | Claude | 오류 수정 | NumPy 버전 충돌(ImportError) 수정 요청 | numpy==1.26.4 다운그레이드 및 matplotlib 재설치 방법 제안 | 반영 | 서윤진 |
| 6월 6일 | Claude | 코드 검증 | uplift_score가 X-Learner 기준으로 저장된 오류 발견 요청 | result_df의 uplift_x → uplift_t 수정 제안 | 반영 | 서윤진 |
