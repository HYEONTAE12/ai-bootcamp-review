# TCP 신뢰성과 오류 제어

## TCP는 신뢰성 프로토콜

* TCP(Transmission Control Protocol)는 **신뢰성 보장**을 위해 다양한 메커니즘을 사용한다.
* 특징:

  * 연결 지향적 (Connection-oriented)
  * 순서 보장 (순서 번호, 재정렬)
  * 오류 검출 및 재전송
  * 흐름 제어, 혼잡 제어 지원

---

## 재전송 기반의 오류 제어

TCP는 데이터가 손상되거나 누락된 경우 \*\*재전송(Retransmission)\*\*을 통해 신뢰성을 보장한다.

### 재전송이 일어나는 경우

1. **중복된 ACK 세그먼트를 수신했을 때**

   * 동일한 ACK 번호가 3번 연속 수신되면, 특정 세그먼트가 손실된 것으로 간주 → 빠른 재전송(Fast Retransmit).

2. **타임아웃(Timeout) 발생 시**

   * 송신자가 보낸 세그먼트에 대한 ACK가 일정 시간(RTO, Retransmission Timeout) 내에 도착하지 않으면 재전송.

---

## 흐름 제어 (Flow Control)

* **목적**: 송신자가 너무 빠르게 보내서 수신자가 감당하지 못하는 상황을 방지.
* **방식**: 윈도우(Window) 기반 제어

### 윈도우(Window)

* 수신 호스트가 **한 번에 받을 수 있는 데이터 양**을 송신자에게 알림.
* 윈도우 크기가 커지면 전송 효율이 증가, 작아지면 안전하지만 느려짐.

### 슬라이딩 윈도우 (Sliding Window)

* 송신자는 수신자의 윈도우 크기만큼 여러 패킷을 연속 전송 가능.
* ACK를 받으면 윈도우를 앞으로 "슬라이드" 시켜 새로운 데이터를 전송.

---

## 혼잡 제어 (Congestion Control)

* **목적**: 네트워크 내 과부하(혼잡)를 방지하기 위함.

### AIMD (Additive Increase, Multiplicative Decrease)

* 선형적으로 윈도우 크기를 증가(가산적 증가)
* 혼잡 감지 시 윈도우 크기를 절반으로 줄임(곱셈적 감소).

### RTT (Round Trip Time)

* 패킷이 송신자 → 수신자 → 송신자로 돌아오기까지 걸리는 시간.
* 혼잡 제어와 타임아웃 값 설정의 기준이 됨.

### 혼잡 회피 (Congestion Avoidance)

* 네트워크가 혼잡 상태에 들어가지 않도록 윈도우 크기를 천천히 늘림.

### 세 번의 중복 세그먼트 발생 → 빠른 회복 (Fast Recovery)

* **Fast Retransmit**: 세 번의 중복 ACK 발생 시 손실 세그먼트 즉시 재전송.
* **Fast Recovery**: 혼잡 윈도우(cwnd)를 절반으로 줄이고 선형 증가 시작.

#### TCP Tahoe vs TCP Reno

* **TCP Tahoe**

  * 중복 ACK 발생 시 → 혼잡 윈도우(cwnd)를 1로 줄이고 Slow Start 재시작.
* **TCP Reno**

  * 중복 ACK 발생 시 → Fast Retransmit & Fast Recovery → cwnd 절반 줄이고 선형 증가.

---

## TCP 오류 제어: ARQ (Automatic Repeat reQuest)

* **ARQ** = 수신자가 오류를 감지하면 송신자에게 **재전송 요청**하는 방식.

### 1. Stop-and-Wait ARQ

* **단순**한 방식: 패킷 하나 보낸 후, ACK 받을 때까지 대기.
* 효율 낮음 (회선 유휴 시간 증가).

### 2. Go-Back-N ARQ

* 여러 패킷을 연속 전송 가능.
* 오류 발생 시 해당 패킷 이후 모든 패킷 재전송.
* **누적 확인 응답(Cumulative ACK)** 사용 → 마지막 정상적으로 수신된 패킷까지 ACK 전달.

### 3. Selective Repeat ARQ

* 오류 발생 시 해당 패킷만 재전송.
* 송신자와 수신자가 각각 버퍼를 사용해 순서 맞춤.
* 효율적이지만 구현이 복잡.

---

## 빠른 재전송 (Fast Retransmit)

* 송신자가 **ACK 누락을 기다리지 않고**, 중복된 ACK가 3번 오면 손실된 세그먼트를 즉시 재전송.
* 네트워크 효율성을 크게 향상.

---

## 파이프라이닝 (Pipelining)

* 여러 패킷을 한꺼번에 연속 전송하는 기법.
* Stop-and-Wait보다 훨씬 효율적.
* Sliding Window, Go-Back-N, Selective Repeat 등이 파이프라이닝의 일종.

---

## 버퍼 오버플로우 (Buffer Overflow)

* 송신자가 너무 많은 데이터를 보내면, 수신자의 버퍼 용량을 초과할 수 있음.
* 이 경우 패킷 손실 발생 → 재전송 필요.
* 흐름 제어(윈도우 크기 조절)를 통해 방지.

---

✅ **정리**

* TCP는 **재전송 기반 오류 제어 + 흐름 제어 + 혼잡 제어**로 신뢰성을 보장.
* 오류 제어는 **ARQ 기법**으로, 흐름 제어는 **슬라이딩 윈도우**, 혼잡 제어는 **AIMD, Fast Retransmit/Recovery**를 활용.
* TCP Reno와 Tahoe는 혼잡 상황 대응 방식에서 차이가 있음.
* 결국 TCP는 “최대한 빠르게, 하지만 안전하게” 데이터를 전달하기 위한 **정교한 제어 메커니즘**을 갖춘 프로토콜.

---
