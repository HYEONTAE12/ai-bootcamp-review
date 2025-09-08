
---

# 📝 분류문제 모델링 방법론 정리

## 1. 실습 개요

* 데이터셋: **위스콘신 유방암 데이터셋 (Breast Cancer Wisconsin)**
* 목표: 환자의 종양이 \*\*악성(malignant, 암)\*\*인지 \*\*양성(benign, 암 아님)\*\*인지 분류하는 **이진분류 문제**
* 피처: 30개
* 샘플: 569개

---

## 2. 데이터셋 불러오기와 확인

```python
from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()

print(cancer["data"].shape)       # (569, 30) → 569개 샘플, 30개 특징
print(cancer["feature_names"])    # 특징 이름
print(cancer["target_names"])     # ['malignant' 'benign']
```

* `0` → malignant (악성, 암)
* `1` → benign (양성, 암 아님)

👉 일반적인 직관(0=암 아님, 1=암)과 반대이므로 주의!

---

## 3. 로지스틱 회귀 (Logistic Regression)

### 기본 개념

* 출력: **0 또는 1 확률**
* 결정 경계: **시그모이드 함수**를 이용해 확률로 해석
* **intercept (절편)** = 바이어스 $b$
* **coef (계수)** = 각 피처의 기울기 $w$

### 한계값(threshold)

```python
probs = model.predict_proba(X_test)[:, 1]
prediction = (probs > 0.5).astype(int)
```

* 기본값: 0.5
* threshold ↑ (0.7 등): 암 판정을 엄격히 → False Positive↓, False Negative↑
* threshold ↓ (0.3 등): 암 판정을 쉽게 → False Negative↓, False Positive↑

👉 의료 데이터에서는 보통 **False Negative(암인데 놓침)** 줄이는 게 더 중요 → threshold를 낮게 잡음

---

## 4. 결정트리 (Decision Tree)

### 불순도(impurity)

* **지니지수(Gini Index)** 또는 \*\*엔트로피(Entropy)\*\*로 노드의 순도를 측정
* 트리는 **불순도를 가장 많이 줄이는 피처**를 기준으로 분할

### 시각화

```python
from sklearn.tree import export_graphviz
export_graphviz(dec_tree, out_file="tree.dot",
                class_names=cancer["target_names"],
                feature_names=cancer["feature_names"],
                impurity=True, filled=True)
```

* Graphviz로 **트리 구조 그림** 출력
* 노드마다 사용한 feature, threshold, 샘플 수, 불순도 표시

### Feature Importance

```python
print(dec_tree.feature_importances_)
```

* 각 피처가 불순도 감소에 기여한 정도
* 합 = 1
* 값이 클수록 더 중요한 feature
* 예: `"worst concave points"`가 높은 중요도를 가짐

👉 중요도를 시각화:

```python
plt.barh(np.arange(n_features), dec_tree.feature_importances_)
plt.yticks(np.arange(n_features), cancer["feature_names"])
```

---

## 5. 서포트 벡터 머신 (SVM)

### 기본 개념

* 데이터를 가장 잘 나누는 \*\*초평면(hyperplane)\*\*을 찾음
* 초평면:

  * 2D → 직선
  * 3D → 평면
  * N차원 → 고차원 평면
* 마진(margin): 초평면과 가장 가까운 점(서포트 벡터) 사이 거리

### 선형 SVM

```python
clf = SVC(kernel='linear', C=1.0)
clf.fit(X, y)
```

* `C` 값: 규제 강도

  * C ↑ → 마진 좁게, 오차 적게 (과적합 위험↑)
  * C ↓ → 마진 넓게, 오차 허용 (일반화↑)

### 결정 경계 시각화

```python
Z = clf.decision_function(xy).reshape(XX.shape)
ax.contour(XX, YY, Z, levels=[-1,0,1], linestyles=['--','-','--'])
```

* 0: 결정경계
* ±1: 마진선
* support\_vectors\_: 마진에 닿은 샘플들

---

## 6. 주요 개념 요약

* **Intercept(bias)**: 모든 feature=0일 때의 기본값
* **Coef(weights)**: feature가 결과에 미치는 영향
* **Standardization(표준화)**: 평균 0, 표준편차 1로 변환 → 학습 안정화
* **Threshold**: 분류 확률 기준점, 민감도/특이도 조절
* **Feature Importance**: 트리 모델에서 각 feature의 영향력
* **Hyperplane**: 분류 경계, SVM의 핵심
* **Support Vectors**: 마진 경계에 위치한 결정적 샘플

---

