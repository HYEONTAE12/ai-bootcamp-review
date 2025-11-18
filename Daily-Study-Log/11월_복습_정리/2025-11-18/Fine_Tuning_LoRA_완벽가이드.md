# LoRA (Low-Rank Adaptation) 완벽 가이드

## 📌 목차
1. [LoRA란 무엇인가?](#lora란-무엇인가)
2. [등장 배경](#등장-배경)
3. [핵심 원리](#핵심-원리)
4. [수학적 이해](#수학적-이해)
5. [Rank 설정 가이드](#rank-설정-가이드)
6. [실전 코드](#실전-코드)
7. [장단점](#장단점)
8. [실무 팁](#실무-팁)
9. [참고자료](#참고자료)

---

## LoRA란 무엇인가?

**LoRA (Low-Rank Adaptation of Large Language Models)**
- 대규모 사전학습 모델을 **효율적으로** Fine-tuning하는 기법
- 전체 파라미터를 학습하지 않고 **극히 일부만** 학습
- Microsoft Research에서 2021년 발표
- 현재 LLM 커스터마이징의 **사실상 표준**

### 한 줄 요약
> "거대 모델의 1% 파라미터만 학습해서 Full Fine-tuning과 동일한 성능을 달성하는 기법"

---

## 등장 배경

### 문제 상황
```
GPT-3: 175B 파라미터
BERT-Large: 340M 파라미터

Fine-tuning 시 필요한 것:
- 엄청난 GPU 메모리 (수십~수백GB)
- 긴 학습 시간
- 높은 비용 💸
```

### 기존 해결책들의 한계
| 방법 | 문제점 |
|------|--------|
| Adapter Layers | 추론 속도 느림 |
| Prefix Tuning | 입력 시퀀스 길이 제한 |
| Prompt Tuning | 성능이 살짝 떨어짐 |

### LoRA의 혁신
- ✅ 추론 속도 그대로 (오버헤드 없음)
- ✅ 메모리 효율 극대화
- ✅ 성능 손실 거의 없음
- ✅ 여러 Task용 Adapter를 쉽게 관리

---

## 핵심 원리

### 기본 아이디어

**관찰:** Fine-tuning 시 가중치 변화는 "저차원(Low-Rank)" 구조를 가진다

```python
# 기존 Fine-tuning
W_new = W_original + ΔW
# ΔW를 전부 학습 (파라미터 수백만 개)

# LoRA
W_new = W_original + A × B
# A, B만 학습 (파라미터 수천 개)
# W_original은 freeze (얼림)
```

### 시각적 비유

**벽(모델) + 스티커(LoRA) 비유:**
```
기존 방식: 벽 전체를 다시 칠함 🎨
→ 페인트 많이 필요, 시간 오래 걸림

LoRA: 벽은 그대로, 작은 스티커만 붙임 🏷️
→ 스티커만 바꾸면 됨, 빠르고 효율적
```

**JPEG 압축 비유:**
```
1000×1000 이미지 저장:
- 원본: 1,000,000 픽셀 정보
- JPEG: 훨씬 적은 정보로 압축
  → 눈으로는 거의 구분 안 됨!

LoRA도 마찬가지로 "가중치 변화"를 압축!
```

---

## 수학적 이해

### 행렬 분해

**원래 가중치 행렬:**
```
W ∈ ℝ^(d×k)  (예: 768×768)
```

**LoRA 분해:**
```
ΔW = A × B

A ∈ ℝ^(d×r)  (예: 768×8)
B ∈ ℝ^(r×k)  (예: 8×768)

여기서 r ≪ min(d, k)  (rank, 매우 작은 값)
```

### 파라미터 수 비교

**예시: BERT의 한 Attention Layer (768 차원)**

| 방법 | 파라미터 수 | 비율 |
|------|------------|------|
| Full Fine-tuning | 768 × 768 = 589,824 | 100% |
| LoRA (r=8) | 768×8 + 8×768 = 12,288 | 2.1% |
| LoRA (r=4) | 768×4 + 4×768 = 6,144 | 1.0% |
| LoRA (r=16) | 768×16 + 16×768 = 24,576 | 4.2% |

### Forward Pass

```python
# Pretrained 모델
h = W_0 @ x  # W_0는 freeze

# LoRA 적용
h = W_0 @ x + (B @ A) @ x
    ↑ 고정     ↑ 학습 가능

# 실제로는 s = α/r (scaling factor) 적용
h = W_0 @ x + (α/r) * (B @ A) @ x
```

---

## Rank 설정 가이드

### Rank(r)란?

**정의:** 행렬 분해 시 중간 차원의 크기

```
A: d × r
B: r × k
rank(A×B) ≤ r
```

**의미:**
- rank가 클수록 → 표현력 ↑, 파라미터 ↑
- rank가 작을수록 → 효율성 ↑, 표현력 ↓

### 일반적인 기본값

| 상황 | 권장 rank |
|------|-----------|
| NLP (LLM) | 8 ~ 16 |
| CV (이미지) | 4 ~ 8 |
| 작은 모델 (BERT-base) | 4 ~ 8 |
| 큰 모델 (GPT-3급) | 16 ~ 32 |
| 간단한 Task | 4 |
| 복잡한 Task | 16 ~ 32 |

### Task 복잡도별 선택

```python
# 간단한 Task (감정 분석, 스팸 필터)
r = 4

# 중간 복잡도 (텍스트 분류, 개체명 인식)
r = 8

# 복잡한 Task (번역, 요약, 질의응답)
r = 16

# 매우 복잡하거나 도메인 전환 큰 경우 (의료→법률)
r = 32 ~ 64
```

### 실험적 선택 방법

**1단계: Grid Search**
```python
for rank in [4, 8, 16, 32]:
    config = LoRAConfig(r=rank)
    model = get_peft_model(base_model, config)
    accuracy = train_and_evaluate(model)
    print(f"rank={rank}: {accuracy}")
```

**2단계: 결과 분석**
```
일반적인 패턴:
rank=4:  accuracy 85.0%
rank=8:  accuracy 89.0%  ← Sweet spot!
rank=16: accuracy 89.2%  (큰 차이 없음)
rank=32: accuracy 89.1%  (오히려 과적합)

→ rank=8 선택!
```

### 실무 결정 플로우

```
시작
 ↓
rank=8로 시작
 ↓
성능 만족? ─YES→ 완료!
 ↓NO
 ├─ 메모리 여유 있음? ─YES→ rank=16 시도
 │                         ↓
 │                     개선됨? ─YES→ 완료!
 │                         ↓NO
 │                     rank=8이 최적
 │
 └─ 메모리 부족? ─YES→ rank=4 시도
                      ↓
                  충분한 성능? ─YES→ 완료!
                      ↓NO
                  더 작은 모델 고려
```

### 논문 실험 결과

**GPT-3 (175B) Fine-tuning (LoRA 원논문):**
```
rank=1:  성능 낮음 (baseline 대비 -5%)
rank=4:  decent 성능 (baseline 대비 -1%)
rank=8:  excellent 성능 (baseline과 동등)
rank=64: excellent 성능 (rank=8과 거의 동일)

결론: rank=8이면 충분!
더 키워도 성능 향상 미미
```

---

## 실전 코드

### 기본 사용법 (Hugging Face PEFT)

```python
from transformers import AutoModelForSequenceClassification
from peft import LoRAConfig, get_peft_model, TaskType

# 1. 사전학습 모델 로드
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

# 2. LoRA Config 설정
lora_config = LoRAConfig(
    r=8,                              # rank
    lora_alpha=16,                    # scaling factor (보통 r*2)
    target_modules=["query", "value"], # 적용할 모듈
    lora_dropout=0.1,                 # dropout
    bias="none",                      # bias 학습 여부
    task_type=TaskType.SEQ_CLS        # task 타입
)

# 3. LoRA 적용
model = get_peft_model(model, lora_config)

# 4. 학습 가능한 파라미터 확인
model.print_trainable_parameters()
# 출력: trainable params: 294,912 || all params: 109,483,778 || trainable%: 0.27%
```

### NLP - 텍스트 분류

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from peft import LoRAConfig, get_peft_model
from datasets import load_dataset

# 데이터 로드
dataset = load_dataset("imdb")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True)

dataset = dataset.map(tokenize, batched=True)

# 모델 + LoRA
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

lora_config = LoRAConfig(
    r=8,
    lora_alpha=16,
    target_modules=["query", "value"],
    lora_dropout=0.1,
    bias="none",
    task_type="SEQ_CLS"
)

model = get_peft_model(model, lora_config)

# 학습
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    learning_rate=3e-4,  # LoRA는 learning rate 크게 설정
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
)

trainer.train()
```

### CV - 이미지 분류

```python
from transformers import AutoImageProcessor, AutoModelForImageClassification
from peft import LoRAConfig, get_peft_model

# 이미지 모델 로드
model = AutoModelForImageClassification.from_pretrained(
    "microsoft/resnet-50",
    num_labels=10,
    ignore_mismatched_sizes=True
)

# LoRA 설정 (CV용)
lora_config = LoRAConfig(
    r=4,  # CV는 보통 rank 작게
    lora_alpha=8,
    target_modules=["query", "value", "key"],  # Attention modules
    lora_dropout=0.1,
    bias="none",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

### 고급 설정

```python
lora_config = LoRAConfig(
    r=16,
    lora_alpha=32,
    
    # 특정 레이어만 선택
    target_modules=[
        "query",
        "key", 
        "value",
        "dense"  # FFN layer도 포함
    ],
    
    # 특정 레이어만 제외
    # modules_to_save=["classifier"],  # classifier는 전체 학습
    
    lora_dropout=0.05,
    bias="none",  # "none", "all", "lora_only"
    
    # Initialization
    init_lora_weights=True,  # Kaiming uniform으로 초기화
)
```

### 학습 후 모델 저장 및 로드

```python
# 저장 (LoRA weights만 저장됨 - 용량 작음!)
model.save_pretrained("./my_lora_model")

# 로드
from peft import PeftModel

base_model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
model = PeftModel.from_pretrained(base_model, "./my_lora_model")

# 추론 모드
model.eval()
```

### 여러 LoRA Adapter 관리

```python
# Task 1용 LoRA 학습
lora_config_task1 = LoRAConfig(r=8, ...)
model = get_peft_model(base_model, lora_config_task1)
# ... 학습 ...
model.save_pretrained("./lora_task1")

# Task 2용 LoRA 학습
lora_config_task2 = LoRAConfig(r=8, ...)
model = get_peft_model(base_model, lora_config_task2)
# ... 학습 ...
model.save_pretrained("./lora_task2")

# 사용 시 갈아끼우기
from peft import PeftModel

# Task 1 사용
model = PeftModel.from_pretrained(base_model, "./lora_task1")

# Task 2로 전환
model.load_adapter("./lora_task2", adapter_name="task2")
model.set_adapter("task2")
```

### LoRA + 양자화 (QLoRA)

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoRAConfig, get_peft_model

# 4-bit 양자화 설정
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

# 양자화된 모델 로드
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto"
)

# LoRA 적용
lora_config = LoRAConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
# 7B 모델을 노트북 GPU에서도 학습 가능!
```

---

## 장단점

### ✅ 장점

**1. 메모리 효율성**
```
BERT-base Full Fine-tuning: ~16GB GPU
BERT-base LoRA:            ~4GB GPU
→ 4배 절약!
```

**2. 학습 속도**
```
학습 파라미터가 적음 → 학습 속도 빠름
Full Fine-tuning: 3시간
LoRA:            1시간
```

**3. 성능 손실 거의 없음**
```
대부분의 Task에서 Full Fine-tuning과 동등
(논문: 평균 0.5% 이내 차이)
```

**4. 모듈성**
```
원본 모델 1개 (10GB)
├── Task A LoRA (10MB)
├── Task B LoRA (10MB)
└── Task C LoRA (10MB)

→ Adapter만 갈아끼우면 됨!
```

**5. 추론 속도**
```
Adapter 방식과 달리 추론 오버헤드 없음
배포 시 W + A×B를 미리 합쳐버리면 됨
```

**6. 과적합 방지**
```
파라미터 수가 적음 → 과적합 위험 감소
특히 데이터가 적을 때 유리
```

### ❌ 단점

**1. 완전히 새로운 도메인에는 부족할 수 있음**
```
예: 자연어 → 코드 생성
    이미지 → 의료 영상
→ 이런 경우 Full Fine-tuning이 나을 수 있음
```

**2. 하이퍼파라미터 민감도**
```
rank, alpha, target_modules 설정이 중요
잘못 설정하면 성능 하락 가능
```

**3. 극소량 데이터에서는 불리**
```
데이터가 100개 미만이면
표현력 부족으로 성능 저하 가능
```

**4. 일부 Task에서는 Full Fine-tuning이 여전히 우세**
```
연구 결과: 약 10-20% Task에서
Full Fine-tuning이 1-2% 더 좋음
```

---

## 실무 팁

### 🎯 언제 LoRA를 사용할까?

**✅ LoRA 추천:**
- GPU 메모리가 부족할 때
- 여러 Task를 동시에 관리해야 할 때
- 빠른 실험이 필요할 때
- 사전학습 모델과 비슷한 도메인일 때
- 프로덕션 배포 시 메모리 절약이 중요할 때

**❌ Full Fine-tuning 고려:**
- GPU 자원이 충분할 때
- 도메인이 완전히 다를 때 (자연어→코드)
- 최고 성능이 절대적으로 중요할 때
- 데이터가 극소량일 때

### 🔧 하이퍼파라미터 튜닝 팁

**1. rank (r)**
```python
# 기본 시작: r=8
# 성능 부족 → r=16
# 메모리 부족 → r=4

# 경험 법칙:
# rank를 2배 늘려도 성능이 0.5% 미만 향상되면 멈추기
```

**2. lora_alpha**
```python
# 일반적으로 lora_alpha = 2 * r
r=8  → lora_alpha=16
r=16 → lora_alpha=32

# alpha/r = scaling factor
# 보통 1~2 사이가 적당
```

**3. target_modules**
```python
# 최소: Query, Value만
target_modules=["query", "value"]

# 중간: Q, K, V 모두
target_modules=["query", "key", "value"]

# 최대: Attention + FFN
target_modules=["query", "key", "value", "dense", "intermediate"]

# 팁: 많이 추가할수록 성능↑, 메모리↑
# 보통 ["query", "value"]로 시작
```

**4. learning_rate**
```python
# LoRA는 Full Fine-tuning보다 learning rate 크게!
# Full Fine-tuning: 1e-5 ~ 5e-5
# LoRA:            1e-4 ~ 5e-4 (10배 정도 크게)
```

**5. lora_dropout**
```python
# 일반적으로 0.05 ~ 0.1
# 데이터 많으면: 0.05
# 데이터 적으면: 0.1
```

### 📊 성능 최적화 체크리스트

```python
# 1. Baseline 먼저 확인
lora_config = LoRAConfig(r=8, lora_alpha=16)
# → 성능 X%

# 2. rank 증가 실험
lora_config = LoRAConfig(r=16, lora_alpha=32)
# → 성능 향상 1% 이상? YES → 채택

# 3. target_modules 추가
target_modules=["query", "key", "value", "dense"]
# → 성능 향상? YES → 채택

# 4. learning_rate 튜닝
for lr in [1e-4, 3e-4, 5e-4]:
    # 실험
    
# 5. 앙상블
# 여러 seed로 학습 후 앙상블
```

### 🚀 메모리 최적화 팁

**1. Gradient Checkpointing**
```python
model.gradient_checkpointing_enable()
# 메모리 절반 감소, 속도 20% 느려짐
```

**2. Mixed Precision (FP16)**
```python
training_args = TrainingArguments(
    fp16=True,  # 메모리 절반
)
```

**3. Gradient Accumulation**
```python
training_args = TrainingArguments(
    per_device_train_batch_size=8,
    gradient_accumulation_steps=4,  # effective batch size = 32
)
```

**4. QLoRA (4-bit 양자화)**
```python
# 가장 강력! 70B 모델도 24GB GPU에서 가능
bnb_config = BitsAndBytesConfig(load_in_4bit=True, ...)
```

### 🎓 디버깅 팁

**파라미터 수 확인**
```python
model.print_trainable_parameters()
# trainable params: 294,912 || all params: 109,483,778 || trainable%: 0.27%

# 0.1% ~ 5% 사이면 적당
# 10% 넘으면 rank가 너무 큼
# 0.01% 이하면 rank가 너무 작음
```

**학습이 안 될 때**
```python
# 1. Learning rate 확인 (너무 작은지?)
# 2. LoRA weights가 업데이트 되는지 확인
for name, param in model.named_parameters():
    if param.requires_grad:
        print(name, param.grad)  # None이면 문제!
        
# 3. target_modules가 제대로 설정되었는지
model.base_model.model  # 확인
```

### 💡 실전 프로젝트 워크플로우

```python
# Phase 1: Quick Baseline (1시간)
lora_config = LoRAConfig(r=4, lora_alpha=8)
# → 빠르게 돌려서 파이프라인 검증

# Phase 2: Optimization (반나절)
for r in [4, 8, 16]:
    # Grid search
    # → Best rank 선정
    
# Phase 3: Fine-tuning (하루)
# Best config로 여러 실험
# - learning rate 튜닝
# - target_modules 조정
# - dropout 조정

# Phase 4: Ensemble (선택)
# 여러 seed로 학습 후 앙상블
```

---

## 비교: LoRA vs 다른 방법들

### LoRA vs Full Fine-tuning

| 항목 | LoRA | Full Fine-tuning |
|------|------|------------------|
| 학습 파라미터 | 0.1% ~ 5% | 100% |
| GPU 메모리 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 학습 속도 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 성능 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 추론 속도 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 모듈성 | ⭐⭐⭐⭐⭐ | ⭐ |

### LoRA vs Adapter Layers

| 항목 | LoRA | Adapter |
|------|------|---------|
| 추론 오버헤드 | 없음 ⭐⭐⭐⭐⭐ | 있음 ⭐⭐⭐ |
| 메모리 효율 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 구현 복잡도 | 간단 | 약간 복잡 |
| 성능 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### LoRA vs Prompt Tuning

| 항목 | LoRA | Prompt Tuning |
|------|------|---------------|
| 학습 파라미터 | 0.1% ~ 5% | 0.01% ~ 0.1% |
| 성능 | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 적용 범위 | 모든 모델 | 대규모 모델만 효과적 |
| 입력 제약 | 없음 | 시퀀스 길이 제한 |

---

## 주요 응용 분야

### 1. LLM 커스터마이징
```python
# ChatGPT, GPT-4 스타일 모델 Fine-tuning
# 회사 내부 데이터로 학습
base_model = "meta-llama/Llama-2-70b"
# LoRA로 효율적 학습
```

### 2. 도메인 Adaptation
```python
# 일반 모델 → 의료, 법률, 금융 도메인
# 적은 메모리로 전문 지식 주입
```

### 3. Stable Diffusion Fine-tuning
```python
# 이미지 생성 모델 커스터마이징
# 특정 스타일 학습 (DreamBooth + LoRA)
```

### 4. 다국어 모델
```python
# 영어 모델 → 한국어 적응
# LoRA로 한국어 성능 향상
```

### 5. Multi-task Learning
```python
# 하나의 base model
# 여러 task별 LoRA adapter
# 런타임에 갈아끼우기
```

---

## 자주 하는 실수

### ❌ 실수 1: Learning Rate를 Full Fine-tuning과 동일하게 설정
```python
# 잘못된 예
learning_rate = 2e-5  # Full Fine-tuning용

# 올바른 예
learning_rate = 3e-4  # LoRA는 더 크게!
```

### ❌ 실수 2: rank만 무작정 키우기
```python
# rank=64로 했는데 성능이 안 오름
# → rank=8이나 16으로 충분한 경우 많음
# → 메모리만 낭비
```

### ❌ 실수 3: target_modules 잘못 설정
```python
# 모델 구조 확인 필수!
print(model)  # 어떤 모듈이 있는지 확인

# BERT: "query", "value"
# GPT: "c_attn", "c_proj"
# LLaMA: "q_proj", "v_proj"
```

### ❌ 실수 4: 저장/로드 실수
```python
# LoRA weights만 저장됨!
model.save_pretrained("./lora")  # ✅

# 전체 모델 저장 (용량 큼)
torch.save(model, "./model.pt")  # ❌ 비효율적
```

### ❌ 실수 5: 추론 시 LoRA 안 머지
```python
# 배포 시 매번 A×B 계산 → 느림
# 미리 합쳐두기
model = model.merge_and_unload()  # ✅
```

---

## 최신 발전 동향 (2024-2025)

### QLoRA (Quantized LoRA)
```python
# 4-bit 양자화 + LoRA
# 70B 모델을 24GB GPU에서 학습 가능!
```

### AdaLoRA
```python
# rank를 layer마다 adaptive하게 조정
# 중요한 layer는 rank 크게, 덜 중요한 layer는 작게
```

### LoRA+
```python
# Learning rate를 A와 B에 다르게 적용
# 성능 소폭 향상
```

### DoRA (Weight-Decomposed LoRA)
```python
# 가중치를 magnitude와 direction으로 분해
# LoRA보다 안정적 학습
```

### Multi-LoRA
```python
# 여러 LoRA를 동시에 사용
# Task별로 다른 LoRA 조합
```

---

## 참고자료

### 논문
- **LoRA 원논문:** [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) (2021)
- **QLoRA:** [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) (2023)
- **AdaLoRA:** [Adaptive Budget Allocation for Parameter-Efficient Fine-Tuning](https://arxiv.org/abs/2303.10512) (2023)

### 공식 구현
- **Hugging Face PEFT:** https://github.com/huggingface/peft
- **Microsoft LoRA:** https://github.com/microsoft/LoRA

### 튜토리얼
- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft)
- [LoRA from Scratch 구현](https://github.com/rasbt/LLMs-from-scratch)

### 블로그
- [Hugging Face: LoRA 소개](https://huggingface.co/blog/lora)
- [Sebastian Raschka: Understanding LoRA](https://magazine.sebastianraschka.com/p/lora-and-dora-from-scratch)

---

## 요약 체크리스트

### ✅ LoRA 핵심 포인트
- [ ] LoRA는 전체 파라미터의 1% 미만만 학습하는 효율적 기법
- [ ] rank=8이 대부분 상황에서 적당한 시작점
- [ ] Full Fine-tuning 대비 메모리 1/4, 속도 2~3배, 성능 거의 동등
- [ ] 여러 Task용 Adapter를 쉽게 관리 가능
- [ ] Learning rate는 Full Fine-tuning보다 10배 크게
- [ ] target_modules는 ["query", "value"]부터 시작
- [ ] 추론 시 오버헤드 없음 (merge 가능)

### 🎯 시작 템플릿
```python
from peft import LoRAConfig, get_peft_model

lora_config = LoRAConfig(
    r=8,                              # rank
    lora_alpha=16,                    # scaling (r*2)
    target_modules=["query", "value"], # attention modules
    lora_dropout=0.1,                 # dropout
    bias="none",
    task_type="SEQ_CLS"               # task type
)

model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()  # 파라미터 확인

# 학습 후
model.save_pretrained("./my_lora")  # 저장 (용량 작음!)
```

---

**마지막 업데이트:** 2025-11-18  


> "LoRA는 거대 모델을 민주화한다. 이제 누구나 노트북으로 LLM을 Fine-tuning할 수 있다."