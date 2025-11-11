

---

# 🧠 Semantic Segmentation Transformer 계열 정리

(SETR → SegFormer)

---

## 🧩 1️⃣ SETR (2021)

> **Transformer를 Semantic Segmentation에 최초로 적용한 모델**

---

### 💡 핵심 아이디어

* 기존 CNN 기반 segmentation(예: FCN, U-Net)의 **국소적(Local)** 한 한계를 극복하고자
  **Transformer의 전역적(Self-Attention) 표현력**을 도입.
* 즉, 이미지를 **패치 단위로 나누어 Transformer로 문맥 관계를 학습**.

---

### ⚙️ 구조 개요

```
[입력 이미지]
   ↓
[Encoder: ViT]
   ↓
[Decoder: SETR-Naive / PUP / MLA]
   ↓
[Segmentation Mask]
```

---

### 🧠 Encoder (ViT 기반)

* **Vision Transformer(ViT)** 를 그대로 사용
* 이미지를 일정 크기의 **Patch 단위**로 나누고,
  이를 **토큰(token)** 으로 변환 후 Transformer Encoder에 입력
* **전역 문맥(Global Context)** 을 학습
* CNN처럼 해상도를 점차 줄이지 않기 때문에 **모든 픽셀 간 관계를 직접 학습**

📌 **장점:**

* 이미지 전역 정보를 효과적으로 학습

⚠️ **단점:**

* ViT 구조 그대로 사용 → **파라미터 수 많음**
* 해상도를 줄이지 않아 **연산량이 매우 많음**

---

### 🧩 Decoder (3가지 변형 제안)

| 이름             | 방식                      | 특징                            |
| -------------- | ----------------------- | ----------------------------- |
| **SETR-Naive** | 단순한 Upsampling          | 구조 단순하지만 정보 손실 발생             |
| **SETR-PUP**   | Progressive Upsampling  | 단계적으로 해상도를 복원해 더 세밀한 복원       |
| **SETR-MLA**   | Multi-Level Aggregation | ViT의 여러 레이어 출력을 결합하여 경계 복원 향상 |

---

### 📘 요약

| 항목          | 설명                       |
| ----------- | ------------------------ |
| **목표**      | Transformer로 픽셀 단위 분할 수행 |
| **Encoder** | ViT 그대로 사용 (전역 정보 학습)    |
| **Decoder** | Naive / PUP / MLA 구조 제안  |
| **장점**      | 전역적 문맥 이해 우수             |
| **단점**      | 파라미터 많고, 연산 복잡도 높음       |

---

## ⚡ 2️⃣ SegFormer (2021, NVIDIA)

> **SETR의 연산 비효율성과 무거운 구조를 개선한 경량 Transformer Segmentation 모델**

---

### 💡 핵심 아이디어

* “**가볍고 빠르면서도 정확한**” Transformer 기반 Segmentation 모델을 만들자.
* ViT처럼 단일 스케일이 아닌, **CNN처럼 계층적(Hierarchical)** 구조로 feature를 추출.

---

### ⚙️ 구조 개요

```
[입력 이미지]
   ↓
[Encoder: Hierarchical Transformer]
   ↓
[Decoder: Lightweight MLP Head]
   ↓
[Segmentation Mask]
```

---

### 🧠 Encoder (Hierarchical Transformer)

| 구성 요소                                | 설명                                          |
| ------------------------------------ | ------------------------------------------- |
| **Hierarchical Transformer Block**   | ViT와 달리, 해상도를 단계적으로 줄이면서 여러 스케일의 feature 추출 |
| **Overlap Patch Merging**            | 패치를 겹치게 나눠서, 주변 문맥(Local continuity)을 유지    |
| **Efficient Self-Attention**         | 연산량을 줄인 효율적 Attention 메커니즘                  |
| **Mix-FFN (Positional Encoding 대체)** | 위치 정보를 별도 인코딩하지 않고 MLP를 통해 내재적으로 학습         |

📘 **결과:**
→ 연산 효율 극대화 + 전역·지역 정보 모두 보존

---

### 🧩 Decoder (Lightweight MLP Head)

* 복잡한 디코더 대신 **단순한 MLP Layer만 사용**
* Encoder의 4단계 feature map을 받아
  각각을 MLP로 통일된 크기로 맞춘 뒤 결합하여 segmentation mask 생성
* 연산량이 매우 적고, 학습도 안정적

📘 **핵심 장점:**

* **가벼움 (Lightweight)**
* **빠름 (Fast)**
* **성능 유지 (Accurate)**

---

### 📘 요약

| 항목          | 설명                                           |
| ----------- | -------------------------------------------- |
| **목표**      | SETR의 비효율성 개선 (가벼운 Transformer Segmentation) |
| **Encoder** | Hierarchical 구조 + Efficient Attention        |
| **Decoder** | 단순 MLP Head (비교적 가벼움)                        |
| **특징**      | Overlap Patch + Mix-FFN으로 성능 향상              |
| **장점**      | 빠르고 정확, 실무/연구 모두 베이스라인으로 자주 사용               |
| **단점**      | 세밀한 경계 복원은 CNN 대비 다소 약함                      |

---

## 🔍 3️⃣ SETR vs SegFormer 비교표

| 구분                      | **SETR**          | **SegFormer**                       |
| ----------------------- | ----------------- | ----------------------------------- |
| **등장 시기**               | 2021 초반           | 2021 후반 (NVIDIA)                    |
| **기반 구조**               | ViT (Flat)        | Hierarchical Transformer            |
| **Encoder**             | ViT 그대로 사용        | Overlap Patch + Efficient Attention |
| **Decoder**             | Naive / PUP / MLA | Lightweight MLP                     |
| **Positional Encoding** | 사용함               | Mix-FFN으로 대체                        |
| **Feature 처리 방식**       | 단일 해상도            | 다중 스케일 (Multi-scale)                |
| **연산 효율**               | 매우 무거움            | 매우 효율적                              |
| **활용도**                 | 연구 중심             | 실무 중심 (베이스라인 다수 사용)                 |

---

## ✅ 한 줄 요약

> **SETR**는 “Transformer를 Segmentation에 처음 적용한 시도”이고,
> **SegFormer**는 “그 구조를 실용적으로 개선해 가볍고 빠르게 만든 모델”입니다.

---

