## 🎯 Object Detection 정리

---

### 📘 **개념**

* **Object Detection(객체 탐지)** 은
  이미지나 영상 속에서 **특정 물체의 위치(Location)** 와 **종류(Class)** 를 동시에 찾아내는 기술이다.

* 단순히 “무엇이 있는가”를 분류하는 **Image Classification** 과 달리,
  “어디에 있는가”까지 탐지해야 하기 때문에
  결과는 **사각형 박스(Bounding Box)** 와 **클래스 라벨** 로 시각화된다.

---

### 🧩 **작동 원리**

1. 입력 이미지에서 모델이 **관심 있는 객체를 찾아냄**
2. 그 객체의 위치를 **x, y, width, height** 좌표로 표시
3. 해당 영역을 **Bounding Box** 로 둘러싸고, **클래스 이름과 확률(score)** 을 함께 표시

> 예: 자동차(0.92), 사람(0.87), 신호등(0.76)

---

### ⚡ **모델 구조 구분**

#### 🥇 **1단계 검출기 (One-Stage Detector)**

* **탐지와 분류를 한 번에 처리** → 빠르고 실시간에 적합
* **대표 모델:**

  * **YOLO (You Only Look Once)**
  * **SSD (Single Shot MultiBox Detector)**
  * **RetinaNet**

🧠 **특징**

* 빠른 속도
* 실시간 영상 처리에 적합 (ex. 자율주행, CCTV 등)
* 다만, **정확도는 약간 낮을 수 있음**

---

#### 🥈 **2단계 검출기 (Two-Stage Detector)**

* **1단계:** 물체가 있을 가능성이 있는 영역(Region Proposal) 추출

* **2단계:** 그 영역을 정교하게 분류 및 박스 조정

* **대표 모델:**

  * **R-CNN**
  * **Fast R-CNN**
  * **Faster R-CNN**

🧠 **특징**

* 속도는 느리지만
* **정확도가 매우 높음**
* 정밀 탐지(예: 의료 영상, 위성 이미지 등)에 자주 사용

---

### 📐 **평가지표**

#### 📏 **IoU (Intersection over Union)**

* 두 박스(예측 박스 vs 정답 박스)가 얼마나 겹치는지를 나타내는 지표
* 0~1 사이의 값

  * `IoU = (교집합 영역) / (합집합 영역)`
  * 예: IoU ≥ 0.5 → “정탐(True Positive)” 로 간주

#### ⭐ **AP (Average Precision) / mAP (mean Average Precision)**

* 여러 IoU 기준(예: 0.5, 0.75 등)에서의 **정확도(Precision)** 평균
* **mAP** 은 여러 클래스의 **AP 평균값**
* Object Detection 모델 성능 평가의 핵심 지표

---

### 🧠 **주요 모델 발전 과정**

#### 🧩 **1️⃣ R-CNN (Regions with CNN features)**

* **처음으로 CNN을 객체 탐지에 적용한 모델 (2014)**
* 입력 이미지에서 Selective Search로 **Region Proposal(후보 영역)** 약 2,000개 추출
* 각 영역을 CNN에 통과시켜 특징 추출 → SVM으로 분류
* **정확도는 높지만 매우 느림** (매번 CNN을 반복 수행)

---

#### ⚙️ **2️⃣ Fast R-CNN**

* R-CNN의 속도 문제 해결
* 전체 이미지를 한 번만 CNN에 통과시켜 **Feature Map** 생성
* 그 위에서 **RoI Pooling** 을 통해 각 영역의 특징만 추출
* 훨씬 빠르면서도 정확도 유지

---

#### 🚀 **3️⃣ Faster R-CNN**

* Fast R-CNN의 **Region Proposal** 단계를 자동화
* **RPN (Region Proposal Network)** 도입 → CNN이 후보 영역을 스스로 생성
* 완전한 **엔드투엔드(end-to-end)** 학습 가능
* **속도와 정확도의 균형** 면에서 현재까지도 많이 사용되는 구조

---

### 💡 **요약**

| 구분      | 내용                                | 대표 모델                           |
| ------- | --------------------------------- | ------------------------------- |
| 1단계 검출기 | 탐지 + 분류를 한 번에 수행 → 빠름             | YOLO, SSD, RetinaNet            |
| 2단계 검출기 | 후보 영역 탐색 후 정밀 분류 → 정확함            | R-CNN, Fast R-CNN, Faster R-CNN |
| 핵심 지표   | IoU, AP, mAP                      | -                               |
| 핵심 기술   | Region Proposal, RoI Pooling, RPN | -                               |

---

📊 **정리 문장**

> Object Detection은 이미지 속에서 **무엇이 어디에 있는지**를 찾아내는 기술로,
> Bounding Box를 통해 객체의 위치를 시각화한다.
> 1단계 모델은 빠른 실시간 탐지를, 2단계 모델은 높은 정확도를 목표로 한다.
> 대표적으로 **R-CNN → Fast R-CNN → Faster R-CNN** 으로 발전해왔다.

---


