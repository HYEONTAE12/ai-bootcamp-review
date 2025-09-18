
---

# 📌 파이썬 & 개발 관련 정리

## 1. 디버깅/출력 도구

### IceCream (`icecream`)

* **용도**: 디버깅 시 print 대신 사용, 가독성 높은 출력 제공
* **사용법**

  ```python
  from icecream import ic

  x = 10
  y = 20
  ic(x, y)
  ```

  출력 예:

  ```
  ic| x: 10, y: 20
  ```
* **특징**

  * 변수명과 값을 자동으로 함께 출력
  * `print()` 대신 `ic()`로 호출
  * 분기점 추적용으로 `ic()`만 호출해도 현재 실행 라인 확인 가능

---

## 2. 반복(iterable) 관련

### tqdm

* **용도**: 반복문에 **진행 상황(progress bar)** 추가
* **사용법**

  ```python
  from tqdm import tqdm
  for i in tqdm(range(100)):
      ...
  ```
* **장점**

  * 작업의 진행률을 시각적으로 보여줌
  * 긴 루프 실행 시 상태 파악 용이

---

## 3. 직렬화/역직렬화

### Pickle

* **직렬화(Serialization)**: 파이썬 객체 → 바이트 스트림 변환 (저장/전송 가능)

* **역직렬화(Deserialization)**: 바이트 스트림 → 원래 객체 복원

* **사용 예시**

  ```python
  import pickle

  # 직렬화
  with open("data.pkl", "wb") as f:
      pickle.dump({"a": 1, "b": 2}, f)

  # 역직렬화
  with open("data.pkl", "rb") as f:
      data = pickle.load(f)
  ```

* **문제점**

  * pickle 파일에는 **임의의 파이썬 코드**가 포함될 수 있음
  * `pickle.load()` 시 코드 실행 → 악성 코드 실행 위험
  * 따라서 **신뢰할 수 없는 소스의 pickle 파일은 로드 금지**

* **대안**

  * 범용 포맷: JSON, MessagePack
  * 모델 공유: **ONNX (Open Neural Network Exchange)**

    * 런타임 의존성이 없고, 다양한 프레임워크 간 호환 가능

---

## 4. 작업(Task) 분리

* **이유**

  * 자원 분배 효율적
  * 불필요한 자원 낭비 방지
  * 코드/기능 모듈화 → 유지보수 용이

* **도구: Fire**

  * 구글이 만든 CLI(Command Line Interface) 자동 생성 라이브러리
  * 파이썬 함수/클래스를 터미널 명령어로 쉽게 실행 가능
  * 예시:

    ```python
    import fire

    def greet(name="World"):
        return f"Hello {name}!"

    if __name__ == "__main__":
        fire.Fire(greet)
    ```

    실행:

    ```bash
    python app.py --name=현태
    ```

---

## 5. 명령어 히스토리 관리

* **history**

  * 터미널에서 실행한 명령어 기록 확인
  * 특정 번호 명령어 재실행 가능

* **사용법**

  ```bash
  history      # 전체 목록 확인
  !156         # 156번째 명령어 재실행
  ```

---

## 6. 코드 스타일 & 주의사항

* **예약어 사용 금지**

  * 파이썬의 예약어(`class`, `def`, `for`, `while`, `lambda`, `try` 등)를 변수명/함수명으로 사용하면 **에러/혼란 발생**
  * 예:

    ```python
    list = [1, 2, 3]   # X → 내장함수 list를 덮어씀
    ```

* **안티패턴(Anti-pattern)**

  * 작동은 하지만 **유지보수/가독성/안정성에 해로운 코드 스타일**
  * 예:

    * `from module import *` → 어떤 함수가 로드됐는지 불명확
    * try-except로 모든 에러 무조건 무시하기
    * 글로벌 변수 남발
    * 예약어를 변수명으로 사용하기

---

# ✅ 요약

* **icecream(ic)**: print 대신 디버깅용 출력 (변수명+값 자동 추적)
* **tqdm**: 반복문 진행률 표시
* **pickle**: 직렬화/역직렬화 → 보안 위험 주의, 대안으로 JSON/ONNX 활용
* **Fire**: Task 분리 & CLI 자동화
* **history / !번호**: 명령어 히스토리 재실행
* **예약어 사용 금지 & 안티패턴 피하기**: 코드 가독성과 안전성 보장

---

