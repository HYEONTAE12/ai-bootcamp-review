
---

# 🔁 순환 신경망(RNN) 정리

## 1) 왜 RNN인가? — 등장 배경

* **가변 길이 시퀀스**(문장, 음성, 센서 시계열)는 DNN/CNN에 바로 넣기 힘듦 → 억지로 `RESIZE/패딩` 필요.
* 시퀀스는 **과거→현재의 순서/의존성**이 중요. 고정 입력만 받는 기존 신경망으로는 한계.
* **아이디어**: 이전 시점 정보를 “상태”로 들고 다음 시점 계산에 함께 사용 ⇒ **RNN**.

---

## 2) 기본 구조와 수식

### 직관

* 매 시점 t에서 입력 (x_t)와 이전 은닉상태 (h_{t-1})를 이용해 현재 은닉상태 (h_t)를 계산.
* (h_t)가 일종의 “메모리(기억)” 역할.

### 표준 RNN(Elman RNN)

[
h_t = \tanh(W_{xh}x_t + W_{hh}h_{t-1} + b_h),\quad
\hat{y}*t = f*{\text{out}}(W_{hy}h_t + b_y)
]

* (f_{\text{out}}): 과제에 따라 Softmax(분류), 선형(회귀) 등.

### 입출력 형태(태스크별)

* **Many-to-One**: 문장→감정분류(전체를 보고 하나의 라벨)
* **One-to-Many**: 잠재벡터 하나→시퀀스 생성(음악/텍스트)
* **Many-to-Many(동일 길이)**: 각 시점 라벨(품사 태깅)
* **Many-to-Many(길이 다름)**: 번역(보통 인코더-디코더)

---

## 3) 왜 `tanh`를 많이 쓰나?

* 출력 범위 ([-1,1]) → **값 폭주 억제**, **부호 정보 유지**(음/양 모두 표현).
* 시계열은 작은 변화에도 민감해야 함(0 근처 기울기 적당).
* `sigmoid(0~1)`는 음수/부호 정보 소실되고, 누적되면 **양수 편향(bias)**.
* (참고) 현대 실습에선 **ReLU 기반 RNN**은 폭주 위험이 크고, LSTM/GRU가 보통의 선택.

---

## 4) 학습: BPTT(Backprop Through Time)

* 시간축으로 “펼친” 네트워크에 **역전파** 적용.
* 문제: 시퀀스 길어지면 **기울기 소실/폭주**.

  * 직관: (\prod_t W_{hh})와 활성화 미분이 반복 곱해지며 0 또는 ∞ 쪽으로 치우침.
* **대응책**

  * LSTM/GRU 같은 **게이트 구조**
  * **Gradient Clipping**(노름 제한)
  * **정규화**(LayerNorm), **정규직교 초기화**, **짧은 TBPTT**(Truncated BPTT)

---

## 5) RNN의 한계 → LSTM/GRU

### LSTM (Long Short-Term Memory)

* **장기 의존성** 완화를 위해 **셀 상태 (c_t)**와 3개 게이트(입력/망각/출력) 사용.
  [
  \begin{aligned}
  i_t&=\sigma(W_{xi}x_t+W_{hi}h_{t-1}+b_i) &&\text{(input gate)}\
  f_t&=\sigma(W_{xf}x_t+W_{hf}h_{t-1}+b_f) &&\text{(forget gate)}\
  o_t&=\sigma(W_{xo}x_t+W_{ho}h_{t-1}+b_o) &&\text{(output gate)}\
  \tilde{c}*t&=\tanh(W*{xc}x_t+W_{hc}h_{t-1}+b_c) \
  c_t&=f_t\odot c_{t-1}+ i_t\odot \tilde{c}_t \
  h_t&=o_t\odot \tanh(c_t)
  \end{aligned}
  ]
* **해석**:

  * `forget gate`가 **무엇을 지울지** 결정
  * `input gate`가 **새 정보 얼마나 넣을지** 결정
  * `output gate`가 **무엇을 내보낼지** 결정

### GRU (Gated Recurrent Unit)

* **더 단순**, 파라미터 적음(속도·메모리 이점) / 성능은 LSTM과 비슷한 경우多.
  [
  \begin{aligned}
  z_t&=\sigma(W_{xz}x_t+W_{hz}h_{t-1}+b_z) &&\text{(update)}\
  r_t&=\sigma(W_{xr}x_t+W_{hr}h_{t-1}+b_r) &&\text{(reset)}\
  \tilde{h}*t&=\tanh(W*{xh}x_t+W_{hh}(r_t\odot h_{t-1})+b_h)\
  h_t&=(1-z_t)\odot h_{t-1}+z_t\odot \tilde{h}_t
  \end{aligned}
  ]
* **해석**:

  * `reset`은 과거를 **얼마나 무시**할지
  * `update`는 새 상태를 **얼마나 채택**할지

> **요약**: 긴 문맥 필요하면 LSTM/GRU 필수. 리소스 빡빡하면 GRU가 실용적.

---

## 6) 실무 팁 — 가변 길이, 패딩, 마스킹

* 배치 학습 위해 보통 **패딩**으로 길이를 맞춤.
* 손실/주의집중이 패딩 토큰에 영향받지 않게 **마스킹** 필수.
* PyTorch: `pack_padded_sequence`, `pad_packed_sequence`
  Keras: `mask_zero=True`, `attention_mask` 등.

---

## 7) 변형/확장

* **양방향 RNN(BiRNN)**: 과거+미래 컨텍스트 모두 활용(태깅/음성 인식에 유용).
* **인코더–디코더 RNN**: 번역, 요약 등 시퀀스 변환.
* **어텐션(Attention)**: 먼 시점 정보 접근을 쉽게 함 → **Transformer**로 진화.
* **규모/성능 관점**: 오늘날 긴 문맥/대규모 데이터에선 **Transformer가 주류**지만,
  **작은 데이터/경량 장치/실시간**에서는 RNN(LSTM/GRU) 여전히 실전적.

---

## 8) 언제 무엇을 쓰나?

* **짧은 시퀀스·경량·실시간**: GRU/LSTM
* **긴 문맥·대규모 학습**: Transformer(어텐션)
* **쌍방향 문맥 필요**: BiLSTM/GRU 또는 BERT류

---

## 9) 하이퍼파라미터 & 실무 체크리스트

* **Hidden size**: 128/256/512부터 탐색
* **Layers**: 1–3층(깊을수록 소실 위험↑ → 게이트/정규화/클리핑 병행)
* **Dropout**: 0.1–0.5 (입력/은닉/출력 사이)
* **Clip grad norm**: 1.0 혹은 5.0
* **Optimizer**: Adam(β₁=0.9, β₂=0.999) 기본
* **Batching**: 길이 기준 정렬 + 패킹/마스킹
* **정규화**: LayerNorm(RNN/LSTM 양쪽에 실험 가치)

---

## 10) 요약 한 줄

> RNN은 **시간적 의존성**을 다루는 기본 해법이고, **장기 의존성 문제**를 LSTM/GRU의 **게이트**로 완화한다.
> 긴 문맥/대규모에는 **Transformer**, 경량/실시간에는 **GRU/LSTM**이 여전히 유효.

---
