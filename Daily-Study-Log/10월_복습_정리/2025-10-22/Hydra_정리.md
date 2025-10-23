

---

# 🐍 Hydra 정리

Hydra는 **딥러닝/머신러닝 프로젝트에서 복잡한 파라미터 관리 문제**를 해결하기 위해 등장한 오픈소스 프레임워크입니다.

---

## 📌 Hydra 배경

딥러닝 프로젝트에서는 수많은 하이퍼파라미터와 설정값을 다룹니다.
이 값을 코드 내부에 직접 박아두면 아래와 같은 문제가 발생합니다.

1. **관리의 어려움**

   * 파라미터가 여러 파일, 클래스, 함수에 흩어져 있으면 일일이 수정해야 함.
2. **코드 일관성 부족**

   * 같은 파라미터가 여러 곳에서 사용되면, 모든 위치를 동시에 업데이트해야 일관성이 유지됨.

---

## 🧾 Hydra 개요

* Hydra는 **설정 파일(yaml)**을 통해 파라미터를 관리하는 프레임워크.
* **신화 속 Hydra**처럼, 여러 개의 머리(설정 파일) → 하나의 몸체(실행 코드)로 유기적으로 관리.
* 다양한 태스크를 설정 조합으로 쉽게 실행할 수 있도록 지원.

---

## 📂 데이터 포맷

* Hydra는 **YAML** 포맷을 사용.
* 사람이 읽기 쉽고 계층 구조를 표현하기 적합.

---

## ✨ Hydra 특징

* **OmegaConf** 기반으로 개발됨.
* YAML로 변수 정의, 참조 가능.
* **커맨드라인에서 손쉽게 파라미터 추가/변경** 가능.
* 여러 개의 설정 파일을 하나의 큰 설정처럼 합쳐 사용 가능.
* **설정 조합을 통해 다양한 실험을 한 번에 실행** 가능.

---

## 📌 Default List

* **Config Group**: 특정 항목(예: 모델 종류)에 여러 선택지가 있을 때, 그 중 기본값을 설정.
* `configs/config.yaml`에 `defaults` 블록을 추가해 지정.
* 예시:

  ```
  # configs/config.yaml
  defaults:
    - model: resnet18
  ```

  * `model/` 폴더에 `resnet18.yaml`, `resnet34.yaml`이 있으면, 기본적으로 `resnet18`을 사용.

---

## ⚙️ 작동 구조

1. **데코레이터 등록**

   ```python
   @hydra.main(config_path="configs", config_name="config")
   def main(cfg):
       ...
   ```

   * `config_path`: 설정 파일 폴더 위치
   * `config_name`: 기본 설정 파일 이름

2. **함수 인자로 Config 받기**

   * `cfg` 객체에 YAML 설정이 매핑됨
   * 접근 방식:

     ```python
     cfg.data.batch_size        # 객체 방식
     cfg["data"]["batch_size"]  # 딕셔너리 방식
     ```

---

## 💻 커맨드라인 오버라이딩

Hydra는 터미널에서 실행 시 파라미터를 쉽게 바꿀 수 있습니다.

* 기존 값 변경:

  ```bash
  python train.py data.batch_size=64 optimizer.lr=0.1
  ```
* 새로운 값 추가 (`+`):

  ```bash
  python train.py +optimizer.weight_decay=0.001
  ```
* 기존 값 수정 또는 추가 (`++`):

  ```bash
  python train.py ++optimizer.lr=0.05 ++data.valid_split=0.2
  ```

---

## 📂 실행 결과 관리

* Hydra는 실행 시마다 자동으로 결과 폴더를 생성:

  ```
  outputs/YYYY-MM-DD/HH-MM-SS/
  ```
* 포함 파일:

  * `.hydra/`

    * `config.yaml` : 최종 사용된 설정값
    * `overrides.yaml` : 커맨드라인에서 덮어쓴 값
    * `hydra.yaml` : Hydra 내부 메타정보 (버전, 실행 위치 등)
  * `[실행한 코드].log` : 실행 로그

👉 덕분에 **실험 재현성**이 매우 높음.

---

## 🔨 Hydra 추가 기능

### 1. Instantiate

* 설정 파일에서 정의한 클래스를 실제 인스턴스로 변환.
* 예시 설정 (`configs/loss.yaml`):

  ```yaml
  loss_function:
    _target_: torch.nn.CrossEntropyLoss
  ```
* 코드에서:

  ```python
  from hydra.utils import instantiate
  criterion = instantiate(cfg.loss_function)
  ```
* 주의: Alias(`import torch.nn as nn`)는 사용할 수 없음.

---

### 2. Multi-run

* 여러 설정 조합을 한 번에 실행.
* `--multirun` 옵션 사용.
* 예시:

  ```bash
  python train.py --multirun model=resnet18,resnet34 loss_function=mse_loss,cross_entropy
  ```
* 자동으로 조합별 실행이 반복되어, **대량 실험 관리에 적합**.

---

## ✅ 요약

| 기능                         | 설명                   |
| -------------------------- | -------------------- |
| **YAML 설정 관리**             | 코드와 파라미터 분리, 재사용성 ↑  |
| **Config Group & Default** | 여러 설정 중 기본값 지정       |
| **커맨드라인 오버라이딩**            | 파라미터 동적 변경/추가 가능     |
| **자동 결과 기록**               | 실행별 폴더 생성 → 재현성 보장   |
| **Instantiate**            | 설정 기반 객체 생성          |
| **Multi-run**              | 여러 설정 조합 실험을 한 번에 실행 |

---

👉 정리하면, Hydra는 **복잡한 설정을 깔끔하게 관리하고, 실험 재현성과 자동화**를 극대화해주는 프레임워크입니다.

---

