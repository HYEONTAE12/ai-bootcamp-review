
---

# 📘 **[1장] Transformer Decoder 전체 흐름 (평생 참고용)**

> **“이 그림 하나로 디코더가 어떻게 단어를 하나씩 생성하는지 완전히 이해할 수 있게 만든 흐름 요약”**

---

# 🧩 **1. 디코더의 입력 (Decoder Input)**

디코더는 _이전까지 생성된 토큰_을 입력으로 받는다.

### 입력 구성:

* **토큰화된 이전 출력들**: <s> → "I" → "am" → …
* **Token Embedding**: 단어 → 벡터
* **Positional Encoding 추가**: 순서 정보 부여

**→ 최종: `[batch, seq_len, d_model]` 크기의 입력 임베딩**이 디코더 블록으로 들어간다.

---

# 🧲 **2. Masked Multi-Head Self-Attention**

> **자기 자신에게 하는 어텐션 + 미래 정보 차단(masking)**

디코더는 문장을 왼쪽에서 오른쪽으로 생성해야 하기 때문에
다음 단어를 미리 보면 안 된다.

여기서 하는 역할:

* 입력 임베딩에서 **Q, K, V 생성**
* **Look-ahead Mask**로 미래 토큰 가리는 연산
* 여러 Head에서 attention 계산 후 concat
* Residual + LayerNorm 통과

**출력: “디코더 내부에서 다음 정보에 참고할 수 있는 자기 참조 정보”**

---

# 🔗 **3. Encoder–Decoder Attention**

> **“디코더의 Query” + “인코더의 Key/Value”**

여기서 디코더는 인코더가 만든 문장 전체 정보를 참고한다.

구성:

* Query = **앞 단계(Self-Attention)의 출력**
* Key/Value = **Encoder Output**

역할:

* 원문(입력 문장)의 의미를 기반으로
  “현재 생성 중인 단어와 가장 관련 있는 위치”를 찾는 과정
* Residual + LayerNorm

**출력: “입력 문장과 현재 생성 흐름을 합친 의미 정보”**

---

# ⚙️ **4. Position-wise Feed Forward Network (FFN)**

> **각 토큰별로 독립적인 비선형 변환**

구성:

* Linear(확장) → ReLU → Linear(축소)
* Residual + LayerNorm

역할:

* 어텐션으로 얻은 정보를 **비선형 조합해 더 표현력 있게 만드는 과정**

---

# 🎯 **5. 최종 Linear + Softmax**

FFN의 결과는 아직 '벡터'일 뿐이다.

* Linear: d_model → vocab_size
* Softmax: 단어 확률로 변환

**→ 확률이 가장 큰 토큰이 “다음 단어”가 된다.**

이 토큰을 다시 입력으로 넣어서 다음 단어를 생성한다.
이 과정을 EOS가 나올 때까지 반복.

---

# 🎬 **[전체 흐름 요약 그림]**

```
(1) Decoder Input 임베딩
       │
       ▼
(2) Masked Multi-Head Self-Attention
     - 미래 단어 차단
     - 자기 자신에게 하는 어텐션
       │
       ▼
(3) Encoder–Decoder Attention
     - Query: 디코더 내부 표현
     - Key/Value: 인코더 출력
       │
       ▼
(4) Feed Forward Network
     - 각 토큰별 비선형 변환
       │
       ▼
(5) Linear → Softmax → 다음 토큰 생성
```

---

# 🧩 **디코더 전체 흐름 핵심 포인트 6개 (다시 봐도 바로 이해용)**

1. **입력은 항상 이전에 생성된 단어들만 사용한다.**
2. **첫 번째 블록에서 미래 단어를 보지 못하도록 Masking을 한다.**
3. **두 번째 블록에서는 인코더 출력과 상호 Attention을 한다.**
4. **Self-Attention + Cross-Attention + FFN = 디코더의 핵심 3단계**
5. **모든 블록마다 Residual + LayerNorm이 반복된다.**
6. **Softmax를 통해 단어를 1개씩 생성한다.**

---
