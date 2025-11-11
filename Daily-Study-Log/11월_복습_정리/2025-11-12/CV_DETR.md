

---

# 🚀 DETR (DEtection TRansformer)

> **DETR**은 “Object Detection(객체 탐지)”에 **Transformer 구조**를 직접 적용한 모델이에요.
> 즉, CNN 기반의 anchor box 중심 탐지 방식을 버리고,
> **"직접적으로(set-based) 객체를 예측하는" 새로운 접근**을 제시했습니다.

---

## 🧠 1. 기존 방식의 한계

기존의 **Faster R-CNN, YOLO** 등은 사람이 **anchor box**(객체 후보 박스)를 미리 정의해야 했어요.
하지만 이 방식에는 다음과 같은 문제가 있었죠 👇

| 한계점            | 설명                                                      |
| -------------- | ------------------------------------------------------- |
| **사람의 개입이 많음** | anchor 크기, 비율을 사람이 정함 → 설계자의 bias가 성능에 큰 영향             |
| **중복 예측 문제**   | 비슷한 위치에 여러 박스가 예측되어 **NMS(Non-Maximum Suppression)** 필요 |
| **전역 정보 부족**   | CNN은 지역적(Local) 특징에 집중해서, 전체 맥락 관계를 파악하기 어려움            |

---

## 💡 2. DETR의 핵심 아이디어

> **Set-based direct prediction**
> → 사람이 정한 anchor box 없이,
> → 모델이 **“이 이미지에는 N개의 객체가 있다”** 를 직접 예측.

즉,
**“객체 탐지를 순서가 없는 집합(set) 예측 문제로 본다”** 는 발상이에요.

---

## ⚙️ 3. DETR 전체 파이프라인

```
이미지 입력
   ↓
CNN (Backbone: ResNet 등)
   ↓
Transformer Encoder
   ↓
Transformer Decoder + Object Query
   ↓
Prediction Head (Class + BBox)
```

---

### 🧩 **Encoder**

* 입력 이미지의 feature map을 Transformer Encoder에 전달.
* **Self-Attention** 을 통해 **모든 픽셀 간의 관계를 학습**함.
* CNN과 달리 **전역 정보(Global Context)** 를 고려해
  물체 간의 **위치, 관계, 상호작용**까지 학습.

📌 **요약:**

> CNN의 "지역적인 시야" 한계를 넘어,
> 이미지를 전체적으로 이해할 수 있게 함.

---

### 🧩 **Decoder**

* 학습 가능한 **Object Query** 들을 입력으로 받음.
* 각 Query는 “하나의 객체를 담당”하도록 학습됨.
* Encoder의 출력(feature map)과 cross-attention을 수행하여
  각 Query가 어떤 객체를 예측할지 결정함.

📌 **Decoder Output**
→ 각 Query별 예측 결과 (`class`, `bbox`) 가 나옴
→ 즉, 총 N개의 Query → N개의 예측 세트

---

### 🎯 **Prediction Head**

* **Classification Head**:
  각 Query가 어떤 클래스에 속하는지 예측 (object / background 포함)
* **Bounding Box Head**:
  각 Query가 담당하는 객체의 위치(x, y, w, h)를 예측

---

## 🔢 4. Hungarian Matching (헝가리안 알고리즘)

DETR의 가장 독특한 부분이에요.

> 모델이 예측한 N개의 box와 실제 정답(ground truth) box를
> **“최적의 1:1 매칭”** 으로 연결해주는 알고리즘이에요.

* 각 예측과 정답 간의 **비용(cost)** 을 계산
* **가장 낮은 전체 비용 조합**을 선택 → 매칭 결정

📌 이 과정 덕분에:

* 중복 예측 제거 (NMS 불필요)
* 예측 결과를 “집합(set)”으로 다룰 수 있음

---

## ⚖️ 5. Loss Function (손실 함수)

단순히 `L1 Loss`만 쓰면, 박스 크기가 다를 때 차이가 크게 나서 학습이 불안정해요.
그래서 **L1 Loss + GIoU(Generalized IoU)** 를 함께 사용합니다.

| 구성                      | 설명                                     |
| ----------------------- | -------------------------------------- |
| **Classification Loss** | 각 Query의 클래스 예측 정확도 계산 (Cross Entropy) |
| **L1 Loss**             | 예측된 bbox 좌표와 실제 좌표 차이                  |
| **GIoU Loss**           | 두 박스가 겹치는 정도(면적 차이)까지 고려하는 손실          |

📘 **최종 BBox Loss**
[
\text{Loss}_{bbox} = \lambda_1 \cdot L1 + \lambda_2 \cdot GIoU
]

---

## 🧩 6. DETR의 장점과 단점

| 구분        | 내용                                                          |
| --------- | ----------------------------------------------------------- |
| ✅ **장점**  | - Anchor box, NMS 제거 (설계 단순화)<br>- 전역 정보 활용으로 물체 간 관계 학습 가능 |
| ⚠️ **단점** | - 학습 수렴이 느림 (많은 데이터 필요)<br>- 작은 물체 탐지에 상대적으로 약함             |

---

## 🔍 7. 한 줄 요약

> **DETR**은 **Object Detection을 “집합 예측(Set Prediction)”으로 재정의**한 모델이며,
> **Transformer의 전역적 Attention**으로 **CNN의 한계를 극복**했다.

---


