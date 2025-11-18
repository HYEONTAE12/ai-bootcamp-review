

---

# 📘 **현대 NLP·AI 업계에서 가장 많이 사용되는 토크나이저 정리**



---

# #️⃣ 1. **SentencePiece (구글, Open Source)**

SentencePiece는 토크나이저 “프레임워크” 이름이야.
내부적으로 **두 가지 모델을 지원**하는데, 둘 다 업계 표준.

### 🔥 (1) Unigram Language Model (업계 1등)

* T5, mT5, ALBERT, XLNet, PaLM, Qwen, LLaMA 계열 일부 등에서 사용
* **확률 기반** subword segmentation
* EM 알고리즘을 사용해 최적의 subword 조합 선택
* 희귀단어/다국어 처리 매우 강함
* SentencePiece가 사실상 표준 구현체

### 📌 특징

* 고정 규칙(BPE)보다 유연
* 다국어 모델에서 성능 우수
* GPT-4/5 계열도 "Unigram 변형" 기반

---

### 🔥 (2) SentencePiece BPE (SP-BPE)

* BPE를 강화한 버전
* OpenAI GPT-2/3 계열이 내부적으로 비슷한 구조 사용
* pure char-BPE보다 더 robust한 구조

### 📌 특징

* BPE보다 안정적
* 빈도 기반 merge 구조는 동일
* 단독보단 Unigram과 함께 SentencePiece 패키지의 일부로 쓰임

---

# #️⃣ 2. **Byte-level BPE (GPT-2, GPT-3 스타일)**

> BPE를 “바이트 단위”로 확장한 방식.
> GPT-2가 이 방식으로 유명함.

### 📌 특징

* 어떤 언어, 문자, 이모지도 **깨지지 않음**
* UTF-8 byte 기반이라 안정성이 매우 높음
* subword 앞에 공백을 구분하기 위해 `'Ġ'` 같은 특수 prefix를 사용

### 🤖 사용 모델

* GPT-2
* GPT-3
* GPT-J, GPT-NeoX
* BLOOM

이 방식은 지금도 많이 쓰임.

---

# #️⃣ 3. **Tiktoken (OpenAI 전용 고속 토크나이저)**

GPT-4, GPT-4o, GPT-4.1, GPT-5.1 등이 사용하는 런타임 엔진.

> “알고리즘 자체는 Unigram 기반 + byte fallback
> 실행 엔진은 Tiktoken으로 매우 빠르게 최적화된 구조”

### 📌 특징

* C에서 구현된 초고속 토크나이저
* byte safety
* 병렬 토크나이징 지원
* OpenAI 모델 전용

### 중요한 점

* **학습 시에는 SentencePiece(Unigram) 기반 알고리즘 사용**
* **실행 시에는 Tiktoken으로 변환된 테이블 활용**

---

# #️⃣ 4. **WordPiece (BERT 스타일, 너가 이미 정리함)**

그래도 참고용 요약만 추가.

### 📌 특징

* MLM(Masked LM) 모델에 최적화
* 자주 등장하는 subword를 만들어내는 구조
* BPE보다 subword 개수를 줄이는 데 강함
* Google BERT가 사용하면서 사실상 업계 표준이 됨

### 사용 모델

* BERT
* RoBERTa
* DistilBERT
* ELECTRA
* KoBERT
* 대부분의 한국어 BERT들

---

# #️⃣ 5. **Word-level Tokenizer (전통 방식, 거의 안 씀)**

### 📌 특징

* 공백 기준 단어 분리
* 희귀 단어와 OOV 문제 심각
* 현대 모델에서는 거의 사용 안 됨

### 사용 사례

* 아주 오래된 RNN/LSTM 기반 모델
* 일부 rule-based NLP 시스템

---

# #️⃣ 6. **Character-level Tokenizer (문자 단위)**

### 📌 특징

* vocabulary 크기가 매우 작음 (수십~수백 개)
* OOV 문제 없음
* 하지만 sequence length가 너무 길어져 성능 떨어짐
* 요약/번역 등에서는 비효율적

### 사용 모델

* 일부 Generative 모델 실험
* Reformer, Charformer 등에서 연구됨

---

# #️⃣ 7. **Byte-level Tokenizer (LLM 시대에 각광)**

Character보다 더 로우레벨로 내려간 방식.

### 특징

* 어떤 문자도 절대 깨지지 않는 0~255 byte range
* 모든 언어 호환
* 이모지, CJK 문제 해결
* 빈도 기반 subword 알고리즘(BPE/Unigram)과 조합하면 강력해짐

### 사용 모델

* GPT-4/5 계열 → Byte fallback 포함
* LLaMA 3
* Mistral
* Qwen 1.5/2

---

# #️⃣ 8. **SentencePiece “통합 방식” (LLama/LLaMA2 스타일)**

Meta LLaMA는 기본적으로 SentencePiece의 BPE 변형을 사용함.

### 특징

* 공백을 특별한 `▁` 표시로 처리 (SentencePiece 특유)
* 랭귀지 독립적
* UTF-8 안정적
* 다국어 성능도 준수

### 사용 모델

* LLaMA 1/2
* 일부 fine-tuned 모델들
* KoAlpaca 기반 모델들

---

# 🎯 **업계에서 실제로 많이 쓰이는 것 순위**

### 2023~2025년 기준 “실전 점유율” 기준으로 보면:

| 순위    | 방식                             | 이유                              |
| ----- | ------------------------------ | ------------------------------- |
| 🥇 1위 | **Unigram LM (SentencePiece)** | T5, PaLM, LLaMA, GPT 계열 대부분 참고  |
| 🥈 2위 | **Byte-level BPE**             | GPT-2/3, NeoX, BLOOM 등 대형 모델 표준 |
| 🥉 3위 | **Tiktoken (전용 런타임)**          | GPT-4~5 계열에서 압도적                |
| 4위    | WordPiece                      | BERT 계열 역사적 표준                  |
| 5위    | SentencePiece-BPE              | 여전히 일부 LLaMA 기반                 |
| 6위    | Character                      | 실험용                             |
| 7위    | Word-level                     | 거의 역사적 잔재                       |

---

# 🧩 이 목록을 보면 한눈에 보이는 흐름

* 예전: Word → WordPiece → BPE
* 현대: BPE → Unigram LM → Byte-level → Custom tokenizer runtime

즉:

> **현대 LLM은 대부분 Unigram LM 또는 Byte-level BPE 계열이다.**
> → BPE/WordPiece보다 훨씬 강력하고 언어적 제약이 적음.

---

