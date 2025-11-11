

---

## 🧠 1️⃣ FCN이 등장한 배경

CNN은 원래 **Classification** 용도로 만들어졌습니다.

* 입력: 이미지 전체
* 출력: “고양이다” / “사람이다” 같은 **하나의 클래스 값**

하지만 **Segmentation**은 다릅니다.

* 입력: 이미지 전체
* 출력: **픽셀마다 클래스** (즉, 이미지 크기만큼의 출력이 필요)

문제는 일반 CNN의 마지막 단계가 **Fully Connected Layer(완전연결층)**이라서
출력 크기가 고정되어 있다는 거예요.
→ 픽셀 단위의 위치 정보가 날아감.
→ 즉, "무엇"은 알아도 "어디"는 모름.

그래서 나온 아이디어가 바로 **Fully Convolutional Network (FCN)**.

---

## 🧩 2️⃣ 핵심 개념 — “완전연결층을 제거하고, Conv로만 구성”

FCN은 이름 그대로 **모든 층을 Convolution으로만 구성**합니다.

> Fully Connected Layer ❌
> Fully Convolutional ✅

즉,

* 기존 CNN의 마지막 `Dense(FC)` 레이어를
  `1×1 Convolution`으로 바꿔서
  **공간 정보를 유지한 채 class score map을 생성**합니다.

이렇게 하면 입력 이미지 크기가 달라도
출력 feature map의 크기가 유연하게 변할 수 있어요.

---

## 🧩 3️⃣ 구조 요약

FCN은 크게 **Encoder–Decoder 구조**로 나뉩니다.

### (1) Encoder — 특징 추출

* 일반 CNN (VGG16, ResNet 등)을 사용
* Downsampling (stride, pooling)으로 **의미(semantic)**를 추출
* 하지만 해상도는 줄어듦 (위치 정보 손실)

### (2) Decoder — 해상도 복원

* Upsampling (보통 Deconvolution / Transposed Convolution 사용)
* 해상도를 원래 이미지 크기로 복원
* 각 픽셀마다 클래스 확률을 예측 → **Segmentation Map**

---

## 🧩 4️⃣ FCN의 세부 버전들

| 모델          | 설명                                             |
| ----------- | ---------------------------------------------- |
| **FCN-32s** | 마지막 feature map을 한 번에 32배 upsampling (해상도 낮음)  |
| **FCN-16s** | 중간 feature map (pool4)와 결합 후 upsampling (더 정밀) |
| **FCN-8s**  | pool3, pool4와 결합 → 해상도 가장 높음                   |

즉, **“Skip Connection”**을 통해
얕은 층(위치 정보 풍부) + 깊은 층(의미 정보 풍부)을 결합해서
정확한 경계를 얻는 방식이에요.

→ 이 개념이 나중에 **U-Net** 구조로 발전합니다.

---

## 🧩 5️⃣ FCN의 결과 예시 (이미지 흐름)

```
입력 이미지  →  Conv + Pool 반복 (downsampling)
            ↓
        Feature Map (7×7)
            ↓
        1×1 Conv (class별 score)
            ↓
        Upsampling (Transposed Conv)
            ↓
        Output (원본 크기의 segmentation mask)
```

---

## 📊 6️⃣ FCN의 장단점

| 구분    | 내용                                                                                                 |
| ----- | -------------------------------------------------------------------------------------------------- |
| ✅ 장점  | - end-to-end 학습 가능<br>- FC layer 제거로 어떤 크기의 이미지도 처리 가능<br>- Classification → Segmentation 자연스럽게 확장 |
| ⚠️ 단점 | - Downsampling으로 해상도 손실<br>- 경계 부분이 흐릿하게 예측됨<br>- 세밀한 구조 복원이 어려움                                   |

→ 그래서 이후 모델(U-Net, DeepLabV3+)이
**Skip Connection**과 **Dilated Conv**를 도입해서 이 약점을 보완했어요.

---

## 🔎 정리 한 줄로 요약

> **FCN은 Fully Connected Layer를 없애고, Convolution과 Upsampling만으로
> 픽셀 단위 예측을 가능하게 만든 최초의 End-to-End Segmentation 구조입니다.**

---

