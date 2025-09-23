
---

# 🛠️ MLOps 파이프라인 단계별 도구 정리

## 1. 프로젝트 관리 도구

* **Linear**

  * 스타트업에서 많이 사용하는 프로젝트 관리 툴
  * 간결하고 직관적 UI, GitHub/GitLab과 연계 쉬움
* **Jira**

  * Atlassian의 대표 프로젝트 관리 툴
  * 애자일 스프린트 관리, 티켓 기반 협업에 강점
* **Notion**

  * 올인원 워크스페이스 (문서, 데이터베이스, 칸반보드)
  * 소규모 팀의 협업 문서/기획 관리에 적합

---

## 2. 데이터 파이프라인 도구

* **Airflow**

  * Python 기반 배치 워크플로우 관리 도구
  * DAG(Directed Acyclic Graph)로 태스크 간 의존성 관리
  * 머신러닝 전용 기능은 부족하지만 범용성이 뛰어남
* **Kafka**

  * 대용량 실시간 스트리밍/메시지 큐 도구
  * 이벤트 기반 데이터 파이프라인 구축에 적합
* **Spark**

  * 대규모 분산 데이터 처리 엔진
  * 메모리 기반 연산으로 Hadoop MapReduce보다 빠름
* **Hadoop**

  * 대규모 데이터 분산 저장/처리 프레임워크 (HDFS + MapReduce)
* **Hive**

  * Hadoop 기반 SQL-like 데이터 웨어하우스
  * 빅데이터 처리 시 SQL 인터페이스 제공
* **S3**

  * AWS 오브젝트 스토리지, 데이터/모델 저장용
* **MinIO**

  * 오픈소스 오브젝트 스토리지 (S3 호환 API 지원)
  * 자체 인프라에서 S3 대체 가능, 고가용성/내구성 확보

---

## 3. Feature Store

* **S3 / MinIO**

  * 피처를 단순 저장소에 파일 형태로 보관할 때 사용 가능
* **Feast**

  * 오픈소스 Feature Store
  * 온라인/오프라인 피처 저장 및 서빙 지원
* **Hopsworks**

  * 엔터프라이즈급 Feature Store 플랫폼
  * 실험 관리, 데이터 버전 관리까지 통합
* **Tecton**

  * 상용 Feature Store, 실시간 피처 엔지니어링 강점
* **SageMaker Feature Store**

  * AWS 관리형 Feature Store
* **Vertex AI Feature Store**

  * Google Cloud 관리형 Feature Store

---

## 4. 소스 코드 저장소 (형상 관리)

* **Git**

  * 분산 버전 관리 시스템
* **GitHub**

  * 클라우드 Git 저장소 서비스, Actions 등 CI/CD 연계 강점
* **GitLab**

  * 자체 호스팅 가능, GitLab CI/CD 내장
* **Bitbucket**

  * Atlassian 제품군(Jira 등)과 연계 강점

---

## 5. CI/CD 도구

* **Jenkins**

  * 오픈소스 CI/CD 서버
  * 유연하지만 설정 복잡, 유지 비용 높음
* **GitHub Actions**

  * GitHub 저장소와 바로 연계되는 CI/CD
  * YAML 기반 파이프라인 정의
* **GitLab CI/CD**

  * GitLab에 내장된 CI/CD, GitHub Actions과 유사
* **CircleCI**

  * SaaS형 CI/CD 서비스, 빠른 빌드와 확장성 강점
* **ArgoCD**

  * Kubernetes 환경에서 GitOps 방식 CD 지원

---

## 6. Automated Pipeline

* **Airflow**

  * 범용 워크플로우 관리, ML 전용 기능 부족
* **Kubeflow**

  * Kubernetes 기반 ML 워크플로우 플랫폼
  * 데이터 → 학습 → 배포 파이프라인 전체 지원
* **MLflow**

  * 머신러닝 중심, 실험 추적·모델 관리에 강점
* **Prefect**

  * Airflow 대안으로 나온 워크플로우 도구, Python 친화적
* **Argo Workflows**

  * Kubernetes 네이티브 워크플로우 엔진, 대규모 ML 워크로드 지원

---

## 7. Model Registry

* **DVC (Data Version Control)**

  * 데이터와 모델 버전 관리를 Git처럼 가능하게 하는 도구
* **Kubeflow**

  * 모델 관리/서빙 통합
* **MLflow**

  * 모델 버전 관리, 실험 관리, 배포까지 지원
* **Weights & Biases (W\&B)**

  * 실험 추적 + 모델 관리 + 대시보드
* **SageMaker Model Registry**

  * AWS 관리형 모델 레지스트리
* **Vertex AI Model Registry**

  * Google Cloud 관리형 모델 레지스트리

---

## 8. 모델 서빙 (CD: Model Serving)

### 프레임워크 레벨

* **PyTorch Serve** : PyTorch 모델 서빙
* **TensorFlow Serving** : TensorFlow 모델 서빙
* **TensorRT** : NVIDIA GPU 최적화된 서빙 엔진
* **ONNX Runtime** : 다양한 프레임워크 모델을 ONNX 포맷으로 변환해 실행

### 서빙 전용 도구

* **Seldon Core** : Kubernetes 기반 모델 서빙 플랫폼
* **KServe (KFServing)** : Kubeflow에서 파생된 서빙 도구
* **BentoML** : Python 친화적 모델 서빙 프레임워크
* **NVIDIA Triton Inference Server** : 멀티프레임워크 지원, GPU 서빙에 최적

---

## 9. 모니터링 & 로깅

* **Prometheus** : 메트릭 수집, 시계열 데이터베이스
* **Grafana** : 메트릭 대시보드 시각화
* **EFK/ELK Stack**

  * Elasticsearch + (Fluentd/Fluent Bit or Logstash) + Kibana
  * 로그 수집/분석/시각화

### ML 전용 모니터링

* **TensorBoard** : 로컬에서 학습 로그/지표 시각화
* **MLflow** : 실험 로그/지표 추적
* **W\&B** : 클라우드 기반 실험 추적/대시보드
* **Kubeflow** : 쿠버네티스 환경에서 지표/실험 관리
* **SageMaker Experiments** : AWS에서 실험 추적 지원

---

## 10. 메시지 브로커 / 트리거

* **RabbitMQ** : 전통적인 메시지 브로커, 안정적인 큐 기반
* **RSMQ (Redis Simple Message Queue)** : Redis 기반 메시지 큐
* **Kafka** : 스트리밍/실시간 데이터 파이프라인, 이벤트 기반 처리
* **ActiveMQ** : 자바 기반 메시지 브로커
* **Amazon SQS** : AWS 관리형 메시지 큐
* **Google Pub/Sub** : Google Cloud 메시징 서비스
* **Azure Service Bus** : Azure 관리형 메시징 서비스

---

## 🧩 요약

* **프로젝트 관리 → 데이터 파이프라인 → Feature Store → 소스 저장소 → CI/CD → Automated Pipeline → Model Registry → Serving → 모니터링 → 메시지 브로커**
* 각 단계마다 오픈소스/클라우드/상용 도구들이 있고, **팀의 데이터 크기, 예산, 클라우드 환경**에 따라 선택해야 함.

---

