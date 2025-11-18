# BERT 핵심 정리

## 📌 BERT란?

**BERT (Bidirectional Encoder Representations from Transformers)**
- Google이 2018년 10월 발표
- NLP에서 Pretrain-Finetune 패러다임을 **대중화**시킨 모델
- Transformer의 **Encoder만** 사용하는 구조
- 진정한 **양방향(Bidirectional)** 문맥 학습

### 한 줄 요약
> "Masked Language Model로 양방향 문맥을 이해하고, Self-Supervised Learning으로 무한한 데이터를 학습하는 Encoder 기반 사전학습 모델"

---

## 🎯 핵심 혁신 3가지

### 1. 구조적 혁신: 진정한 양방향

**기존 모델들의 한계:**

```
ELMo (2018.1):
- Forward LSTM + Backward LSTM 따로 학습
- 두 결과를 concat
- "독립적" 양방향 (진짜 양방향 아님)

GPT-1 (2018.6):
- Transformer Decoder 사용
- 단방향 (→만 봄)
- 생성에는 좋지만 이해 태스크에 불리
```

**BERT의 해결:**

```python
# Self-Attention으로 모든 토큰이 동시에 상호작용
"나는 [MASK] 먹었다"

# [MASK] 예측 시:
- "나는" (왼쪽 문맥) ✓
- "먹었다" (오른쪽 문맥) ✓
- 동시에 참조! (Self-Attention)

→ 진짜 양방향 문맥 이해!
```

**ELMo vs BERT 비교:**
| 모델 | 양방향 방식 | 결과 |
|------|-----------|------|
| ELMo | Forward + Backward 독립 학습 → concat | 따로따로 |
| BERT | Self-Attention으로 모든 방향 동시 학습 | 통합적 |

### 2. 학습 방법: Self-Supervised Learning

**핵심: 사람이 라벨링 안 해도 됨!**

```python
# 원본 텍스트 자체가 정답
원본: "나는 오늘 학교에 갔다"
입력: "나는 오늘 [MASK] 갔다"
정답: "학교에" ← 자동 생성!

# 무한한 학습 데이터 생성 가능
# 비용: $0
# 시간: 데이터 수집만
```

**효율성:**
```
Supervised Learning:
- 데이터 수집: 1일
- 라벨링: 100일 ← 사람이 일일이
- 학습: 1일
총: 102일

Self-Supervised Learning (BERT):
- 데이터 수집: 1일
- 라벨링: 0일 ← 자동!
- 학습: 1일
총: 2일
```

### 3. 사전학습 태스크: MLM + NSP

**MLM (Masked Language Model)**
```python
# 입력의 15%를 랜덤 마스킹
원본: "나는 밥을 먹었다"
입력: "나는 [MASK] 먹었다"
목표: [MASK] = "밥을" 예측

# 실제 마스킹 전략:
- 80%: [MASK]로 치환
- 10%: 랜덤 단어로 치환  
- 10%: 그대로 유지
```

**NSP (Next Sentence Prediction)**
```python
# 두 문장이 연속인지 판단

# IsNext (50%)
A: "나는 학생이다"
B: "학교에 다닌다" ← 실제 다음 문장
라벨: 1

# NotNext (50%)
A: "나는 학생이다"
B: "하늘이 파랗다" ← 랜덤 문장
라벨: 0

# [CLS] 토큰으로 문장 관계 예측
```

**참고:** 후속 연구(RoBERTa)에서 NSP는 효과가 미미한 것으로 밝혀짐

---

## 🏗️ BERT 구조

### 전체 아키텍처

```
Input
  ↓
[Embedding Layer]
  - Token Embedding
  - Segment Embedding (문장 A/B 구분)
  - Position Embedding (위치 정보)
  ↓
[Encoder Block 1]
  - Multi-Head Self-Attention
  - Add & Norm
  - Feed-Forward Network (FFN)
  - Add & Norm
  ↓
[Encoder Block 2]
  - (동일)
  ↓
... (12개 또는 24개 반복)
  ↓
[Encoder Block N]
  ↓
[Output]
  - [CLS] 토큰: 문장 전체 표현
  - 각 토큰: 문맥 반영된 표현
```

### 모델 크기

| 모델 | Layers | Hidden Size | Attention Heads | 파라미터 |
|------|--------|-------------|-----------------|---------|
| BERT-base | 12 | 768 | 12 | 110M |
| BERT-large | 24 | 1024 | 16 | 340M |

### Input 형식

```python
# 단일 문장
[CLS] 문장 [SEP]

# 문장 쌍 (QA, NLI 등)
[CLS] 문장A [SEP] 문장B [SEP]

# Embedding
최종 임베딩 = Token Emb + Segment Emb + Position Emb
```

---

## 💡 Self-Attention의 진가

### 양방향 이해의 메커니즘

```python
# "나는 밥을 먹었다"에서 "밥을" 이해하기

# Query: "밥을"이 다른 단어들을 얼마나 볼까?
Q = W_q @ 밥을_embedding

# Key: 각 단어가 "밥을"에게 얼마나 중요할까?
K = W_k @ [나는, 밥을, 먹었다]_embeddings

# Attention Score 계산
scores = softmax(Q @ K^T / sqrt(d_k))
# scores = [0.2, 0.3, 0.5]
#          ↑    ↑    ↑
#         나는  밥을  먹었다
# "먹었다"와 연관성이 가장 높음!

# Value: 실제 정보
V = W_v @ [나는, 밥을, 먹었다]_embeddings

# 최종 출력
output = scores @ V
# "밥을" 표현에 "먹었다" 정보가 많이 반영됨
```

**핵심:**
- 모든 단어가 모든 단어를 동시에 참조
- 문맥에 따라 중요도 자동 계산
- 순방향/역방향 구분 없이 통합적 이해

---

## 🚀 학습 과정

### 사전학습 (Pretraining)

**데이터:**
```
Wikipedia: 2.5B words
BookCorpus: 800M words
총: 3.3B words (33억 단어)

→ 모두 라벨링 없이 Self-Supervised로 학습!
```

**학습 목표:**
```python
Total_Loss = MLM_Loss + NSP_Loss

# 동시에 최적화
# - MLM: 문맥 이해, 단어 의미 학습
# - NSP: 문장 관계 학습
```

**학습 환경:**
- GPU: TPU v3 (64개)
- 학습 시간: 약 4일
- Batch size: 256

### Fine-tuning

**다양한 Task에 적용:**

```python
# 1. 텍스트 분류 (감정 분석 등)
[CLS] 문장 [SEP]
→ [CLS] 토큰 출력 → Classifier

# 2. 질의응답 (QA)
[CLS] 질문 [SEP] 문서 [SEP]
→ 각 토큰에서 시작/끝 위치 예측

# 3. 개체명 인식 (NER)
[CLS] 문장 [SEP]
→ 각 토큰마다 라벨 예측

# 4. 자연어 추론 (NLI)
[CLS] 전제 [SEP] 가설 [SEP]
→ [CLS]로 Entailment/Contradiction/Neutral 분류
```

**Fine-tuning 특징:**
- 사전학습 가중치로 시작
- Task별 마지막 레이어만 추가
- 전체 모델을 작은 learning rate로 재학습
- 보통 2-4 epoch이면 충분

---

## 📊 BERT의 영향

### 성능 향상

```
BERT 이전 (2018.9):
- GLUE 벤치마크: 평균 70-75%

BERT 등장 (2018.10):
- GLUE 벤치마크: 평균 80%+
- 11개 NLP 태스크 중 11개 모두 SOTA

→ NLP의 ImageNet 모멘트!
```

### 파생 모델들

**BERT 이후 쏟아진 개선 모델:**

| 모델 | 연도 | 주요 개선 |
|------|------|----------|
| **RoBERTa** | 2019 | NSP 제거, 더 긴 학습, 더 큰 배치 |
| **ALBERT** | 2019 | 파라미터 공유로 경량화 |
| **ELECTRA** | 2020 | Replaced Token Detection (더 효율적) |
| **DistilBERT** | 2019 | Knowledge Distillation으로 50% 경량화 |

---

## 🔍 기존 모델과 비교

### ELMo vs GPT vs BERT

| 항목 | ELMo | GPT-1 | BERT |
|------|------|-------|------|
| **구조** | Bi-LSTM | Transformer Decoder | Transformer Encoder |
| **방향** | 독립적 양방향 | 단방향 (→) | 통합적 양방향 (↔) |
| **사전학습** | LM (양방향 따로) | LM (단방향) | MLM + NSP |
| **특화** | 문맥 표현 | 생성 | 이해 |
| **병렬화** | 어려움 (LSTM) | 쉬움 | 쉬움 |

### Transfer Learning 관점

```
CV (Computer Vision):
2012: AlexNet → ImageNet 사전학습
→ Transfer Learning 보편화

NLP:
2013-2017: Word2Vec, GloVe (단어 수준만)
2018: BERT → 문맥 기반 Transfer Learning
→ NLP의 Transfer Learning 시대 개막!
```

---

## 💻 실전 코드 예시

### 기본 사용법

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# 1. 모델 & 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2  # Binary classification
)

# 2. 입력 준비
text = "This movie is great!"
inputs = tokenizer(
    text,
    padding=True,
    truncation=True,
    return_tensors="pt"
)

# 3. 예측
outputs = model(**inputs)
predictions = torch.softmax(outputs.logits, dim=-1)
print(predictions)  # [부정 확률, 긍정 확률]
```

### Fine-tuning 예시

```python
from transformers import BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

# 데이터셋 로드
dataset = load_dataset("imdb")

# 토크나이징
def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True)

dataset = dataset.map(tokenize, batched=True)

# 모델
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

# 학습 설정
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    learning_rate=2e-5,  # BERT Fine-tuning은 작은 lr
    warmup_steps=500,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
)

# 학습
trainer.train()
```

### 한국어 BERT 사용

```python
# KoBERT, KoELECTRA, klue/bert 등

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# KLUE BERT
tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")
model = AutoModelForSequenceClassification.from_pretrained(
    "klue/bert-base",
    num_labels=17  # 횬태님 문서 분류 17개 클래스
)

# 사용법은 영어 BERT와 동일!
text = "이 영화 정말 재미있어요"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
```

---

## ⚡ 실무 팁

### 1. Fine-tuning 하이퍼파라미터

```python
# 일반적인 추천값
learning_rate = 2e-5  # BERT는 작게! (1e-5 ~ 5e-5)
batch_size = 16 or 32
epochs = 2-4  # 보통 3epoch이면 충분
warmup_ratio = 0.1  # 전체 step의 10%

# 작은 데이터셋 (<5000):
epochs = 3-5
learning_rate = 3e-5

# 큰 데이터셋 (>100000):
epochs = 2-3
learning_rate = 2e-5
```

### 2. 메모리 절약 팁

```python
# Gradient Checkpointing
model.gradient_checkpointing_enable()  # 메모리 절반

# Mixed Precision (FP16)
training_args = TrainingArguments(
    fp16=True,  # GPU 메모리 절반
)

# Gradient Accumulation
training_args = TrainingArguments(
    per_device_train_batch_size=8,
    gradient_accumulation_steps=4,  # effective batch = 32
)
```

### 3. 입력 길이 주의

```python
# BERT 최대 토큰: 512
# 길이 초과 시 자동 truncation

tokenizer(
    text,
    max_length=512,
    truncation=True,  # 긴 텍스트 자르기
    padding='max_length',  # 짧은 텍스트 패딩
)
```

### 4. [CLS] 토큰 활용

```python
# 문장 전체 표현 추출
outputs = model(**inputs, output_hidden_states=True)
cls_embedding = outputs.hidden_states[-1][:, 0, :]  # [CLS] 토큰
# → 문장 임베딩으로 사용 (검색, 유사도 계산 등)
```

---

## 🎯 BERT의 한계

### 1. 생성 불가능
```python
# BERT는 Encoder-only
# 텍스트 생성(generation)에는 부적합
# → GPT 계열 사용 권장
```

### 2. 긴 문맥 처리 한계
```python
# 최대 512 토큰
# 논문, 책 전체 같은 긴 문서 처리 어려움
# → Longformer, BigBird 등 대안 모델 사용
```

### 3. 계산 비용
```python
# Self-Attention의 복잡도: O(n²)
# 긴 시퀀스에서 매우 느림
# → DistilBERT, ALBERT 등 경량화 모델 고려
```

### 4. NSP의 비효율
```python
# 후속 연구에서 NSP 효과 미미 발견
# RoBERTa, ELECTRA 등은 NSP 제거
```

---

## 📚 핵심 요약

### BERT를 한 문장으로

> "Masked Language Model로 Self-Supervised 학습을 통해 양방향 문맥을 이해하는 Transformer Encoder 기반 사전학습 모델"

### BERT의 3대 혁신

1. **구조**: Self-Attention 기반 진짜 양방향
2. **학습**: Self-Supervised (자동 라벨 생성)
3. **전이**: Pretrain-Finetune 패러다임 대중화

### 기억할 핵심

- ✅ **Encoder-only** 구조 (이해 특화)
- ✅ **MLM** (15% 마스킹 → 예측)
- ✅ **Self-Supervised** (무한한 학습 데이터)
- ✅ **양방향** (Self-Attention으로 통합적 문맥)
- ✅ **Transfer Learning** (Pretrain → Finetune)
- ✅ **[CLS]** 토큰 (문장 전체 표현)
- ✅ **Fine-tuning** (모든 NLP 태스크에 적용 가능)

### 언제 BERT를 쓸까?

**✅ BERT 추천:**
- 텍스트 분류 (감정 분석, 스팸 필터)
- 질의응답 (QA)
- 개체명 인식 (NER)
- 자연어 추론 (NLI)
- 문장 유사도, 검색

**❌ BERT 비추천:**
- 텍스트 생성 → GPT 계열
- 매우 긴 문서 → Longformer, BigBird
- 실시간 처리 (속도 중요) → DistilBERT, ALBERT

---

## 🔗 참고자료

### 논문
- **BERT 원논문:** [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) (2018)
- **Attention 메커니즘:** [Attention is All You Need](https://arxiv.org/abs/1706.03762) (2017)

### 구현
- **Hugging Face Transformers:** https://github.com/huggingface/transformers
- **공식 BERT (TensorFlow):** https://github.com/google-research/bert

### 튜토리얼
- [Hugging Face BERT 문서](https://huggingface.co/docs/transformers/model_doc/bert)
- [Jay Alammar: The Illustrated BERT](http://jalammar.github.io/illustrated-bert/)

---

**마지막 업데이트:** 2025-11-18  

> "BERT는 NLP의 ImageNet 모멘트를 만들었다. Pretrain-Finetune이 이제 NLP의 표준이다."