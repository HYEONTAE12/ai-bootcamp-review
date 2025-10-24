
---

# 🏛️ 고전 컴퓨터 비전 (Classical Computer Vision)

## 📌 개요

* **고전 컴퓨터 비전**: 규칙 기반의 이미지 처리 알고리즘을 사용

  * Ex: Edge Detection, Filtering, Morphological Transform 등
* **딥러닝 기반 컴퓨터 비전**: 대규모 데이터와 신경망을 학습하여 자동으로 특징을 추출

---

# 🔧 Morphological Transform (형태학적 변환)

## 📖 정의

* 이미지 형태(구조)를 변형시키는 연산
* 주로 **흑백(Binary) 이미지**에서 수행
* **입력 요소**

  1. **원본 이미지** (Binary Image)
  2. **커널(구조 요소, Structuring Element)**

---

## 🔲 커널(Structuring Element)

* **역할**: 이미지에서 특정 영역(픽셀 주변)을 탐색하는 "필터"
* **형태**: 사각형, 원형, 십자가 모양 등 다양하게 정의 가능
* **크기**: 보통 `3x3`, `5x5` 등 작은 크기를 사용

---

## 🌟 Morphological 연산의 중요성

* **노이즈 제거**: 작은 점 잡음 제거
* **객체 분리**: 붙어 있는 물체를 분리
* **객체 연결**: 끊어진 선이나 경계 연결
* **형태 분석**: 객체의 윤곽선/구조 분석

---

## 🔹 주요 연산

### 1. **Erosion (침식)**

* **정의**: 객체의 경계를 **축소**하는 연산
* **동작 원리**:

  * 커널이 덮는 모든 픽셀이 1일 때만 결과 픽셀을 1로 유지
  * 그렇지 않으면 0으로 변경
* **효과**:

  * 객체가 작아짐 (얇아짐)
  * 작은 잡음 제거 가능

---

### 2. **Dilation (팽창)**

* **정의**: 객체의 경계를 **확장**하는 연산
* **동작 원리**:

  * 커널 영역 내에 1이 하나라도 있으면 결과 픽셀을 1로 설정
* **효과**:

  * 객체가 커짐 (두꺼워짐)
  * 끊어진 객체 연결

---

### 3. **Opening**

* **정의**: **Erosion → Dilation** 순서로 수행
* **효과**:

  * 작은 잡음 제거
  * 객체의 형태를 부드럽게 다듬음

---

### 4. **Closing**

* **정의**: **Dilation → Erosion** 순서로 수행
* **효과**:

  * 객체의 내부 구멍 메움 (Hole Filling)
  * 끊어진 객체 경계 연결

---

## ✨ 추가 Morphological 연산

* **Morphological Gradient**

  * Dilation 결과 – Erosion 결과
  * 객체의 **윤곽선(Edge)** 추출 가능

* **Top-hat Transform**

  * 원본 – Opening 결과
  * 작은 밝은 영역 추출 (노이즈나 작은 패턴 감지)

* **Black-hat Transform**

  * Closing 결과 – 원본
  * 작은 어두운 영역 추출

---

## 🏁 정리

* **Erosion**: 객체 축소, 잡음 제거
* **Dilation**: 객체 확장, 끊어진 부분 연결
* **Opening**: 작은 잡음 제거 (Erosion → Dilation)
* **Closing**: 구멍 메우기, 경계 연결 (Dilation → Erosion)
* **Gradient/Top-hat/Black-hat**: 객체 윤곽·특징 추출

---

