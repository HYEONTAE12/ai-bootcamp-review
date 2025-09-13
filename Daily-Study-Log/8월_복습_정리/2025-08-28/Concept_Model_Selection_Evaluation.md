
---

# Model Selection & Evaluation 정리

## 1. 모델 선택 (Model Selection)

### 📌 실무에서의 모델 선택 원칙

* 효과적이고 **효율적으로** 모델을 선택해야 함.
* 대표적인 알고리즘은 **모두 테스트**해보는 것이 유리.
* **논문 기반 최신 알고리즘**도 리스트업 후 테스트 권장 (단, 논문 데이터셋 ≠ 실제 업무 데이터셋).
* 최신이거나 복잡한 알고리즘이 반드시 최고 성능을 내는 것은 아님.
* **다양한 작동 원리**를 가진 알고리즘을 비교하는 것이 중요 (동일한 방식끼리만 비교 X).

### 📌 Regression 모델

* 목표: **잔차(residual)를 최소화**하는 선을 찾는 과정
* 주요 모델:

  * **선형 회귀**: Linear, Ridge, Lasso, Elastic Net
  * **비선형 회귀**: Polynomial Regression, Log Regression
  * **Tree 계열**: Decision Tree Regressor

    * Bagging 앙상블: RandomForest Regressor
    * Boosting 앙상블: XGBoost, LightGBM, CatBoost 등

### 📌 Classification 모델

* 목표: **두 클래스를 가장 잘 나누는 결정 경계(Decision Boundary)를 찾는 것**
* 주요 모델:

  * Logistic Regression
  * SVM (Support Vector Machine)
  * Tree 계열 Classifier

    * Bagging: RandomForest Classifier
    * Boosting: LightGBM, XGBoost, CatBoost 등
  * Neural Network (딥러닝 모델)

---

## 2. Feature Engineering (Feather Mart 설계)

### 📌 핵심

* 좋은 모델보다 **좋은 Feature**가 더 큰 성능 차이를 만든다.
* 모델링 전에 Feature Mart를 설계:

  * 다양한 변수 조합
  * 파생변수 생성 (예: ratio, difference, interaction feature 등)
* 원하는 성능이 안 나온다면:

  1. 모델 변경보다 Feature Mart를 다시 설계
  2. Feature를 **풍부하게 확장**
* 내가 가진 데이터로 Feature Mart의 확장이 한계에 도달 → 그때 **논문, 새로운 알고리즘 탐색**

---

## 3. 모델 성능 비교 (Model Evaluation)

### 📌 비교 조건

* 동일한 **Data set**
* 동일한 **환경(random state 고정)**
* 동일한 **평가지표(Metrics)**
* 실제 서비스 환경과 유사하게 평가

---

### 📊 Regression 평가 지표

* **MAE (Mean Absolute Error)**

  * 실제값과 예측값 차이의 절댓값 평균
  * 단위가 원래 데이터와 같아 직관적
  * Outlier에 덜 민감
* **MSE (Mean Squared Error)**

  * 차이를 제곱 → 큰 오차에 더 민감
* **RMSE (Root MSE)**

  * 제곱한 값에 루트 적용 → 단위 맞춤
* **R² (결정계수)**

  * 0\~1 사이 값, 1에 가까울수록 설명력이 높음

👉 MAE, MSE, RMSE → 0에 가까울수록 좋음
👉 R² → 1에 가까울수록 좋음

---

### 📊 Classification 평가 지표

* **Precision (정밀도)**

  * 모델이 Positive라 예측한 것 중 실제로 Positive인 비율
* **Recall (재현율, 민감도)**

  * 실제 Positive 중에서 모델이 Positive로 예측한 비율
* **F1-Score (조화평균)**

  * Precision & Recall의 균형
  * 데이터 불균형 문제에서 중요
* **ROC-AUC**

  * ROC Curve 아래 면적
  * AUC=1이면 완벽 분류, 0.5면 랜덤 추측 수준

👉 현업에서는 문제 상황(비용, 위험, 중요도)에 따라 Precision vs Recall 중 어디에 집중할지 결정

---

## 4. 데이터 전처리 (Preprocessing)

* **표준화 (Standardization)**

  * 평균 0, 분산 1 기준으로 변환 (정규분포 형태)
  * 음/양의 상관관계 모두 반영 가능
* **정규화 (Normalization)**

  * 0\~1 범위로 변환
  * 다른 스케일의 변수를 비교하기 용이

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

scaler1 = StandardScaler()
X_std = scaler1.fit_transform(X)

scaler2 = MinMaxScaler()
X_norm = scaler2.fit_transform(X)
```

---

## 5. 모델링 프로세스

1. **모델 선택**
2. **훈련 (Train)**
3. **과적합 여부 확인** (train/validation 비교)
4. **평가지표 확인** (F1-score, ROC-AUC 등)
5. **DataFrame으로 기록** (모델명, 지표 값 append)
6. **다음 모델도 동일하게 진행**
7. **최종 비교 및 선택**

---

## 6. 과적합 & 하이퍼파라미터 튜닝

* **과적합 (Overfitting)**:

  * Train 데이터에만 최적화 → Test/실제 데이터 성능 저하
* **하이퍼파라미터 튜닝 목적**:

  * 과적합 방지 + 성능 향상
  * Grid Search, Random Search, Bayesian Optimization 등 활용

---

## 7. 데이터 분할 (Data Split)

```
[--------------------------------------------------------------]
[----------train-----------][----validation---][------test-----]
```

* **Train**: 모델 학습
* **Validation**: 하이퍼파라미터 조정 및 모델 검증
* **Test**: 최종 성능 평가 (절대 유출 금지)

---

## 8. 전체 워크플로우 (정리)

### 📌 Chapter 1: 기획

* 문제정의 → 기대효과 → 해결방안 → 우선순위 → 데이터 분석 → 성과측정 → 모델 운영

### 📌 Chapter 2: 데이터 준비

* 사용 가능 데이터 확인
* Target Label 생성
* 샘플링 전략 수립

### 📌 Chapter 3: 데이터 마트 설계

* Feature Mart 설계 (문제 상황별 맞춤 변수)
* Regression → 상관계수(Corr)
* Classification → 정보가치(IV, Information Value)

### 📌 Chapter 4: 모델링

* 데이터 전처리 (정규화/표준화)
* Model Selection
* 성능 비교 & Model Evaluation

---

✅ **핵심 결론**

* 최신 알고리즘보다 **좋은 Feature Engineering**이 성능을 좌우한다.
* 동일한 조건에서 공정하게 성능을 비교해야 한다.
* 과적합 방지와 하이퍼파라미터 튜닝은 모델 실무 성능 향상 핵심이다.

---

