
---

# 🧠 Semantic Segmentation (의미론적 분할)

## 📘 개념

* 이미지의 **모든 픽셀 단위로 클래스(class)를 예측**하는 컴퓨터 비전(Task).
* 즉, 이미지 내의 **각 픽셀(pixel)이 어떤 객체에 속하는지**를 분류하는 것.

> 🪄 예시:
>
> * 고양이 사진 → “고양이(1)”, “배경(0)”
> * 자율주행 → “도로, 차량, 사람, 신호등” 등 각 픽셀을 태깅

---

## 🧩 특징

| 구분        | 내용                                  |
| --------- | ----------------------------------- |
| **목표 단위** | 이미지의 개별 **픽셀(Pixel)**               |
| **출력 형태** | 입력 이미지와 같은 크기의 **Segmentation Map** |
| **결과**    | 각 픽셀마다 클래스 ID가 지정된 **마스크 이미지**      |
| **활용 분야** | 자율주행, 의료 영상 분석, 위성 이미지, 배경 제거 등     |

---

## ⚙️ 작동 원리

### 1️⃣ Feature Extraction (특징 추출)

* CNN(Convolutional Neural Network)을 사용해 이미지에서 **고수준 특징(feature)** 추출
* 보통 **Downsampling (Pooling)** 을 통해 공간 크기를 줄이고 의미적 정보를 강화

### 2️⃣ Pixel-wise Classification (픽셀별 예측)

* 마지막에 **각 픽셀에 대한 클래스 확률을 계산**
* 입력 크기와 동일한 크기로 복원해야 하므로 **Upsampling** 단계가 필요

---

## 🔍 Sliding Window 방식

* 이미지를 작은 **윈도우(window)** 단위로 잘라서
  **각 윈도우마다 분류(Classification)** 를 수행하는 초기 방식

| 특징    | 설명                                |
| ----- | --------------------------------- |
| ✅ 장점  | 단순 구조, 기존 CNN을 그대로 활용 가능          |
| ⚠️ 단점 | 계산량이 많고, **중복 연산** 발생 → 속도가 매우 느림 |
| 💡 개선 | FCN, U-Net 등의 등장으로 대체됨            |

---

## 🧱 FCN (Fully Convolutional Network)

### 📘 개념

* CNN의 **완전연결층(FC Layer)** 을 모두 제거하고
  오직 **Convolution 연산만으로 구성된 네트워크**

> 즉, 이미지 입력 크기에 관계없이
> **픽셀 단위의 예측을 직접 수행할 수 있는 구조**

### ⚙️ 핵심 아이디어

* 기존 CNN의 출력(feature map)을
  **Deconvolution(Transpose Convolution)** 을 통해 **업샘플링(Up-sampling)**
* 입력 이미지와 동일한 크기의 **Segmentation Map** 복원

### 🧩 구조 개요

1. **인코더(Encoder)**: 일반 CNN처럼 특징 추출 (VGG, ResNet 등)
2. **디코더(Decoder)**: Deconvolution으로 공간 정보를 복원

---

## 🔄 Deconvolution (Transpose Convolution)

### 📘 개념

* **Feature map을 확장(Upsampling)** 하여
  원본 이미지 크기와 동일한 Segmentation Map 생성

```python
# PyTorch 예시
import torch.nn as nn
up = nn.ConvTranspose2d(in_channels=256, out_channels=128, kernel_size=4, stride=2, padding=1)
```

| 용어                | 설명                                     |
| ----------------- | -------------------------------------- |
| **Convolution**   | 입력 → Feature Map (Downsampling 효과)     |
| **Deconvolution** | Feature Map → 원본 크기 복원 (Upsampling 효과) |

> FCN, U-Net, SegNet, DeepLab 등 대부분의 모델이
> 이 **Deconvolution 기반 복원 구조**를 사용함.

---

## 🧾 요약 정리

| 항목          | 설명                                 |
| ----------- | ---------------------------------- |
| **Task 이름** | Semantic Segmentation              |
| **목표**      | 이미지 내 **각 픽셀을 클래스 단위로 분류**         |
| **출력 형태**   | Segmentation Map (입력과 동일한 크기)      |
| **핵심 구조**   | Encoder + Decoder (FCN, U-Net 등)   |
| **핵심 연산**   | Convolution / Deconvolution        |
| **과거 방식**   | Sliding Window (비효율적, 현재는 거의 사용 X) |

---

