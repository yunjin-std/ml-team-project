# VALIDATION_LOG.md
## 팀원: 서윤진 | 프로젝트: Uplift Modeling 기반 마케팅 타겟 최적화

---

## 검증 사례 1 — SHAP values shape 처리 방식

**AI가 제안한 내용**

RandomForest 분류 모델의 SHAP 값을 `shap_values_t1[1]` 로 인덱싱하면
`(n_samples, n_features)` shape의 배열을 얻을 수 있다고 제안함

**실제 실행 결과**

`shap_values_t1[1]` 결과가 `(8523, 12)`가 아닌 `(12, 2)` shape으로 반환됨
→ summary_plot에서 AssertionError 발생

**수정한 내용**

```python
# 수정 전 (AI 초안)
shap_vals = shap_values_t1[1]

# 수정 후 (직접 검증 후 수정)
shap_arr = np.array(shap_values_t1)
if shap_arr.ndim == 3:
    shap_vals = shap_arr[:, :, 1]  # 3차원일 경우 마지막 축으로 클래스 선택
elif shap_arr.ndim == 2:
    shap_vals = shap_arr
else:
    shap_vals = shap_arr[1]
```

**왜 수정했는가**

sklearn의 RandomForestClassifier + shap.TreeExplainer 조합에서 shap_values의
출력 구조가 버전에 따라 `(n_samples, n_features, n_classes)` 3차원으로 반환되는
경우가 있음을 실행 결과로 확인
→ ndim 조건 분기로 버전 무관하게 처리되도록 수정

---

## 검증 사례 2 — uplift_score 기준 모델 오류 발견

**AI가 제안한 내용**

최종 결과표(result_df) 생성 시 uplift_score 컬럼에 X-Learner 기준 점수를
저장하는 코드를 초안으로 제안함

**실제 확인 결과**

```python
# 오류 코드 (AI 초안)
result_df['uplift_score'] = uplift_x.round(3)  # X-Learner 기준
```

최종 채택 모델은 T-Learner임에도 X-Learner 점수가 저장되어
비용 시뮬레이션, 세그먼트 분류, top_factor 전체가 잘못된 모델 기준으로 계산됨

**수정한 내용**

```python
# 수정 후
result_df['uplift_score'] = uplift_t.round(3)  # T-Learner 기준 (최종 채택 모델)
```

**왜 수정했는가**

프로젝트 전체에서 X-Learner는 과적합 의심으로 참고용으로만 사용하고
T-Learner를 최종 채택 모델로 결정했기 때문에
결과 CSV 및 비용 시뮬레이션 모두 T-Learner 기준으로 일관성 유지 필요

---

## 검증 사례 3 — Lenta AUUC 비교 해석 오류 수정

**AI가 제안한 내용**

Hillstrom AUUC(17.24) vs Lenta AUUC(235.22) 를 단순 수치로 비교 출력하는
비교표를 초안으로 제안함

**실제 검토 결과**

두 AUUC를 그대로 나열하면 "Lenta 모델 성능이 14배 좋다"는 오해를 줄 수 있음
→ AUUC는 데이터 규모(샘플 수)에 비례해 커지는 지표이므로
Lenta(687,029명)가 Hillstrom(64,000명)보다 약 10배 크면
AUUC도 자연히 약 10배 커지는 구조

**수정한 내용**

단순 비교표에 아래 해석 및 정규화 비교 추가:

```python
# 정규화 AUUC 추가
norm_h = auuc_hillstrom / n_hillstrom * 1000  # 2.0234
norm_l = auuc_lenta     / n_lenta     * 1000  # 1.7119
# → 정규화 후 두 값 비슷한 스케일 → "둘 다 작동한다"는 방향성 확인
```

**왜 수정했는가**

절대값 비교가 아닌 "두 도메인 모두 AUUC > 0 (Random 대비 양수)" 라는
방향성 비교가 크로스도메인 검증의 핵심 메시지이기 때문
발표에서 오해 없이 정확한 결론 전달을 위해 수정

