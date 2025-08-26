
---

# 📊 데이터 전처리 & 데이터 마트 기획/설계 정리

## 1. Data Sampling (데이터 샘플링)

### 1) 시계열 데이터 (Time series data)

* **Up-sampling (업샘플링)**

  * 시간 주기를 더 세분화 (예: 일 단위 → 시간 단위)
  * 새로운 구간에 값이 없으면 **결측치(NaN) 발생** → `ffill()`, `bfill()`, `interpolate()` 등으로 채움
* **Down-sampling (다운샘플링)**

  * 시간 주기를 더 큰 단위로 (예: 시간 단위 → 일 단위)
  * 집계 함수 사용: `mean()`, `max()`, `min()`, `sum()`

### 2) 비시계열 데이터 (Non-time series data)

* **Class Imbalance 문제**

  * Target 데이터가 적을 경우 → **Over-sampling** (예: SMOTE, RandomOverSampler)
  * 데이터가 너무 많을 경우 → **Under-sampling** (예: RandomUnderSampler)
* **Stratified Sampling (층화추출)**

  * Target 분포(비율)를 유지하면서 샘플링
  * 분류 문제(Classification)에서 필수적

---

## 2. Over-sampling / Under-sampling & Stratified Sampling

### ✅ Over-sampling

* **장점**

  * 소수 클래스 데이터 부족 문제 해소
  * 모델이 소수 클래스 패턴을 더 잘 학습
* **단점**

  * 데이터 중복 생성 → Overfitting 위험

### ✅ Under-sampling

* **장점**

  * 학습 속도 향상 (데이터 축소)
  * 데이터 불균형 단순화
* **단점**

  * 다수 클래스의 데이터 손실 → 정보 손실 위험

### ✅ Stratified Sampling (층화추출)

* **비례층화추출 (Proportional Stratified Sampling)**

  * Target 분포(비율)를 유지하며 추출
* **장점**

  * 모집단 분포를 잘 반영 → 대표성 보장
  * 불균형 데이터에서도 안정적인 샘플 확보
* **단점**

  * 층(집단) 구성이 잘못되면 왜곡 발생
  * 복잡한 데이터셋일수록 층 정의가 까다로움

---

## 3. 데이터 전처리 과정 (Preprocessing)

1. **결측치 확인 및 처리**

   * `isnull().sum()` 으로 결측치 개수 확인
   * 처리 방식: `fillna()`, `dropna()`, 예측 모델 기반 대체 등

2. **이상치(Outlier) 처리**

   * Z-score, IQR 방식으로 탐지
   * 제거할지 유지할지 → **업무 담당자 지침에 따라 결정**

3. **중복 데이터 처리**

   * `duplicated()` 확인 후
   * `drop_duplicates()`로 제거

4. **데이터 타입 변환**

   * 날짜 → `datetime`
   * 범주형 → `category`
   * 정수/실수 변환 등

---

## 4. 데이터 수준 사전 점검 (Data Readiness Check)

1. **Target Label 생성**

   * 문제 정의에 맞게 라벨 생성 (예: 구매 여부, 이탈 여부)

2. **Target Ratio 확인**

   * 클래스 불균형 확인 (`value_counts(normalize=True)`)

3. **분석 방향성 결정**

   * 데이터 수준으로 문제 해결 가능 여부 점검
   * 필요시 추가 데이터 수집 고려

---

## 5. 데이터 마트 기획 및 설계

### 데이터 흐름 구조

```
Data Source → Data Lake → Data Warehouse → Data Mart
```

1. **Data Sources**

   * 원천 데이터 (로그 데이터, 구매 데이터, 고객 정보, 출국 데이터 등)
   * 아직 가공되지 않은 **레거시 데이터, 원본 데이터**

2. **Data Lake**

   * Source에서 **원하는 데이터만 수집**
   * 다양한 데이터 원천에서 추출, 가공 전 상태로 저장

3. **Data Warehouse**

   * 수집한 데이터를 **유형별/주제별로 정리, 통합**
   * 데이터 품질 관리, 일관성 유지

4. **Data Mart**

   * 특정 프로젝트/분석 목적에 맞게 **특화된 데이터셋 구축**
   * Feature Engineering 진행
   * 분석 및 모델 학습을 위한 데이터셋 최종 단계

---

## 6. 가설 수립 및 변수 설계 (Hypothesis → Mart 구성)

* **가설 → Category → 변수 → Type → 설명 → Logic(산식)**

| 가설                     | Category | 변수명        | Type  | 설명              | Logic                       |
| ---------------------- | -------- | ---------- | ----- | --------------- | --------------------------- |
| 신규 고객은 할인 쿠폰에 민감하다     | 고객 특성    | 쿠폰 사용 여부   | int   | 쿠폰 사용(1)/미사용(0) | flag 생성                     |
| 재방문 고객은 구매금액이 높다       | 구매 정보    | 총 구매 금액    | float | 고객별 총 구매금액      | `sum(price)`                |
| 특정 국가 고객은 특정 상품군을 선호한다 | 지역/상품    | 국가별 상품군 비율 | float | 국가별 상품군 비중      | `groupby(country, product)` |

---

# ✅ 정리

* **Data Sampling** → 시계열/비시계열 샘플링 전략
* **전처리** → 결측치, 이상치, 중복, 데이터 타입 변환
* **데이터 수준 점검** → Target 라벨 생성 & 비율 확인
* **데이터 마트 설계** → Source → Lake → Warehouse → Mart 구조
* **가설 기반 변수 설계** → Category별 Feature 정의

---

