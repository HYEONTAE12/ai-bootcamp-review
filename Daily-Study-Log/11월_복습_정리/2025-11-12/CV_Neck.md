

---

## 🧩 **Neck (넥) 정리**

### 📘 1. 정의

> **Neck**은 **Backbone(인코더)** 에서 추출된 여러 단계의 feature map을
> **Head(디코더)** 가 쓰기 좋은 형태로 **가공·통합해주는 중간 구조**입니다.

즉,
**“특징을 연결하고 보강하는 다리 역할”** 을 하는 부분이에요.

---

### ⚙️ 2. 위치

```
[Encoder (Backbone)] → [Neck] → [Decoder (Head)]
```

* **Encoder(Backbone)**: 이미지의 다양한 특징 추출
* **Neck**: 여러 스케일(크기)의 feature를 결합하고 정제
* **Decoder(Head)**: 최종 결과물(분류, 박스, 마스크 등) 예측

---

### 🧠 3. 주요 역할

| 역할                                      | 설명                                                                                  |
| --------------------------------------- | ----------------------------------------------------------------------------------- |
| **1️⃣ Feature 통합 (Multi-scale Fusion)** | Backbone의 여러 단계에서 나온 feature map(1/4, 1/8, 1/16 등)을 합쳐서, 큰 물체와 작은 물체를 모두 인식할 수 있게 함 |
| **2️⃣ 정보 전달 (Bridge 역할)**               | Encoder의 출력과 Decoder의 입력을 자연스럽게 연결                                                  |
| **3️⃣ 정보 강화 (Feature Refinement)**      | 상·하위 layer의 정보를 결합해 더 풍부한 표현 생성                                                     |
| **4️⃣ 연산 효율화**                          | Decoder가 부담 없이 쓸 수 있도록 feature 크기와 채널 조정                                            |

---

### 🧩 4. 대표적인 Neck 구조

| 이름          | 풀네임                            | 설명                                  | 사용 예시                    |
| ----------- | ------------------------------ | ----------------------------------- | ------------------------ |
| **FPN**     | Feature Pyramid Network        | 여러 해상도의 feature map을 위로 업샘플링하며 결합   | Faster R-CNN, Mask R-CNN |
| **PANet**   | Path Aggregation Network       | FPN을 확장해, 위↔아래 양방향으로 정보 전달          | YOLOv4, DetectoRS        |
| **BiFPN**   | Bi-directional FPN             | 가중치 기반으로 feature 중요도를 학습하며 효율적으로 결합 | EfficientDet             |
| **NAS-FPN** | Neural Architecture Search FPN | 자동 탐색을 통해 최적의 피라미드 구조 설계            | AutoML 기반 모델             |

---

### 🧩 5. 비유로 이해하기

> 🎨 **Encoder**는 “재료를 준비하는 공장”
> 🔩 **Neck**은 “재료를 잘 섞고 다듬는 조립 라인”
> 🏁 **Decoder**는 “완성품을 만들어내는 조립 공정”

즉,
Neck은 여러 특징을 한데 모아서 “Decoder가 쉽게 이해하도록” 만들어주는
**정보 가공소**라고 생각하면 돼요.

---

### ✅ 6. 한 줄 요약

> **Neck = Backbone과 Head를 연결하면서,
> 여러 스케일의 feature를 통합하고 강화하는 중간 가공층**

---

