
---

# 🐳 Docker 핵심 키워드 정리

## 🔍 컨테이너 / 이미지 확인

* `docker ps` → 실행 중인 컨테이너 확인
* `docker ps -a` → 중지된 것 포함 전체 컨테이너 확인
* `docker images` → 도커 이미지 목록 확인

---

## 🚀 컨테이너 생성 & 실행

* `docker run` → 새 컨테이너 생성 후 실행

  * `-itd` → 상호작용 모드(-it) + 백그라운드 실행(-d)
  * `--name my-mlops` → 컨테이너 이름 지정
  * `python:3.11-bookworm` → 사용할 이미지

예시:

```bash
docker run -itd --name my-mlops python:3.11-bookworm
```

* `docker exec -it [컨테이너명] bash` → 실행 중 컨테이너 접속
* `exit` → 컨테이너 내부에서 빠져나오기

---

## ❌ 컨테이너 중지 & 삭제

* `docker stop [컨테이너ID/이름]` → 컨테이너 중지
* `docker rm -f [컨테이너ID/이름]` → 실행 중이어도 강제 삭제

---

## 📦 Docker 라이프사이클 흐름

1. 이미지 다운로드 → `docker pull`
2. 컨테이너 생성 → `docker run`
3. 컨테이너 실행/접속 → `docker exec`
4. 컨테이너 중지 → `docker stop`
5. 컨테이너 삭제 → `docker rm`

👉 **이미지(Image)** = 설계도
👉 **컨테이너(Container)** = 실행된 프로그램 (집 짓기 vs 실제 집으로 비유 가능)

---


