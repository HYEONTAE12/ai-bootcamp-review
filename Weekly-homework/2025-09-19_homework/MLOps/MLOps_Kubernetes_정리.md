

---

# 쿠버네티스(Kubernetes) 정리본 — 개념부터 실전까지

## 1) 쿠버네티스란?

* **정의**: 컨테이너화된 애플리케이션의 **배포·확장·운영 자동화** 오픈 소스 오케스트레이터
  → 구글의 Borg 경험을 바탕으로 시작, 현재 **CNCF** 관리
* **목표**: 운영 복잡도↓, 가용성·확장성↑, 일관된 배포 파이프라인
* **주요 이점**

  * 배포 자동화(롤아웃/롤백)
  * 서비스 디스커버리 & 로드밸런싱
  * 오토스케일링(HPA/VPA/클러스터 오토스케일러)
  * 자체 치유(헬스체크 기반)
  * 인프라 추상화(클라우드/온프레 공통 API)

---

## 2) 클러스터 아키텍처(High-level)

**Control Plane(마스터) + Worker Nodes**

### 🔹 Control Plane(마스터 컴포넌트)

| 컴포넌트                             | 역할                                                             |
| -------------------------------- | -------------------------------------------------------------- |
| **kube-apiserver**               | 모든 요청의 단일 진입점, 인증/인가, 상태 조회·변경 API                             |
| **etcd**                         | 클러스터의 **소스 오브 트루스**(분산 KV 저장소)                                 |
| **kube-scheduler**               | 새 파드를 어떤 노드에 배치할지 결정(리소스/어피니티/테인트·톨러레이션 고려)                    |
| **kube-controller-manager**      | 다양한 컨트롤러 실행(ReplicaSet/Deployment/Node/Job 등) → **원하는 상태**로 수렴 |
| **cloud-controller-manager(옵션)** | 클라우드 자원 연동(로드밸런서, 라우팅 등)                                       |

### 🔹 Worker Node(노드 컴포넌트)

| 컴포넌트                  | 역할                                                   |
| --------------------- | ---------------------------------------------------- |
| **kubelet**           | 파드 사양 수신·컨테이너 실행·헬스 관리                               |
| **kube-proxy**        | Service 가상 IP(ClusterIP) 트래픽을 파드로 포워딩(iptables/IPVS) |
| **Container Runtime** | 컨테이너 엔진(containerd, CRI-O 등)                         |

### 🔹 애드온

* **CoreDNS**, **Ingress Controller**, **메트릭/모니터링 스택**, **CNI 플러그인**(Calico/Flannel 등)

---

## 3) 작동 방식(Desired State → 컨트롤 루프)

1. **클러스터 구성**
2. **API 서버와 통신**: `kubectl`/CI/CD/오퍼레이터가 **오브젝트(YAML)** 제출
3. **상태 저장**: 스펙이 **etcd**에 저장
4. **스케줄링**: 스케줄러가 파드를 적합한 노드에 **바인딩**
5. **실행/관리**: kubelet이 컨테이너 실행, 컨트롤러가 **원하는 상태**로 수렴
6. **서비스 관리**: Service/Endpoints/kube-proxy로 디스커버리·로드밸런싱
7. **자동 롤아웃/롤백**
8. **스케일링 & 자체 치유**

---

## 4) 핵심 오브젝트(리소스)

### 4.1 Pod

* **가장 작은 배포 단위**: 1개 이상 컨테이너 묶음(네트워크/스토리지 공유)
* **특징**: 컨테이너 그룹핑, 공유 리소스, **일시적**(짧은 수명), **사이드카 패턴** 적합
* **Probe**: `liveness/readiness/startup` → 자체 치유/트래픽 제어

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-pod
spec:
  containers:
    - name: app
      image: nginx:1.25
      ports:
        - containerPort: 80
      readinessProbe:
        httpGet: { path: /, port: 80 }
        initialDelaySeconds: 5
```

### 4.2 ReplicaSet

* 파드 **복제본 수 보장**(예: 항상 3개)
* 보통 직접 쓰기보다 **Deployment가 내부적으로 사용**

### 4.3 Deployment

* 파드/ReplicaSet **선언적 관리**, **롤링 업데이트/롤백**, 스케일링, 버전 관리

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: demo-deploy, labels: { app: web } }
spec:
  replicas: 3
  selector: { matchLabels: { app: web } }
  strategy:
    type: RollingUpdate
    rollingUpdate: { maxUnavailable: 0, maxSurge: 1 }
  template:
    metadata: { labels: { app: web } }
    spec:
      containers:
        - name: app
          image: nginx:1.25
          ports: [{ containerPort: 80 }]
```

### 4.4 Service

* 파드 집합에 **안정적 가상 IP** 제공, **로드밸런싱 & 서비스 발견**
* **타입**

  * **ClusterIP**(기본, 내부)
  * **NodePort**(노드 포트 외부 노출)
  * **LoadBalancer**(클라우드 L4 LB 연동)
  * **Headless(`clusterIP: None`)**: 파드 개별 IP 노출
  * **ExternalName**: 외부 DNS 이름 매핑

```yaml
apiVersion: v1
kind: Service
metadata: { name: demo-svc }
spec:
  selector: { app: web }
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 80
```

### 4.5 Ingress(HTTP/HTTPS L7 라우팅)

* 도메인/경로 기반 라우팅, TLS 종료
* **Ingress Controller**(Nginx/Traefik 등) 필요

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: { name: demo-ing }
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend: { service: { name: demo-svc, port: { number: 80 } } }
```

### 4.6 Namespace

* 리소스 **논리적 격리**, **Quota/LimitRange** 적용 단위

### 4.7 ConfigMap & Secret

* **ConfigMap**: 설정(평문), **Secret**: 민감정보
* 파드에 **env/파일 마운트**로 주입(필요 시 at-rest 암호화)

### 4.8 스토리지(PV/PVC/StorageClass)

* **Volume**: 파드 생명주기와 분리된 데이터 저장
* **PV**(실제 스토리지) ↔ **PVC**(요청), **StorageClass**로 동적 프로비저닝

### 4.9 워크로드(배치/유·무상태)

* **Job**: 끝나는 작업(성공 횟수 보장)
* **CronJob**: 스케줄 반복 실행
* **DaemonSet**: 모든 노드에 1개씩 파드(로그/모니터링 에이전트)
* **StatefulSet**: 고정 ID·스토리지 필요한 **유상태**(DB/Kafka 등)

---

## 5) 네트워킹 모델 요약

* **Pod ↔ Pod**: 클러스터 내 **평평한 네트워크**(모든 파드 고유 IP) — **CNI 플러그인**이 구현
* **Service**: ClusterIP로 가상 IP 제공 → **kube-proxy**가 파드 뒤로 분산(iptables/IPVS)
* **DNS**: CoreDNS — `svc.namespace.svc.cluster.local` 네임 해석
* **NetworkPolicy**: 파드 간 통신 **허용/차단**(CNI 지원 필요)

---

## 6) 스케줄링 & 배치 전략

* **노드 선택**: `nodeSelector`, **노드/파드 어피니티·안티어피니티**
* **테인트/톨러레이션**: 특정 노드에 선별 배치/차단
* **토폴로지 스프레드**: AZ/노드 간 **균등 분산**
* **리소스 요청/제한**: `resources.requests/limits`(CPU/메모리)

---

## 7) 스케일링

* **HPA**: CPU 등 메트릭 기반 **파드 수 자동 조절**
* **VPA**: 파드 **리소스 요청/제한** 자동 조정(재시작 수반)
* **Cluster Autoscaler**: **노드** 자체 증감(클라우드 통합)

---

## 8) 롤아웃 전략 & 자체 치유

* **RollingUpdate**(기본): 새 파드 늘리고 옛 파드 줄이며 전환
* **Recreate**: 전부 내리고 새로 띄움
* **Blue/Green, Canary**: Ingress/Service 라우팅으로 **점진적 트래픽 전환**
* **자체 치유**: liveness/readiness/startup probe, **PDB**로 과도한 축출 방지

---

## 9) 보안 & 접근 제어

* **RBAC**: 역할 기반 권한 제어(Role/RoleBinding/ClusterRole/ClusterRoleBinding)
* **ServiceAccount**: 파드의 API 접근 계정
* **Secret 암호화**: at-rest 암호화, 이미지 풀 시크릿
* **Pod Security(PSA)**: privileged/baseline/restricted 정책
* **NetworkPolicy**: **제로 트러스트** 트래픽 최소 허용

---

## 10) 관측(Observability)

* **로그**: `kubectl logs`, 중앙 수집(Fluent Bit/Elastic/OpenSearch)
* **메트릭**: metrics-server(리소스), Prometheus(앱/클러스터), Grafana(대시보드)
* **이벤트**: `kubectl describe`(스케줄 실패/이미지 풀 실패 등 원인 파악)

---

## 11) YAML 작성 팁

* **라벨/어노테이션** 일관성(`app`, `component`, `version`)
* **리소스 요청/제한** 반드시 명시
* **Config 분리**(ConfigMap/Secret) → 이미지 재빌드 없이 설정 교체
* **환경별 오버레이**: Kustomize/Helm
* **Probe 설정** 습관화 → 배포 안정성↑

---

## 12) 자주 쓰는 `kubectl`

```bash
# 조회
kubectl get nodes|pods|svc -A
kubectl describe pod <name> -n <ns>
kubectl logs -f <pod> [-c <container>]

# 배포/수정
kubectl apply -f k8s/
kubectl rollout status deploy/<name>
kubectl rollout undo deploy/<name>

# 디버그
kubectl exec -it <pod> -- sh
kubectl port-forward svc/<svc> 8080:80
```

---

## 13) 흔한 오해/실수

* **ReplicaSet만 사용** → 롤아웃/롤백 어려움, **Deployment가 기본**
* **리소스 미지정** → 스케줄 불안정/노이즈 네이버 문제, `requests/limits` 필수
* **프로브 미설정** → 준비 안 된 파드에 트래픽 유입
* **시크릿 평문 관리** → Secret(+암호화) 사용
* **네트워크 폴리시 미적용** → 내부 트래픽 전부 오픈 위험

---

## 14) ML/MLOps 관점 팁

* **모델 서빙**: Deployment(+HPA)로 추론 API 운영, GPU 필요 시 NVIDIA Device Plugin + `nvidia.com/gpu`
* **배치 파이프라인**: Job/CronJob으로 정기 피처 생성/리포트, 실패 재시도
* **데이터/모델 버전**: PV/PVC + 객체 스토리지, ConfigMap/Secret로 엔드포인트·버전 주입
* **그레이드 릴리스**: Ingress + Canary(헤더/비율 기반)
* **관측**: 추론 지연/에러율을 Prometheus로 수집 → HPA 커스텀 메트릭

---

## 15) 한눈에 보기(치트시트)

| 오브젝트                 | 핵심 역할                     |
| -------------------- | ------------------------- |
| **Pod**              | 실행 단위(컨테이너 묶음)            |
| **ReplicaSet**       | 파드 개수 보장                  |
| **Deployment**       | 롤링 업데이트/롤백, 선언적 관리(실무 기본) |
| **Service**          | 고정 가상 IP + 로드밸런싱          |
| **Ingress**          | HTTP/HTTPS 라우팅, TLS       |
| **Namespace**        | 논리적 격리, Quota/LimitRange  |
| **ConfigMap/Secret** | 설정/민감정보 주입                |
| **PV/PVC/SC**        | 영속 스토리지/동적 프로비저닝          |
| **HPA/VPA/CA**       | 파드/리소스/노드 자동 확장           |

---

## 16) 최소 예시(Deployment + Service + Ingress)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: app, labels: { app: app } }
spec:
  replicas: 2
  selector: { matchLabels: { app: app } }
  template:
    metadata: { labels: { app: app } }
    spec:
      containers:
        - name: app
          image: ghcr.io/org/app:1.0.0
          ports: [{ containerPort: 8080 }]
          resources:
            requests: { cpu: "200m", memory: "256Mi" }
            limits:   { cpu: "500m", memory: "512Mi" }
          readinessProbe:
            httpGet: { path: /health, port: 8080 }
            initialDelaySeconds: 5

---
# service.yaml
apiVersion: v1
kind: Service
metadata: { name: app-svc }
spec:
  selector: { app: app }
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP

---
# ingress.yaml (Ingress Controller 필요)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ing
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service: { name: app-svc, port: { number: 80 } }
```

---

## 17) 다음 스텝

* 로컬(kind/미니쿠베)·클라우드 기준 **실행 가능한 예제 매니페스트 묶음**
* **HPA 연동 예시**(CPU → 커스텀 메트릭)
* **GPU 추론 파드 스펙**(NVIDIA Device Plugin 포함)
* **네임스페이스/Quota/LimitRange** 템플릿
* **NetworkPolicy** 기본(deny-all → 필요한 것만 허용)

---


