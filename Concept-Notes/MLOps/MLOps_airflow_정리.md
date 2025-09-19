
---

# 📌 Airflow DAG 정리

## DAG(Directed Acyclic Graph)란?

* **방향성을 가진 비순환 그래프**
* Airflow에서 **워크플로우(작업의 흐름)** 를 정의하는 주요 구성 요소
* DAG는 여러 \*\*작업(Task)\*\*과 이들 간의 **의존성**을 표현

---

### DAG 구성 요소

* **작업(Task)**
  DAG 안에서 실행되는 하나의 작업 단위 (예: Python 함수 실행, Bash 명령 실행 등)

* **의존성(Dependency)**
  어떤 작업이 끝나야 다른 작업이 실행될 수 있는지 정의 (→ 순서를 표현)

* **Operator**
  실제 작업을 정의하는 객체 (예: `PythonOperator`, `BashOperator`)

* **Task Instance**
  특정 시점에 실행되는 Task의 실제 인스턴스

* **Workflow**
  여러 Task와 그 의존성을 모아 놓은 전체 실행 흐름

---

### DAG 주의 사항

* **의존성 순환 금지**
  DAG는 비순환 구조이므로, 순환 참조가 있으면 안 됨.

* **스케줄링**
  DAG 실행 주기는 `schedule_interval`로 명확히 설정해야 함.

* **오류 처리**
  Task 실패 시 재시도, 알림 메일, 대체 Task 실행 등을 설정해 안정적으로 운영해야 함.

---

## DAG 주요 파라미터

```python
from airflow import DAG
from datetime import datetime

with DAG(
    dag_id="example_dag",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args={
        "retries": 1,
    },
    description="설명 예시",
    tags=["example", "tutorial"],
) as dag:
    ...
```

### 1. **dag\_id**

* DAG의 고유 이름
* Airflow UI에서 이 이름으로 DAG을 식별

### 2. **start\_date**

* DAG 실행 기준 시작일
* 첫 실행은 `start_date` + `schedule_interval` 이후에 발생

### 3. **schedule\_interval**

* DAG 실행 주기
* 예시:

  * `"@daily"` : 매일 0시
  * `"@hourly"` : 매시간
  * `"0 9 * * *"` : 매일 9시 (cron 표현식)

### 4. **catchup**

* 과거 스케줄 실행 여부
* `True` (기본): start\_date부터 현재까지 모든 실행을 “밀린 것”까지 전부 실행
* `False`: 현재 시점 이후만 실행

### 5. **default\_args**

* DAG 내 Task들의 공통 인자
* 예:

  ```python
  default_args = {
      "retries": 1,
      "retry_delay": timedelta(minutes=5),
      "email": ["alert@example.com"],
  }
  ```

### 6. **description**

* DAG에 대한 설명 (UI에 표시됨)

### 7. **tags**

* DAG을 그룹핑하거나 검색할 수 있도록 붙이는 태그

### 8. **max\_active\_runs**

* 동시에 실행 가능한 DAG 인스턴스 개수 제한
* 예: `max_active_runs=1` → 이전 실행이 끝나야 다음 실행 시작

### 9. **default\_view**

* DAG UI에서 기본 뷰 설정
* `"tree"` (기본), `"graph"`, `"calendar"`

---

# 📌 Docker로 Jenkins 구현

### docker-compose.yml 예시

```yaml
version: '3.8'
services:
  jenkins:
    image: jenkins/jenkins:lts   # LTS(안정 버전) Jenkins 이미지 사용
    ports:
      - "8080:8080"              # Jenkins 웹 UI
      - "50000:50000"            # 에이전트 연결 포트
    volumes:
      - jenkins_home:/var/jenkins_home   # Jenkins 데이터(설정, 플러그인, job 등) 영속화
    environment:
      - JENKINS_OPTS=--httpPort=8080     # Jenkins가 사용할 HTTP 포트 설정
    restart: unless-stopped              # 컨테이너가 꺼져도 자동 재시작

volumes:
  jenkins_home: 
```

---

### 구성 요소 설명

* **services.jenkins.image** : Jenkins 공식 LTS 이미지를 사용
* **ports**

  * `8080`: Jenkins 웹 UI 접속 포트
  * `50000`: Jenkins 에이전트(slave) 노드와 연결할 때 사용하는 포트
* **volumes**

  * `jenkins_home`을 `/var/jenkins_home`에 마운트해서 컨테이너 재시작해도 데이터 보존
* **environment**

  * `JENKINS_OPTS`: Jenkins 실행 옵션 (여기서는 포트 지정)
* **restart**

  * `unless-stopped`: 수동으로 멈추지 않는 이상 자동 재시작

---

✅ **정리**

* **Airflow DAG** : 워크플로우(Task와 의존성)를 정의하고, 주기적으로 실행 관리하는 단위
* **Docker Jenkins** : Jenkins를 도커 컨테이너로 실행해서 CI/CD 서버 구축

---
