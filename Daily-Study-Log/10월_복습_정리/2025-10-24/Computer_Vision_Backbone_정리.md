

---

# 🧩 Backbone in Computer Vision

## 📌 Backbone의 역할

* Backbone은 **이미지에서 중요한 특징(Visual Feature)을 추출**하는 네트워크의 주요 부분.
* 입력 이미지를 여러 계층(layer)을 거쳐 압축하고 추상화하여, 다양한 **비전 태스크**(classification, detection, segmentation 등)에 활용 가능한 **고수준 feature map**을 생성.
* 즉, **공통 시각 인코더(Shared Visual Encoder)** 역할을 수행함.

---

## 🏗️ Backbone 구조

* **Layer (층)**

  * Conv, Pooling, BatchNorm, Activation 등으로 구성됨.
  * 저수준(low-level) 특징(엣지, 색상, 질감)부터 고수준(high-level) 특징(객체 모양, 패턴)까지 점진적으로 추출.

* **Backbone = 여러 Layer의 집합**

  * 이미지 크기를 점차 줄이고, 채널(Feature Dimension)을 늘리며 추상화된 Feature를 학습.
  * 예: VGG, ResNet, EfficientNet, Swin Transformer 등은 잘 알려진 Backbone 아키텍처.

---

## 🎨 Visual Feature

* 이미지에서 **태스크 해결에 필요한 정보**를 담고 있는 표현.
* 예:

  * Classification → 클래스별 구분에 필요한 패턴
  * Detection → 객체 위치 및 크기에 대한 단서
  * Segmentation → 픽셀 단위의 영역 정보

---

## 🔄 Encoder-Decoder 구조

### Encoder의 역할

* Backbone에서 나온 Feature를 **한 번 더 가공**하여 Task에 맞게 적합한 표현을 전달.
* 주로 Conv/Transformer 블록으로 구성.
* 예: Feature Pyramid Network(FPN), Vision Transformer의 Encoder 블록.

### Decoder의 역할

* Encoder가 전달한 Feature를 **최종 태스크 출력**으로 변환.
* Task에 따라 구조가 달라짐:

1. **Classification**

   * 출력: 클래스별 확률 (Softmax)
   * 구조: Fully Connected Layer
   * 질문: "이 이미지에는 어떤 객체가 있나?"

2. **Detection**

   * 출력: Bounding Box + 클래스별 확률
   * 구조: Region Proposal + 회귀(Regression) + 분류(Classification)
   * 질문: "어디에, 어떤 물체가 있나?"

3. **Segmentation**

   * 출력: 픽셀 단위 클래스 맵 (Mask)
   * 구조: Upsampling, Deconvolution, Skip-Connection
   * 질문: "이 픽셀은 어떤 클래스에 속하는가?"

---

## 🧩 Backbone & Decoder의 관계

* **Backbone**

  * 공통적으로 이미지를 "이해"하는 부분
  * 다양한 태스크에서 **재사용 가능** (Pretrained 모델 → Transfer Learning)

* **Decoder**

  * 태스크별로 다른 형태의 출력을 만들어야 함
  * 따라서 Task가 달라지면 Decoder 구조도 반드시 수정 필요

👉 **즉, Backbone은 공통 / Decoder는 Task-specific**

---

# 📊 요약

1. **Backbone** → 이미지 특징 추출 (공통 인코더)
2. **Encoder** → Feature를 더 정제해 Task에 맞게 가공
3. **Decoder** → 최종 출력 (Classification / Detection / Segmentation 등)
4. **Backbone은 재사용 가능하지만, Decoder는 Task에 따라 변한다.**

---

