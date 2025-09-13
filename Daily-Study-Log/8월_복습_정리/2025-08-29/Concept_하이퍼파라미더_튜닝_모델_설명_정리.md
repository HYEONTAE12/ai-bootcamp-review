
---

# ⚙️ Hyper-parameter Tuning & Model Explanation 정리

---

## 🔑 Parameter vs Hyper-parameter

* **Parameter (파라미터)**

  * 모델 학습을 통해 **자동으로 결정**되는 값
  * 예: 선형회귀의 가중치(β), 신경망의 weight & bias
  * 👉 *데이터에 의해 최적화됨*

* **Hyper-parameter (하이퍼파라미터)**

  * 모델 학습 전에 **사람이 직접 세팅**해야 하는 값
  * 예: 학습률(learning rate), 트리 깊이(max\_depth), 정규화 계수(lambda)
  * 👉 *최적의 Parameter를 찾기 위해 조정하는 "환경 변수"*

---

## 🎯 대표적 Hyper-parameter Tuning 방법론

### 1) **Grid Search**

* 정의: 지정된 범위 내에서 **모든 조합을 탐색**하여 최적값을 찾는 방식
* 장점: 전체 탐색 → 최적값 보장
* 단점: 연산량 ↑, 시간 오래 걸림
* 👉 *소규모 데이터/모델에 적합*

---

### 2) **Random Search**

* 정의: 지정된 범위 내에서 **무작위로 조합 샘플링**
* 장점: 연산량 ↓, 빠름, 고차원 파라미터에서 효율적
* 단점: 최적 조합을 놓칠 수도 있음
* 👉 *Grid Search보다 실용적, 자주 사용*

---

### 3) **Bayesian Optimization (베이지안 최적화)**

* 정의: \*\*확률 모델(가우시안 프로세스 등)\*\*을 이용해, 이전 탐색 결과를 기반으로 다음 탐색 위치를 정하는 방식
* 장점: 탐색 효율 ↑, 최소한의 시도로 최적값 근접
* 단점: 구현 복잡
* 👉 *대규모 데이터·복잡한 모델에서 중요*

---

## 🔁 교차 검증 (Cross Validation)

* 데이터셋을 **여러 개의 fold로 분할** 후, 번갈아 학습/검증을 수행하는 방식
* 목적: **데이터 편향 방지** & **일반화 성능 검증**
* 예: k-Fold CV (k=5 → 데이터셋을 5개로 나눠 학습/검증 반복)

### 📌 `cross_val_score`

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(scores.mean())  # 평균 성능
```

* **cv=5** → 5겹 교차 검증
* **scoring** → 평가 지표 선택 (accuracy, f1, roc\_auc 등)
* 👉 *모델 선택(Model Selection) 과정에서 필수*

---

## 🔎 Model Explanation (모델 설명)

> 모델의 예측 결과를 **"왜 그렇게 나왔는지" 설명할 수 있는 방법**
> → 현업 팀원 설득, 커뮤니케이션, 의사결정에 필요

---

### 1) **Permutation Importance**

* 개념: 특정 피처 값을 **무작위로 섞어버린 후**, 성능이 얼마나 떨어지는지 측정
* 아이디어: 해당 피처가 **중요하다면 성능 크게 하락**
* 장점: 직관적, 모든 모델에 적용 가능
* 단점: 계산량 많음

---

### 2) **Shapley Value / SHAP**

* 개념: 게임이론(협력 게임) 기반, 각 피처가 모델 예측값에 **얼마나 기여했는지** 수치화
* 방식:

  * 피처가 포함되었을 때와 빠졌을 때의 성능 차이를 평균
  * 공정하게 기여도 분배
* **SHAP (SHapley Additive exPlanations)**: Shapley Value를 ML에 적용한 대표적 방법론
* 장점: 개별 예측 단위에서도 설명 가능 (*"이 고객은 나이 변수 때문에 구매 확률 ↑"*)
* 단점: 계산 복잡

---

## ✅ 전체 요약

1. **Parameter**: 모델이 학습으로 얻는 값
2. **Hyper-parameter**: 우리가 직접 세팅하는 값 → Tuning 필요
3. **Tuning 방법**

   * Grid Search (완전 탐색, 정확 but 느림)
   * Random Search (랜덤, 빠름)
   * Bayesian Optimization (확률 모델 기반, 효율적 → 중요)
4. **Cross Validation**: 일반화 성능 검증을 위한 필수 절차
5. **Model Explanation**

   * Permutation Importance: 피처 무작위 섞어서 중요도 확인
   * Shapley Value/SHAP: 공정한 기여도 측정, 해석력 ↑

---

