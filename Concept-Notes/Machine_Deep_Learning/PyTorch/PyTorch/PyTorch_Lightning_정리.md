
---

# ⚡ PyTorch Lightning 정리

PyTorch Lightning은 **PyTorch 코드 구조를 단순화**하고, **연구/개발 → 실험 관리 → 배포**까지 지원하는 프레임워크입니다.

---

## 🎯 PyTorch Lightning의 장점

1. **보일러플레이트(반복 코드) 제거**

   * 학습 루프(`for`문, backward, step 등) 같은 걸 직접 작성할 필요 없음.
   * 코드가 간결해져 **협업**과 **유지보수**가 쉬워짐.

2. **실험 표준화**

   * 여러 사람이 같은 프레임워크 규칙에 맞춰 코드를 작성 → 실험 관리가 체계적.
   * 연구 단계에서 특히 유용 (코드 재현성 ↑).

3. **로깅/실험 추적 통합**

   * W&B, MLflow, TensorBoard 등과 기본 연동 지원.
   * 실험 기록, 메트릭 추적, 시각화를 쉽게 적용 가능.

4. **분산 학습 지원**

   * 단 한 줄 옵션으로 분산 학습 가능:

     ```python
     Trainer(accelerator="gpu", devices=4, strategy="ddp")
     ```
   * Multi-GPU, TPU, 멀티 노드 클러스터까지 자동 지원.
   * 대규모 데이터셋/모델 학습에 최적.

5. **Production 친화성**

   * **LightningLite**, **Fabric**, **LightningApp** 등 배포/서빙 도구 제공.
   * 학습 코드와 추론 코드가 분리 → 재사용성과 유지보수 용이.

---

## 🧩 LightningModule 구성 요소

LightningModule은 `nn.Module`을 확장한 클래스로, **학습·평가·추론 로직을 구조화**합니다.

* **`__init__`**

  * 레이어, 손실 함수, 메트릭 정의.
  * 모델의 주요 구성 초기화.

* **`forward(batch)`**

  * 입력 데이터를 모델에 통과시키는 과정 정의.

* **`configure_optimizers()`**

  * Optimizer 및 (선택적) Scheduler 반환.
  * 예시:

    ```python
    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10)
        return [optimizer], [scheduler]
    ```

* **`training_step(batch, batch_idx)`**

  * 학습 데이터 미니배치별 손실 계산 및 로그 기록.
  * ⚡ PyTorch Lightning이 `zero_grad()`, `backward()`, `step()` 등을 대신 실행하므로 직접 작성할 필요 없음.

* **`validation_step(batch, batch_idx)`**

  * 검증 데이터셋에 대한 손실 및 메트릭 계산.

* **`test_step(batch, batch_idx)`**

  * 테스트 데이터셋에 대한 성능 평가 (손실, 메트릭).

* **`predict_step(batch, batch_idx)`**

  * 추론 단계 정의 (예측값 반환).
  * 분류 확률이나 로짓 등을 반환하도록 자유롭게 구현 가능.

📌 [공통] 평가(`eval()`), 추론 시 `torch.no_grad()` 같은 반복 코드도 작성할 필요 없음.

---

## 🔧 Trainer 주요 메서드

Trainer는 **학습 실행 엔진** 역할을 담당합니다.

* **`.fit()`**

  * 학습 실행.
  * LightningModule, `train_dataloader`, `val_dataloader`를 받아서 자동 학습 진행.
  * 내부적으로 `training_step`, `validation_step`, `configure_optimizers`를 호출.

* **`.validate()`**

  * 검증 데이터셋 평가.
  * 학습 종료 후, 별도로 검증만 수행 가능.

* **`.test()`**

  * 테스트 데이터셋 평가.
  * `test_step`을 호출하여 모델 성능 평가.

* **`.predict()`**

  * 추론 실행.
  * `predict_step`을 호출해 결과(예측값) 반환.

---

## 📊 전체 구조 요약

| 구성 요소                  | 역할             | 작성 필요 여부 |
| ---------------------- | -------------- | -------- |
| `__init__`             | 레이어/손실/메트릭 정의  | ✅        |
| `forward`              | 모델 순전파 정의      | ✅        |
| `configure_optimizers` | 옵티마이저, 스케줄러 설정 | ✅        |
| `training_step`        | 학습 배치 손실 계산    | ✅        |
| `validation_step`      | 검증 배치 평가       | 선택적      |
| `test_step`            | 테스트 평가         | 선택적      |
| `predict_step`         | 추론 로직          | 선택적      |

---

✅ **정리**

* PyTorch Lightning은 **반복 코드 제거 + 실험 표준화 + 분산 학습 지원**으로 연구/실무 모두에서 강력.
* `LightningModule` + `Trainer` 조합으로 **모델 정의**와 **학습 실행**을 분리 → 코드 재사용성과 유지보수성이 크게 향상됨.

---

