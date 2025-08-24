---

# CPU 파이프라인과 성능 최적화 기법 정리

## 1. 기본 5-Stage 파이프라인

CPU는 명령어를 겹쳐 실행하기 위해 파이프라인을 사용한다. 대표적으로 **MIPS 구조의 5단계 파이프라인**은 다음과 같다.

1. **IF (Instruction Fetch)**

   * PC(Program Counter)가 가리키는 주소에서 명령어를 가져옴.
   * 동시에 다음 명령어의 주소(PC+4)도 계산해둔다.

2. **ID (Instruction Decode & Register Fetch)**

   * 명령어를 해석(Opcode, Register, Immediate 등).
   * 필요한 레지스터 값 읽기.
   * 제어 신호 생성.

3. **EX (Execute / Address Calculation)**

   * ALU 연산 수행.
   * 분기 명령어라면 조건 판단 및 분기 대상 주소 계산.

4. **MEM (Memory Access)**

   * Load/Store 명령일 경우 데이터 메모리에 접근.

5. **WB (Write Back)**

   * 연산 결과를 레지스터 파일에 기록.

---

## 2. 파이프라인 성능을 높이는 기법들

### 🔹 슈퍼스칼라 (Superscalar)

* \*\*한 사이클에 여러 명령어를 동시에 발행(issue)\*\*할 수 있는 구조.
* 병렬성이 높아지지만, 명령어 간 **데이터 의존성**이나 **제어 의존성** 때문에 제약 발생.

---

### 🔹 Out-of-Order Execution (순서 비순차 실행)

* 프로그램 순서 그대로 실행하지 않고, **독립적인 명령어부터 먼저 실행**.
* 병목 현상(예: 메모리 접근 대기)을 피할 수 있음.
* \*\*리오더 버퍼(Reorder Buffer)\*\*를 사용해 프로그램이 요구하는 최종 순서를 보장.
* **Register Renaming**을 통해 WAW, WAR 같은 가짜 의존성 해결.

---

### 🔹 Speculative Execution (추측 실행) & 분기 예측(Branch Prediction)

* 분기 명령을 만나면 CPU는 실제 결과를 기다리지 않고 **예측된 경로를 먼저 실행**.
* 맞으면 성능 향상, 틀리면 **파이프라인 플러시(Flush)** 후 올바른 경로를 다시 실행.
* 현대 CPU는 성능을 위해 **고급 분기 예측기**를 탑재해 정확도를 극대화.

---

### 🔹 분기 명령(Branch Instruction)이란?

* 프로그램의 실행 흐름을 바꾸는 명령.
* **조건 분기**: 조건이 참일 때만 점프 (예: `BEQ`, `BNE`).
* **무조건 분기**: 조건과 상관없이 점프 (예: `J`).
* 고수준 언어의 `if`, `for`, `while`이 저수준에서는 분기 명령으로 변환됨.

---

### 🔹 Forwarding (데이터 전달)

* 앞 명령어의 결과를 레지스터에 기록하기 전에, **바로 다음 EX 단계로 전달**.
* RAW 의존성에서 불필요한 stall을 줄여줌.
* 단, **메모리에서 읽어오는 LW(load)** 직후 결과는 forwarding만으로 해결이 어려움 → stall 불가피.

---

## 3. 의존성과 해저드

### 🔹 두 가지 큰 의존성

1. **데이터 의존성(Data Dependency)**

   * 앞 명령어의 연산 결과가 뒤 명령어에 필요할 때 발생.
   * 해결 방법: Forwarding, Out-of-Order, Register Renaming 등.

2. **제어 의존성(Control Dependency)**

   * 분기 명령 실행 결과가 확정되기 전까지 어떤 명령을 실행해야 할지 모를 때 발생.
   * 해결 방법: 분기 예측 + 추측 실행, 틀리면 플러시.

---

### 🔹 데이터 의존성의 세 가지 유형

1. **RAW (Read After Write) — 진짜 의존성**

   * 앞 명령이 값을 쓰고 나서, 뒤 명령이 그 값을 읽어야 함.
   * 해결: Forwarding, stall.

2. **WAR (Write After Read) — 반의존성**

   * 앞 명령이 읽기 끝내기 전에, 뒤 명령이 같은 위치에 쓰려 하면 문제.
   * 해결: Register Renaming.

3. **WAW (Write After Write) — 출력 의존성**

   * 두 명령이 같은 위치에 연속으로 쓰려 할 때 순서가 바뀌면 최종 결과가 달라짐.
   * 해결: Register Renaming + Out-of-Order 제어.

---

## 🔹 데이터 vs 제어 의존성 비교

* **데이터 의존성**: 값이 준비될 때까지 **강제 stall** 필요.
* **제어 의존성**: 분기 예측을 활용해 **예측 실행** 가능.

  * 맞으면 stall 회피, 틀리면 flush라는 penalty.

---

