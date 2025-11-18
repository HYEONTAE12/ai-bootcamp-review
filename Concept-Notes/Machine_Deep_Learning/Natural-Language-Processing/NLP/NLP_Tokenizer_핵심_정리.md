# Tokenizer 완벽 가이드

## 📌 Tokenizer란?

**정의:**
> 텍스트를 모델이 이해할 수 있는 작은 단위(토큰)로 나누는 과정

```
입력: "I love playing"
출력: ["I", "love", "play", "##ing"]
```

---

## 🎯 Tokenization 기준들

### 1. 띄어쓰기 (Whitespace)

```
"I love you" → ["I", "love", "you"]
```

**장점:** 간단  
**단점:** 신조어 처리 불가

### 2. 단어 (Word-based)

```
"Don't stop" → ["Do", "n't", "stop"]
```

**장점:** 의미 보존  
**단점:** 
- Vocab 크기 폭발 (수십만~수백만)
- OOV(Out-of-Vocabulary) 문제
- 신조어, 오타 처리 불가

```python
# OOV 문제 예시
학습 vocab: ["cat", "dog", "love"]
새 단어: "puppies" → [UNK] (Unknown) ✗
# 의미 손실!
```

### 3. 형태소 (Morpheme)

```
"running" → ["run", "ing"]
"loved" → ["love", "ed"]
```

**장점:** 의미 단위 분리  
**단점:** 언어별 형태소 분석기 필요 (한국어: KoNLPy 등)

### 4. 서브워드 (Subword) ⭐ 현재 표준

```
"unbelievable" → ["un", "##believ", "##able"]
"lowest" → ["low", "##est"]
```

**장점:**
- OOV 해결 ✓
- 적당한 Vocab 크기 (3만~5만)
- 의미 단위 어느정도 보존

**단점:** 완벽한 의미 단위는 아님

---

## 📊 방식별 비교

| 방식 | Vocab 크기 | OOV 문제 | 의미 보존 | 사용 |
|------|-----------|---------|---------|------|
| 띄어쓰기 | 작음 | 있음 | 낮음 | 거의 안 씀 |
| 단어 | **매우 큰** | **심각** | 높음 | 옛날 방식 |
| 형태소 | 중간 | 적음 | 높음 | 언어별 제한 |
| **서브워드** | **적당** | **없음** | **중간** | **현재 표준** |

---

## 🔥 Subword Tokenization

### 핵심 아이디어

```
단어 수준: Vocab 너무 큼, OOV 문제
문자 수준: 의미 없음, 시퀀스 너무 김

→ 그 중간! 서브워드!
```

**처음 보는 단어도 표현 가능:**

```python
# 학습 vocab: ["low", "##er", "##est"]

# 학습 때 본 단어
"lower" → ["low", "##er"] ✓

# 처음 보는 단어 (학습 안 했음)
"lowest" → ["low", "##est"] ✓
# 서브워드 조합으로 표현 가능!
```

---

## 🚀 BPE (Byte Pair Encoding)

### 핵심 원리

**Bottom-up (상향식): 문자 → 서브워드**

```
시작(최소): ['l', 'o', 'w', 'e', 'r']
   ↓ 합치기
과정(중간): ['lo', 'w', 'er']
   ↓ 계속 합치기
종료(목표): ['low', 'er'] (목표 vocab 크기 도달)
```

**NOT:** 단어 → 쪼개기 → 문자 (✗)  
**BUT:** 문자 → 합치기 → 서브워드 (✓)

### 알고리즘

```python
# Step 0: 코퍼스 준비
corpus = [
    "low low low low lower",
    "newest newest widest"
]

# Step 1: 문자 단위 분리 (+ 단어 끝 표시)
vocab = {
    'l o w </w>': 4,      # "low" 4번
    'l o w e r </w>': 1,  # "lower" 1번
    'n e w e s t </w>': 2,
    'w i d e s t </w>': 1,
}

# Step 2: 가장 빈번한 문자 쌍 찾기
# 'e s' 쌍이 3번으로 가장 많음
→ 'es' 생성

vocab = {
    'l o w </w>': 4,
    'l o w e r </w>': 1,
    'n e w es t </w>': 2,  # 'e s' → 'es'
    'w i d es t </w>': 1,
}

# Step 3: 다시 가장 빈번한 쌍
# 'es t' 쌍이 3번
→ 'est' 생성

vocab = {
    'l o w </w>': 4,
    'l o w e r </w>': 1,
    'n e w est </w>': 2,
    'w i d est </w>': 1,
}

# Step 4: 계속 반복
# 'l o' 쌍이 5번
→ 'lo' 생성

# ... 목표 vocab 크기(예: 1000)까지 반복
```

### 실제 사용 (학습 후)

```python
# 학습된 subword: ['lo', 'w', 'er', 'est', ...]

# "lower" 토크나이징
1. "lower" 시작
2. 가장 긴 매치 찾기: "lo" ✓ → ['lo', 'wer']
3. "w" ✓ → ['lo', 'w', 'er']
4. "er" ✓ → ['lo', 'w', 'er']

최종: ["lo", "w", "er"]

# "lowest" 토크나이징 (처음 본 단어!)
1. "lowest" 시작
2. "lo" ✓ → ['lo', 'west']
3. "w" ✓ → ['lo', 'w', 'est']
4. "est" ✓ → ['lo', 'w', 'est']

최종: ["lo", "w", "est"]
# OOV 없음! ✓
```

### BPE 특징

**기준:** 빈도(Frequency)  
**표시:** `</w>` (단어 끝)  
**사용:** GPT-2, GPT-3, RoBERTa

---

## 🎓 WordPiece (BERT 사용)

### BPE와의 차이

**BPE:**
```python
# 단순히 빈도만 봄
'e' + 's' 가 100번 등장 → 병합!
```

**WordPiece:**
```python
# "병합했을 때 언어모델이 더 잘 예측할까?" 확인
'e' + 's' 병합 시 → 언어모델 점수 계산
점수 높으면 → 병합!

# 더 똑똑한 병합!
```

### 우도(Likelihood) 기반

**우도 = "이 조합이 얼마나 의미있는가?"**

```python
# 우도 점수 계산
Score = P('in') / (P('i') × P('n'))

# 예시:
P('i') = 0.04
P('n') = 0.05
P('in') = 0.04

Score = 0.04 / (0.04 × 0.05) = 20

# 점수 높음 = 'i'와 'n'이 함께 나타날 확률 높음
# → 'in'은 의미있는 단위! 병합하자!
```

**의미:**
- 점수 높음 = 자주 같이 등장 = 의미있는 조합
- 점수 낮음 = 우연히 같이 등장 = 의미없는 조합

### WordPiece 알고리즘

```python
# Step 1: 문자 단위 시작 (BPE와 동일)
vocab = ['a', 'b', 'c', ..., 'z']

# Step 2: 모든 후보 쌍의 우도 점수 계산
후보:
'p'+'l' → 점수: 5
'i'+'n' → 점수: 20  ← 가장 높음!
'n'+'g' → 점수: 15

# Step 3: 가장 높은 점수 병합
→ 'in' 추가
vocab = ['a', 'b', ..., 'in', ..., 'z']

# Step 4: 반복
다음 후보:
'in'+'g' → 점수: 25  ← 최고!
'play' → 점수: 20

→ 'ing' 추가
vocab = ['a', 'b', ..., 'in', 'ing', ..., 'z']

# ... 목표 크기까지 반복
```

### ## (더블 샤프) 표시

**의미:** "이 토큰은 단어의 중간이다"

```python
# 단어 시작 (## 없음)
"I love you" → ['i', 'love', 'you']

# 단어 중간 (## 있음)
"playing" → ['play', '##ing']
            ↑       ↑
         시작    중간(##)

# 복원
'play' + '##ing' 
→ ## 제거 → 'play' + 'ing' 
→ 'playing' ✓
```

### 실제 예시

```python
# BERT WordPiece 결과

"playing" → ['play', '##ing']
             ↑       ↑
          동사원형  진행형

"unbelievable" → ['un', '##bel', '##iev', '##able']
                  ↑     ↑       ↑        ↑
                부정   어근    어근    형용사화

"walked" → ['walk', '##ed']
            ↑       ↑
         동사원형  과거형

# 의미있는 단위로 잘 나뉨! ✓
```

### WordPiece 특징

**기준:** 우도(Likelihood) - 언어모델 예측 성능  
**표시:** `##` (단어 중간)  
**사용:** BERT, ELECTRA

---

## 🔍 BPE vs WordPiece 비교

| 항목 | BPE | WordPiece |
|------|-----|-----------|
| **병합 기준** | 빈도 (Frequency) | 우도 (Likelihood) |
| **시작** | 문자 단위 | 문자 단위 |
| **방향** | Bottom-up (합치기) | Bottom-up (합치기) |
| **특수 표시** | `</w>` (단어 끝) | `##` (단어 중간) |
| **지능** | 단순 카운트 | 언어모델 기반 (더 똑똑) |
| **사용 모델** | GPT-2, RoBERTa | BERT, ELECTRA |

### 같은 점

- 문자에서 시작 (최소 단위)
- 점점 합쳐서 서브워드 생성 (Bottom-up)
- OOV 문제 해결
- 적당한 vocab 크기 (3만~5만)

### 다른 점

**병합 기준:**

```python
# 코퍼스: "play play play playing"

# BPE (빈도):
'p'+'l' = 4번 → 'pl' 생성
'l'+'a' = 4번 → 'la' 생성
# 단순!

# WordPiece (우도):
'play' 조합 = 언어모델이 잘 예측 (점수 높음) → 'play' 생성
'ing' 조합 = 언어모델이 잘 예측 (점수 높음) → 'ing' 생성
# 똑똑!
```

**결과 차이:**

```python
# "unbelievable" 토크나이징

# BPE 결과:
['un', 'be', 'liev', 'able']
      ↑    ↑   ↑
    의미O 의미? 의미?

# WordPiece 결과:
['un', '##believ', '##able']
      ↑      ↑        ↑
    부정  "믿다"   형용사화
    
# WordPiece가 더 의미있게!
```

---

## 🛠️ 실전 코드 (최소한)

### BERT (WordPiece)

```python
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# 토큰화
text = "I love playing football"
tokens = tokenizer.tokenize(text)
print(tokens)
# ['i', 'love', 'play', '##ing', 'football']

# ID 변환
ids = tokenizer.encode(text)
print(ids)
# [101, 1045, 2293, 2652, 2075, 2374, 102]
#  ↑                              ↑
# [CLS]                         [SEP]

# 복원
decoded = tokenizer.decode(ids)
print(decoded)
# "[CLS] i love playing football [SEP]"
```

### GPT-2 (BPE)

```python
from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

text = "I love playing"
tokens = tokenizer.tokenize(text)
print(tokens)
# ['I', 'Ġlove', 'Ġplaying']
#       ↑        ↑
#    Ġ = 띄어쓰기 (BPE 방식)
```

### 한국어 (KoBERT)

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('klue/bert-base')

text = "안녕하세요 반갑습니다"
tokens = tokenizer.tokenize(text)
print(tokens)
# ['안녕', '##하', '##세요', '반갑', '##습니다']
```

---

## 📈 모델별 Tokenizer

| 모델 | Tokenizer | Vocab 크기 | 특징 |
|------|-----------|-----------|------|
| **BERT** | WordPiece | 30,000 | `##` 표시 |
| **GPT-2** | BPE | 50,257 | Byte-level |
| **GPT-3** | BPE | 50,257 | GPT-2와 동일 |
| **RoBERTa** | BPE | 50,265 | Byte-level |
| **T5** | SentencePiece | 32,000 | Unigram |
| **ELECTRA** | WordPiece | 30,000 | BERT와 동일 |
| **ALBERT** | SentencePiece | 30,000 | Unigram |
| **XLNet** | SentencePiece | 32,000 | Unigram |

---

## 💡 핵심 정리

### Tokenizer 전체 흐름

```
1. 원본 텍스트
   ↓
2. Tokenization (작은 단위로 나누기)
   ↓
3. 토큰들
   ↓
4. ID 변환 (숫자로)
   ↓
5. 모델 입력
```

### Subword의 장점

```
✅ OOV 문제 해결
- 처음 보는 단어도 서브워드 조합으로 표현

✅ 적당한 Vocab 크기
- 단어 수준: 수십만~수백만
- 서브워드: 3만~5만

✅ 의미 어느정도 보존
- "playing" → ['play', '##ing']
- 동사원형 + 진행형으로 의미 파악 가능
```

### BPE vs WordPiece 요약

**BPE (단순):**
- 빈도만 세서 병합
- 간단하고 빠름
- GPT 계열 사용

**WordPiece (똑똑):**
- 언어모델 예측 성능 기반 병합
- 더 의미있는 서브워드
- BERT 계열 사용

### 선택 가이드

```python
# 상황별 선택

# 영어 NLP:
BERT (WordPiece) ✓

# 다국어:
mBERT, XLM-R (SentencePiece) ✓

# 생성 태스크:
GPT-2/3 (BPE) ✓

# 한국어:
KoBERT (WordPiece) ✓
or KoGPT (BPE) ✓
```

---

## 🎯 기억할 핵심

### 1. Tokenization의 목적
> 텍스트를 모델이 처리 가능한 단위로 나누기

### 2. Subword가 현재 표준
> OOV 해결 + 적당한 Vocab 크기

### 3. BPE = 빈도 기반
> 문자 → 합치기 → 서브워드 (Bottom-up)

### 4. WordPiece = 우도 기반
> BPE + 언어모델 점수 = 더 똑똑한 병합

### 5. ## 표시
> BERT의 WordPiece에서 단어 중간을 나타냄

---

## 📚 참고자료

### 논문
- **BPE 원논문:** [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) (2016)
- **WordPiece:** Google's Neural Machine Translation System (2016)
- **SentencePiece:** [SentencePiece: A simple and language independent approach](https://arxiv.org/abs/1808.06226) (2018)

### 구현
- **Hugging Face Tokenizers:** https://github.com/huggingface/tokenizers
- **SentencePiece:** https://github.com/google/sentencepiece

### 튜토리얼
- [Hugging Face Tokenizers 문서](https://huggingface.co/docs/tokenizers)
- [The Illustrated Word2vec](http://jalammar.github.io/illustrated-word2vec/)

---

**마지막 업데이트:** 2025-11-18  


> "Subword Tokenization은 NLP의 OOV 문제를 해결한 혁신이다. BPE는 단순하고, WordPiece는 똑똑하다."