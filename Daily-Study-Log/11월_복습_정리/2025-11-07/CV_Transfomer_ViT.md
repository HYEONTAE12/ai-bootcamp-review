

---

# 🧠 Transformer

## 📍 정의

**Transformer**는 2017년 Google에서 발표한 논문

> “Attention Is All You Need”
> 을 기반으로 만들어진 **딥러닝 모델 구조(Architecture)**로,
> 기존의 RNN이나 CNN 기반 모델이 가진 **long-term dependency**(장기 의존성) 문제를 **Self-Attention** 메커니즘으로 해결하기 위해 등장했다.

---

## 🚧 등장 배경

### 🔹 RNN / LSTM의 한계

* 입력 데이터를 **순차적으로 처리**하기 때문에 긴 문장에서
  앞부분의 정보가 뒤로 갈수록 **점점 손실되는 문제** 발생
* 병렬 처리 불가능 → 학습 속도 느림
* 긴 문장일수록 **gradient vanishing / exploding** 문제가 심화

### 🔹 CNN의 한계

* 지역적인(Local) 패턴은 잘 학습하지만,
  **멀리 떨어진 두 객체 간의 관계(Context)** 를 학습하기 어려움
* 이미지나 문장에서 전체적인 의미나 상관관계를 파악하는 데 한계

> ➡️ 이런 한계를 해결하기 위해 **Attention** 메커니즘이 도입되었고,
> 이를 완전히 구조화한 모델이 바로 **Transformer**다.

---

## ⚙️ 핵심 개념: Attention

### 🔸 Attention의 아이디어

입력 전체를 한 번에 보고,
**중요한 부분에 더 높은 가중치(Attention weight)** 를 부여함으로써
모델이 문맥상 핵심 정보에 “집중”하도록 만드는 개념.

### 🔸 Self-Attention

* 문장 내의 단어들이 **서로를 참조하면서 의미적 관계를 학습**
* 예: “The animal didn’t cross the street because **it** was too tired.”
  → ‘it’이 ‘animal’을 가리킨다는 관계를 학습

> RNN처럼 순서대로 처리하지 않아도,
> **모든 단어 간 관계를 한 번에 고려**할 수 있다.

---

## 🧩 Transformer 구조

| 구성 요소                                         | 역할                                     |
| :-------------------------------------------- | :------------------------------------- |
| **Encoder**                                   | 입력 문장을 받아 문맥 정보를 인코딩                   |
| **Decoder**                                   | 인코딩된 정보를 기반으로 출력(번역문 등) 생성             |
| **Self-Attention Layer**                      | 입력 내부의 단어 간 관계를 계산                     |
| **Multi-Head Attention**                      | 여러 관점에서 Attention을 수행하여 풍부한 문맥 표현      |
| **Positional Encoding**                       | 순서 정보가 없는 구조의 한계를 보완하기 위해 단어 위치 정보를 더함 |
| **Feed-Forward Network (FFN)**                | 비선형 변환을 통해 표현 능력 강화                    |
| **Residual Connection & Layer Normalization** | 학습 안정화 및 정보 손실 방지                      |

---

## 🔍 Self-Attention의 작동 방식 (개념 흐름)

1. 각 단어를 **Query(Q)**, **Key(K)**, **Value(V)** 벡터로 변환
2. Query와 모든 Key의 유사도를 계산하여 Attention Score 도출
3. Score를 Softmax로 정규화 → 가중치 생성
4. 가중치 × Value 를 합산해 최종 Attention 출력 생성

> 즉, 문장 내의 단어들이 **서로에게 얼마나 주의를 기울여야 하는지** 계산하는 과정

---

## 🔄 Multi-Head Attention

* 하나의 Attention만으로는 단어 간 관계를 충분히 표현하기 어려움
* 여러 개의 Attention Head를 사용하여
  **다양한 관점(의미적, 문법적 등)** 에서 관계를 학습
* 병렬적으로 처리되어 학습 효율도 높음

---

## ⚡ Transformer의 장점

| 항목            | 설명                                         |
| :------------ | :----------------------------------------- |
| **병렬 처리 가능**  | RNN과 달리 모든 입력을 동시에 처리 가능 → 학습 속도 빠름        |
| **장기 의존성 해결** | 문장 전체를 한 번에 참조 가능                          |
| **확장성**       | 다양한 Task에 쉽게 확장 가능 (NLP, Vision, Speech 등) |
| **표현력 강화**    | Multi-Head Attention으로 풍부한 문맥 학습           |

---

## 🧠 Vision Transformer (ViT)

* Transformer 구조를 **이미지 분류**에 적용한 모델
* 이미지를 작은 **Patch** 단위로 나누고,
  이를 단어(Token)처럼 처리하여 **Self-Attention**으로 학습
* CNN보다 **전역적(Contextual)** 관계를 더 잘 학습함

---

## 📚 요약 정리

| 구분         | 내용                                                          |
| :--------- | :---------------------------------------------------------- |
| **문제**     | RNN: 장기 의존성 / CNN: 전역 관계 학습 불가                              |
| **핵심 해결책** | Self-Attention을 통한 문맥 관계 학습                                 |
| **핵심 구조**  | Encoder, Decoder, Multi-Head Attention, Positional Encoding |
| **장점**     | 병렬 처리, 장기 의존성 해결, 확장성                                       |
| **활용 분야**  | NLP (BERT, GPT), Vision (ViT), Audio, Multimodal 등          |

---
