# SQL 기초 정리

## 1. SQL이란?
- **SQL (Structured Query Language)**  
  관계형 데이터베이스(RDB)에서 데이터를 **정의, 조작, 제어**하기 위해 사용하는 표준 언어
- 데이터베이스의 모든 작업(조회, 삽입, 수정, 삭제, 구조 변경, 권한 관리 등)에 사용됨

---

## 2. SQL의 구성요소 4가지
1. **DDL (Data Definition Language)**  
   데이터베이스나 테이블 구조를 정의/변경/삭제하는 명령어  
   - 주요 명령어: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`

2. **DML (Data Manipulation Language)**  
   데이터베이스에 저장된 데이터를 조회/삽입/수정/삭제하는 명령어  
   - 주요 명령어: `SELECT`, `INSERT`, `UPDATE`, `DELETE`

3. **DCL (Data Control Language)**  
   데이터베이스의 사용자 권한을 부여/회수하는 명령어  
   - 주요 명령어: `GRANT`, `REVOKE`

4. **TCL (Transaction Control Language)**  
   트랜잭션의 실행과 취소를 제어하는 명령어  
   - 주요 명령어: `COMMIT`, `ROLLBACK`, `SAVEPOINT`

---

## 3. 데이터 정의어 (DDL)
| 명령어 | 설명 |
|--------|------|
| `CREATE` | 데이터베이스, 테이블 생성 |
| `ALTER` | 테이블 구조 변경 (컬럼 추가/변경/삭제) |
| `DROP` | 데이터베이스, 테이블 삭제 |
| `TRUNCATE` | 테이블의 모든 데이터 삭제 (구조 유지) |

---

## 4. 데이터 조작어 (DML)
| 명령어 | 설명 |
|--------|------|
| `SELECT` | 데이터 조회 |
| `INSERT` | 데이터 삽입 |
| `UPDATE` | 데이터 수정 |
| `DELETE` | 데이터 삭제 |

---

## 5. 데이터 제어어 (DCL)
| 명령어 | 설명 |
|--------|------|
| `GRANT` | 권한 부여 |
| `REVOKE` | 권한 회수 |

---

## 6. 트랜잭션 제어어 (TCL)
| 명령어 | 설명 |
|--------|------|
| `COMMIT` | 트랜잭션 확정 |
| `ROLLBACK` | 트랜잭션 취소 |
| `SAVEPOINT` | 트랜잭션 내 저장 지점 설정 |

---

## 7. 문자형 데이터 타입
| 타입 | 설명 |
|------|------|
| `CHAR(n)` | 고정 길이 문자열 (n자 고정, 부족하면 공백 채움) |
| `VARCHAR(n)` | 가변 길이 문자열 (최대 n자) |
| `TINYTEXT` | 최대 255자 |
| `TEXT` | 최대 65,535자 |
| `MEDIUMTEXT` | 최대 16,777,215자 |
| `LONGTEXT` | 최대 4,294,967,295자 |
| `JSON` | JSON 형식 데이터 저장 |

---

## 8. 숫자형 데이터 타입
| 타입 | 설명 |
|------|------|
| `TINYINT` | 1바이트 정수 (-128 ~ 127) |
| `SMALLINT` | 2바이트 정수 (-32,768 ~ 32,767) |
| `MEDIUMINT` | 3바이트 정수 (-8,388,608 ~ 8,388,607) |
| `INT` / `INTEGER` | 4바이트 정수 (-2,147,483,648 ~ 2,147,483,647) |
| `BIGINT` | 8바이트 정수 |
| `DECIMAL(p,s)` | 고정 소수점 (정밀도 p, 소수 s) |
| `FLOAT` | 4바이트 부동 소수점 |
| `DOUBLE` | 8바이트 부동 소수점 |

---

## 9. 값이 저장되는 형태 (타입 개념)
- **정수형**: 소수점 없는 숫자
- **실수형**: 소수점 있는 숫자
- **문자형**: 텍스트, 문자열
- **날짜/시간형**: `DATE`, `DATETIME`, `TIMESTAMP`
- **논리형**: `BOOLEAN` (참/거짓)

---

## 10. DML 핵심 개념
- DML은 **CRUD** 작업을 담당
  - **C(Create)** → `INSERT`
  - **R(Read)** → `SELECT`
  - **U(Update)** → `UPDATE`
  - **D(Delete)** → `DELETE`

---

## 11. SQL 기초 - SELECT 문법
```sql
SELECT 컬럼명1, 컬럼명2
FROM 테이블명
WHERE 조건;
````

**예시**

```sql
SELECT name, age
FROM member
WHERE age >= 20;
```

---

## 12. SQL 기초 - 비교 연산자

| 연산자                | 의미                     |
| ------------------ | ---------------------- |
| `=`                | 같다                     |
| `<>`, `!=`         | 같지 않다                  |
| `<`                | 작다                     |
| `>`                | 크다                     |
| `<=`               | 작거나 같다                 |
| `>=`               | 크거나 같다                 |
| `BETWEEN A AND B`  | A 이상 B 이하              |
| `IN (값1, 값2, ...)` | 목록 중 하나와 일치            |
| `LIKE`             | 패턴 일치 검색 (`%`, `_` 사용) |
| `IS NULL`          | 값이 NULL인지 확인           |

**LIKE 예시**

```sql
SELECT name
FROM member
WHERE name LIKE '김%'; -- '김'으로 시작하는 이름
```

---

## 📌 정리

* **SQL**: 데이터 정의(DDL), 조작(DML), 제어(DCL), 트랜잭션 제어(TCL)로 구성
* **데이터 타입**: 문자형, 숫자형, 날짜형, JSON 등
* **DML**: CRUD 작업 (INSERT, SELECT, UPDATE, DELETE)
* **비교 연산자**: 데이터 검색 조건 지정 시 필수

```


# DML (Data Manipulation Language)

테이블 “행 데이터”를 조회/추가/수정/삭제.

## 1) SELECT ― 조회

```sql
-- 기본
SELECT col1, col2
FROM `project.dataset.table`;

-- 별칭(AS)
SELECT col1 AS 이름, col2 AS 나이 FROM `...`;

-- 중복 제거
SELECT DISTINCT col1 FROM `...`;

-- 조건(WHERE)
SELECT * FROM `...` WHERE age >= 20 AND city = 'Seoul';

-- 패턴 매칭 (LIKE: %=0+글자, _=한 글자)
SELECT * FROM `...` WHERE title LIKE '%양양%';

-- 집계와 그룹
SELECT city, COUNT(*) AS cnt
FROM `...`
GROUP BY city;

-- 그룹 조건(HAVING: 집계결과에 조건)
SELECT city, COUNT(*) cnt
FROM `...`
GROUP BY city
HAVING COUNT(*) >= 10;

-- 정렬/개수 제한
SELECT * FROM `...` ORDER BY created_at DESC LIMIT 100;

-- 조인
SELECT a.id, b.name
FROM `...a` a
JOIN `...b` b ON a.user_id = b.id;

-- 집합 연산
SELECT id FROM `...A`
UNION ALL
SELECT id FROM `...B`;

-- 서브쿼리/CTE
WITH top_city AS (
  SELECT city FROM `...` GROUP BY city ORDER BY COUNT(*) DESC LIMIT 1
)
SELECT * FROM `...` WHERE city IN (SELECT city FROM top_city);

-- 윈도 함수(누적, 순위 등)
SELECT user_id,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY ts) AS running_sum
FROM `...`;

-- 🔸QUALIFY(윈도우 결과 필터)
SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ts DESC) rn
FROM `...`
QUALIFY rn = 1;

-- 🔸배열 UNNEST
SELECT user_id, item
FROM `...`, UNNEST(items) AS item;
```

자주 쓰는 집계함수: `COUNT(*)`, `SUM(col)`, `AVG(col)`, `MIN(col)`, `MAX(col)`
조건 분기: `CASE WHEN 조건 THEN 값 ELSE 값 END`

## 2) INSERT ― 추가

```sql
-- 값으로 넣기
INSERT INTO `project.dataset.table` (value)
VALUES ('hello world'), ('hi there');

-- SELECT 결과로 넣기
INSERT INTO `project.dataset.table` (user_id, amount)
SELECT user_id, amount
FROM `project.src_ds.payments`
WHERE status = 'OK';
```

## 3) UPDATE ― 수정

```sql
-- 단순 수정
UPDATE `project.dataset.table`
SET status = 'done'
WHERE id = 123;

-- 🔸다른 테이블 값을 이용해 수정
UPDATE `project.dataset.target` t
SET t.price = s.new_price
FROM `project.dataset.source` s
WHERE t.sku = s.sku;
```

## 4) DELETE ― 삭제

```sql
DELETE FROM `project.dataset.table`
WHERE created_at < DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY);
-- WHERE 없이 쓰면 모든 행 삭제 주의!
```

## 5) MERGE ― 업서트(있으면 UPDATE/없으면 INSERT)

```sql
MERGE `project.dataset.target` T
USING `project.dataset.source` S
ON T.id = S.id
WHEN MATCHED THEN
  UPDATE SET T.name = S.name, T.updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
  INSERT (id, name, created_at) VALUES (S.id, S.name, CURRENT_TIMESTAMP());
```

---

# DDL (Data Definition Language)

스키마/테이블/뷰 등 “구조”를 만들고 바꾸고 지움.

## 1) CREATE ― 생성

```sql
-- 🔸데이터셋(=스키마)
CREATE SCHEMA `project.dataset`;

-- 테이블
CREATE TABLE `project.dataset.table` (
  id INT64,
  value STRING,
  created_at TIMESTAMP
);

-- 🔸파티션/클러스터
CREATE TABLE `project.dataset.events` (
  user_id STRING,
  ts TIMESTAMP,
  event STRING
)
PARTITION BY DATE(ts)
CLUSTER BY user_id;

-- SELECT로 만들기(CTAS)
CREATE TABLE `project.dataset.top_users` AS
SELECT user_id, SUM(amount) total
FROM `project.dataset.payments`
GROUP BY user_id;

-- 뷰/머터리얼라이즈드 뷰
CREATE VIEW `project.dataset.vw_recent` AS
SELECT * FROM `project.dataset.t`
WHERE ts >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY);

CREATE MATERIALIZED VIEW `project.dataset.mv_top_users` AS
SELECT user_id, SUM(amount) total
FROM `project.dataset.payments`
GROUP BY user_id;

-- 🔸UDF/프로시저
CREATE FUNCTION `project.dataset.fn_norm`(x FLOAT64) AS (x/100.0);
CREATE PROCEDURE `project.dataset.proc_example`() BEGIN
  INSERT INTO `project.dataset.log` (msg) VALUES ('hello');
END;
```

## 2) ALTER ― 변경

```sql
-- 컬럼 추가/이름변경/타입변경
ALTER TABLE `project.dataset.table` ADD COLUMN note STRING;
ALTER TABLE `project.dataset.table` RENAME COLUMN note TO memo;
ALTER TABLE `project.dataset.table` ALTER COLUMN value SET DATA TYPE STRING;

-- 🔸옵션/파티션/클러스터 변경(일부 가능)
ALTER TABLE `project.dataset.events` SET OPTIONS (description = 'event log');
```

## 3) DROP ― 삭제

```sql
DROP TABLE `project.dataset.table`;
DROP VIEW  `project.dataset.vw_recent`;
DROP SCHEMA `project.dataset`;  -- 내부 객체 없을 때만
```

## 4) TRUNCATE ― 모든 행 빠르게 삭제(구조는 유지)

```sql
TRUNCATE TABLE `project.dataset.table`;
```

