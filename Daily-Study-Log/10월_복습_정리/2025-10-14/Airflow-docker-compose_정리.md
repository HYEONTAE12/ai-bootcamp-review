
---

# 🧭 Airflow Docker Compose 정리 & 복습 노트

## 📌 1. Docker Compose의 역할

Airflow는 여러 개의 서비스로 구성돼 있기 때문에
각 서비스를 한 번에 실행·관리하기 위해 **Docker Compose**를 사용한다.

### ✅ 사용 목적

* Airflow는 여러 컨테이너로 구성됨
  (`webserver`, `scheduler`, `worker`, `redis`, `postgres`, `triggerer` 등)
* `docker-compose.yml` 파일은
  **이 서비스들을 한 번에 정의하고 실행하는 역할**을 함.

### ✅ 실행 명령어

```bash
docker compose up -d
```

(`docker-compose.yml` 파일이 있는 경로에서 실행)

---

## 📄 2. YAML 파일 기본 구조

YAML은 들여쓰기로 계층을 표현하며,
XML이나 JSON보다 간결하고 사람이 읽기 쉬운 구조를 가진다.

### 주요 구성

```yaml
x-airflow-common:    # 공통 설정 블록
services:            # 실제 컨테이너 서비스 정의
volumes:             # 데이터 영속화 볼륨 정의
```

---

## ⚙️ 3. `x-airflow-common` 블록

Airflow 서비스들이 공유하는 **공통 설정**을 모아둔 구역.

### 예시

```yaml
x-airflow-common:
  &airflow-common
  image: apache/airflow:2.8.1
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor
  volumes:
    - ./dags:/opt/airflow/dags
```

### 📌 키워드

| 기호    | 의미                              |
| ----- | ------------------------------- |
| `&이름` | 앵커(Anchor): 이 블록을 저장            |
| `*이름` | 불러오기                            |
| `<<:` | 병합(Merge): 불러온 블록 내용을 현재 위치에 합침 |

### 예시 재사용

```yaml
airflow-scheduler:
  <<: *airflow-common       # 공통 설정 전체 복사
  command: scheduler
  environment:
    <<: *airflow-common-env # env만 병합
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
```

### 📘 복습 포인트

* `<<: *airflow-common` → 전체 공통 세트 병합
* `<<: *airflow-common-env` → env만 병합해서 일부 수정
* 큰 블록 병합 후 `environment:`를 다시 쓰면 **공통 env가 교체**되므로 주의!

---

## 🧩 4. Airflow 필수 서비스

| 서비스명                  | 역할                                 |
| --------------------- | ---------------------------------- |
| **postgres**          | 메타데이터 DB (DAG 상태, 변수, 로그 저장)       |
| **redis**             | 브로커(작업 대기열) — Scheduler와 Worker 연결 |
| **airflow-webserver** | UI 제공 (DAG 실행·상태 확인)               |
| **airflow-scheduler** | DAG 스캔, 실행 스케줄 관리, Task를 큐에 등록     |
| **airflow-worker**    | 실제 Task 실행 담당                      |
| **airflow-triggerer** | 비동기(Task 대기) 처리 담당                 |
| **airflow-init**      | 초기 DB 설정 수행 (1회 실행용)               |
| **airflow-cli**       | 임시 명령 실행용 컨테이너 (옵션)                |
| **flower**            | Celery Worker 모니터링용 웹 UI (옵션)      |

---

## ⚙️ 5. Executor 비교 (작업 실행 방식)

| Executor               | 설명                      | 비유        |
| ---------------------- | ----------------------- | --------- |
| **SequentialExecutor** | 한 번에 하나의 Task만 실행       | 혼자 일하는 사람 |
| **LocalExecutor**      | 한 컴퓨터 안에서 여러 Task 병렬 실행 | 같은 사무실 팀  |
| **CeleryExecutor**     | 여러 서버(Worker)가 분산 실행    | 전 세계 지점 팀 |

---

## 🔁 6. 주요 구성요소의 동작 구조

### 📍 전체 흐름 (CeleryExecutor 기준)

```
Scheduler ──> Redis(Queue) ──> Worker ──> DB(Postgres)
```

* **Scheduler**: DAG을 읽고 실행 가능한 Task를 판단 → Redis에 메시지로 등록
* **Redis**: Task 대기열(Queue)을 보관
* **Worker**: Redis에서 Task를 꺼내 실제로 실행
* **Webserver**: 결과를 DB에서 읽어 UI로 표시

---

## ⚡ 7. Triggerer의 역할

Airflow 2.x에서 새로 추가된 프로세스.

### 이유

* Sensor Operator들이 “조건을 기다리는 동안” Worker를 점유해서 비효율적이었음.
* Triggerer가 **대신 기다려줌**으로써 Worker 자원을 아낌.

### 작동 원리

1. Worker가 실행 중 기다릴 상황이 생기면, Task를 Triggerer에게 넘김.
2. Triggerer는 비동기(Async I/O)로 대기.
3. 조건이 만족되면 Worker를 다시 깨워 이어서 실행.

👉 **Worker는 일할 때만 일하고, 대기 시간에는 놀지 않는다!**

---

## 🧠 8. 복습 퀴즈

| 질문                                          | 핵심 답변                                                    |
| ------------------------------------------- | -------------------------------------------------------- |
| **Q1. CeleryExecutor에서 필수 컨테이너는?**          | postgres, redis, webserver, scheduler, worker, triggerer |
| **Q2. `x-airflow-common`은 어디서, 어떻게 재사용하나?** | `&airflow-common`으로 정의 후 `<<: *airflow-common`으로 병합      |
| **Q3. Scheduler와 Worker의 차이?**              | Scheduler는 Task를 정하고, Worker는 실행한다                       |
| **Q4. Redis의 역할?**                          | 작업(Task)을 임시로 보관하는 큐(Queue)                              |
| **Q5. Triggerer의 역할?**                      | Worker 대신 비동기 대기, 자원 절약                                  |
| **Q6. Executor 3종 차이?**                     | Sequential(1명), Local(한 팀), Celery(여러 지점 팀)              |

---

## ✨ 핵심 포인트

* YAML에서 `<<:` 병합 문법이 “얕은 병합(shallow merge)”이라, **env를 다시 쓸 때는 공통 env 병합을 반드시 추가해야 한다.**
* `airflow-init`은 **항상 맨 처음 1회만 실행**하는 초기화 컨테이너다.
* CeleryExecutor를 쓸 땐 Redis와 Postgres가 둘 다 필수다.
* Triggerer는 **“비동기 + Worker 자원 절약”**의 핵심.

---
