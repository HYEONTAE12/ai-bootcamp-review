

---

## 🧩 1️⃣ Skip Connection이 등장한 이유

CNN의 Encoder(인코더)는 **Downsampling**을 반복하면서
“무엇(semantic)”은 잘 학습하지만,
“어디(spatial)” — 즉 **정확한 위치 정보**는 잃게 됩니다.

예를 들어,

* 눈, 코, 입이 있다는 건 알아도
* 눈의 **정확한 위치**나 **경계선**은 모르게 되는 거죠.

그래서 Segmentation처럼 “픽셀 단위 위치 예측”이 필요한 작업에서는
이 손실된 위치 정보를 복구해줘야 합니다.
그 역할을 하는 게 바로 👉 **Skip Connection**입니다.

---

## 🧱 2️⃣ 구조적 개념 (Encoder–Decoder 사이의 연결)

Skip Connection은

> **Encoder의 feature map을 Decoder 쪽으로 직접 전달(연결)**하는 구조입니다.

즉,

* Encoder 초반부(해상도 높고 위치 정보 풍부)에서 나온 feature를
* Decoder 후반부(업샘플링 중인 부분)로 **건너뛰어 연결(skip)** 시킵니다.

이걸 그림으로 표현하면 아래와 같아요:

```
입력 이미지
   ↓
 [Encoder]
   ↓
 ──────┐
       │ (Skip Connection)
       ↓
 [Decoder]
   ↓
 출력 (Segmentation Mask)
```

---

## ⚙️ 3️⃣ Skip Connection의 작동 방식

U-Net을 예시로 들어볼게요.

### (1) Encoder

* 여러 번 Conv + Pool 반복 → feature map 해상도 점점 작아짐
* 이때 각 단계의 feature map을 **저장**해둡니다.

  * 예: pool1, pool2, pool3 …

### (2) Decoder (Upsampling 단계)

* Upsampling으로 feature map 해상도를 키움
* 같은 단계의 Encoder feature map과 **Concatenate(연결)** 또는 **Add(덧셈)**

즉,
`Decoder Feature + Encoder Feature → 더 풍부한 정보`

| 연산 방식    | 설명                                      |
| -------- | --------------------------------------- |
| `Concat` | 채널 방향으로 이어붙임 (U-Net 방식)                 |
| `Add`    | 같은 크기의 feature끼리 더함 (ResNet, DeepLab 등) |

---

## 🧠 4️⃣ 왜 중요한가?

| 구분              | Encoder만 있을 때 | Skip Connection 있을 때 |
| --------------- | ------------- | -------------------- |
| 해상도             | 낮음            | 높음                   |
| 경계 복원           | 흐림            | 선명                   |
| 위치 정보           | 손실            | 복구                   |
| 의미 정보           | 풍부            | 유지                   |
| 최종 Segmentation | 거칠고 번짐        | 정확하고 경계 뚜렷           |

즉, Skip Connection은
**고수준 의미(feature)**와 **저수준 위치(feature)**를 **결합**해서
정확한 픽셀 단위 예측이 가능하게 만드는 핵심 장치입니다.

---

## 🔍 5️⃣ 수식으로 보면

예를 들어 Decoder의 업샘플된 feature를 `F_d`,
Encoder의 같은 해상도 feature를 `F_e`라 하면,

* 단순 덧셈 방식:
  [
  F_{out} = F_d + F_e
  ]

* Concatenate 방식:
  [
  F_{out} = \text{Concat}(F_d, F_e)
  ]

그 뒤 다시 Convolution을 통과하면서 두 feature를 융합합니다.
이 과정이 픽셀 경계나 세부 구조 복원에 큰 도움이 됩니다.

---

## 🚀 6️⃣ Skip Connection이 쓰이는 대표 구조

| 모델             | 연결 방식  | 특징                          |
| -------------- | ------ | --------------------------- |
| **U-Net**      | Concat | 가장 대표적, 경계 복원 강점            |
| **FCN-8s**     | Add    | 중간 feature(p3, p4)를 결합      |
| **ResNet**     | Add    | Gradient vanishing 방지용 skip |
| **DeepLabV3+** | Concat | 저해상도 context + 고해상도 edge 결합 |

---

## 📌 정리

> **Skip Connection은**
> Downsampling 과정에서 잃은 **공간적(위치) 정보**를
> Encoder의 저수준 feature로부터 복원하기 위해
> Decoder로 직접 전달하는 연결 구조입니다.

즉,

* "무엇"은 깊은 층이 주고,
* "어디"는 얕은 층이 보완하며,
* 둘이 합쳐져 “정확한 픽셀 예측”이 가능해집니다. ✅

---
