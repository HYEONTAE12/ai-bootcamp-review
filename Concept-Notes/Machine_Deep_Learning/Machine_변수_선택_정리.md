
---

# 📘 변수 선택(Feature Selection) 정리

## 1. 변수 선택의 개념

* **정의**: 모델 학습에 필요한 변수를 중요도에 따라 선택하는 과정
  → 불필요하거나 중복된 변수를 제거해 모델의 성능과 해석력을 향상
* **중요 포인트**:

  * 성능 향상: 불필요한 Feature 제거 → 과적합 방지
  * 해석 용이성: 변수 수를 줄여 모델을 이해하기 쉬움
  * 계산 효율성: 연산량 감소, 학습 속도 향상

---

## 2. 변수 선택 방법의 3가지 접근법

### 2.1 Filter Methods

* **아이디어**: 변수 간 **통계적 관계**를 기반으로 중요도 평가
* **장점**: 빠른 계산, 모델 독립적
* **단점**: 변수 간 상호작용을 고려하지 못함

#### 주요 기법

1. **상관관계 기반**

   * 변수 간 상관계수(correlation coefficient) 계산
   * 상관성이 높은 변수 제거 (중복 정보 축소)
2. **분산 기반**

   * 분산이 매우 작은 변수 제거 (정보량 부족)
3. **카이제곱 검정 (Chi-Square Test)**

   * 범주형 독립변수 X 와 종속변수 Y 간 독립성 검정
   * 절차:

     1. 각 X, Y 조합의 빈도수 계산
     2. 기대빈도와 관측빈도의 차이 → 카이제곱 통계량 산출
     3. p-value가 충분히 낮으면 귀무가설(독립)을 기각 → Y와 관련 있음

---

### 2.2 Wrapper Methods

* **아이디어**: 실제 **모델의 성능**을 기준으로 변수 선택
* **장점**: 변수 간 상호작용 고려 가능, 모델 성능과 직결
* **단점**: 계산량 많음(특히 Feature 개수가 많을 때)

#### 주요 기법

1. **Forward Selection (전진 선택)**

   * Feature가 없는 상태에서 시작 → 성능 개선에 기여하는 변수를 하나씩 추가
2. **Backward Elimination (후진 제거)**

   * 모든 Feature로 시작 → 성능에 기여도가 낮은 변수를 하나씩 제거
3. **Recursive Feature Elimination (RFE, 재귀적 제거)**

   * 모델 학습 → 중요도가 낮은 Feature 제거 → 반복 수행

---

### 2.3 Embedded Methods

* **아이디어**: 모델 학습 과정에서 변수 중요도를 산출
* **장점**: 효율적이며 모델 성능과 직결
* **단점**: 모델에 따라 결과 해석 차이 발생 가능

#### 주요 기법

1. **트리 기반 모델 (Tree-based Feature Importance)**

   * 의사결정트리, 랜덤포레스트, XGBoost 등에서 split 기여도 활용
2. **규제 기반 (Regularization)**

   * L1 규제(Lasso): 불필요한 Feature 가중치를 0으로 만들어 자동 선택
   * L2 규제(Ridge): 큰 가중치를 억제해 중요 변수만 강조

---

## 3. 확장된 Feature Selection 방법

### 3.1 Permutation Importance

* **아이디어**: Feature를 **shuffle → 노이즈 처리** → 성능 저하 확인
* **원리**:

  * 중요 Feature일수록 shuffle 시 성능이 크게 하락
* **주의점**:

  * Feature 개수가 많을 경우 비효율적
  * 랜덤성에 따라 결과 변동 가능

### 3.2 Target Permutation (Null Importance 기법)

* **아이디어**: Target을 shuffle해 \*\*무작위 관계(null importance)\*\*를 만든 뒤, 실제 importance와 비교
* **절차**:

  1. Target shuffle → 모델 학습 → Null importance 분포 도출
  2. 원래 Target으로 학습 → Original importance 산출
  3. Null vs Original 비교 → 실제로 중요한 Feature 판별
* **장점**: Noise 변수와 유의미한 변수를 구분 가능

### 3.3 Adversarial Validation

* **아이디어**: Train / Validation 데이터 분포 차이를 검증
* **절차**:

  1. Train 데이터에 label=0, Validation 데이터에 label=1 부여
  2. 합쳐서 분류 모델 학습
  3. 모델이 두 데이터를 잘 구분할수록 분포 차이가 큼
* **활용**:

  * 데이터 분포 차이 탐지
  * Feature 중요도를 통해 두 데이터셋 차이를 유발하는 변수 확인

---

## 4. 비교 정리

| 방법론                    | 아이디어              | 장점              | 단점           | 대표 예시                  |
| ---------------------- | ----------------- | --------------- | ------------ | ---------------------- |
| Filter                 | 통계적 관계 기반         | 빠름, 모델 독립적      | 상호작용 고려 불가   | 상관관계, 분산, 카이제곱         |
| Wrapper                | 모델 성능 기반          | 상호작용 고려 가능      | 계산량 많음       | Forward/Backward, RFE  |
| Embedded               | 학습 과정에서 중요도 추출    | 효율적, 성능 직결      | 모델 종속적       | 트리 기반, L1/L2 규제        |
| Permutation            | 성능 변화 기반          | 직관적             | 랜덤성, 비효율 가능  | Permutation Importance |
| Target Permutation     | Null vs Actual 비교 | Noise 변수 제거 효과적 | 계산량 많음       | Null Importance        |
| Adversarial Validation | 데이터 분포 차이 학습      | 분포 차이 검출 가능     | 직접적 FS 목적 아님 | Train vs Val 분포 차이 탐지  |

---

