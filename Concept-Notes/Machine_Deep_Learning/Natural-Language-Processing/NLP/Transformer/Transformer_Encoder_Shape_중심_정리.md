
---

# 🚀 Transformer Encoder — Shape 중심 정리 (평생 참고용)

---

# 🔷 0. 기본 축 의미

```
B = batch_size       (문장/이미지 묶음 개수)
S = seq_len          (토큰/패치 개수)
D = d_model          (토큰 벡터 길이)
H = num_heads        (멀티헤드 개수)
d = head_dim = D/H   (각 head가 보는 차원)
```

---

# 🔷 1. 입력 단계 Shape

### ✔ 토큰화

```
seq_len = S
```

### ✔ 임베딩

```
x: (B, S, D)
```

### ✔ 포지셔널 인코딩 추가

```
(B, S, D)
```

---

# 🔷 2. Multi-Head Self-Attention Shape 흐름

아래는 **정확한 shape 변화 과정**이다.

---

## ✔ (1) Q, K, V 생성

입력 x에 대해:

```
Q = xW_Q
K = xW_K
V = xW_V

Q, K, V shape:
(B, S, D)
```

---

## ✔ (2) head로 분리 (reshape + transpose)

```
(B, S, D)
→ reshape
(B, S, H, d)
→ transpose
(B, H, S, d)
```

이제 head마다 독립적으로 Attention 가능.

---

## ✔ (3) Self-Attention (head별)

Attention 결과:

```
(B, H, S, d)
```

각 head는 **자기 관점**에서 문장을 처리.

---

## ✔ (4) head concat (원래 차원 복구)

```
(B, H, S, d)
→ transpose
(B, S, H, d)
→ reshape
(B, S, D)
```

head들을 채널 방향으로 합침.

---

## ✔ (5) 최종 선형 변환 W_O

```
(B, S, D)
```

MHA 블록 최종 output.

---

## ✔ (6) Residual + LayerNorm

```
(B, S, D)
```

입력과 완전히 동일한 shape 유지.

---

# 🔷 3. FeedForward Network(FFN) Shape 흐름

입력은 MHA 블록의 출력 x1:

```
x1: (B, S, D)
```

---

## ✔ (1) 1차 선형 변환 (확장)

```
(B, S, D)
→ (B, S, d_ff)   # d_ff = 4D가 일반적
```

---

## ✔ (2) GELU/ReLU

```
(B, S, d_ff)
```

---

## ✔ (3) 2차 선형 변환 (축소)

```
(B, S, d_ff)
→ (B, S, D)
```

---

## ✔ (4) Residual + LayerNorm

```
(B, S, D)
```

FFN 출력도 항상 입력과 동일.

---

# 🔷 4. 인코더 전체 스택 (N 레이어)

레이어를 여러 개 쌓으면:

```
Layer 0 입력:        (B, S, D)
↓
Layer 1 출력:        (B, S, D)
↓
Layer 2 출력:        (B, S, D)
↓
...
↓
Layer N 출력:        (B, S, D)
```

항상 shape 변화 없음.

---

# 🔷 5. 전체 Shape 흐름 — 한눈에 요약

```
입력 x:                      (B, S, D)
↓
Q,K,V:                       (B, S, D)
↓ reshape
Q,K,V:                       (B, H, S, d)
↓ Attention per head
Attn:                        (B, H, S, d)
↓ concat
Concat:                      (B, S, D)
↓ W_O
MHA output:                  (B, S, D)
↓ Residual + Norm
x1:                          (B, S, D)
↓ FFN expand
(B, S, d_ff)
↓ activation
(B, S, d_ff)
↓ FFN shrink
(B, S, D)
↓ Residual + Norm
x2 (레이어 출력):            (B, S, D)
```

---

# 🔷 6. 10초 만에 복습 가능한 절대 핵심

* **Q/K/V**: (B, S, D)
* **split heads**: (B, H, S, d)
* **attention**: (B, H, S, d)
* **concat**: (B, S, D)
* **FFN**: (B, S, D) → (B, S, d_ff) → (B, S, D)
* **모든 레이어 입력과 출력 shape 동일**: (B, S, D)

---

