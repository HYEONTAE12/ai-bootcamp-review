# 강의 메모 핵심 정리 + 보충

## 1) 디버깅/로깅 도구: `icecream`

* **뭐임?** `print`보다 똑똑한 디버깅 프린터. 변수명, 위치(파일:라인), 값까지 자동 출력.
* **왜 씀?** “여기서 무슨 값이지?”를 빠르게 확인. 라인 분기 체크에 `ic()`만 호출해도 위치 찍힘.
* **자주 쓰는 패턴**

  ```python
  from icecream import ic

  ic(a, b)          # 변수명과 값 함께 출력
  ic()              # 현재 파일/라인만 찍어서 '여기 찍힘' 확인용
  ic.enable()       # 출력 켜기
  ic.disable()      # 출력 끄기 (배포 전)
  ```
* **print → ic** 바꾸기: `print(a)` 대신 `ic(a)`로.
  (권장) 전역으로 `print = ic` 같은 건 지양.

---

## 2) 진행률 표시: `tqdm`

* **뭐임?** 이터러블에 감싸면 루프 진행률/ETA를 보여줌.
* **예시**

  ```python
  from tqdm import tqdm
  for i in tqdm(range(10000)):
      ...
  ```
* **데이터로더와 함께**

  ```python
  for batch in tqdm(dataloader, total=len(dataloader)):
      ...
  ```

---

## 3) 직렬화/역직렬화: `pickle`

* **왜 씀?** 파이썬 객체(모델, 스케일러 등)를 **바이트로 저장(직렬화)** 했다가 **복원(역직렬화)**.
* **기본 사용**

  ```python
  import pickle
  with open("obj.pkl", "wb") as f:
      pickle.dump(obj, f)

  with open("obj.pkl", "rb") as f:
      obj = pickle.load(f)     # 역직렬화
  ```
* **문제점(중요)**: **신뢰할 수 없는 피클을 `load` 하면 코드가 실행될 수 있어 보안 취약**.
  → **항상 내가 만든 파일만** 로드. 해시 검증(SHA256)이나 서명 검토 고려.
  → 단순 구조는 **JSON/YAML** 등으로, 모델은 **ONNX** 등 표준 포맷 추천.
* **joblib**: 대용량 NumPy 포함 모델을 더 빠르게 저장하는데 자주 쓰지만, **내부적으로 pickle 계열**이므로 **보안상 동일 주의**.

---

## 4) ONNX: 모델 공통 포맷

* **뭐임?** 프레임워크 독립 **모델 교환 포맷**(IR). PyTorch/TF → ONNX로 내보내고, **ONNX Runtime** 등으로 실행.
* **장점**

  * **런타임/언어 독립**(Python 없이도 C++/Java 등에서 추론 가능)
  * 배포 표준화, 최적화(Graph/Kernel 최적화, EPs: CUDA, TensorRT 등)
* **언제 씀?**

  * 서비스/앱이 파이썬에 의존하지 않게 하려는 경우
  * 타 언어 스택(예: Java)에서 모델 추론 필요할 때

---

## 5) 작업(Task) 분리

* **왜 나눔?**

  * **자원 분배**: CPU/GPU, I/O 분리 → 병렬/비동기 처리 효율↑
  * **자원 낭비 방지**: 긴 작업/짧은 작업 섞일 때 병목 제거
  * **관심사 분리**: 학습/전처리/평가/서빙 모듈화
* **도구 예시**

  * **모듈/서브커맨드 분리**: 함수별로 CLI 제공 → 빠른 작업 실행
  * **`fire`**: 파이썬 객체로 **즉시 CLI 생성**

    ```python
    import fire

    class Task:
        def train(self, epochs=10): ...
        def infer(self, path: str): ...

    if __name__ == "__main__":
        fire.Fire(Task)   # `python app.py train --epochs=20`
    ```

---

## 6) 셸 히스토리 활용

* **히스토리 보기**: `history`
* **번호로 재실행**: `!156`  → 히스토리 156번 명령 재실행
* **이전 명령 재실행**: `!!`
* **접두어로 재실행**: `!git` → 마지막 `git`으로 시작한 명령 재실행
* **빠른 치환**: `^foo^bar` → 직전 명령의 `foo`를 `bar`로 바꿔 재실행

---

## 7) 예약어/내장 이름 사용 지양 (안티패턴)

* **피해야 할 변수명**: `list`, `dict`, `str`, `sum`, `len`, `map`, `id`, `type`, `input` 등 **파이썬 내장**을 가리는 이름.
* **왜?** 디버깅 지옥(내장을 덮어써서 예기치 않은 에러).
* **해법**: 접미어 붙이기

  ```python
  list_ = [...]
  dict_ = {...}
  sum_ = ...
  ```

---

## 8) 한 페이지 요약

* **icecream**: `ic(x)`, `ic()`로 위치/값 즉시 확인. 배포 전 `ic.disable()`.
* **tqdm**: 루프 진행률/ETA. `tqdm(range(...))`.
* **pickle**: (역)직렬화. **신뢰된 파일만 load**. 대안: JSON/YAML/ONNX.
* **ONNX**: 프레임워크/언어 독립 배포. ONNX Runtime로 추론.
* **Task 분리**: 자원/관심사 분리. `fire`로 작업별 CLI.
* **history/!N**: 히스토리 재실행으로 속도 ↑.
* **예약어 금지**: 내장 이름 가리지 말 것. 필요시 `_` 접미사.

.
