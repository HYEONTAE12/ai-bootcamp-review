

---

# 🧭 2-Stage Detector

## 📘 정의

> **2-Stage Detector**는 객체 탐지를 두 단계로 나누어 수행하는 방식입니다.
> 1️⃣ **객체가 있을 법한 후보 영역(Region Proposal)** 을 먼저 찾고,
> 2️⃣ 그 후보 영역들을 **분류(Classification) + 위치 보정(Regression)** 하는 구조입니다.

---

## 🧩 **Stage 1: Region Proposal**

* 이미지 전체를 탐색하지 않고, **객체가 있을 법한 후보 영역(ROI)** 을 먼저 생성
* R-CNN에서는 **Selective Search**,
  Faster R-CNN에서는 **RPN(Region Proposal Network)** 으로 대체됨

---

## 🧩 **Stage 2: Classification & Bounding Box Regression**

* Stage 1에서 얻은 ROI들을 입력으로 받아
  각 영역이 어떤 클래스인지 분류하고,
  Bounding Box 좌표를 더 정확히 조정함

---

## ⚙️ R-CNN Pipeline (2-Stage 구조의 시작점)

1. **Input Image**
   → 원본 이미지를 입력받음

2. **Region Proposal (Selective Search)**
   → 약 **2000개**의 후보 영역 추출
   → 색상, 질감, 경계선을 기준으로 비슷한 영역을 묶어 생성

3. **Crop & Resize**
   → 각 후보 영역을 **224×224** 크기로 맞춤 (CNN 입력 크기 통일)

4. **Feature Extraction (CNN)**
   → 각 ROI를 **CNN(AlexNet)** 에 통과시켜 **특징 벡터(feature vector)** 추출

5. **Classification (SVM)**
   → 특징 벡터를 **클래스별 SVM**에 입력해 객체 종류 예측
   → 배경인지 여부도 판별

6. **Bounding Box Regression**
   → 박스 위치를 세밀하게 조정 (좌표 보정)

---

### 🧩 **정리 흐름**

> `Input Image → Region Proposal → Crop & Resize → CNN → SVM Classifier → Bounding Box Regression`

---

## ❌ R-CNN의 단점

| 구분        | 문제점   | 설명                                 |
| --------- | ----- | ---------------------------------- |
| **연산량**   | 매우 큼  | 약 2000개의 ROI 각각에 CNN 수행 → 비효율적     |
| **속도**    | 매우 느림 | 이미지 한 장당 수 초 이상 소요                 |
| **학습 구조** | 복잡    | CNN, SVM, BBox Regressor를 각각 따로 학습 |
| **크기 보정** | 정보 손실 | 모든 ROI를 강제로 224×224로 Resize        |

---

## 🚀 이후 발전

| 모델                      | 주요 개선점                                  | 특징                |
| ----------------------- | --------------------------------------- | ----------------- |
| **Fast R-CNN (2015)**   | 한 번만 CNN을 수행 후 ROI Pooling으로 각 영역 특징 추출 | 속도 ↑, 연산 중복 제거    |
| **Faster R-CNN (2016)** | Region Proposal 단계까지 CNN으로 학습 (RPN 도입)  | 완전한 End-to-End 구조 |

---

## 💡 요약

| 구분                   | 내용                                                       |
| -------------------- | -------------------------------------------------------- |
| **2-Stage Detector** | “Region Proposal → Classification & Regression”의 두 단계 구조 |
| **대표 모델**            | R-CNN, Fast R-CNN, Faster R-CNN                          |
| **장점**               | 정확도 높음 (정교한 탐색)                                          |
| **단점**               | 속도 느림 (실시간 어려움)                                          |
| **대표 개선 방향**         | One-Stage Detector (YOLO, SSD 등)로 발전                     |

---

.
