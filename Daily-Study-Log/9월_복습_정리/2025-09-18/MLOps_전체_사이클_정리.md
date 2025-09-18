
---

# 🛠️ MLOps 전체 사이클 정리

MLOps(Machine Learning Operations)는 **데이터 수집 → 모델 개발 → 배포 → 운영/모니터링 → 롤백**까지 전체 라이프사이클을 자동화하고 관리하는 과정이야.

---

## 1. 데이터 단계 (Data)

* **데이터 수집 & 저장**

  * 원천 데이터 확보 (DB, 로그, API, S3 등)
  * 버킷(S3) 같은 클라우드 스토리지 활용
  * 불필요 시 리소스 삭제: 버킷, 인스턴스, 키 페어, 보안 그룹, IAM 사용자/그룹 정리

* **데이터 전처리**

  * 결측치 처리, 이상치 제거
  * 피처 엔지니어링
  * 데이터 버전 관리(DVC, Git-LFS 등)

* **데이터 검증**

  * 데이터 스키마 검증
  * 훈련/검증/테스트 세트 분리

---

## 2. 모델 단계 (Model)

* **모델 학습**

  * 오프라인 추론: 배치 데이터 기반 학습
  * 온라인 추론: 실시간 서비스용 학습/로드

* **모델 관리**

  * 전역 스코프에 모델 1회 로드 (자원 절약)
  * 신규 모델 교체 시 기존 모델 메모리 릴리즈
  * 문제 발생 시 모델 **롤백** (데이터/모델 버전 함께 관리)

* **모델 저장 & 버전 관리**

  * MLflow, Weights & Biases, S3 등 사용
  * 모델 버전별 메타데이터 관리

---

## 3. 애플리케이션 단계 (Application)

* **FastAPI 기반 API 서버**

  * `uvicorn`으로 실행
  * `pydantic`으로 요청/응답 데이터 검증
  * `CORSMiddleware`로 다중 출처 제어 (보안 강화)
  * `async def`로 비동기 처리

* **API 서버 실행 스크립트**

  * 실행 권한 부여:

    ```bash
    chmod +x start_api_server.sh
    ./start_api_server.sh
    ```

* **로그 관리**

  * 실시간 로그 확인:

    ```bash
    tail -f nohup.out
    ```

---

## 4. 환경 단계 (Environment)

* **Python 의존성 관리**

  * 패키지 확인:

    ```bash
    pip list
    pip freeze
    ```
  * 의존성 설치:

    ```bash
    pip install -r requirements.txt
    ```

* **가변/불변 객체 주의**

  * 리스트 같은 뮤터블 객체를 함수 파라미터 기본값으로 직접 사용 금지
  * `None`을 기본값으로 두고 `is None / is not None`으로 확인

---

## 5. 컨테이너 단계 (Containerization)

* **Dockerfile 기반 빌드**

  * 현재 경로 기준 빌드:

    ```bash
    docker build -t my-mlops:v1 .
    ```

* **환경 변수 주입**

  * `-e` 옵션 활용

* **이미지 관리**

  * 태깅:

    ```bash
    docker tag my-mlops:v1 hyoentae/my-mlops:v1
    ```
  * 푸시:

    ```bash
    docker push hyoentae/my-mlops:v1
    ```

* **네트워크 관리**

  * 기본 브리지 네트워크에서는 컨테이너 이름 자동 등록 X
  * 커스텀 네트워크 생성 시 컨테이너 이름으로 상호 인식 가능

---

## 6. 배포 단계 (Deployment)

* **배포 파이프라인**

  * Git 저장소 활용 (GitHub 등)
  * `.env` 같은 민감 정보는 제외
  * `develop → release → main` 브랜치 전략
  * CI/CD (Jenkins, GitHub Actions, GitLab CI 등) 연계

* **배포 전략 (무중단 배포)**

  * **Rolling Update**

    * Pod/서버를 점진적으로 교체
    * 롤백 빠르고 무중단 운영 가능
  * **Blue-Green**

    * 블루(운영 중)와 그린(신규) 환경을 동시에 유지
    * 전환 순간에 트래픽을 한 번에 변경
  * **Canary**

    * 일부(예: 10%) 트래픽만 신규 버전으로 보내고 점진적으로 확장
    * 장애 위험 최소화
  * **Linear**

    * 일정 시간마다 점진적 트래픽 조정 (카나리의 변형)

---

## 7. 모니터링 & 성능 테스트 (Monitoring)

* **부하 테스트 도구**

  * nGrinder (고급 성능 테스트)
  * wrk (간단한 부하 테스트)

    ```bash
    wrk -t 1 -c 1 -d 15s --latency -H 'accept: application/json' http://<url>
    ```

* **메트릭 수집**

  * Prometheus, Grafana
  * 응답 속도, 에러율, 리소스 사용량 모니터링

---

## 8. 운영 & 롤백 (Operation)

* **문제 상황**

  * 신규 모델 배포 후 에러 발생 시 즉시 롤백
  * 데이터/모델/애플리케이션 버전별 롤백 전략 필요

* **롤백 방식**

  * 온라인 추론: 기존 모델 다시 로드
  * 오프라인 추론: 이전 데이터 버전/모델 버전 복원
  * 배포 전략 활용 (Rolling, Blue-Green, Canary에서 롤백은 빠르게 가능)

---

# ✅ 전체 사이클 흐름 요약

```
데이터 수집 → 데이터 전처리/검증 → 모델 학습 & 버전 관리 → API 서버(FastAPI) 구성 
→ Docker 컨테이너화 → CI/CD 배포 파이프라인 → 무중단 배포(롤링/블루그린/카나리) 
→ 모니터링 & 부하 테스트 → 문제 발생 시 롤백
```

---
