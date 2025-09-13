
---

# 📘 Gradient Boosting Machine (GBM) 심화 정리

## Bagging

* **정의**: 부트스트랩(bootstrap) 기법으로 표본을 여러 번 뽑아 각각의 모델을 학습시키고, 결과를 집계(평균, 투표 등)하는 앙상블 방법
* **초점**: **분산(Variance) 감소**

### 장점

* 과적합 가능성 감소
* 일반화 성능 증가
* 분산 감소

---

## Boosting

* **정의**: 약한 학습기(Weak learner)를 순차적으로 학습하면서 이전 모델의 오차(Error)에 집중해 점점 더 좋은 모델을 만들어가는 방법
* **초점**: **편향(Bias) 감소**

---

## AdaBoost

* 이전 모델이 **틀리게 예측한 데이터**에 가중치를 크게 부여 → 다음 모델이 해당 데이터를 더 잘 학습할 수 있도록 조정

---

## GBM (Gradient Boosting Machine)

* **정의**: 손실 함수(Loss function)를 기반으로, 그 \*\*Gradient(경사)\*\*를 이용하여 오차가 최소화되도록 다음 모델을 업데이트하는 방식
* **특징**: Boosting 방식의 단점을 보완하고 성능을 강화
* **파생 알고리즘**:

  * **XGBoost**: 정규화 추가, 속도 및 성능 개선
  * **LightGBM**: 대용량 데이터에서 빠르고 효율적, 메모리 사용 최적화
  * **CatBoost**: 범주형 변수(Categorical features) 자동 처리 최적화

---

## Gradient Descent (경사하강법)

* **정의**: 손실 함수를 최소화하기 위해 **기울기(Gradient)** 방향으로 파라미터를 반복적으로 업데이트하는 최적화 기법
* **GBM에서의 역할**: 각 단계에서 Gradient를 계산하여 새로운 모델(트리)을 오차 감소 방향으로 학습시킴

---

## 주요 Regularization 기법 (GBM 안정화)

1. **Subsampling**

   * 전체 데이터 대신 **일부 샘플만 추출**하여 학습
   * 장점: 과적합 방지, 계산량 감소

2. **Shrinkage (Learning Rate)**

   * 새로운 모델의 기여도를 줄이는 방식
   * 작은 Learning rate + 많은 트리 → 더 강력하고 안정적인 모델

3. **Early Stopping**

   * 검증 데이터에서 성능 개선이 일정 기간 나타나지 않으면 학습을 조기 종료

---

## LightGBM

* **특징**: Gradient Boosting 기반으로, 훈련 속도와 메모리 효율성을 높이고 대규모 데이터에서 뛰어난 성능 제공

### 주요 파라미터

* **max\_depth**: 트리의 최대 깊이 제어
* **num\_leaves**: 트리의 leaf 개수 → 복잡도를 제어하는 핵심
* **min\_data\_in\_leaf**: 리프 노드가 가져야 하는 최소 데이터 개수 (Default=20)

---

### 학습 속도 제어

* **feature\_fraction**

  * 각 iteration에서 사용할 Feature 일부만 무작위 선택
  * 특징: 차원 축소 효과, 학습 속도 증가

* **bagging\_fraction**

  * Feature가 아닌 **행(Row)** 샘플을 무작위로 추출
  * 특징: 데이터 샘플링으로 과적합 방지 + 속도 증가

---

### 학습 장비 제어

* **device\_type**: CPU / GPU 선택
* **max\_bin**: Feature를 이산화할 때 사용하는 bin 수

  * 값을 낮추면 속도 증가 (단, 성능 저하 위험 있음)

---

## LightGBM의 핵심 기법

1. **GOSS (Gradient-based One-Side Sampling)**

   * Gradient가 큰 데이터(학습에 중요한 데이터)는 남기고, 작은 데이터는 샘플링 → 속도 향상 + 성능 유지

2. **EFB (Exclusive Feature Bundling)**

   * 서로 상관관계가 거의 없는 Feature들을 묶어서 차원을 줄이는 방법 → 메모리 사용량 감소

---