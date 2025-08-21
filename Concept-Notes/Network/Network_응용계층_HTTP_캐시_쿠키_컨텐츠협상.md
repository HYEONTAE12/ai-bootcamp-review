# 🖥️ HTTP · 네트워크 핵심 정리

---

## 1. `curl` 명령어 옵션

`curl`은 **HTTP 요청/응답을 테스트하기 위한 명령줄 도구**입니다. 주로 API 테스트, 디버깅, 데이터 다운로드에 사용합니다.

### 주요 옵션

* **`-x`** : 프록시 서버를 통해 요청 전송

  ```bash
  curl -x http://proxy.example.com:8080 http://naver.com
  ```
* **`-I`** : **헤더 정보만 요청** (응답 본문은 출력하지 않음)

  ```bash
  curl -I http://naver.com
  ```
* **`-i`** : 응답 헤더 + 응답 본문 모두 출력
* **`-v`** : 요청/응답 과정을 **상세 로그(Verbose)** 로 출력
* **`-o [파일명]`** : 응답 결과를 파일로 저장

  ```bash
  curl -o index.html http://naver.com
  ```
* **`-d`** : 요청 본문 데이터 전송 (주로 POST 요청)

  ```bash
  curl -d "id=test&pw=1234" http://example.com/login
  ```
* **`-H`** : 요청에 **헤더 추가**

  ```bash
  curl -H "Content-Type: application/json" -d '{"name":"현태"}' http://example.com
  ```

---

## 2. 캐시(Cache)

### 네트워크에서의 캐시

* **정의**: 서버의 지연을 줄이기 위해 **웹 페이지, 이미지, 동영상 등의 사본을 임시 저장하는 기술**
* **저장 위치**

  * **클라이언트(브라우저 캐시)** : 자주 방문하는 페이지를 로컬 디스크에 저장
  * **캐시 서버/프록시 서버** : 다수 사용자가 공통으로 접근할 수 있는 캐시 저장소

---

### Cache-Control 헤더

HTTP 응답에 포함되어 캐시 동작을 제어합니다.

* **`Cache-Control: max-age=숫자`**

  * 캐시 유효 시간을 초 단위로 지정
  * 예: `max-age=3600` → 1시간 동안 캐시 사용

* **`Cache-Control: no-cache`**

  * 캐시 저장은 가능하지만, 재사용 전에 **반드시 서버에 검증 요청** 필요

* **`Cache-Control: no-store`**

  * **캐시에 저장하지 않음** (민감한 데이터 전송 시 사용: 금융정보, 로그인 응답 등)

---

### 캐시된 자원 검증

* **If-Modified-Since**

  * 클라이언트가 마지막으로 받은 응답의 수정 시간을 서버에 알려줌
  * 서버는 변경 없으면 `304 Not Modified` 반환 → 캐시 사용 가능

* **ETag (Entity Tag)**

  * 자원의 버전을 식별하는 고유 값
  * 요청 시 `If-None-Match` 헤더에 전달 → 같으면 `304 Not Modified` 반환

---

## 3. 쿠키(Cookie)

* **정의**: 서버가 클라이언트에 내려보내고, 브라우저에 저장하는 **이름=값 형태의 데이터**
* **특징**

  * 유효기간(`Expires`, `Max-Age`) 존재
  * 특정 도메인/경로에서만 전송 (`Domain`, `Path`)

---

### 쿠키와 세션(Session)

* **쿠키**

  * 클라이언트(브라우저)에 저장
  * 사용자가 직접 수정 가능 → 보안에 취약
  * 저장 용량/개수 제한 존재 (약 4KB, 도메인당 20개 내외)
  * 사용 예: 자동 로그인, 사이트 설정 기억

* **세션**

  * 서버에 저장 (클라이언트는 세션 ID만 쿠키로 보관)
  * 상대적으로 보안이 강함
  * 서버 자원 소모 (세션 저장 공간 필요)
  * 사용 예: 로그인 상태 유지, 장바구니

👉 **정리**: 쿠키는 **클라이언트 저장용**, 세션은 **서버 저장용**.

---

### 쿠키의 보안 속성

* **Secure** : HTTPS 연결에서만 전송
* **HttpOnly** : JavaScript에서 접근 불가 → XSS 공격 방지

---

## 4. 콘텐츠 협상 (Content Negotiation)

### 정의

클라이언트가 원하는 콘텐츠 형식(언어, 데이터 포맷, 인코딩 등)을 서버에 알려주면,
서버가 가장 적합한 콘텐츠로 응답하는 기능.

### 주요 헤더

* **`Accept`** : 클라이언트가 받을 수 있는 콘텐츠 타입 지정

  * 예: `Accept: text/html, application/json`
* **`Accept-Language`** : 선호 언어 지정

  * 예: `Accept-Language: ko, en;q=0.8`
* **`Accept-Encoding`** : 인코딩 방식 지정 (gzip, deflate 등)

### 예시

```http
GET /hello HTTP/1.1
Host: example.com
Accept: application/json
Accept-Language: ko
```

➡️ 서버는 JSON 형식의 한국어 응답을 반환할 수 있음

---

# 📌 최종 요약

* **`curl`**: HTTP 요청 테스트용 도구 (옵션별로 목적 다름)
* **캐시**: 자원 사본 저장해 성능 향상 (`Cache-Control`, `ETag`, `If-Modified-Since`)
* **쿠키**: 클라이언트에 저장되는 작은 데이터 (보안 옵션: Secure, HttpOnly)
* **세션**: 서버에서 상태 저장, 쿠키에는 세션 ID만 저장
* **콘텐츠 협상**: 클라이언트가 원하는 포맷/언어를 서버가 맞춰주는 기능 (`Accept` 계열 헤더 활용)

---

