
---

# 📘 **[3장] Encoder–Decoder Attention (Cross-Attention)**

> **“디코더가 인코더가 만든 ‘입력 문장의 의미’를 읽어오는 단계”**
> **디코더 출력의 50%는 이 블록에서 결정된다.**

---

# 🧩 **1. 이 블록의 한 문장 요약**

> **디코더 내부 상태(Query)가 인코더 출력(Key/Value)을 참조하면서
> ‘입력 문장의 어떤 부분이 다음 출력 단어와 관련 있는지’ 찾는 과정.**

Self-Attention이 “나 자신만 보는 것”이라면,
Cross-Attention은 **“입력 문장을 바라보는 눈”**이다.

---

# 🧲 **2. 입력과 출력**

### ✔ 입력

* **Query(Q)**:
  Masked Self-Attention의 출력
  shape: `[batch, tgt_len, d_model]`
* **Key(K), Value(V)**:
  **Encoder의 마지막 출력**
  shape: `[batch, src_len, d_model]`

### ✔ 출력

* 인코더 정보가 반영된 디코더 내부 의미 표현
  shape: `[batch, tgt_len, d_model]`
  (크기 그대로 유지)

---

# 🔍 **3. 전체 흐름 (시각적)**

```
Decoder Input → (Masked Self-Attention Output)
             │
             ▼
        Query = W_q * H_decoder
        Key   = W_k * H_encoder
        Value = W_v * H_encoder
             │
             ▼
        Scaled Dot-Product Attention
             │
             ▼
        Multi-Head concat + Linear
             │
             ▼
        Residual Connection + LayerNorm
             │
             ▼
       Cross-Attended Decoder State
```

---

# 🧱 **4. 단계별 상세 설명**

## 🟦 **① Query는 디코더가 만든 “현재 상황”**

디코더는 지금까지 만든 단어들이 있고,
그 정보를 요약한 벡터가 Self-Attention을 통해 만들어짐.

이걸 W_q를 통해 Query로 만든다.

**Query = "지금 단어를 만들려면 어떤 입력 단어가 중요하지?"**

---

## 🟥 **② Key/Value는 인코더의 전체 문장 정보**

인코더 출력은 "입력 문장의 모든 의미"를 담고 있음.

여기서:

* Key = 각 입력 토큰의 라벨
* Value = 각 입력 토큰의 실제 의미 정보

즉:

**K, V = 입력 문장 전체를 ‘참조 가능한 상태’로 만든 것**

---

## 🟩 **③ QKᵀ 통해 입력 문장의 어떤 위치를 볼지 결정**

```
attention_score = QKᵀ / √d_k
```

여기서 중요한 점:

### 🧠 Query(tgt_len) × Key(src_len)

→ 디코더의 t번째 단어는
→ 인코더의 모든 단어와 유사도를 비교함.

즉:

* “I am a student” → encoder
* “저는 ___” → decoder 생성 중

디코더는:
“지금 ‘저는’ 뒤에 올 단어는 입력 문장의 어떤 부분을 보면 될까?”
이걸 계산해서 집중해야 할 위치를 찾는다.

---

## 🟧 **④ Softmax → Value 조합**

Softmax로 정규화된 attention weight를
Value(입력 문장의 의미)와 곱한다.

```
Attention = Softmax(QKᵀ/√d_k) V
```

결과:
**입력 문장의 의미 중 “지금 필요한 부분”만 가져온 벡터**

---

## 🟪 **⑤ Multi-Head Attention**

여러 head를 쓰는 이유:

* Head1: 의미적 관계
* Head2: 문법적 관계
* Head3: 위치적 정보
* Head4: 문장 구조

**입력 문장을 다양한 시각에서 보는 것**

각 head에서 attention 수행 → concat → Linear

---

## 🟫 **⑥ Residual + LayerNorm**

```
Output = LayerNorm( Query_input + MultiHeadAttention )
```

역할:

* 정보 손실 방지
* 그래디언트 안정
* 깊은 구조에서도 학습 안정
* Self-Attention과 Encoder 정보가 조화롭게 합쳐짐

---

# 🎯 **5. 이 블록의 정확한 역할 6개**

1. **인코더가 만든 입력 문장 정보를 디코더에 주입**
2. **현재 생성 중인 단어와 가장 연관 있는 입력 단어를 찾아줌**
3. **번역·요약·대화 같은 “입력→출력” 작업의 핵심 단계**
4. **Self-Attention으로 만든 디코더 내부 문맥을 강화**
5. **입력과 출력의 alignment(정렬)를 만드는 핵심**
6. **디코더가 “입력 문장을 실제로 이해하는 구간”**

즉, 이 블록이 없으면
**번역도 요약도 절대 제대로 안 된다.**

---

# 🧾 **6. 핵심 요약 (초압축)**

> **Query = 디코더의 현재 상태,
> Key/Value = 인코더 출력.
> 둘을 비교해 “입력 문장 중 필요한 부분”을 뽑아 디코더에 전달하는 블록.**

이 블록은 **입력 문장의 의미를 그대로 생성 문장에 반영하는 핵심 연결 지점**이다.

---

