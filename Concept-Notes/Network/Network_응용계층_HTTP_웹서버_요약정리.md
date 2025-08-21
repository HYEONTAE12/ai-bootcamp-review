
# 🌐 웹 서버와 HTTP 정리

## 1. 웹 서버 (Web Server)

* **정의**: 클라이언트(브라우저)의 요청(Request)을 받아 웹 페이지나 데이터를 응답(Response)해주는 서버 프로그램.
* **역할**

  * 정적인 자원(HTML, CSS, JS, 이미지 등) 제공
  * 동적인 자원(웹 어플리케이션 실행 결과) 제공
  * 보안(SSL/TLS 적용, 접근 제어)
  * 과부하 방지(로드 밸런싱, 캐싱 활용)
  * 여러 웹 어플리케이션 서버(WAS)와 연동 용이

---

## 2. 웹 어플리케이션 (Web Application)

* **정의**: 사용자의 요청에 따라 서버 측에서 동적으로 처리되는 프로그램.
* **예시**: 로그인 시스템, 쇼핑몰 장바구니, 게시판, 검색 서비스
* **실행 환경**

  * WAS(Web Application Server)에서 동작
  * DBMS, 비즈니스 로직, API 등과 연계

---

## 3. 자원(Resource)

* **정적인 자원 (Static Resource)**

  * 서버에 미리 저장된 그대로 전달되는 데이터
  * HTML, CSS, JS, 이미지, 동영상 파일 등
* **동적인 자원 (Dynamic Resource)**

  * 서버에서 코드 실행 후 결과를 생성해 응답
  * PHP, JSP, ASP.NET, Python Django/Flask, Node.js 등

---

## 4. HTTP의 특징

* **요청-응답 기반 (Client-Server 구조)**

  1. 클라이언트(브라우저)가 요청(Request)을 보냄
  2. 서버(Web Server)가 응답(Response)을 반환

* **미디어 독립적**

  * 어떤 종류의 데이터(텍스트, 이미지, 영상 등)도 전송 가능
  * `Content-Type` 헤더를 통해 데이터 형식 구분

* **비연결성 (Connectionless)**

  * HTTP/1.0, 1.1, 2.0 모두 TCP 기반
  * TCP는 연결 지향적이지만, HTTP 자체는 요청-응답 단위로 연결을 종료
  * → 서버의 자원 효율성 확보 가능

* **스테이트리스 (Stateless)**

  * 서버는 클라이언트의 상태를 저장하지 않음
  * 상태 관리 필요 시 → 쿠키, 세션, 토큰(JWT) 활용

* **지속 연결 (Keep-Alive)**

  * HTTP/1.1부터 기본 활성화
  * 하나의 TCP 연결에서 여러 요청/응답 처리 가능
  * 네트워크 비용 절감, 성능 향상

---

## 5. HTTP 버전별 특징

1. **HTTP/0.9**

   * 초기 버전, 단순히 HTML 문서만 전송 가능
2. **HTTP/1.0**

   * 요청마다 연결 생성 후 종료 (비효율적)
   * 응답 상태 코드, 헤더 도입
3. **HTTP/1.1**

   * Keep-Alive 기본 적용
   * 파이프라이닝, 캐싱, 호스트 헤더 지원
4. **HTTP/2.0**

   * 멀티플렉싱 지원 (한 연결에서 여러 요청 동시 처리)
   * 헤더 압축, 서버 푸시(Server Push) 기능 추가
5. **HTTP/3.0**

   * TCP 대신 **QUIC(UDP 기반)** 사용
   * 연결 성립 속도 개선, 지연(Latency) 감소

---

## 6. HTTP 메시지 개관

### 📌 요청(Request) 메시지 구조

* **Start line**

  ```
  [HTTP 메서드] [요청 대상(URI)] [HTTP 버전]
  ```

  예시:

  ```
  GET /index.html HTTP/1.1
  ```

* **대표적인 HTTP 메서드**

  1. `GET` → 데이터 조회 (멱등성 有, 캐시 가능)
  2. `POST` → 데이터 생성/처리 (멱등성 無, 캐시 불가)
  3. `PUT` → 전체 수정/덮어쓰기 (멱등성 有, 캐시 가능)
  4. `PATCH` → 부분 수정 (멱등성 無, 캐시 불가)
  5. `DELETE` → 자원 삭제 (멱등성 有, 캐시 불가)

* **멱등성 (Idempotence)**
  같은 요청을 여러 번 보내도 결과가 동일한가?

* **캐시 가능성 (Cacheability)**
  응답을 캐싱하여 재사용할 수 있는가?

---

### 📌 응답(Response) 메시지 구조

* **Start line**

  ```
  [HTTP 버전] [상태 코드] [이유 문구]
  ```

  예시:

  ```
  HTTP/1.1 200 OK
  ```

* **상태 코드**

  1. **2XX: 성공**

     * 200 OK: 요청 성공
     * 201 Created: 리소스 생성 성공
  2. **3XX: 리다이렉션**

     * 301 Moved Permanently: 영구 이동
     * 302 Found: 임시 이동
     * 304 Not Modified: 캐시 사용
  3. **4XX: 클라이언트 오류**

     * 400 Bad Request: 잘못된 요청
     * 401 Unauthorized: 인증 필요
     * 403 Forbidden: 접근 금지
     * 404 Not Found: 리소스 없음
  4. **5XX: 서버 오류**

     * 500 Internal Server Error: 서버 내부 오류
     * 502 Bad Gateway: 게이트웨이 오류
     * 503 Service Unavailable: 서버 과부하/점검 중

---

## 7. HTTP 헤더

* **형식**

  ```
  header-field = field-name ":" field-value
  ```

* **대표적인 헤더**

  * `Host` : 요청 대상 서버의 도메인
  * `Date` : 메시지 생성 시간
  * `Referer` : 현재 요청을 보낸 페이지의 URL
  * `User-Agent` : 요청 보낸 클라이언트 정보
    예: Mozilla / Windows NT 10.0 / Chrome / Safari
  * `Server` : 응답을 보낸 서버의 정보
  * `Content-Type` : 데이터 형식 (예: text/html, application/json)
  * `Content-Encoding` : 압축 방식 (gzip, deflate 등)
  * `Content-Length` : 본문 크기(바이트 단위)
  * `Content-Language` : 컨텐츠 언어(예: ko, en, jp)

---

📌 정리하면, HTTP는 **비연결성 + 스테이트리스 + 요청-응답 구조**라는 특징을 가지며, 버전별로 성능 향상과 보안 강화가 이루어져 왔습니다.

---
