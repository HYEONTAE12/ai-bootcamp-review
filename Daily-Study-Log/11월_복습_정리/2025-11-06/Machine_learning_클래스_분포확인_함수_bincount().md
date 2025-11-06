
---

## 🧩 `bincount()` 함수 정리

### 📘 기본 개념

* **정수형 데이터에서 각 값이 몇 번 나왔는지를 빠르게 세주는 함수**
* 주로 **라벨 분포 확인**이나 **클래스 불균형 분석**에 사용

```python
import numpy as np

labels = np.array([0, 0, 1, 2, 2, 2])
print(np.bincount(labels))  # [2 1 3]
```

➡ 클래스 0: 2번, 클래스 1: 1번, 클래스 2: 3번 등장

---

### ⚙️ 추가 옵션: `weights`

* 각 값에 **가중치(weight)** 를 줄 수 있음

```python
x = np.array([0, 0, 1, 1])
weights = np.array([0.5, 0.5, 1.0, 1.5])
print(np.bincount(x, weights=weights))  # [1.0 2.5]
```

> 클래스 0 → 0.5 + 0.5 = 1.0
> 클래스 1 → 1.0 + 1.5 = 2.5

---

### 🚀 딥러닝 실무 활용 예시

#### 1️⃣ 클래스 불균형 비율 계산

```python
counts = np.bincount(train_labels)
class_weights = 1.0 / counts
```

→ 클래스가 적을수록 높은 가중치 부여

#### 2️⃣ PyTorch 형태로 변환

```python
import torch
labels = torch.tensor([0, 1, 1, 2])
print(torch.bincount(labels))  # tensor([1, 2, 1])
```

---

### 📌 정리표

| 항목         | 내용                              |
| ---------- | ------------------------------- |
| **함수명**    | `np.bincount`, `torch.bincount` |
| **입력 타입**  | 정수형 1차원 배열                      |
| **출력 값**   | 각 정수값의 등장 횟수                    |
| **주요 사용처** | 클래스 분포 확인, 불균형 보정, 가중치 계산       |
| **옵션**     | `weights`: 각 항목에 가중치 부여         |
| **주의**     | 실수형 입력은 불가능 (정수형만 가능)           |

---
