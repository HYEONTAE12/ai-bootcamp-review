
---

# Hydra `run_dir`와 Checkpoint 저장 정리

## 🔹 Hydra가 자동으로 하는 일

Hydra는 실행할 때마다 자동으로 **결과 저장 폴더(run_dir)** 를 만듭니다.

* 기본 경로: `outputs/날짜/시간`
* 자동 저장되는 내용:

  * `.hydra/config.yaml` → 최종 실행 config
  * `.hydra/overrides.yaml` → CLI로 바꾼 옵션
  * `.hydra/hydra.yaml` → Hydra 내부 config
  * `stdout/stderr` 로그 (`train.log` 등)

👉 즉, Hydra는 **실험 재현을 위한 최소 정보(config + 로그)** 를 자동 기록해줍니다.

---

## 🔹 Checkpoint를 run_dir에 저장하는 이유

1. **재현성 보장**

   * 모델 가중치(checkpoint)까지 같은 폴더에 저장하면
     `config + 로그 + 모델 상태`를 모두 포함한 완전한 재현 가능 패키지가 됨.

2. **실험 관리 편리**

   * Hydra가 만든 run_dir이 **시간/실험 단위로 구분**되기 때문에
     checkpoint까지 같이 있으면 “이 실험의 결과물이 뭐였는지”를 쉽게 추적할 수 있음.

3. **멀티런(sweep) 안전**

   * Hydra는 sweep 실행 시 job마다 다른 run_dir을 생성.
   * checkpoint를 run_dir에 두면 job 간 덮어쓰기를 방지할 수 있음.

---

## 🔹 코드 예시

```python
from hydra.core.hydra_config import HydraConfig
from pathlib import Path
import torch

def save_checkpoint(model, optimizer, epoch):
    run_dir = Path(HydraConfig.get().runtime.output_dir)
    ckpt_path = run_dir / f"checkpoint_epoch_{epoch}.pt"
    torch.save({
        "epoch": epoch,
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
    }, ckpt_path)
    print(f"✅ Checkpoint saved at {ckpt_path}")
```

---

## 📂 실행 결과 예시

```
outputs/2025-10-24/22-15-03/
│── .hydra/config.yaml
│── .hydra/overrides.yaml
│── train.log
│── checkpoint_epoch_10.pt
│── checkpoint_epoch_20.pt
```

---

## ✅ 정리

* Hydra는 **config와 로그만** 자동으로 저장해준다.
* **모델 checkpoint는 직접 run_dir에 저장**해야 한다.
* 이렇게 하면 **하나의 run_dir만 있으면 실험을 그대로 복원할 수 있음** → 관리 & 재현성 극대화.

---

