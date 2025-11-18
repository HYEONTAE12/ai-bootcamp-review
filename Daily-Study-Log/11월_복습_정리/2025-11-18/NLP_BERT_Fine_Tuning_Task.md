# BERT Fine-tuning Tasks 가이드

## 📌 Fine-tuning 개요

### 기본 원리

**핵심 아이디어:**
> 사전학습된 BERT에 **테스크별 레이어 1-2개만 추가**하고, 전체를 작은 learning rate로 재학습

```
Pretrained BERT (함께 학습됨, 고정 X)
     ↓
+ Task-specific Head (새로 추가, 1-2 layers)
     ↓
Task Output
```

### 공통 구조

**전체 프로세스:**

```python
# 1. Pretrained BERT 로드
model = BertForTaskXXX.from_pretrained('bert-base-uncased')
# → BERT + Task-specific Head 자동 생성

# 2. 데이터 준비 및 Fine-tuning
# → BERT 가중치 + Head 모두 학습

# 3. Task 수행
# → 학습된 모델로 예측
```

**공통 원칙:**

| 항목 | 설정 |
|------|------|
| **Learning Rate** | 2e-5 ~ 5e-5 (작게!) |
| **Epochs** | 2 ~ 4 (짧게!) |
| **Batch Size** | 16 ~ 32 |
| **Warmup** | 전체 step의 10% |
| **Optimizer** | AdamW |

**왜 작은 lr과 짧은 epoch?**
- BERT는 이미 학습된 모델
- 너무 많이 학습하면 Pretrain 지식 손실 (Catastrophic Forgetting)
- Task-specific Head만 주로 학습되도록

---

## 🎯 4가지 주요 Fine-tuning Tasks

### Task 비교표

| Task | 입력 형식 | 사용 토큰 | Head 구조 | 출력 |
|------|---------|---------|----------|------|
| **문장 분류** | `[CLS] 문장 [SEP]` | [CLS]만 | Linear(768 → labels) | 클래스 |
| **토큰 분류** | `[CLS] 토큰들 [SEP]` | 모든 토큰 | Linear(768 → labels) × 각 토큰 | 토큰별 라벨 |
| **QA** | `[CLS] Q [SEP] Doc [SEP]` | 모든 토큰 | 2개 Linear(768 → 1) | 시작/끝 위치 |
| **문장 쌍** | `[CLS] A [SEP] B [SEP]` | [CLS]만 | Linear(768 → labels) | 관계 |

---

## 1️⃣ 문장 분류 (Sequence Classification)

### 개념

**정의:** 문장 하나 → 하나의 클래스 예측

**용도:**
- 감정 분석 (긍정/부정/중립)
- 스팸 필터링
- 주제 분류
- 독성 댓글 탐지

### 구조

```
입력: [CLS] This movie is great [SEP]
       ↓
    [BERT Encoder]
       ↓
[CLS][토큰1][토큰2][토큰3][토큰4][SEP]
  ↓
[CLS] 토큰만 추출 (문장 전체 표현)
  ↓
[Linear: 768 → num_labels]
  ↓
[Softmax]
  ↓
클래스 확률: [0.1, 0.9] → 긍정!
```

### 핵심 포인트

**왜 [CLS] 토큰만?**
- BERT 사전학습 시 [CLS]가 문장 전체를 요약하도록 학습됨
- NSP(Next Sentence Prediction) 태스크에서 [CLS] 사용
- 문장 레벨 표현을 담고 있음

**Head 구조:**
```python
cls_output = bert_output[:, 0, :]  # [batch, 768]
logits = Linear(cls_output)         # [batch, num_labels]
probs = Softmax(logits)
```

### 간단 코드

```python
from transformers import BertForSequenceClassification

# 모델 (BERT + Classification Head)
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2  # 긍정/부정
)

# 예측
inputs = tokenizer("This movie is great", return_tensors="pt")
outputs = model(**inputs)
prediction = torch.argmax(outputs.logits, dim=-1)
```

---

## 2️⃣ 토큰 분류 (Token Classification)

### 개념

**정의:** 각 토큰마다 라벨 예측

**용도:**
- NER (Named Entity Recognition): 개체명 인식
- POS (Part-of-Speech) Tagging: 품사 태깅
- Chunking: 구문 분석

### 구조

```
입력: [CLS] Elon Musk founded Tesla [SEP]

    [BERT Encoder]
       ↓
[CLS][Elon][Musk][founded][Tesla][SEP]
  ↓    ↓     ↓      ↓       ↓     ↓
각 토큰마다 Linear 적용
  ↓    ↓     ↓      ↓       ↓
  O  B-PER I-PER    O     B-ORG
```

### NER 라벨 체계 (BIO)

**BIO Tagging:**
```
B (Begin):  개체의 시작
I (Inside): 개체의 중간/끝
O (Outside): 개체 아님

예시:
"Elon Musk founded Tesla Inc"
  ↓
B-PER I-PER   O    B-ORG I-ORG
```

**주요 개체 타입:**
- PER: Person (인명)
- ORG: Organization (조직명)
- LOC: Location (지명)
- DATE: 날짜
- MISC: 기타

### 핵심 포인트

**왜 모든 토큰?**
- 각 토큰이 어떤 개체인지 개별적으로 판단
- 토큰 레벨 예측 필요

**Head 구조:**
```python
# 모든 토큰의 출력 사용
token_outputs = bert_output  # [batch, seq_len, 768]

# 각 토큰마다 분류
logits = Linear(token_outputs)  # [batch, seq_len, num_labels]
predictions = torch.argmax(logits, dim=-1)
# 각 위치의 라벨 예측
```

**[CLS]와 [SEP]은?**
- 보통 예측하지 않거나 'O' 라벨
- Loss 계산 시 제외하는 경우 많음

### 간단 코드

```python
from transformers import BertForTokenClassification

# 모델
model = BertForTokenClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=9  # O, B-PER, I-PER, B-ORG, ...
)

# 예측
inputs = tokenizer("Elon Musk founded Tesla", return_tensors="pt")
outputs = model(**inputs)
predictions = torch.argmax(outputs.logits, dim=-1)
# 각 토큰의 라벨: [O, B-PER, I-PER, O, B-ORG]
```

---

## 3️⃣ 질의응답 (Question Answering)

### 개념

**정의:** 질문과 문서가 주어지면, 문서에서 답의 위치 찾기

**용도:**
- SQuAD (Stanford Question Answering Dataset)
- 문서 기반 QA
- Reading Comprehension

### 구조

```
입력: [CLS] Who founded Tesla [SEP] Tesla was founded by Elon Musk in 2003 [SEP]
토큰:   0     1    2      3      4     5    6    7      8   9    10   11  12  13

    [BERT Encoder]
       ↓
각 토큰의 출력
       ↓
Start Head: 각 토큰이 답 시작일 확률
End Head:   각 토큰이 답 끝일 확률
       ↓
Start: 토큰 9 (Elon) ← 가장 높은 확률
End:   토큰 10 (Musk) ← 가장 높은 확률
       ↓
답: "Elon Musk"
```

### 핵심 포인트

**두 개의 Head:**
```python
# Start Position Head
start_logits = Linear_start(bert_output)  # [batch, seq_len]
start_probs = Softmax(start_logits)
# 각 토큰이 답의 시작일 확률

# End Position Head
end_logits = Linear_end(bert_output)  # [batch, seq_len]
end_probs = Softmax(end_logits)
# 각 토큰이 답의 끝일 확률

# 답 추출
start_idx = argmax(start_logits)
end_idx = argmax(end_logits)
answer = tokens[start_idx:end_idx+1]
```

**제약 조건:**
- `start_idx ≤ end_idx` (시작이 끝보다 앞)
- 보통 질문 부분([SEP] 이전)은 제외
- `end_idx - start_idx < max_answer_length` (너무 긴 답 방지)

**답이 없는 경우:**
```
질문: "What is Google's founder?"
문서: "Tesla was founded by Elon Musk"

→ [CLS] 토큰을 start/end로 예측
→ "답 없음" 처리
```

### 입력 구성

```python
# 질문과 문서 분리
[CLS] 질문 [SEP] 문서 [SEP]
  ↑          ↑       ↑
Segment 0  경계  Segment 1

# Segment Embedding:
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
 ↑ 질문 부분     ↑ 문서 부분

# 답은 항상 Segment 1 (문서)에서만 찾음
```

### 간단 코드

```python
from transformers import BertForQuestionAnswering

# 모델
model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

# 예측
question = "Who founded Tesla?"
context = "Tesla was founded by Elon Musk in 2003"
inputs = tokenizer(question, context, return_tensors="pt")

outputs = model(**inputs)
start_idx = torch.argmax(outputs.start_logits)
end_idx = torch.argmax(outputs.end_logits)

# 답 추출
answer = tokenizer.decode(inputs['input_ids'][0][start_idx:end_idx+1])
```

---

## 4️⃣ 문장 쌍 분류 (Sentence Pair Classification)

### 개념

**정의:** 두 문장의 관계 예측

**용도:**
- NLI (Natural Language Inference): 자연어 추론
- Paraphrase Detection: 패러프레이즈 탐지
- Semantic Similarity: 의미 유사도

### 구조

```
입력: [CLS] A man is playing guitar [SEP] A person is making music [SEP]
        ↓
    [BERT Encoder]
        ↓
[CLS] 토큰 추출 (두 문장의 관계 표현)
        ↓
[Linear: 768 → 3]
        ↓
[Softmax]
        ↓
[0.85, 0.05, 0.10]
   ↑
Entailment (함의)
```

### NLI (자연어 추론)

**3가지 관계:**

**1. Entailment (함의)**
```
전제(A)가 참이면 가설(B)도 반드시 참

A: "모든 고양이는 동물이다"
B: "내 고양이는 동물이다"
→ Entailment ✓
```

**2. Contradiction (모순)**
```
전제(A)가 참이면 가설(B)는 거짓

A: "그는 집에 있다"
B: "그는 학교에 있다"
→ Contradiction ✗
```

**3. Neutral (중립)**
```
전제(A)로 가설(B)의 참/거짓 판단 불가

A: "그는 학생이다"
B: "그는 키가 크다"
→ Neutral ?
```

### 핵심 포인트

**왜 [CLS] 토큰?**
- NSP 사전학습에서 [CLS]가 문장 쌍 관계 학습
- 두 문장의 상호작용이 [CLS]에 집약됨

**[SEP] 토큰의 역할:**
```
[CLS] 문장A [SEP] 문장B [SEP]
            ↑
      두 문장 구분 표시
      Segment Embedding도 다름
```

**다른 활용:**

**Paraphrase Detection (패러프레이즈):**
```
A: "He is a student"
B: "He studies at school"
→ Paraphrase (같은 의미) or Not
```

**Semantic Similarity (의미 유사도):**
```
A: "Dog is running"
B: "Cat is sleeping"
→ Similarity Score: 0.3 (낮음)

A: "Dog is running"
B: "Puppy is running"
→ Similarity Score: 0.9 (높음)
```

### 간단 코드

```python
from transformers import BertForSequenceClassification

# 모델
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=3  # Entailment, Contradiction, Neutral
)

# 예측
premise = "A man is playing guitar"
hypothesis = "A person is making music"
inputs = tokenizer(premise, hypothesis, return_tensors="pt")

outputs = model(**inputs)
prediction = torch.argmax(outputs.logits, dim=-1)
# 0: Entailment, 1: Contradiction, 2: Neutral
```

---

## 🔧 Fine-tuning 실전 팁

### Learning Rate 전략

**기본 설정:**
```python
learning_rate = 2e-5  # 또는 3e-5, 5e-5
# BERT는 이미 학습됨 → 작게!
```

**Layer-wise Learning Rate Decay:**
```python
# 아래층(임베딩): 더 작은 lr (범용 지식 보존)
# 위층(출력): 더 큰 lr (태스크 특화)

optimizer = AdamW([
    {'params': model.bert.embeddings.parameters(), 'lr': 1e-5},
    {'params': model.bert.encoder.layer[:6].parameters(), 'lr': 2e-5},
    {'params': model.bert.encoder.layer[6:].parameters(), 'lr': 3e-5},
    {'params': model.classifier.parameters(), 'lr': 5e-5},
])
```

### Warmup

**목적:** 초기에 작은 lr로 시작 → 점진적 증가

```python
# 전체 step의 10%를 warmup
warmup_steps = total_steps * 0.1

# Scheduler
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=warmup_steps,
    num_training_steps=total_steps
)
```

### 데이터 크기별 가이드

| 데이터 크기 | Epochs | Learning Rate | Batch Size |
|------------|--------|---------------|-----------|
| 소규모 (<5K) | 5-10 | 3e-5 ~ 5e-5 | 8-16 |
| 중규모 (5K-50K) | 3-5 | 2e-5 ~ 3e-5 | 16-32 |
| 대규모 (>50K) | 2-3 | 1e-5 ~ 2e-5 | 32-64 |

### Overfitting 방지

```python
# 1. Early Stopping
# validation loss가 증가하면 중단

# 2. Dropout
model.config.hidden_dropout_prob = 0.1
model.config.attention_probs_dropout_prob = 0.1

# 3. Weight Decay
optimizer = AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)

# 4. Data Augmentation
# Back-translation, synonym replacement 등
```

---

## 📊 Task별 성능 벤치마크

### GLUE Benchmark (BERT-base)

| Task | Type | Metric | BERT Score |
|------|------|--------|-----------|
| **MNLI** | 문장 쌍 (NLI) | Accuracy | 84.6% |
| **QQP** | 문장 쌍 (Paraphrase) | Accuracy | 71.2% |
| **QNLI** | 문장 쌍 (QA→NLI) | Accuracy | 90.5% |
| **SST-2** | 문장 분류 (감정) | Accuracy | 93.5% |
| **CoLA** | 문장 분류 (문법) | Matthews Corr | 52.1 |
| **STS-B** | 문장 쌍 (유사도) | Pearson Corr | 85.8 |
| **MRPC** | 문장 쌍 (Paraphrase) | F1 | 88.9% |
| **RTE** | 문장 쌍 (Entailment) | Accuracy | 66.4% |

### SQuAD (QA)

| Model | SQuAD 1.1 (EM/F1) | SQuAD 2.0 (EM/F1) |
|-------|------------------|------------------|
| **BERT-base** | 80.8 / 88.5 | 73.7 / 76.3 |
| **BERT-large** | 84.1 / 90.9 | 78.7 / 81.9 |
| Human | 82.3 / 91.2 | 86.8 / 89.5 |

---

## 🎯 핵심 정리

### Task 선택 가이드

```
입력 1개 문장 + 클래스 예측
→ 문장 분류 (Sequence Classification)

입력 1개 문장 + 각 토큰 라벨
→ 토큰 분류 (Token Classification)

입력 질문 + 문서 → 답 위치
→ QA (Question Answering)

입력 2개 문장 + 관계 예측
→ 문장 쌍 분류 (Sentence Pair Classification)
```

### [CLS] vs 모든 토큰

**[CLS] 토큰만 사용:**
- 문장 분류
- 문장 쌍 분류
- 이유: 문장 전체 표현 필요

**모든 토큰 사용:**
- 토큰 분류 (NER)
- QA (위치 찾기)
- 이유: 토큰별 예측 필요

### Fine-tuning 체크리스트

```python
✅ Pretrained BERT 로드
✅ Task-specific Head 자동 추가됨
✅ Learning rate: 2e-5 (작게!)
✅ Epochs: 2-4 (짧게!)
✅ Warmup: 10%
✅ Batch size: 16-32
✅ Gradient clipping: 1.0
✅ Weight decay: 0.01
✅ Early stopping 설정
```

### 일반적인 Fine-tuning 코드 패턴

```python
from transformers import BertForXXX, Trainer, TrainingArguments

# 1. 모델 로드 (BERT + Task Head)
model = BertForXXX.from_pretrained(
    'bert-base-uncased',
    num_labels=num_labels
)

# 2. 학습 설정
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    learning_rate=2e-5,
    warmup_steps=500,
    weight_decay=0.01,
    logging_steps=100,
    eval_steps=500,
    save_steps=500,
    load_best_model_at_end=True,
)

# 3. Trainer로 학습
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

---

## 📚 참고자료

### 논문
- **BERT:** [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) (2018)
- **SQuAD:** [SQuAD: 100,000+ Questions for Machine Comprehension](https://arxiv.org/abs/1606.05250) (2016)
- **GLUE:** [GLUE: A Multi-Task Benchmark](https://arxiv.org/abs/1804.07461) (2018)

### 벤치마크
- **GLUE:** https://gluebenchmark.com/
- **SQuAD:** https://rajpurkar.github.io/SQuAD-explorer/
- **SuperGLUE:** https://super.gluebenchmark.com/

### 실습 자료
- **Hugging Face Course:** https://huggingface.co/course
- **BERT Fine-tuning Tutorial:** https://mccormickml.com/2019/07/22/BERT-fine-tuning/

---

**마지막 업데이트:** 2025-11-18  

> "BERT Fine-tuning은 간단하다: Pretrained BERT + Task Head 1-2개 + 작은 lr로 짧게 학습. 이것이 전부다."