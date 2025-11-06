

---

# 🧠 U-Net (유넷)

## 📘 개념

* **Semantic Segmentation**(픽셀 단위 분할)에 특화된 **Fully Convolutional Network 구조**
* 2015년 **의료 영상 분할(Medical Image Segmentation)** 논문 *“U-Net: Convolutional Networks for Biomedical Image Segmentation”* 에서 처음 제안됨
* 이름처럼 구조가 **U 모양**이어서 U-Net이라 부름
  (왼쪽은 Encoder, 오른쪽은 Decoder)

---

## 🧩 구조 개요

```
입력
  ↓
[Encoder 1] ────────────────┐
  ↓                        │
[Encoder 2] ────────────┐   │
  ↓                    │   │
[Encoder 3] ────────┐   │   │
  ↓                │   │   │
[Encoder 4] ───┐    │   │   │
  ↓             │   │   │   │
[Bottleneck]    │   │   │   │
  ↓              ↓   ↓   ↓   ↓
[Decoder 4] ← concat(Enc4)
  ↓
[Decoder 3] ← concat(Enc3)
  ↓
[Decoder 2] ← concat(Enc2)
  ↓
[Decoder 1] ← concat(Enc1)
  ↓
[1×1 Conv → Segmentation Map]
```

---

## ⚙️ 1. Encoder (Contracting Path)

| 단계                                                        | 역할                                      |
| --------------------------------------------------------- | --------------------------------------- |
| 🔹 **Conv(3×3) → ReLU → Conv(3×3) → ReLU → MaxPool(2×2)** | 특징 추출 및 공간 축소                           |
| 🔹 **Downsampling**                                       | 이미지 크기를 절반씩 줄이며 feature 의미(semantic) 강화 |
| 🔹 **채널 수 증가**                                            | 깊을수록 더 복잡한 특징 학습                        |

---

## ⚙️ 2. Decoder (Expanding Path)

| 단계                                | 역할                                         |
| --------------------------------- | ------------------------------------------ |
| 🔹 **Upsampling (Deconvolution)** | 해상도 복원 (`ConvTranspose2d` 또는 `Upsample×2`) |
| 🔹 **Skip Connection**            | 같은 단계의 Encoder feature와 **concat** (경계 복원) |
| 🔹 **Conv(3×3) × 2**              | 합쳐진 feature 정제 및 잡음 제거                     |

> Decoder는 Encoder의 축소 정보를 받아,
> **픽셀 단위 세밀한 위치 복원**과 **경계선 정교화**를 담당함.

---

## ⚙️ 3. 마지막 출력층 (Head)

| 항목                       | 설명                                                |
| ------------------------ | ------------------------------------------------- |
| `Conv(1×1)`              | 채널 수를 클래스 개수로 변환                                  |
| Binary Segmentation      | 출력 채널 1개 → `BCEWithLogitsLoss`, 추론 시 `sigmoid`    |
| Multi-class Segmentation | 출력 채널 = 클래스 수 → `CrossEntropyLoss`, 추론 시 `argmax` |

---

## 🧱 핵심 개념 요약

| 항목           | 설명                                      |
| ------------ | --------------------------------------- |
| **U-Net 구조** | Encoder + Decoder + Skip Connection     |
| **핵심 아이디어**  | Low-level(위치 정보) + High-level(의미 정보) 결합 |
| **출력 크기**    | 입력 이미지와 동일                              |
| **장점**       | 적은 데이터로도 높은 정확도, 경계 인식 우수               |
| **대표 분야**    | 의료 영상, 街 지도 라벨링, 위성 이미지 분할 등            |

---

## 🧠 변형 모델 (Variants)

| 모델                  | 특징                                    |
| ------------------- | ------------------------------------- |
| **U-Net++**         | Skip 연결을 Dense하게 확장 (중간 계층 보정)        |
| **Attention U-Net** | Skip에 Attention Gate 추가, 의미 있는 위치만 강조 |
| **ResUNet**         | Conv 블록을 Residual 구조로 바꿔 학습 안정화       |
| **3D U-Net**        | 3D 입력(CT, MRI 등) 처리용 확장 버전            |

---

## 🚀 실무 팁

* 입력 크기는 **2ⁿ 단위 (256, 512)** 권장 — 업/다운 정렬 편리
* Binary segmentation은 `Dice loss + BCEWithLogitsLoss` 조합 자주 사용
* 작은 객체 많은 데이터 → **random crop, elastic transform** 효과적
* Feature map 크기 불일치 시 `Center Crop` or `Padding` 사용

---

