
---

# 🧠 CV Model 성능 향상 전략 정리

---

## 🗂️ 1. 데이터(Data)

### 📊 EDA (Exploratory Data Analysis)

* **핵심:** 가설 수립이 중요
  → “이미지를 보니 이런 전처리나 증강을 사용하면 성능이 향상될 것 같다.”
* 이미지 및 **object의 분포 파악**
* **이미지 다양성** 확인
* **이상치 및 noise 종류** 파악

---

### 🧩 Augmentation (데이터 증강)

EDA 결과를 바탕으로 **적절한 증강 기법**을 선택해 적용합니다.

**효과**

* 데이터 수 증가
* 모델의 **Robustness(강건성)** 향상
* **Imbalance(불균형)** 보정

**기본 기법**

* Horizontal Flip
* Crop
* Median Blur
* Contrast
* Hue / Saturation / Value
* Gamma 등

---

### 🚀 Further Augmentation (고급 증강)

#### ✂️ Cutout

* 이미지의 일부를 **마스킹(가림)** 하여 학습
* 모델이 이미지의 일부분에 의존하지 않도록 하여 **일반화 성능 향상**

#### 🔀 Mixup

* 서로 다른 두 이미지와 label을 **선형적으로 결합**
* 데이터 다양성 증가 및 **노이즈에 덜 민감**
* **일반화 성능 향상**

#### 🧩 CutMix

* 두 이미지를 **일부 교차 결합**
* label 또한 같은 비율로 혼합
* **데이터 다양성 + 일반화 성능 향상**

#### 📋 Copy & Paste

* 객체를 잘라 다른 이미지에 붙여넣기
* **Detection / Segmentation**에서 자주 사용
* 객체의 **위치, 형태 다양성 증가**

#### 🧠 Pseudo Labeling

* **비지도 데이터에 가짜 라벨 부여**
* 학습 데이터 부족 문제 해결
* 더 다양한 데이터 활용으로 **일반화 성능 향상**

---

## 🧮 2. 모델(Model)

### ⚙️ Hyperparameter Tuning (하이퍼파라미터 조정)

#### 📉 Scheduler

* **Learning Rate를 동적으로 조정**
* 효율적인 수렴 유도

#### ⚖️ Weight Decay

* 가중치의 제곱합에 패널티 부여
* 특정 weight의 과도한 성장 억제 → **Overfitting 방지**

#### 📦 Batch Size

* **큰 batch** → 전체 분포 근사, noise에 덜 민감
* **작은 batch** → 메모리 효율, generalization 약간 향상
* Task 특성에 맞는 **적절한 값** 탐색 필요

#### 🔁 Epoch

* 데이터 반복 학습 횟수 조절
* 너무 작으면 **underfitting**, 너무 크면 **overfitting**

#### 💧 Dropout

* 일부 neuron을 **무작위로 비활성화**
* 특정 뉴런 간 의존성 완화
* **Overfitting 방지**

---

### 🧠 Ensemble (앙상블)

여러 모델의 예측 결과를 결합해 **성능을 향상**시키는 방법

#### ✅ Ensemble 유형

| 유형                                    | 설명                                       |
| ------------------------------------- | ---------------------------------------- |
| **Model Ensemble**                    | 서로 다른 구조의 모델 결과를 결합                      |
| **Data Ensemble**                     | 서로 다른 데이터 split/augmentation으로 학습한 결과 결합 |
| **Framework Ensemble**                | 다른 DL 프레임워크(PyTorch, TF 등)로 학습한 결과 결합    |
| **Seed Ensemble**                     | seed를 바꿔 여러 번 학습 후 결합                    |
| **Hyperparameter Ensemble**           | 서로 다른 하이퍼파라미터 조합으로 학습 후 결합               |
| **Snapshot Ensemble**                 | 학습 중 서로 다른 시점의 모델을 저장해 결합                |
| **SWA (Stochastic Weight Averaging)** | 일정 주기마다 모델 weight 평균화                    |
| **Model Soup**                        | 여러 모델의 파라미터를 평균내어 inference cost 절감      |

#### 🧾 예측 결과 기반 Ensemble

**Classification**

* **Hard Voting**: 다수결 방식 (가장 많이 예측된 class 선택)
* **Soft Voting**: 예측 확률 평균

**Object Detection**

* **Hard-NMS**: 겹치는 박스 중 score 낮은 것 완전 제거
* **Soft-NMS**: score 가중치만 낮춤
* **WBF (Weighted Box Fusion)**: 각 박스에 가중치 부여해 융합 (정보 손실 ↓)

**Segmentation**

* **Hard Voting**: pixel 단위 다수결
* **Soft Voting**: pixel 단위 확률 평균

---

## 🧪 3. 학습·추론·평가 (Training / Inference / Evaluation)

### 🧩 좋은 Validation Set 조건

* **Test 분포에 잘 generalize** 되는 경우
* Validation 성능이 오를 때 **Test 성능도 함께 상승**
* Validation Score ↔ Test Score 간 **높은 상관관계**

---

### 🧭 Validation 전략

| 전략                                | 설명                                   |
| --------------------------------- | ------------------------------------ |
| **Random Split**                  | 랜덤하게 train/val 분리                    |
| **K-Fold CV**                     | 모든 데이터가 val로 한 번씩 사용됨                |
| **Stratified K-Fold**             | Class 비율 유지하며 분할 (imbalance 대응)      |
| **Multi-Label Stratified K-Fold** | Multi-label 데이터의 label 비율 유지         |
| **Group K-Fold**                  | 같은 group이 train/val에 동시에 들어가지 않도록 분할 |

---

### 🧠 TTA (Test Time Augmentation)

* **Training cost 증가 없이** test sample에 augmentation 적용
* 여러 변형된 test 이미지를 예측 → **결과 평균**
* 다양하게 변형된 test image로 **robustness 향상**

> ⚠️ **train 시 사용한 augmentation과 일치**하도록 구성해야 함

---

## 🔍 4. 모델 결과 분석 (Model Interpretability)

### 🔥 Grad-CAM

* CNN 모델이 **어떤 영역에 주목하는지** 시각화
* 특정 class의 gradient와 **마지막 conv layer의 활성화 맵**을 이용
* 잘못된 예측의 원인 분석에 유용

### 🎯 Attention Heatmap

* Transformer 모델의 **self-attention 가중치 시각화**
* 모델이 입력 이미지의 **어떤 부분에 집중하는지** 파악 가능

---

## 📘 정리 요약

| 단계        | 핵심 포인트                               |
| --------- | ------------------------------------ |
| **데이터**   | EDA 기반 전처리 및 증강 전략 수립                |
| **모델**    | 하이퍼파라미터, regularization, ensemble 활용 |
| **학습/평가** | 검증 전략, TTA, robust validation 구성     |
| **분석**    | Grad-CAM / Attention으로 성능 근거 시각화     |

---

