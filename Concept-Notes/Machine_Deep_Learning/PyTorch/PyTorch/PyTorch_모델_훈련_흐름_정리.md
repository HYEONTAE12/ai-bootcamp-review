
---

# 📌 PyTorch Dataset · DataLoader · Model · Training · Inference 정리

## 1. Dataset과 DataLoader

### 🔹 Dataset

* **역할**: 단일 데이터를 모델 입력에 적합한 형태(`torch.Tensor`)로 변환 및 반환.
* **종류**

  * PyTorch 내장 Dataset: `MNIST`, `CIFAR10`, `ImageFolder` 등.
  * Custom Dataset: 직접 구현 필요.
    `torch.utils.data.Dataset` 클래스를 상속하고 다음 3개 메서드를 구현해야 함:

    1. `__init__`: 데이터셋 로드, 경로/변수 선언
    2. `__getitem__`: 주어진 인덱스에 해당하는 데이터 반환
    3. `__len__`: 전체 데이터 개수 반환
* **주의사항**

  * 반환 데이터는 **tensor**여야 함.
  * 반환 형태: `Tensor`, `(Tensor, Tensor)`, `{key: Tensor}` 가능.
  * 모든 샘플의 차원은 **일관성** 있어야 함 (배치 구성 때문).

---

### 🔹 DataLoader

* **역할**: `Dataset`에서 데이터를 꺼내 **미니배치 단위**로 묶어 제공.
* **주요 인자**

  1. `dataset`: 사용할 Dataset 객체 (필수)
  2. `batch_size` (기본=1): 미니배치 크기
  3. `shuffle` (기본=False): 매 epoch마다 데이터 순서 섞기
  4. `num_workers` (기본=0): 데이터 로딩에 사용할 서브 프로세스 수
  5. `drop_last` (기본=False): 마지막 배치 크기가 맞지 않으면 버릴지 여부
  6. `collate_fn`: 배치 데이터 결합 방식을 정의 (특히 sequence data에서 중요)
* **미니배치**: 전체 데이터를 잘게 나눈 부분집합. 학습 시 메모리 절약 및 학습 안정화 효과.

---

## 2. 모델 (Model)

### 🔹 PyTorch 제공 모델

* **Torchvision**: ResNet, VGG 등 이미지 분석 특화 모델.
* **PyTorch Hub**: Computer Vision, NLP, Audio, Generative 모델 등 공개 모델 사용 가능.

### 🔹 Custom Model

* 이유: 기존 모델 변형, 새로운 아키텍처 실험 필요.
* **구현 방법**

  * `torch.nn.Module` 클래스를 상속받아 작성.
  * 필수 메서드:

    1. `__init__`: `super().__init__()` 호출, 레이어 정의 및 파라미터 초기화
    2. `forward`: 입력 데이터 연산 정의

---

## 3. 학습(Training)의 기본 구조

### 🔹 학습 루프 일반 구조

```python
for epoch in range(num_epochs):
    for data, label in dataloader:
        optimizer.zero_grad()           # 1. 이전 gradient 초기화
        output = model(data)            # 2. 순전파
        loss = loss_function(output, label)  # 3. 손실 계산
        loss.backward()                 # 4. 역전파(gradient 계산, Autograd 활용)
        optimizer.step()                 # 5. 파라미터 업데이트
```

### 🔹 Autograd & Computational Graph

* **Autograd**: 자동 미분 시스템.
* **Computational graph**:

  * 노드(Node): 연산 (예: +, ×, ReLU)
  * 엣지(Edge): 입력/출력 텐서
* PyTorch는 tensor 연산 시 그래프를 기록 → `loss.backward()` 호출 시 미분 자동 계산.

---

## 4. 추론(Inference)과 평가(Evaluation)

* **추론 과정**: 학습된 모델로 새로운 입력에 대한 예측 수행.
* **필요 설정**

  1. `model.eval()`

     * Dropout, BatchNorm 같은 레이어를 **추론 모드**로 전환.
  2. `with torch.no_grad():`

     * Autograd 비활성화 → gradient 계산 안 함.
     * 메모리 사용량 절감, 속도 향상.

### 🔹 예시

```python
model.eval()
with torch.no_grad():
    for data in test_loader:
        output = model(data)
        # 예측 결과 처리
```

### 🔹 평가 지표

* 분류(Classification): Accuracy, Precision, Recall, F1-score
* 회귀(Regression): MSE, RMSE, MAE

---

## 5. 추가 보충 내용

* **Collate Function (`collate_fn`)**

  * DataLoader가 배치를 구성할 때, 데이터를 어떻게 묶을지 정의하는 함수.
  * NLP 등 길이가 다른 데이터를 다룰 때 패딩(padding)을 넣거나, Dict 형태를 맞출 때 필요.

* **Epoch**

  * 학습 데이터 전체를 한 번 다 학습하는 주기.
  * `epoch` 수가 너무 많으면 과적합 위험 → `early stopping` 활용.

* **GPU 사용**

  ```python
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  model.to(device)
  data, label = data.to(device), label.to(device)
  ```

* **Optimizer 예시**

  * `torch.optim.SGD`, `torch.optim.Adam` 등.
  * 하이퍼파라미터: learning rate, momentum, weight decay 등.

---

## ✅ 최종 정리

* **Dataset**: 단일 데이터 단위 처리/반환
* **DataLoader**: Dataset을 미니배치로 묶어 반환
* **Model**: `nn.Module` 상속 → `__init__` + `forward` 정의
* **Training Loop**: `zero_grad → forward → loss → backward → step`
* **Autograd**: computational graph 기반 자동 미분
* **Inference**: `model.eval()` + `torch.no_grad()`
* **보충 개념**: `collate_fn`, epoch, GPU 사용법, 평가 지표

---

