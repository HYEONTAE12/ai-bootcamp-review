
---

# 📌 EfficientNet 정리 (에피션트넷)

## 1. 🧠 EfficientNet이란?

EfficientNet은 **효율성(Efficiency)**에 초점을 맞춘 CNN(Convolutional Neural Network) 아키텍처입니다.
주요 목표는 **더 적은 파라미터와 연산량으로 높은 정확도**를 달성하는 것입니다.

* **핵심 아이디어**:
  기존 CNN 모델들은 네트워크를 확장할 때 보통 한 가지 방향(깊이, 너비, 해상도)만 늘리는데,
  EfficientNet은 세 가지 모두를 **균형 있게 동시에 늘리는 컴파운드 스케일링(Compound Scaling)** 기법을 사용합니다.

---

## 2. ⚙️ EfficientNet의 주요 구성 요소

### ✅ 1) Baseline 구조

* EfficientNet-B0는 기본 구조로, 이 위에 B1 ~ B7로 확장됨.
* MobileNetV2의 **Inverted Residual Block (Inverted Bottleneck)** 구조를 기반으로 함.

### ✅ 2) Depthwise Separable Convolution

* 연산량을 줄이기 위해 사용되는 경량 컨볼루션 기법
* 구성:

  * **Depthwise Convolution**: 채널별로 독립적으로 필터 적용
  * **Pointwise Convolution (1x1)**: 채널 간 정보를 통합

### ✅ 3) Squeeze-and-Excitation (SE) Block

* 채널 간 중요도를 학습하여 강조할 채널을 선택함
* 특징 있는 채널을 강화함으로써 성능 향상

### ✅ 4) Swish 활성화 함수

* ( f(x) = x \cdot \text{sigmoid}(x) )
* ReLU보다 부드럽고 성능이 좋은 것으로 알려짐

---

## 3. 📈 Compound Scaling (복합 스케일링)

> EfficientNet의 성능과 효율성을 동시에 끌어올리는 핵심 기법

### 기존의 스케일링 방식과의 차이

| 스케일링 방식       | 설명                              |
| ------------- | ------------------------------- |
| 깊이만 확장        | 더 많은 층으로 표현력 향상 (예: ResNet-152) |
| 너비만 확장        | 더 많은 채널로 세밀한 정보 표현              |
| 해상도만 증가       | 더 고해상도의 이미지 입력                  |
| **컴파운드 스케일링** | 위 세 가지를 **비율 기반으로 동시에 확장**      |

### 수식 예시

[
\text{depth} = \alpha^\phi,\quad \text{width} = \beta^\phi,\quad \text{resolution} = \gamma^\phi
]
단, (\alpha \cdot \beta^2 \cdot \gamma^2 \approx 2) 이라는 제약조건을 둠

---

## 4. 🧪 퀴즈 모음 (음성 대화 기반)

| 번호 | 질문                                       | 정답                                    |
| -- | ---------------------------------------- | ------------------------------------- |
| 1  | EfficientNet에서 스케일링 시 고려하는 3가지 요소는?      | 깊이(depth), 너비(width), 해상도(resolution) |
| 2  | EfficientNet이 기존 모델보다 더 효율적인 이유는?        | 컴파운드 스케일링 덕분에 균형 잡힌 확장 가능             |
| 3  | Depthwise Separable Convolution의 구성 요소는? | Depthwise + Pointwise Convolution     |
| 4  | SE Block의 역할은?                           | 채널 중요도를 학습해 특정 채널 강조                  |
| 5  | EfficientNet의 기본 구조는 어떤 모델에서 차용했나?       | MobileNetV2                           |
| 6  | EfficientNet에서 사용되는 활성화 함수는?             | Swish 함수                              |
| 7  | EfficientNet은 몇 층으로 구성돼 있나요?             | 버전마다 다름. B0는 약 18~20층, B7은 훨씬 깊음      |

---

## 5. 🔍 기타 주요 포인트

* **확장 버전**:

  * B0 (Baseline), B1 ~ B7로 점차 크기 확장
  * 이후 **EfficientNetV2** 등장 (더 빠른 학습, 더 높은 정확도)
* **적용 분야**:

  * 이미지 분류, 객체 탐지, 세분화 등 거의 모든 컴퓨터 비전 분야

---

## 6. 🧩 요약

> EfficientNet = 효율적 구조 (Depthwise, SE Block, Swish) + 균형 잡힌 스케일링 (Compound Scaling)

이 두 가지 요소가 결합되어 높은 정확도와 적은 연산량을 동시에 달성한 모델입니다.

---


