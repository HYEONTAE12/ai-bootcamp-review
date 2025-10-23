---

# 🔹 W&B 주요 기능 정리

## 1. `wandb.init()`

* **기능**: 새로운 W&B 런(run)을 시작하고 서버에 연결
* **주요 인자**

  * `project="프로젝트명"` → 어떤 프로젝트에 기록할지
  * `name="실험명"` → 런 이름 지정
  * `config={...}` → 하이퍼파라미터/세팅 기록
* **예시**

  ```python
  import wandb
  wandb.init(project="my_project", name="exp1", config={"lr": 0.001, "epochs": 10})
  ```

---

## 2. `wandb.log()`

* **기능**: 실험 중의 metric, loss, accuracy 같은 값들을 기록 (그래프 생성)
* **사용 방식**

  ```python
  for epoch in range(10):
      train_loss = 0.5
      acc = 0.8
      wandb.log({"train_loss": train_loss, "accuracy": acc, "epoch": epoch})
  ```
* → W&B 대시보드에서 실시간으로 그래프 확인 가능

---

## 3. `wandb.finish()`

* **기능**: 현재 런(run)을 종료
* **언제 사용?**

  * 실험 끝나고 로그 마무리할 때
* **예시**

  ```python
  wandb.finish()
  ```

---

## 4. `wandb.watch()`

* **기능**: 모델 파라미터와 gradient를 자동으로 기록/시각화
* **주로 PyTorch에서**

  ```python
  wandb.watch(model, log="all")
  ```
* `log="all"` → gradient와 parameter histogram 모두 기록

---

## 5. `wandb.Image()`

* **기능**: 로그에 이미지 기록할 때 사용
* **예시**

  ```python
  images, labels = next(iter(dataloader))
  wandb.log({"examples": [wandb.Image(img, caption=str(lbl)) for img, lbl in zip(images, labels)]})
  ```
* 데이터 샘플, 예측 결과, 시각화된 이미지 등을 저장할 때 유용

---

## 6. Sweep

* **Sweep** = 여러 하이퍼파라미터 조합을 자동으로 탐색하는 기능
* Sweep은 2가지 구성 요소로 돌아감:

  1. **Sweep Config** (탐색할 하이퍼파라미터 범위 정의)
  2. **Agent** (실제로 실험 실행)

---

## 7. `wandb.sweep()`

* **기능**: Sweep을 생성하고 ID 반환
* **예시**

  ```python
  sweep_config = {
      "method": "grid",  # grid, random, bayes
      "parameters": {
          "lr": {"values": [0.001, 0.01]},
          "batch_size": {"values": [16, 32]}
      }
  }
  sweep_id = wandb.sweep(sweep=sweep_config, project="my_project")
  ```

---

## 8. `wandb.agent()`

* **기능**: 특정 sweep을 실행하는 "worker"
* **예시**

  ```python
  def train():
      wandb.init()
      # wandb.config 안에서 sweep 값이 자동으로 전달됨
      lr = wandb.config.lr
      batch_size = wandb.config.batch_size
      ...
      wandb.finish()

  wandb.agent(sweep_id, function=train, count=4)
  ```
* `count` = 몇 번의 실험을 실행할지 지정
* 여러 서버/노드에서 동시에 agent 실행 가능 → 분산 하이퍼파라미터 탐색 가능

---

# 🔹 전체 흐름 요약

1. **기본 실험**

   * `wandb.init()` → `wandb.log()` 반복 → `wandb.finish()`

2. **모델 추적**

   * `wandb.watch(model)`

3. **데이터/결과 시각화**

   * `wandb.Image()`

4. **하이퍼파라미터 탐색**

   * `wandb.sweep()`으로 sweep 생성
   * `wandb.agent()`으로 실험 자동 실행

---

✅ 정리 문장

* `init` = 런 시작
* `log` = 메트릭 기록
* `finish` = 런 종료
* `watch` = 모델 파라미터/gradient 추적
* `Image` = 이미지 로그
* `sweep` = 하이퍼파라미터 탐색 정의
* `agent` = sweep 실행기(worker)

---


