
---

# 📌 `train` 함수 코드 리뷰

```python
from time import sleep
import numpy as np
from icecream import ic
from tqdm import tqdm
```

* **`sleep`** : 반복 후 일정 시간 멈추게 하기 위해 사용
* **`ic`** : `icecream` 라이브러리, 디버깅 시 가독성 좋게 값들을 확인하기 위함
* **`tqdm`** : `for` 루프 진행률을 시각적으로 보여주는 라이브러리

---

```python
def train(model, train_loader):
    total_loss = 0
    for features, labels in tqdm(train_loader):
        predictions = model.forward(features)
        labels = labels.reshape(-1, 1)
        loss = np.mean((predictions - labels) ** 2)
        # ic(loss)
```

* `train` 함수는 **모델**과 **배치 단위를 제공하는 데이터 로더**(`train_loader`)를 입력으로 받음.
* `total_loss`를 0으로 초기화한 후, `tqdm`으로 감싼 `train_loader`에서 `features, labels`를 배치 단위로 가져옴.
* 진행률은 `tqdm`을 통해 시각적으로 확인 가능.
* `model.forward(features)` : 현재 배치의 feature를 입력해 예측값(`predictions`)을 계산.
* `labels.reshape(-1, 1)` : 라벨 벡터 차원을 `(배치 크기, 1)`로 맞춰 모델 출력 형상과 일치시킴.
* `loss` : `(예측값 - 실제값)^2`의 평균(MSE)을 계산해 손실로 사용.
* 필요시 `ic(loss)`로 손실 값을 디버깅 출력 가능.

---

```python
        model.backward(features, labels, predictions)
```

* 모델의 `backward` 메서드를 호출하여 **역전파(backpropagation)** 수행.
* 가중치가 업데이트되도록 `features`, `labels`, `predictions`를 전달.

---

```python
        total_loss += loss
        sleep(0.05)
```

* `total_loss`에 현재 배치의 손실을 누적.
* `sleep(0.05)`로 각 배치 학습 후 0.05초 멈춤 (진행 속도 제어 목적).

---

```python
    return total_loss / len(train_loader)
```

* 학습 종료 후, **평균 손실값**을 반환.
* `len(train_loader)`는 전체 배치 수.

---

# ✅ 요약

* `train` 함수는 배치 단위로 **순전파 → 손실 계산 → 역전파 → 손실 누적**을 수행.
* `tqdm`을 통해 학습 진행률을 시각적으로 확인할 수 있음.
* 최종적으로 **전체 배치 평균 손실**을 반환해 모델의 학습 상태를 확인할 수 있게 함.

---

