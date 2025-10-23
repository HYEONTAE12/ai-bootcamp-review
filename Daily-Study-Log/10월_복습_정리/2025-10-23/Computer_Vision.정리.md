


---

# 🖼️ Computer Vision 정리

## 📌 Vision의 정의

* **Vision**: 시각적인 정보들의 집합
* 즉, 인간이 눈으로 보는 것처럼 **시각 정보를 디지털 데이터(숫자)**로 변환해 저장하고 분석하는 모든 개념을 포함한다.

---

## 🔹 Computer Vision 단계 (저수준 → 고수준)

### 1️⃣ Low-level Vision (저수준)

픽셀 단위에서의 **기본 이미지 처리 & 특징 추출**

#### 🔧 Image Processing

* **Resize**
  주변 픽셀 값을 고려한 보간(interpolation)으로 크기 조정

  * 방식: Nearest Neighbor, Bilinear, Bicubic 등

* **Color Jitter**
  픽셀마다 독립적으로 색상/밝기/채도/대비 조정

  * 데이터 증강(Data Augmentation)에 자주 활용

#### 🔍 Feature Extraction

* **Edge Detection**
  픽셀 값이 급격히 변하는 지점을 검출 (경계 찾기)

  * 기법: Sobel, Canny, Laplacian

* **Segmentation by Color**
  색상 정보(RGB, HSV 등)를 기준으로 영역 분할

  * 예: K-means 군집화

* **Watershed Segmentation**
  색상 + 밝기 + 경계(Gradient) 고려 → 객체 윤곽선 분리

  * 물이 흘러가며 영역을 나누는 원리

---

### 2️⃣ Mid-level Vision (중수준)

**여러 이미지 간 관계**를 분석하거나
**2D → 3D 변환**을 수행하는 단계

#### 🖼️ Images → Image

* **Panorama Stitching**
  여러 장의 이미지에서 **특징점 매칭 → 변환(Homography)** → 이어붙여 파노라마 생성

#### 🌍 Images → World

* **Multi-view Stereo (MVS)**
  여러 장의 2D 이미지 → **깊이 추정 → 3D 포인트 클라우드** 생성

  * 과정:

    1. Feature Matching (대응점 찾기)
    2. Surface Reconstruction (점 → 메쉬)
    3. Texture Mapping (원본 사진 질감 입힘 → 사실적 3D 모델 완성)

* **Depth Estimation**
  2D 이미지에서 객체의 상대적 깊이 추정

  * 활용: 자율주행, 로봇 비전

* **LIDAR**
  레이저 반사 시간과 각도로 고정밀 **3D 포인트 클라우드 생성**

---

### 3️⃣ High-level Vision (고수준)

이미지를 **이해(semantic 이해)**하는 단계

#### 🧠 Semantics

* **Image Classification**
  전체 이미지를 하나의 클래스(고양이/개 등)로 분류

* **Object Detection**
  이미지 내 객체의 위치(Bounding Box) + 클래스 식별

  * 모델 예시: YOLO, Faster R-CNN

* **Segmentation**
  객체를 **픽셀 단위로 분류**

  * Semantic Segmentation: 클래스 단위 (예: 개 vs 고양이)
  * Instance Segmentation: 동일 클래스 내 개별 객체 구분 (예: 고양이 2마리 따로)

---

## 🏁 전체 흐름 요약

1. **Low-level** → 픽셀 처리, 경계 검출
2. **Mid-level** → 이미지 간 관계, 3D 복원
3. **High-level** → 객체 이해, 의미 분석

👉 한마디로, Computer Vision은
**“빛(이미지) → 숫자화 → 구조화 → 의미 해석”** 과정이다.

---
