

---

# 🧠 앙상블 기법 정리: Stacking vs Blending

## 🔹 1. Stacking (스태킹)

### 📘 개념

* 여러 **기본 모델(Base Models)** 의 예측 결과를 모아
  **메타 모델(Meta Model)** 이 최종 예측을 수행하는 구조

> 즉, "모델 위에 또 다른 모델을 쌓는다(Stack)"는 개념

### ⚙️ 구조

1. **1단계(Base Models)**: 서로 다른 알고리즘으로 학습 (예: LightGBM, CNN, SVM 등)
2. **2단계(Meta Model)**: 1단계 모델들의 예측 결과를 입력으로 받아 최종 예측

### 🧩 예시

```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

base_models = [
    ('svc', SVC(probability=True)),
    ('tree', DecisionTreeClassifier())
]

meta_model = LogisticRegression()

stack = StackingClassifier(estimators=base_models, final_estimator=meta_model)
stack.fit(X_train, y_train)
```

### ✅ 장점

* 서로 다른 모델의 **강점을 조합** 가능
* **메타 모델이 자동으로 가중치를 학습**

### ⚠️ 단점

* 구조가 복잡하고 계산 비용이 큼
* **데이터 누수(Leakage)** 방지를 위해 **K-Fold 기반 예측값** 필요

---

## 🔹 2. Blending (블렌딩)

### 📘 개념

* 여러 모델의 예측값을 **단순 결합(평균 or 가중 평균)** 하는 방식

> 모델들의 “투표”나 “평균 의견”을 반영하는 간단한 앙상블

### ⚙️ 구조

1. 여러 모델을 각각 학습
2. 예측 결과를 단순히 평균 or 가중합으로 결합

### 🧩 예시

```python
pred1 = model1.predict_proba(X_test)
pred2 = model2.predict_proba(X_test)

# 단순 평균 블렌딩
final_pred = (pred1 + pred2) / 2
```

### ✅ 장점

* 구현이 간단하고 빠름
* 데이터 누수 위험이 거의 없음

### ⚠️ 단점

* 단순 결합이라 **모델 간 상호 관계 학습 불가**
* 가중치를 수동으로 조정해야 할 수도 있음

---

## 🧾 비교 요약

| 구분           | **Stacking**           | **Blending**          |
| ------------ | ---------------------- | --------------------- |
| **개념**       | 여러 모델 예측을 메타 모델이 다시 학습 | 여러 모델 예측을 단순 결합       |
| **결합 방식**    | 학습 기반(메타 모델이 존재)       | 평균·가중합 등 비학습 기반       |
| **데이터 누수**   | 발생 위험 있음 (K-Fold 필요)   | 거의 없음                 |
| **복잡도**      | 높음 (2단계 구조)            | 낮음 (단순 계산)            |
| **성능**       | 일반적으로 더 높음             | 간단하지만 효과적             |
| **대표 사용 예시** | LightGBM + Meta LR     | CNN + EfficientNet 평균 |

---
