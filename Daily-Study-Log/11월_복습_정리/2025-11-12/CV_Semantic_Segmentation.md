

---

# 🎨 Semantic Segmentation 정리

---

## 🧠 1. 개념 정의

> **Semantic Segmentation**은 이미지의 **모든 픽셀마다 클래스(Label)** 를 예측하는 작업입니다.

즉,
이미지의 **각 픽셀 단위로 "이 픽셀이 무엇인지"를 분류**하는 것이 목표예요.

📘 예시

* 고양이 사진에서
  → 고양이 부분의 픽셀 = “cat”
  → 배경 부분의 픽셀 = “background”

결과적으로, **클래스 레이블만으로 구성된 “출력 이미지(mask)”** 를 생성합니다.

---

## ⚙️ 2. 해상도 복원을 위한 방법들

Segmentation에서는 **인코딩(축소)** 후 **디코딩(복원)** 과정이 필요합니다.
즉, feature map을 점점 **크게(upsampling)** 만들어 원래 이미지 크기로 돌려야 하죠.

이를 위한 대표적인 방법들이 아래 세 가지예요 👇

---

### 🧩 **1️⃣ Transposed Convolution**

> Convolution의 역방향 연산을 통해 feature map 크기를 키우는 방법.

* `Deconvolution`이라고도 부름
* 커널이 **학습 가능(learnable)** 하다는 점이 핵심
* 단순한 확대가 아니라, **학습을 통해 복원 과정 자체를 최적화**

📘 예시:
U-Net, FCN 등에서 디코더 단계에 자주 사용

---

### 🧩 **2️⃣ Upsampling**

> 단순히 이미지를 “크게 늘리는” 연산 (학습되지 않음)

* 보통 **Interpolation(보간)** 기법을 사용

  * 최근접 이웃 (Nearest Neighbor)
  * 쌍선형 (Bilinear)
  * 쌍삼차 (Bicubic)
* 계산은 간단하지만, **학습으로 최적화되지 않음**

📘 예시:
FCN의 마지막 단계나 Feature Pyramid 구조 등에서 사용

---

### 🧩 **3️⃣ Unpooling**

> Pooling으로 줄어든 해상도를 다시 키우는 과정

* **Pooling**: max pooling, average pooling 등으로 이미지 해상도 ↓
* **Unpooling**: 디코딩 시 **잃어버린 위치 정보를 복원하며 해상도 ↑**
* Max Pooling에서 “어디가 최댓값이었는지” 인덱스를 저장해 두었다가
  Unpooling 시 그 위치에 다시 값을 복원하는 식으로 구현 가능

📘 예시:
SegNet 구조 등에서 사용

---

## 🧩 3. Dilated Convolution (팽창 합성곱)

> Convolution 연산 시 **커널 원소 간 간격을 넓혀서** 더 넓은 범위를 보는 방법.

* 간격 크기를 **Dilation Rate** 로 정의
* Dilation Rate를 키우면,
  → **커널이 커버하는 영역(Receptive Field)** 이 넓어짐
* 해상도를 줄이지 않으면서
  **넓은 문맥(Context)** 정보를 얻을 수 있음

📘 장점:

* 이미지의 전역 정보와 지역 정보를 동시에 학습 가능
* 특히 **고해상도 이미지의 Segmentation**에 적합

📘 예시:
DeepLab 시리즈(DeepLabV2~V3+)에서 핵심적으로 사용됨

---

## 🧠 4. FCN (Fully Convolutional Network)

> **Segmentation을 위한 최초의 End-to-End 구조**
> 완전연결층(FC Layer)을 없애고, **Convolution + Upsampling만으로**
> 픽셀 단위 예측을 수행한 모델이에요.

---

### ⚙️ 핵심 아이디어

* 기존 CNN 분류 모델은 마지막에 **Fully Connected Layer** 로 클래스 하나만 예측함
* FCN은 이를 없애고, **모든 층을 Convolution으로 구성**
* 마지막 feature map을 **Upsampling (Deconvolution)** 해서
  입력 이미지 크기로 복원 → **픽셀 단위 출력** 생성

---

### 🧩 구조 요약

```
입력 이미지
   ↓
[Encoder: Convolution + Pooling]
   ↓
[Decoder: Transposed Convolution (Upsampling)]
   ↓
[Pixel-wise Classification]
```

---

### 🎯 특징 요약

| 항목                        | 설명                             |
| ------------------------- | ------------------------------ |
| **핵심 구조**                 | Conv + Upsampling만 사용          |
| **Fully Connected 제거 이유** | 위치 정보 손실 방지                    |
| **출력 형태**                 | 각 픽셀의 클래스 확률 맵                 |
| **의의**                    | 최초의 End-to-End Segmentation 구조 |

---

## 🧾 5. 전체 요약표

| 구분                        | 설명                             | 특징                    |
| ------------------------- | ------------------------------ | --------------------- |
| **Semantic Segmentation** | 이미지의 각 픽셀을 클래스 단위로 분류          | 출력은 “클래스 맵”           |
| **Transposed Conv**       | 학습 가능한 커널로 해상도 복원              | Upsampling보다 정교함      |
| **Upsampling**            | Interpolation으로 크기 확대          | 빠르지만 학습 불가            |
| **Unpooling**             | Pooling의 역과정                   | 위치 정보 복원              |
| **Dilated Conv**          | 커널 간격 확대, receptive field 확장   | 고해상도 segmentation에 적합 |
| **FCN**                   | 최초의 End-to-End Segmentation 구조 | Fully Connected 제거    |

---

