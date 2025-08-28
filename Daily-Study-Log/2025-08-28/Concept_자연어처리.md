
---

# 자연어처리(NLP)

## 1. 자연어처리란?

* **자연어 (Natural Language)**: 인간이 일상적으로 사용하는 언어 (예: 한국어, 영어 등)
  → 반대 개념은 **인공 언어** (Python, C언어 등 프로그래밍 언어)
* **자연어처리(NLP)**: 이러한 인간의 언어를 **컴퓨터가 이해하고 처리**할 수 있도록 만드는 기술

---

## 2. 단어 표현 (Word Representation)

### 📌 원-핫 인코딩 (One-Hot Encoding)

* 단어를 **0과 1의 벡터**로 표현
* 표현하고 싶은 단어 위치에만 `1`, 나머지는 `0`
* 예: 단어 집합 {dog, cat} →

  * `dog = [1, 0]`
  * `cat = [0, 1]`

**단점**

1. 단어 간의 의미/관계성을 반영하지 못함
2. 단어 집합 크기 = 벡터 차원 → 희소벡터(Sparse Vector) 문제 발생
3. 메모리 비용이 매우 큼

---

### 📌 Word2Vec

* 원-핫 인코딩 한계를 극복하기 위해 제안된 방식
* **Dense Vector (분산 표현, Embedding)** 사용
* 목표: **의미가 유사한 단어는 벡터 공간에서 가까운 위치에 있도록 학습**
* 학습 방법:

  * CBOW (Continuous Bag of Words): 주변 단어 → 중심 단어 예측
  * Skip-gram: 중심 단어 → 주변 단어 예측

**장점**

* 단어 간 의미적 유사성 반영 (예: `king - man + woman ≈ queen`)

**한계**

* 문맥(Context) 정보 반영 불가
* **동음이의어** 문제 (예: "bank" = 강둑 / 은행 → 같은 벡터로 표현됨)

---

## 3. 문맥 기반 단어 표현 (Contextual Word Embedding)

### 📌 ELMo (Embeddings from Language Models)

* **양방향 LSTM 기반 언어 모델**을 사용하여 단어 임베딩 생성
* **특징**: 같은 단어라도 문맥에 따라 다른 벡터로 표현

예:

* "He went to the **bank** to deposit money." → 금융기관 의미
* "He sat by the **bank** of the river." → 강둑 의미

**장점**

* 문맥 정보를 반영하여 동음이의어 문제 해결

**단점**

* RNN/LSTM 기반이라 학습/추론 속도가 느림
* 긴 문장에서의 장기 의존성(Long-term dependency) 문제 여전

---

### 📌 Transformer

* 2017년 Google 논문 \*"Attention is All You Need"\*에서 제안
* **Self-Attention** 메커니즘을 기반으로 문맥을 효과적으로 파악
* 병렬 연산 가능 → RNN/LSTM보다 빠르고 효율적
* 이후 모든 최신 NLP 모델의 기반이 됨

---

## 4. 대표적 Transformer 기반 모델

### 📌 BERT (Bidirectional Encoder Representations from Transformers)

* Google (2018)에서 제안
* **양방향 인코더 모델** → 양쪽 문맥(앞뒤)을 모두 활용
* **사전학습(Pre-training)** 방식:

  1. **Masked Language Model (MLM)**: 문장 중 일부 단어를 \[MASK]로 가리고 맞히기
  2. **Next Sentence Prediction (NSP)**: 두 문장이 연속된 문장인지 판별

**장점**

* 다양한 NLP 다운스트림 태스크에 뛰어난 성능 (QA, 문서 분류 등)
* 문맥 반영 + 일반화 능력 우수

**단점**

* 사전학습과 파인튜닝 과정에서 **큰 연산 자원 필요**

---

### 📌 GPT (Generative Pre-trained Transformer)

* OpenAI (2018\~현재)에서 개발
* **디코더 기반 Transformer** 구조 사용
* **사전학습(Pre-training)** 방식:

  * **Causal Language Modeling (CLM)**: 이전 단어들을 보고 다음 단어 예측
* **특징**

  * 생성(Generation) 태스크에 강점
  * ChatGPT, GPT-4/5 등은 GPT 계열 모델

**장점**

* 대규모 데이터로 학습 → 강력한 언어 생성 능력
* Few-shot / Zero-shot Learning 가능 (프롬프트 기반 학습)

**단점**

* BERT와 달리 양방향 문맥 반영이 약함 (순방향 예측 기반)
* 데이터 편향 및 사실성 문제

---

## 5. 단어 표현 발전 흐름

1. **원-핫 인코딩** → 희소벡터, 관계성 없음
2. **Word2Vec / GloVe** → 의미 반영 (Dense Vector), 문맥 반영 불가
3. **ELMo** → 문맥 반영 가능 (LSTM 기반)
4. **Transformer (BERT, GPT 등)** → Self-Attention 기반, 문맥+효율성+성능 모두 향상

---

✅ **핵심 요약**

* NLP는 인간 언어를 컴퓨터가 이해/처리하는 기술
* 단어 표현은 **원-핫 → Word2Vec → ELMo → Transformer**로 발전
* 최신 NLP는 Transformer 기반 (BERT: 이해, GPT: 생성)

---

