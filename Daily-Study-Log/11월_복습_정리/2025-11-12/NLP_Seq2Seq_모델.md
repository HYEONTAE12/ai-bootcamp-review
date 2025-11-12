
---

# 🧠 Sequence-to-Sequence (Seq2Seq) 모델 정리

---

## 📌 개요

**Sequence-to-Sequence(Seq2Seq)** 모델은
👉 **입력된 시퀀스(sequence)를 다른 시퀀스로 변환하는 모델 구조**입니다.

* 대표적인 예시: **번역(Translation)**
  → "I love you" → "나는 너를 사랑해"

이 모델은 크게 두 부분으로 구성됩니다.

---

## 🔹 1. Encoder (인코더)

* 입력 시퀀스를 받아 **고정된 길이의 벡터**로 변환합니다.
* 이 벡터는 입력 전체의 의미를 압축적으로 담고 있으며,
  **문맥 벡터(Context Vector)** 라고 부릅니다.

> 인코더 RNN은 입력 시퀀스의 모든 시점 정보를 종합해 문맥 벡터를 생성합니다.

**예시:**

```
입력: [I, love, you]
출력: [context_vector]
```

---

## 🔹 2. Decoder (디코더)

* 인코더가 전달한 **문맥 벡터(Context Vector)** 를 받아
  새로운 시퀀스를 **한 단어씩 순차적으로 생성**합니다.
* 이전에 생성한 단어(출력)를 다음 시점의 입력으로 활용하여
  문맥적으로 일관된 문장을 생성합니다.

> 디코더는 “현재 문맥 + 이전 출력”을 기반으로 다음 출력을 예측합니다.

**예시:**

```
입력: [context_vector]
출력: [나는, 너를, 사랑해]
```

---

## 🔄 Seq2Seq의 개념적 대응 관계

| 구분                               | 대응 관계                     |
| -------------------------------- | ------------------------- |
| **Sequence → Sequence**          | 입력 시퀀스를 출력 시퀀스로 변환        |
| **Encoder → Decoder**            | 입력을 요약(인코딩) → 출력을 생성(디코딩) |
| **자연어 이해 → 자연어 생성**              | 입력 문장 의미 파악 → 새로운 문장 생성   |
| **Autoencoder → Autoregressive** | 입력 복원 구조 → 이전 출력 기반 예측 구조 |

---

## ⚙️ RNN (Recurrent Neural Network)

RNN은 **시퀀스 데이터(Sequence Data)** 를 처리하기 위해 고안된 신경망 구조입니다.
입력의 시간적 순서를 고려하며, **이전 시점의 정보를 기억**하고 다음 시점에 전달합니다.

---

### 🧩 RNN 입력-출력 형태 유형

| 유형               | 구조              | 예시                            |
| ---------------- | --------------- | ----------------------------- |
| **One-to-One**   | 단일 입력 → 단일 출력   | 이미지 분류 (Image Classification) |
| **One-to-Many**  | 단일 입력 → 시퀀스 출력  | 이미지 캡셔닝 (Image Captioning)    |
| **Many-to-One**  | 시퀀스 입력 → 단일 출력  | 감정 분석 (Sentiment Analysis)    |
| **Many-to-Many** | 시퀀스 입력 → 시퀀스 출력 | 기계 번역 (Machine Translation)   |

---

## 🔁 Bidirectional RNN (양방향 RNN)

* 일반적인 RNN은 시퀀스를 **앞에서 뒤로(Forward)** 만 처리하지만,
  Bidirectional RNN은 **양방향(Forward + Backward)** 으로 정보를 학습합니다.
* 따라서, **문맥(Context)** 정보를 더 풍부하게 반영할 수 있습니다.

> 예: “나는 학교에 갔다” 문장에서
> “학교에”의 의미를 이해하려면 **앞 단어(나는)** 와 **뒤 단어(갔다)** 모두 고려해야 함

---

## 🏗️ Deep RNN (심층 RNN)

* 단일 RNN Layer 위에 여러 층을 **쌓은 형태**
* 각 층이 이전 층의 출력을 입력으로 받아 **추상적 표현(High-level Representation)** 을 학습
* 더 복잡한 패턴 학습 가능하지만, **Gradient Vanishing(기울기 소실)** 문제 발생 가능

> 이를 해결하기 위해 LSTM, GRU 같은 구조가 등장함.

---

## 📚 확장 개념 요약

| 개념                                | 설명                                            |
| --------------------------------- | --------------------------------------------- |
| **LSTM (Long Short-Term Memory)** | RNN의 장기 의존성 문제를 해결하기 위해 고안된 구조                |
| **GRU (Gated Recurrent Unit)**    | LSTM보다 단순한 구조, 계산 효율 높음                       |
| **Attention Mechanism**           | Seq2Seq의 한계를 보완, 입력 시퀀스의 중요한 부분에 가중치 부여       |
| **Transformer**                   | Attention만으로 시퀀스 관계를 학습하는 구조, RNN의 한계를 완전히 극복 |

---

## 🧠 전체 구조 요약

```text
입력 시퀀스 ─► [Encoder RNN] ─► Context Vector ─► [Decoder RNN] ─► 출력 시퀀스
```

* Encoder: 입력 이해 (자연어 이해)
* Decoder: 결과 생성 (자연어 생성)
* Attention / Transformer: 문맥 정보 손실 보완

---

## 💬 대표 활용 예시

| Task                            | 설명                         |
| ------------------------------- | -------------------------- |
| **기계 번역 (Machine Translation)** | “I love you” → “나는 너를 사랑해” |
| **챗봇 (Chatbot)**                | 입력 문장 → 응답 문장              |
| **텍스트 요약 (Summarization)**      | 긴 문장 → 짧은 요약               |
| **음성 인식 (Speech Recognition)**  | 음성 시퀀스 → 텍스트 시퀀스           |
| **자막 생성 (Video Captioning)**    | 영상 프레임 → 문장 생성             |

---

