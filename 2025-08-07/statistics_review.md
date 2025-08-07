# 📊 통계 핵심 개념 요약

---

## 📌 중심극한정리 (Central Limit Theorem)

- 모집단의 분포와 관계없이, **표본 크기가 충분히 크면**  
  표본평균의 분포는 **정규분포에 가까워진다**.
- 중심은 **모평균(μ)**, 모양은 **정규분포**
- 통계량의 분포 개념의 출발점이 되는 핵심 이론

---

## 📌 카이제곱 분포 (Chi-Squared Distribution)

- **제곱된 정규분포 통계량의 분포**
- **분산에 관련된 검정**이나 추정에 사용됨
- 사용 사례:
  1. 모분산 추정 및 검정
  2. 적합도 검정
  3. 독립성 검정
- 특징:
  - 분포는 **자유도(df)**에 따라 모양이 결정됨
  - **오른쪽으로 비대칭** (right-skewed)
  - 값은 **0 이상만 존재** (음수 없음)
  - 자유도가 커질수록 **정규분포에 근접**

---

## 📌 t 분포 (Student’s t-distribution)

- 모분산을 모를 때, 소표본(n < 30)에서 사용하는 분포
- 정규분포와 비슷하지만 **꼬리가 더 두껍다**
- 사용 사례:
  1. 모평균에 대한 추론 (소표본)
  2. 두 집단 평균 비교 (t-test)
  3. 회귀 계수의 유의성 검정

---

## 📌 F 분포 (F-distribution)

- 두 개의 **분산을 비교**하기 위한 분포
- 사용 사례:
  1. **분산분석(ANOVA)** – 3개 이상의 집단 비교
  2. 회귀 모델의 **전체 유의성 검정**
- 특징:
  - 항상 **0 이상**
  - 자유도가 두 개 있음: \(df_1, df_2\)

---

## ⚠️ 오류의 종류

| 종류 | 정의 | 위험성 |
|------|------|--------|
| **1종 오류 (Type I Error)** | 귀무가설이 참인데 기각함 | **거짓을 믿는 위험** |
| **2종 오류 (Type II Error)** | 귀무가설이 거짓인데 기각하지 않음 | **진실을 놓치는 위험** |

---

## 📈 선형회귀의 기본 가정 5가지

1. **선형성 (Linearity)**  
   - 독립변수 X와 종속변수 Y는 선형 관계를 가져야 함

2. **오차의 정규성 (Normality of Residuals)**  
   - 잔차는 정규분포를 따라야 함

3. **오차의 독립성 (Independence)**  
   - 오차끼리 독립이어야 함 (자기상관 X)

4. **다중공선성 없음 (No Multicollinearity)**  
   - 독립변수들 간의 상관관계가 너무 높으면 안 됨  
   - 확인 방법: `VIF (variance_inflation_factor)`

5. **등분산성 (Homoscedasticity)**  
   - 오차의 분산이 일정해야 함  
   - 즉, 예측값에 따라 잔차의 분산이 커지거나 작아지면 안 됨

---

## 🧮 잔차 vs 오차

| 구분 | 정의 |
|------|------|
| **오차 (Error)** | 모집단 회귀식 기준으로 예측값과 실제값의 차이 |
| **잔차 (Residual)** | 표본 회귀식 기준으로 예측값과 실제값의 차이 |

---

## 📏 모델 성능 지표

- **MSE (Mean Squared Error)**: 잔차 제곱의 평균
- **RMSE (Root Mean Squared Error)**: MSE의 제곱근 (해석 쉬움)
  - **아웃라이어 영향에 민감함**

---

## 📌 분산 팽창 요인 (VIF: Variance Inflation Factor)

- 다중공선성을 확인하는 지표
- 일반적으로:
  - **VIF > 10**: 심각한 다중공선성
  - **VIF > 5**: 다중공선성 가능성 있음
- 계산 방법:
  ```python
  from statsmodels.stats.outliers_influence import variance_inflation_factor

  vif = pd.DataFrame()
  vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
  vif["Feature"] = X.columns
