

---

# 📌 Code Review: `SimpleDataLoader`

```python
import math
import numpy as np

class SimpleDataLoader:
    def __init__(self, features, labels, batch_size=32, shuffle=True):
        self.features = features
        self.labels = labels
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_samples = len(features)
        self.indices = np.arange(self.num_samples)
```

### 🔹 `__init__`

* `features`, `labels`, `batch_size`, `shuffle` 값을 입력받아 초기화.
* `features`의 길이를 구해서 `num_samples`에 저장.
* `self.indices = np.arange(self.num_samples)` → `0 ~ num_samples-1` 까지의 인덱스를 생성.

> ⚠️ `features`는 numpy 객체이므로 `len(features)`는 numpy의 `__len__`이 실행된다.
> 해당 클래스에서 `len(instance)`를 사용하려면 반드시 `__len__` 메서드를 정의해야 한다.

---

```python
    def __iter__(self):
        if self.shuffle:
            np.random.shuffle(self.indices)
        self.current_idx = 0
        return self
```

### 🔹 `__iter__`

* 클래스 객체가 `for`문에서 반복 가능하도록 만드는 메서드.
* `shuffle=True`일 경우 `indices`를 무작위로 섞어 학습 데이터 순서를 랜덤하게 만든다.
* `current_idx`를 `0`으로 초기화하고 자기 자신(`self`)을 반환.

> ⚠️ **주의점**: 테스트 세트에서는 `shuffle=False`로 설정해야 한다.
> 모델 평가 시 데이터 순서가 바뀌면 안 되기 때문이다.

---

```python
    def __next__(self):
        if self.current_idx >= self.num_samples:
            raise StopIteration

        start_idx = self.current_idx
        end_idx = start_idx + self.batch_size
        self.current_idx = end_idx

        batch_indices = self.indices[start_idx:end_idx]
        return self.features[batch_indices], self.labels[batch_indices]
```

### 🔹 `__next__`

* `이터레이터`가 한 번 호출될 때마다 `batch_size` 만큼 데이터를 반환.
* `current_idx >= num_samples`일 경우 `StopIteration`을 발생시켜 반복 종료.
* `start_idx`와 `end_idx`를 이용해 미니배치 단위로 데이터 추출.
* 같은 인덱스로 `features`와 `labels`를 매칭시켜 반환.

---

```python
    def __len__(self):
        return math.ceil(self.num_samples / self.batch_size)
```

### 🔹 `__len__`

* 데이터셋을 **몇 개의 배치로 나눌 수 있는지** 반환.
* `num_samples / batch_size`의 결과를 `math.ceil`로 올림 처리 → 남는 데이터도 하나의 배치로 포함.
* 예: `num_samples=100, batch_size=32` → `32, 32, 32, 4` → 총 4개의 배치.

---

# ✅ 정리

* `__init__`: 데이터와 파라미터 초기화 + 인덱스 생성
* `__iter__`: 반복 가능 객체로 정의 + 필요 시 셔플 적용
* `__next__`: 배치 단위로 데이터를 순차적으로 반환, 끝나면 `StopIteration` 발생
* `__len__`: 전체 배치 개수를 계산해 반환

---

