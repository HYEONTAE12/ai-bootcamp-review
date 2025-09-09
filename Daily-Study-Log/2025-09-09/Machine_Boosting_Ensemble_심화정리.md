

---

# Gradient Boosting & Ensemble 심화 정리

## 1. Bagging vs Boosting

### 🔹 Bagging (Bootstrap Aggregating)

* **개념**: 원본 데이터를 부트스트랩(복원추출)으로 여러 표본을 생성 → 각 표본으로 모델 학습 → 결과를 평균/투표.
* **목표**: 분산(Variance) 감소.
* **대표 알고리즘**: Random Forest.

**장점**

* 과적합 방지.
* 병렬 학습 가능 → 속도 유리.
* 안정적 예측 성능.

**단점**

* 약한 모델(Weak learner)을 강하게 만드는 데는 한계가 있음.
* 편향(Bias)은 줄이지 못함.

---

### 🔹 Boosting

* **개념**: 순차적으로 모델을 학습하면서, 이전 모델이 틀린 데이터를 다음 모델이 보완.
* **목표**: 편향(Bias) 감소.
* **대표 알고리즘**: AdaBoost, GBM, XGBoost, LightGBM, CatBoost.

**장점**

* 약한 모델을 순차적으로 보강 → 높은 성능.
* 예측력이 뛰어남.

**단점**

* 순차적 학습 → 병렬화가 어렵고 느릴 수 있음.
* 과적합 위험 존재 (특히 learning rate, depth 조절 실패 시).

---

## 2. 주요 Boosting 알고리즘

### 🔹 AdaBoost (Adaptive Boosting)

* 오분류된 데이터에 더 큰 가중치를 부여 → 이후 모델이 집중하도록 유도.
* Decision Stump(깊이가 1인 트리)를 기본 약한 학습기로 자주 사용.

---

### 🔹 GBM (Gradient Boosting Machine)

* **Loss Function**의 Gradient(기울기)를 활용하여 다음 모델이 보완하도록 학습.
* 성능은 좋지만, 트리마다 순차적으로 학습해야 해서 느림.
* 대표적인 후속 발전 알고리즘이 XGBoost, LightGBM, CatBoost.

---

### 🔹 XGBoost (Extreme Gradient Boosting)

* GBM의 개선판, 실무와 대회에서 가장 많이 쓰이는 모델 중 하나.
* **특징**:

  * Regularization(규제 항) 추가 → 과적합 방지.
  * 분산 처리 가능 (병렬화 지원).
  * Missing Value 자동 처리.
* **장점**: 빠른 속도, 높은 성능, 다양한 튜닝 옵션.
* **단점**: 파라미터 많음 → 튜닝 난이도 높음.

---

### 🔹 LightGBM

* Microsoft에서 개발. 대용량 데이터에 특화.
* **특징**:

  * **Leaf-wise 성장 방식** (기존 Depth-wise 대비) → 더 깊은 트리, 더 높은 정확도.
  * **GOSS**(Gradient-based One-Side Sampling): 중요한 데이터 위주로 학습.
  * **EFB**(Exclusive Feature Bundling): 희소한 Feature 묶어서 차원 축소.
* **장점**: 대용량, 고차원 데이터에서도 빠르고 메모리 효율적.
* **단점**: 작은 데이터셋에서는 과적합 발생 가능.

---

### 🔹 CatBoost

* Yandex(러시아)에서 개발, 범주형 데이터(Categorical Data)에 특화.
* **특징**:

  * One-Hot, Label Encoding 없이 카테고리형 자동 처리.
  * Ordered Boosting 기법 → 데이터 누수 방지.
  * Hyperparameter 튜닝이 상대적으로 단순.
* **장점**: 범주형 변수가 많을 때 강력.
* **단점**: 속도는 LightGBM보다 느릴 수 있음.

---

## 3. Gradient Boosting 핵심 개념 보충

* **Subsampling**: 매 Iteration마다 데이터 일부만 사용 → 과적합 방지 + 학습 속도 향상.
* **Shrinkage (Learning Rate)**: 각 트리의 기여도를 줄여 점진적으로 최적화.
* **Early Stopping**: 일정 라운드 동안 개선이 없으면 학습 중단 → 과적합 방지.
* **Regularization**: 복잡도 제한(트리 깊이, L1/L2 페널티 등) → 과적합 억제.

---

## 4. LightGBM 주요 파라미터

### 🔹 트리 구조 관련

* `max_depth`: 트리 최대 깊이 제한. (과적합 방지용)
* `num_leaves`: 트리의 리프 노드 개수. (성능 ↔ 과적합 trade-off)
* `min_data_in_leaf`: 리프 노드가 가져야 할 최소 샘플 수. (과적합 방지 핵심)

### 🔹 학습 속도 & 샘플링

* `feature_fraction`: 매 트리마다 사용할 Feature 비율. (과적합 방지, 속도 향상)
* `bagging_fraction`: 매 트리마다 사용할 데이터 샘플 비율.
* `bagging_freq`: 배깅 적용 빈도.

### 🔹 정규화 & 과적합 방지

* `lambda_l1`: L1 정규화 (가중치 절대값 제약).
* `lambda_l2`: L2 정규화 (가중치 제곱 제약).
* `min_gain_to_split`: 최소 정보 이득 (split 되려면 이득이 있어야 함).

### 🔹 학습 제어

* `learning_rate`: 학습률 (Shrinkage).
* `n_estimators`: 생성할 트리 개수.
* `early_stopping_rounds`: 일정 라운드 개선 없으면 학습 종료.

### 🔹 디바이스 & 메모리

* `device_type`: cpu / gpu 설정.
* `max_bin`: Feature를 이산화할 때 최대 bin 수 (작을수록 속도 ↑, 성능 ↓ 가능).

---

## 5. 실무 팁

1. **데이터 크기 기준 선택**

   * 대용량(수십만 \~ 수백만 행): LightGBM 추천.
   * 범주형 Feature 많음: CatBoost 추천.
   * 튜닝 리소스 풍부 / 안정적: XGBoost 추천.

2. **튜닝 전략**

   * Step 1: `num_leaves`, `max_depth` 조절 (복잡도).
   * Step 2: `min_data_in_leaf`, `lambda_l1/l2`, `feature_fraction` 등 정규화 조절.
   * Step 3: `learning_rate` 줄이고 `n_estimators` 늘려 안정화.

3. **Early Stopping 적극 활용**

   * 과적합 방지 + 시간 절약.

4. **Ensemble**

   * 실무에서는 LightGBM, XGBoost, CatBoost를 함께 돌려 **스태킹/블렌딩**하면 성능이 확 올라감 (특히 캐글 대회에서 기본 전략).

---

## 6. 비교 요약

| 알고리즘     | 장점              | 단점              | 적합한 경우         |
| -------- | --------------- | --------------- | -------------- |
| XGBoost  | 안정적, 튜닝 다양, 병렬화 | 파라미터 복잡, 메모리 부담 | 범용, Kaggle 기본기 |
| LightGBM | 빠름, 대용량 최적      | 소규모 데이터 과적합 가능  | 수십만 건 이상 데이터   |
| CatBoost | 범주형 자동 처리, 안정적  | 상대적으로 느림        | 범주형 변수가 많은 데이터 |

---

👉 정리하면, **Bagging은 분산 줄이는 방법, Boosting은 편향 줄이는 방법**이고, 실무에서는 \*\*LightGBM(속도/대용량), XGBoost(범용/안정성), CatBoost(범주형 특화)\*\*를 상황에 따라 선택하는 게 핵심

---
