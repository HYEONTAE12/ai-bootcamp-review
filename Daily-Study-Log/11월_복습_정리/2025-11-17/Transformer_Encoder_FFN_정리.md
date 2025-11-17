
---

# 🚀 FeedForward Network(FFN) 블록 완전 정리 (평생 참고용)

---

# 🔷 0. FFN의 핵심 역할 (한 줄 요약)

> **토큰끼리의 상호작용(MHA) 후,
> 각 토큰을 “개별적으로 더 복잡하게 비틀어주는(비선형 변환)” 단계.**

즉:

* MHA = “토큰끼리 대화”
* FFN = “각 토큰의 내부 뇌를 더 똑똑하게 만드는 과정”

---

# 🔷 1. FFN 전체 흐름 (한눈에)

```
입력 x1 (batch, seq, d_model)
      ↓
1) 1차 선형 변환 (확장)
      ↓
2) 비선형 함수(GELU/ReLU)
      ↓
3) 2차 선형 변환 (축소)
      ↓
출력 (batch, seq, d_model)
      ↓
4) Residual + LayerNorm
```

---

# 🔷 2. 내부 구조 (단순하지만 강력함)

Transformer FFN은 **토큰별로 독립적으로** 아래 변환을 수행한다.

## ✔ STEP 1) 1차 선형 변환

d_model → d_ff 로 확장

```
h = x1W1 + b1
```

shape:

```
(batch, seq, d_ff)
```

**d_ff는 보통 d_model의 4배 정도**
예: d_model=512 → d_ff=2048

이 확장 단계가 FFN을 “강력하게” 만드는 핵심.

---

## ✔ STEP 2) 비선형 활성 함수 (GELU 또는 ReLU)

```
h_act = GELU(h)   # 또는 ReLU
```

shape 동일:

```
(batch, seq, d_ff)
```

역할:

* “문자를 숫자로 바꾸고 → 패턴을 비틀어주는” 뇌의 심층 변환
* MHA에서 못 잡아낸 비선형 패턴 학습

---

## ✔ STEP 3) 2차 선형 변환

d_ff → 다시 d_model로 축소

```
out = h_actW2 + b2
```

shape:

```
(batch, seq, d_model)
```

---

## ✔ STEP 4) Residual + LayerNorm

```
x2 = LayerNorm(x1 + out)
```

* 원본 정보(x1)에 더해서 안정성을 보존
* training stability 극적으로 증가

---

# 🔷 3. FFN의 의미를 직관적으로 말하면

### 📌 Self-Attention은

> “토큰끼리 서로 정보를 주고받는 과정”

### 📌 FFN은

> “받아온 정보를 토대로 각 토큰이 스스로 더 깊은 생각을 하는 과정”

쉽게 말해:

> **Multi-Head는 ‘관계’를 학습하고,
> FFN은 ‘특징 변환’을 학습한다.**

---

# 🔷 4. FFN의 Shape 흐름 (아주 중요)

```
입력 x1:
(batch, seq, d_model)

1차 선형:
→ (batch, seq, d_ff)

활성화:
→ (batch, seq, d_ff)

2차 선형:
→ (batch, seq, d_model)

Residual + Norm:
→ (batch, seq, d_model)
```

즉 **입력과 출력의 모양이 같은 형태를 유지**한다.

---

# 🔷 5. 왜 d_ff가 큰가? (자주 놓치는 부분)

FFN은 token-wise MLP라,
**토큰끼리 상호작용이 없다.**

그렇다면 강력한 표현력을 가지려면?

> **차원을 크게 확장했다가 줄이는 구조(d_model → d_ff → d_model)**
>
> 이게 “토큰 한 개의 내부 표현력을 극대화”해준다.

GPT, BERT, ViT 등 거의 모든 Transformer에서
d_ff는 d_model의 **4배**가 표준이다.

---

# 🔷 6. 요약 그림 (가장 보기 좋은 형태)

```
x1: (batch, seq, d_model)
      │
      ▼
Linear (d_model → d_ff)
      │
      ▼
GELU / ReLU
      │
      ▼
Linear (d_ff → d_model)
      │
      ▼
Residual + LayerNorm
      │
      ▼
Output (batch, seq, d_model)
```

---

# 🔷 7. FFN 블록 핵심 요약 10초 버전

* 토큰끼리 상호작용 없이 **각 토큰 독립적으로 비선형 변환**
* 구조: `Linear → GELU → Linear`
* 내부 차원을 크게 확장(d_ff)하여 표현력 강화
* 출력은 항상 `(batch, seq, d_model)`
* Residual + LayerNorm 포함
  → “토큰 자체를 똑똑하게 만드는 단계”

---

