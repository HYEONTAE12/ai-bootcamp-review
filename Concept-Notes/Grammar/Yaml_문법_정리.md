
---

# 📘 YAML 문법 정리

YAML(YAML Ain’t Markup Language)은 **사람이 읽기 쉬운 데이터 직렬화 포맷**으로, 설정 파일에서 자주 사용됩니다.
(Hydra, PyTorch Lightning, Docker Compose 등 다양한 환경에서 활용)

---

## 1. 들여쓰기

* 기본적으로 **2칸** 들여쓰기를 권장 (4칸도 가능하지만 혼용 금지).
* 들여쓰기는 **계층 구조**를 나타냄.

```yaml
data:
  batch_size: 32
  shuffle: true
```

---

## 2. 데이터 형식 (Key: Value)

* `key: value` 형태로 정의.
* `:` 뒤에는 반드시 **공백** 필요.

```yaml
learning_rate: 0.001
optimizer: adam
```

---

## 3. 배열 (List)

* `-` 로 항목을 표시.

```yaml
layers:
  - conv1
  - conv2
  - fc1
```

---

## 4. 주석

* `#` 이후는 모두 주석으로 처리됨.

```yaml
# 학습률 설정
learning_rate: 0.01
```

---

## 5. 참/거짓 (Boolean)

* `true` / `false`
* `yes` / `no` (소문자 권장)

```yaml
use_gpu: true
debug_mode: no
```

---

## 6. 숫자 (정수 / 실수)

* 따옴표 없이 사용 → 숫자로 인식.

```yaml
epochs: 10
dropout: 0.25
```

---

## 7. 문자열 (String)

* 기본적으로 따옴표 없어도 문자열로 인식.
* 공백, 특수문자가 포함되면 `' '` 또는 `" "` 로 감싸야 함.

```yaml
model_name: resnet50
note: "experiment with batch size = 64"
```

---

## 8. Null (빈 값)

* `null`, `~`, 아무 값 없음 → 모두 null로 처리됨.

```yaml
description: null
comment: ~
extra: 
```

---

## 9. 여러 줄 문자열

* `|` : 줄바꿈을 그대로 유지
* `>` : 줄바꿈을 공백으로 변환

```yaml
message: |
  첫 번째 줄
  두 번째 줄 (줄바꿈 유지)

summary: >
  첫 번째 줄
  두 번째 줄 (한 줄로 합쳐짐)
```

---

## 10. Anchor & Alias (참조 기능)

* `&` : 값에 이름을 붙임 (Anchor)
* `*` : 이미 정의한 Anchor 참조 (Alias)

```yaml
defaults: &defaults
  lr: 0.001
  batch_size: 32

experiment1:
  <<: *defaults
  model: resnet18

experiment2:
  <<: *defaults
  model: resnet34
```

---

## ✅ 요약

| 문법 요소        | 설명                     | 예시                        |           |      |
| ------------ | ---------------------- | ------------------------- | --------- | ---- |
| 들여쓰기         | 계층 구조                  | `data:\n  batch_size: 32` |           |      |
| Key-Value    | `:` + 공백 필수            | `lr: 0.001`               |           |      |
| 배열           | `-` 사용                 | `- conv1`                 |           |      |
| 주석           | `#` 이후 무시              | `# comment`               |           |      |
| Boolean      | `true/false`, `yes/no` | `use_gpu: true`           |           |      |
| 숫자           | 따옴표 없이 숫자로 인식          | `epochs: 20`              |           |      |
| 문자열          | 따옴표 선택적                | `"text with space"`       |           |      |
| Null         | `null`, `~`, 빈 값       | `value: null`             |           |      |
| 여러 줄 문자열     | `                      | `(줄 유지),`>` (줄 합치기)       | `message: | ...` |
| Anchor/Alias | 값 재사용                  | `<<: *defaults`           |           |      |

---

