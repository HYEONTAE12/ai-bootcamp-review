
---

# 🚀 Multi-Head Self-Attention 완전 정리 (평생 참고용)

---

# 🔷 0. MHA의 핵심 역할 (이해의 핵)

> **한 토큰이 문장 안의 모든 토큰을 보고,
> “누가 중요한지” 가중치를 계산한 뒤
> 중요한 토큰들의 정보를 모아 자기 자신을 업데이트하는 과정.**

즉:

* 토큰 간 정보교환
* 문맥 이해
* 장거리 의존성 해결

인코더의 핵심 기능을 담당.

---

# 🔷 1. 전체 블록 흐름 (한눈에)

```
입력 x (batch, seq, d_model)
     ↓
1) Q, K, V 생성
     ↓
2) Multi-Head로 분리 (num_heads)
     ↓
3) head 단위 Self-Attention 수행
     ↓
4) head 결과 concat
     ↓
5) 선형 변환 (W_O)
     ↓
6) Residual + LayerNorm
     ↓
출력: (batch, seq, d_model)
```

---

# 🔷 2. Step-by-Step — 핵심만 그림처럼 보기

---

## 🔹 STEP 1) Q, K, V 생성

입력 x를 “3가지 관점”으로 바라봄:

```
Q = xW_Q     ← “내가 누구를 볼지”
K = xW_K     ← “나는 어떤 특징을 가진 토큰인지”
V = xW_V     ← “내 정보(내용)”
```

모두 shape은 동일:

```
(batch, seq, d_model)
```

---

## 🔹 STEP 2) Head로 나누기 (Multi-Head)

전체 차원 d_model을 head 개수로 나눔:

```
head_dim = d_model // num_heads
```

그리고 reshape:

```
(batch, seq, d_model)
→ (batch, num_heads, seq, head_dim)
```

**의미:**

* 각 head는 전체 벡터의 일부(head_dim)만 보고
* 그 부분에서 “자기만의 관점”을 학습한다.

---

## 🔹 STEP 3) head별 Self-Attention 수행

각 head는 **문장 전체를 스스로 스캔**한다.

그림 느낌:

```
토큰_i → 모든 K_j를 스캔 → 중요도 계산 → 중요도와 V_j를 조합
```

수식은 이후에 보고, 지금은 느낌만:

> 한 head = 하나의 시각(측면)으로 문장을 바라본다.

결과 shape:

```
(batch, seq, head_dim)
```

이걸 head 개수만큼 수행.

---

## 🔹 STEP 4) head concat (원래 차원 복구)

모든 head 결과를 옆으로 붙인다:

```
(batch, seq, head_dim * num_heads)
= (batch, seq, d_model)
```

Multi-head의 정보가 **한 벡터로 합쳐지는 순간.**

---

## 🔹 STEP 5) 선형 변환 (W_O)

합쳐진 벡터를 한 번 더 변환해
최종 attention output 생성:

```
attn_out = concat_output @ W_O
```

shape는 동일:

```
(batch, seq, d_model)
```

---

## 🔹 STEP 6) Residual + LayerNorm

원래 입력 x와 합산하여 정보 손실 방지:

```
x1 = LayerNorm(x + attn_out)
```

Self-attention 블록의 최종 출력.

---

# 🔷 3. 직관 메타포 (진짜 이해 잘되는 버전)

**문장 = 여러 사람이 있는 회의실**
각 토큰 = 사람 하나

* Q = “내가 누구에게 질문할까?”
* K = “내가 어떤 정보를 가진 사람일까?”
* V = “내가 실제로 말할 내용”

Self-Attention =

> 회의실 사람 하나가 전체 사람을 둘러본 뒤
> **중요한 사람들 의견만 모아서 자기 생각을 업데이트**하는 과정.

Multi-Head =

> 한 사람이 “여러 관점(성격/경력/위치/거리)”으로 각각 회의를 돌려보는 것.

---

# 🔷 4. MHA Shape 흐름표 (아주 중요)

```
입력 x:
(batch, seq, d_model)

Q,K,V 생성:
(batch, seq, d_model)

reshape/split:
(batch, seq, d_model)
→ (batch, num_heads, seq, head_dim)

Self-Attention:
(batch, num_heads, seq, head_dim)

concat:
(batch, seq, d_model)

W_O:
(batch, seq, d_model)

Residual + LayerNorm:
(batch, seq, d_model)
```

딱 이 표만 봐도 전체가 떠오르는 수준.

---

# 🔷 5. Multi-Head를 왜 쓰는가? (핵심 3줄)

1. **여러 관점으로 문장을 바라보기 위해**
   (문법/의미/거리 등 다른 패턴 학습)

2. **d_model을 여러 subspace로 나누면 파라미터 폭발을 막는다**

3. **head 수를 늘려도 전체 output shape(d_model)은 유지된다**

---

# 🔷 6. 10초 요약 버전 (최고 압축)

> **MHA = Q/K/V 만들고 → head로 나눠 → head별 attention → concat → W_O → residual/norm.**
>
> 역할: 토큰끼리 문맥 정보를 교환해 “더 똑똑한 토큰 벡터”로 만드는 과정.

---
