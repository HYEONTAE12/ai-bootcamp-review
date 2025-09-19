

---

# 📌 Code Review: `main.py`

```python
import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # /opt/mlops
)
```

### 🔹 경로 설정

* `abspath(__file__)`: 현재 실행 중인 파일의 절대 경로 반환.
* `dirname`을 두 번 호출 → `/opt/mlops/src` → `/opt/mlops` 까지 상위 디렉토리 이동.
* 최종적으로 `/opt/mlops` 경로를 `sys.path`에 추가하여 **모듈 임포트 경로 문제를 해결**.

---

```python
import fire
import wandb
import numpy as np
from dotenv import load_dotenv
from icecream import ic
```

### 🔹 외부 라이브러리

* **fire**: CLI(Command Line Interface)를 간단히 만들어주는 라이브러리 (Task 단위 실행).
* **wandb**: 실험 기록/추적 도구.
* **dotenv (load\_dotenv)**: `.env` 파일에서 환경 변수를 로드.
* **icecream**: 디버깅용 출력 라이브러리 (`print` 대체).

---

```python
from src.dataset.watch_log import get_datasets
from src.dataset.data_loader import SimpleDataLoader
from src.model.movie_predictor import MoviePredictor, model_save
from src.utils.utils import init_seed, auto_increment_run_suffix
from src.utils.enums import ModelTypes
from src.train.train import train
from src.evaluate.evaluate import evaluate
from src.inference.inference import (
        load_checkpoint,
        init_model,
        inference,
        recommend_to_df
)
from src.postprocess.postprocess import write_db
```

### 🔹 모듈화된 내부 코드 임포트

* 데이터셋 처리, 모델 정의, 학습/평가/추론, 후처리까지 역할별로 모듈화하여 관리.

---

```python
init_seed()
load_dotenv()
```

### 🔹 초기 설정

* `init_seed()`: 랜덤 시드를 고정해 어디서 실행하든 결과가 달라지지 않도록 재현성 확보.
* `load_dotenv()`: `.env` 파일에서 환경 변수를 로드.

---

```python
def get_runs(project_name):
    return wandb.Api().runs(path=project_name, order="-created_at")
```

### 🔹 get\_runs

* `project_name`을 입력받아 W\&B API를 호출.
* 해당 프로젝트의 **실험(run) 목록을 최신순**으로 반환.

---

```python
def get_latest_run(project_name):
    runs = get_runs(project_name)
    if not runs:
        return f"{project_name}-000"
    return runs[0].name
```

### 🔹 get\_latest\_run

* 최신 run 이름을 반환.
* 만약 기존 run이 없다면 `"project_name-000"`을 기본값으로 반환.
* 이후 새로운 run 이름을 생성할 때 기준이 됨.

---

```python
def run_train(model_name, num_epochs=10):
    ModelTypes.validation(model_name)
```

### 🔹 모델 검증

* `ModelTypes.validation(model_name)`
  → 전달된 `model_name`이 Enum에 정의된 유효한 모델인지 확인.
* 등록되지 않은 모델명일 경우 `ValueError` 발생.

---

```python
    api_key = os.environ["WANDB_API_KEY"]
    wandb.login(key=api_key)
```

### 🔹 W\&B 로그인

* 환경 변수에서 `WANDB_API_KEY`를 가져와 로그인.
* 외부에 노출되면 안 되므로 `.env` 파일로 관리하는 것이 일반적.

---

```python
    project_name = model_name.replace("_", "-")  # movie_predictor → movie-predictor
    run_name = get_latest_run(project_name)
    next_run_name = auto_increment_run_suffix(run_name)
```

### 🔹 프로젝트/실험 이름 설정

* 언더바(`_`)를 하이픈(`-`)으로 변환해 W\&B 프로젝트 이름으로 사용.
* `get_latest_run()`으로 마지막 실험 이름을 가져오고,
* `auto_increment_run_suffix()`로 실험 번호를 +1 증가시켜 새로운 run 이름 생성.

---

```python
    wandb.init(
        project=project_name,
        id=next_run_name,
        name=next_run_name,
        notes="content-based movie recommend model",
        tags=["content-based", "movie", "recommend"],
        config=locals(),
    )
```

### 🔹 실험 초기화 (wandb.init)

* `project`: 프로젝트 이름
* `id` / `name`: run 식별자 (예: movie-predictor-001)
* `notes`: 설명
* `tags`: 필터링/분류용 태그
* `config=locals()`: 현재 함수 내의 모든 로컬 변수를 config로 저장 → 하이퍼파라미터 추적 가능.

---

```python
    train_dataset, val_dataset, test_dataset = get_datasets()
    train_loader = SimpleDataLoader(train_dataset.features, train_dataset.labels, batch_size=32, shuffle=True)
    val_loader = SimpleDataLoader(val_dataset.features, val_dataset.labels, batch_size=64, shuffle=False)
    test_loader = SimpleDataLoader(test_dataset.features, test_dataset.labels, batch_size=64, shuffle=False)
```

### 🔹 데이터셋 & DataLoader 생성

* `get_datasets()` → 데이터셋을 `train`, `val`, `test`로 분리 후 전처리 완료된 객체 반환.
* `train_loader`: 학습 데이터, 셔플 적용.
* `val_loader`, `test_loader`: 검증/테스트 데이터, **셔플 미적용** (순서 보존 필요).

---

```python
    model_params = {
        "input_dim": train_dataset.features_dim,
        "num_classes": train_dataset.num_classes,
        "hidden_dim": 64
    }
    model_class = ModelTypes[model_name.upper()].value
    model = model_class(**model_params)
```

### 🔹 모델 초기화

* `features_dim`: 입력 벡터 차원 수.
* `num_classes`: 출력 클래스 개수.
* `hidden_dim`: 은닉층 차원 수.
* `ModelTypes Enum`에서 해당 모델 클래스 추출 후 인스턴스 생성.

---

```python
    for epoch in range(num_epochs):
        train_loss = train(model, train_loader)
        val_loss, _ = evaluate(model, val_loader)
        wandb.log({"Loss/Train": train_loss})
        wandb.log({"Loss/Valid": val_loss})
```

### 🔹 학습 루프

* `train()`: 모델 학습 → 훈련 손실 반환.
* `evaluate()`: 검증 데이터 평가 → 검증 손실 반환.
* `wandb.log()`: 학습/검증 손실을 W\&B에 기록.
* 손실 추이를 통해 **과적합 여부 확인 가능**.

---

```python
    wandb.finish()
    test_loss, predictions = evaluate(model, test_loader)
    model_save(
        model=model,
        model_params=model_params,
        epoch=num_epochs,
        loss=train_loss,
        scaler=train_dataset.scaler,
        label_encoder=train_dataset.label_encoder,
    )
```

### 🔹 학습 종료 & 저장

* `wandb.finish()`: run 종료.
* `evaluate(model, test_loader)`: 테스트 데이터 평가.
* `model_save()`:

  * 모델 가중치/바이어스
  * 하이퍼파라미터
  * 학습 손실 값
  * 전처리기(`scaler`, `label_encoder`)
    → `.pkl` 파일로 직렬화 저장.

---

```python
def run_inference(data=None, batch_size=64):
    checkpoint = load_checkpoint()
    model, scaler, label_encoder = init_model(checkpoint)
```

### 🔹 추론 준비

* `load_checkpoint()`: 최근 저장된 체크포인트 불러오기.
* `init_model()`: 동일 구조의 모델을 생성하고 가중치/전처리기 로드.

---

```python
    if data is None:
        data = []
    data = np.array(data)
```

### 🔹 입력 데이터 처리

* 외부에서 데이터가 들어오지 않으면 빈 리스트 사용.
* numpy 배열로 변환 후 모델 입력 형태에 맞춤.

---

```python
    recommend = inference(model, scaler, label_encoder, data, batch_size)
    print(recommend)
    write_db(recommend_to_df(recommend), "mlops", "recommend")
```

### 🔹 추론 실행

* `inference()`: 입력 데이터를 스케일링 → 배치 처리 → 순전파 → 결과 디코딩.
* `write_db()`: 추천 결과를 DataFrame으로 변환해 DB(`mlops.recommend`)에 저장.

---

```python
if __name__ == "__main__":
    fire.Fire({
        "train": run_train,
        "inference": run_inference,
    })
```

### 🔹 CLI 실행

* `fire.Fire()`로 CLI Task를 정의.
* 실행 예시:

  ```bash
  python main.py train --model_name movie_predictor
  python main.py inference --data "[[1, 2, 3]]"
  ```

---

# ✅ 정리

* **경로 설정**: sys.path 조정으로 모듈 임포트 문제 해결.
* **환경 설정**: 시드 고정, 환경 변수 로드.
* **W\&B 연동**: 실험 버전 관리 + 로그 기록.
* **데이터셋 & 모델 초기화**: 모듈화된 코드로 데이터/모델 관리.
* **학습 루프**: train → validate → log.
* **모델 저장**: 결과 + 전처리기까지 `.pkl`로 직렬화.
* **추론**: 체크포인트 불러와 결과 반환 + DB 저장.
* **CLI 실행**: `fire`로 Task(`train`, `inference`) 실행 가능.

---

