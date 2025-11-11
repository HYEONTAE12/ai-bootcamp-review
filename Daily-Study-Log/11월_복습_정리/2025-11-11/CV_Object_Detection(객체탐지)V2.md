
---

# 🧭 Object Detection (객체 탐지)

## 📘 정의

> **Object Detection**은
> 이미지 또는 영상 안에서 **여러 객체의 위치(Location)**를 **Bounding Box(경계 상자)**로 찾고,
> 동시에 각 객체가 어떤 **클래스(Class)**인지 **분류(Classification)**하는 기술입니다.

즉,
👉 “**무엇이(where)** + **어디에(what)** 있는가”를 동시에 예측하는 문제입니다.

---

## 🧩 주요 개념 정리

### 🔹 1. Bounding Box (경계 상자)

* 객체의 외곽을 감싸는 **최소 크기의 사각형 영역**

* 보통 4개의 좌표 값으로 표현됨
  [
  (x_{min}, y_{min}, x_{max}, y_{max})
  ]
  또는
  [
  (x_{center}, y_{center}, width, height)
  ]

* 예시:

  ```json
  { "class": "cat", "bbox": [34, 58, 210, 190] }
  ```

* 한 이미지 안에 여러 개의 bounding box가 존재할 수 있습니다.

---

### 🔹 2. Annotation (어노테이션)

* **Object Detection 학습용 데이터의 핵심 구성요소**
* 사람이 직접 이미지 내 객체의 위치를 박스로 표시하고,
  그 박스에 **객체의 클래스 라벨(class label)**을 붙이는 과정입니다.
* 이렇게 생성된 라벨 정보를 **모델 학습에 사용**합니다.

📘 예시 (VOC 포맷):

```xml
<object>
  <name>dog</name>
  <bndbox>
    <xmin>48</xmin>
    <ymin>240</ymin>
    <xmax>195</xmax>
    <ymax>371</ymax>
  </bndbox>
</object>
```

---

### 🔹 3. Detection vs Classification vs Segmentation

| 구분                       | 설명                      | 출력 형태          |
| ------------------------ | ----------------------- | -------------- |
| **Image Classification** | 이미지 전체에 하나의 라벨을 예측      | `class`        |
| **Object Detection**     | 여러 객체의 **위치 + 클래스**를 예측 | `bbox + class` |
| **Segmentation**         | 픽셀 단위로 객체의 경계를 구분       | `mask`         |

---

## ⚙️ Object Detection의 기본 파이프라인

1. **입력 이미지 전처리**
   (리사이즈, 정규화 등)
2. **특징 추출 (Feature Extraction)**
   CNN, Transformer 등을 사용해 이미지 특징 맵 생성
3. **객체 위치 예측 (Localization)**
   Bounding Box 좌표를 예측
4. **객체 클래스 예측 (Classification)**
   각 Bounding Box 안의 객체 종류를 예측
5. **후처리 (Post-Processing)**

   * **NMS (Non-Max Suppression)**: 겹치는 박스 제거
   * **Confidence Thresholding**: 신뢰도 낮은 예측 제거

---

## 🧠 대표 알고리즘 흐름

| 세대                       | 모델                                | 특징                           |
| ------------------------ | --------------------------------- | ---------------------------- |
| **1세대 (Two-Stage)**      | R-CNN → Fast R-CNN → Faster R-CNN | Region Proposal 기반, 정확도 높음   |
| **2세대 (One-Stage)**      | YOLO, SSD                         | 실시간 탐지 가능, 속도 빠름             |
| **3세대 (Transformer 기반)** | DETR, DINO                        | Attention 기반, Anchor-free 구조 |

---

## 🎯 정리 요약

| 개념                   | 설명                                        |
| -------------------- | ----------------------------------------- |
| **Object Detection** | 이미지 안의 객체의 **위치**와 **종류**를 동시에 예측         |
| **Bounding Box**     | 객체를 감싸는 최소 사각형                            |
| **Annotation**       | Bounding Box + 클래스 라벨 정보를 포함한 학습용 데이터     |
| **주요 모델**            | R-CNN, Fast/Faster R-CNN, YOLO, SSD, DETR |
| **핵심 기술**            | CNN 기반 특징 추출, NMS, Confidence score 계산    |

---
