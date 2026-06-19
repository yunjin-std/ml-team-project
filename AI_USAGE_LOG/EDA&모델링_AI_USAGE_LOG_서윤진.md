# AI Usage Log — 서윤진

| 날짜 | 사용 도구 | 목적 | 입력한 요청 | 받은 결과 | 실제 반영 여부 | 팀원 이름 |
|------|----------|------|------------|----------|--------------|----------|
| 5/16 | Claude | EDA 코드 작성 | 데이터 변수 확인, 결측치 확인, treatment/control 비율 확인, 방문율/전환율/구매액 분포 확인, 주요 feature와 outcome 관계 확인 코드 요청 | 항목별 주피터 노트북 셀 코드 생성 | 반영 (일부 오타 수정 후 사용) | 서윤진 |
| 5/16 | Claude | EDA 결과 해석 | 주피터에서 돌린 EDA 결과 사진 공유 후 해석 요청 | 데이터 변수 타입, 결측치 현황, 그룹 균형 검증, Outcome 비교, Feature-Outcome 관계 해석 제공 | 반영 | 서윤진 |
| 5/17 | Claude | 학습 Feature 정리 | EDA 결과 바탕으로 모델에 넣을 변수 정리 요청 | Feature 12개 확정, 인코딩 방법(Ordinal/One-Hot), Target 변수 확정, 제외 변수 및 이유 정리 | 반영 | 서윤진 |
| 5/17 | Claude | 모델링 코드 작성 | Baseline, Response Model(LR/RF), Uplift Model(S/T/X-Learner) 코드 요청 | 전체 모델링 코드 및 평가 지표(AUC, Uplift@K, AUUC, Qini Curve) 코드 생성 | 반영 (RF 클래스 불균형 문제 수정 후 사용) | 서윤진 |
| 5/17 | Claude | 모델링 결과 해석 | 각 모델 결과 사진 공유 후 해석 요청 | Baseline/Response Model/Uplift Model 결과 해석, T-Learner 채택 근거, 최적 발송 구간 분석 제공 | 반영 | 서윤진 |
| 5/18 | Claude | CSV 파일 생성 | T-Learner로 전체 64,000명 예측 결과 CSV 생성 코드 요청 | Mens/Womens T-Learner 결합 예측 코드 및 recommendation 컬럼 추가 코드 생성 | 반영 | 서윤진 |
| 5/18 | Claude | 노션 정리 | EDA & 모델링 결과를 팀원 공유용 노션 문서로 정리 요청 | 중간 발표 전 목표 달성 현황 전체 정리 제공 | 반영 | 서윤진 |
| 5/18 | Claude | 발표 그래프 생성 | PPT용 EDA & 모델링 그래프 이미지 파일 요청 | Outcome 비교, 매칭 효과, Feature Importance, Uplift@K, Qini Curve 그래프 5개 생성 | 일부 반영 (실제 데이터로 재생성) | 서윤진 |
