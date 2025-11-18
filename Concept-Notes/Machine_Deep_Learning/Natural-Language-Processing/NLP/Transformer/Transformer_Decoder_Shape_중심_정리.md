
---

# 📘 **[6장] Transformer Decoder 전체 Shape 변화 흐름 (평생 참고용 1장)**

> **“입력 임베딩 → Self-Attention → Cross-Attention → FFN → Linear+Softmax → next token”까지
> 모든 단계의 shape 변화만 모아서 1페이지로 정리한 최종 요약본**

---

# 🧩 0. 초기 입력

### **Token IDs**

```
[batch, tgt_len]
```

---

# 🧩 1. 임베딩 + 포지셔널 인코딩

### Token Embedding:

```
[batch, tgt_len, d_model]
```

### Positional Encoding 추가 후:

```
[batch, tgt_len, d_model]
(변화 없음)
```

---

# 🧩 2. Masked Multi-Head Self-Attention

### Q, K, V 생성

(각 head에 나누기 전)

```
Q: [batch, tgt_len, d_model]
K: [batch, tgt_len, d_model]
V: [batch, tgt_len, d_model]
```

### Head 분할

```
→ [batch, num_heads, tgt_len, d_k]
```

### Attention Score (QKᵀ)

```
[batch, num_heads, tgt_len, tgt_len]
```

### Softmax 및 Value 가중합

```
[batch, num_heads, tgt_len, d_v]
```

### Head concat

```
→ [batch, tgt_len, d_model]
```

### Output Linear + Residual + LayerNorm

```
→ [batch, tgt_len, d_model]
```

---

# 🧩 3. Encoder–Decoder Attention (Cross-Attention)

### Query = 디코더 출력

```
[batch, tgt_len, d_model]
→ reshape: [batch, num_heads, tgt_len, d_k]
```

### Key = 인코더 출력

```
[batch, src_len, d_model]
→ reshape: [batch, num_heads, src_len, d_k]
```

### Value = 인코더 출력

```
[batch, src_len, d_model]
→ reshape: [batch, num_heads, src_len, d_v]
```

### Attention score (QKᵀ)

```
[batch, num_heads, tgt_len, src_len]
```

### Softmax + V 가중합

```
[batch, num_heads, tgt_len, d_v]
```

### Head concat

```
→ [batch, tgt_len, d_model]
```

### Output Linear + Residual + LayerNorm

```
→ [batch, tgt_len, d_model]
```

---

# 🧩 4. Feed Forward Network (FFN)

### 첫 Linear (확장)

```
[batch, tgt_len, d_model] → [batch, tgt_len, d_ff]
```

### 활성함수

```
[batch, tgt_len, d_ff]
```

### 두 번째 Linear (축소)

```
[batch, tgt_len, d_ff] → [batch, tgt_len, d_model]
```

### Residual + LayerNorm

```
→ [batch, tgt_len, d_model]
```

---

# 🧩 5. 출력 Projection → 단어 확률

### Linear (d_model → vocab_size)

```
[batch, tgt_len, d_model] → [batch, tgt_len, vocab_size]
```

### Softmax

```
[batch, tgt_len, vocab_size]
```

### 다음 토큰 선택 (argmax / sampling)

```
[batch]
```

---

# 🧩 6. Autoregressive Loop (다음 스텝)

선택된 next_token을 decoder 입력에 붙여 다음 스텝 실행:

```
next_input = concat(prev_tokens, next_token)
shape: [batch, tgt_len+1]
```

→ 다시 1번으로 돌아감

---

# 🎯 **전체 시각화 흐름도 (최종 압축 버전)**

```
[batch, tgt_len]
      │
      ▼
Embedding + Positional
[batch, tgt_len, d_model]
      │
      ▼
Masked Self-Attention
[batch, tgt_len, d_model]
      │
      ▼
Encoder–Decoder Attention
[batch, tgt_len, d_model]
      │
      ▼
Feed Forward Network
[batch, tgt_len, d_model]
      │
      ▼
Linear (→ vocab_size)
[batch, tgt_len, vocab_size]
      │
      ▼
Softmax → next_token
[batch]
      │
      ▼
다음 스텝 디코더 입력으로 재사용
```

---

# 🧠 **한 문장 요약**

> **Decoder는 모든 block을 거치는 동안 shape을 `[batch, tgt_len, d_model]`로 유지하고,
> 마지막 Projection 단계에서만 `[batch, tgt_len, vocab_size]`로 확장되며 그 마지막 단어를 선택해 다음 토큰을 생성한다.**

---

