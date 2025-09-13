# 응용 계층 (Application Layer)

응용 계층은 네트워크 서비스의 **최종 사용자와 직접 맞닿는 계층**이다.
웹 브라우저(HTTP), 이메일(SMTP, IMAP), 파일 전송(FTP), 도메인 이름 해석(DNS) 등이 동작한다.

---

## DNS (Domain Name System)

* **정의**: 사람이 기억하기 쉬운 \*\*도메인 이름([www.naver.com)\*\*을](http://www.naver.com%29**을) 실제 통신에 필요한 \*\*IP 주소(223.130.200.104)\*\*로 변환해주는 시스템.
* **특징**:

  * 계층적 구조로 설계됨.
  * 전 세계적으로 분산된 서버들이 협력하여 동작.

---

### 계층적 도메인 구조

도메인은 **계층적(hierarchical)** 구조로 관리된다.

* 예: `www.naver.com`

  * `.` (루트)
  * `com` (TLD, 최상위 도메인)
  * `naver` (2차 도메인)
  * `www` (호스트명)

---

### 각 도메인을 담당하는 도메인 서버

1. **ROOT 네임 서버**

   * 도메인 네임 해석의 출발점.
   * “.com”, “.org” 등 **TLD 서버의 위치 정보**를 제공.

2. **TLD 서버 (Top-Level Domain Server)**

   * 최상위 도메인(`.com`, `.net`, `.kr`)을 관리.
   * 해당 도메인의 **권한 있는 DNS 서버(Authoritative Server)** 정보를 알려줌.

3. **Authoritative DNS 서버**

   * 실제 도메인(`naver.com`)에 대한 최종 정보(IP 주소 등)를 가지고 있는 서버.
   * 관리자가 등록한 레코드 보관.

4. **Local DNS 서버 (리졸버, Resolver)**

   * 사용자의 PC나 ISP가 운영하는 서버.
   * 클라이언트 요청을 대신 받아 루트부터 차례대로 질의하여 결과를 가져옴.

---

### 질의 방식

* **반복적 질의 (Iterative Query)**

  * 로컬 DNS 서버가 루트, TLD, 권한 서버를 차례대로 직접 물어보는 방식.
  * "내가 직접 갈 테니 주소만 알려줘."

* **재귀적 질의 (Recursive Query)**

  * 클라이언트가 로컬 DNS 서버에 요청하면, 로컬 DNS 서버가 대신 끝까지 찾아서 결과를 돌려줌.
  * "네가 대신 찾아와서 알려줘."

---

### DNS 레코드 종류

* **A 레코드**: 도메인 → IPv4 주소 매핑
* **AAAA 레코드**: 도메인 → IPv6 주소 매핑
* **CNAME 레코드**: 별칭(Alias) → 실제 도메인 이름 매핑
* **NS 레코드**: 해당 도메인을 관리하는 네임 서버 지정
* **SOA 레코드 (Start of Authority)**: 도메인 존(zone)의 시작 정보 (관리자, 갱신 주기 등)

---

### DNS 캐시

* DNS 조회 결과를 일정 시간 동안 보관하는 기능.
* 반복적인 질의 속도 향상, 트래픽 감소.
* 단, 잘못된 정보가 캐싱되면 문제 발생 가능(캐시 포이즈닝 공격).

---

## URI / URL / URN

* **URI (Uniform Resource Identifier)**

  * 인터넷에서 **자원을 식별**하는 통합 개념.
  * URL과 URN을 포함하는 상위 개념.

* **URL (Uniform Resource Locator)**

  * 자원의 \*\*위치(Location)\*\*를 나타냄.
  * 예: `https://www.example.com/index.html`

* **URN (Uniform Resource Name)**

  * 자원의 \*\*이름(Name)\*\*을 전역적으로 고유하게 지정.
  * 예: `urn:isbn:0451450523` (책 ISBN)

---

## URL 구성 요소

예시:

```
https://user:pass@www.example.com:8080/path/page?query=abc#section
```

* **scheme**: 통신 프로토콜 (예: `http`, `https`, `ftp`)
* **authority**:

  * 사용자 정보 (`user:pass`) \[옵션]
  * 호스트명 (`www.example.com`)
  * 포트 번호 (`:8080`)
* **path**: 자원 위치 (`/path/page`)
* **query**: 추가적인 파라미터 (`?query=abc`)
* **fragment**: 문서 내 특정 위치 (`#section`)

---

✅ **정리**

* 응용 계층은 사용자가 직접 쓰는 서비스 계층.
* DNS는 계층적 구조와 여러 서버(루트, TLD, Authoritative, Local)를 통해 도메인을 IP로 변환.
* DNS는 반복 질의, 재귀 질의 방식을 사용하며, 다양한 레코드(A, AAAA, CNAME, NS, SOA)를 가짐.
* URI는 자원 식별자, URL은 위치 기반, URN은 이름 기반.
* URL은 scheme, authority, path, query, fragment로 구성됨.

---
