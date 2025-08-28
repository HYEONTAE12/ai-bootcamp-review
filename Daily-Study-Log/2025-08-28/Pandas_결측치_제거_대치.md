
---

# 📌 결측값 처리 요약 (GitHub/Notion 용)

## 1. 결측치 탐색 함수

| 함수                      | 설명                   | 예시 코드              |
| ----------------------- | -------------------- | ------------------ |
| `isna()` / `isnull()`   | 결측치면 True, 아니면 False | `df.isna()`        |
| `.sum()`                | 결측치 개수 집계            | `df.isna().sum()`  |
| `notna()` / `notnull()` | 결측치가 아니면 True        | `df.notna()`       |
| `.sum()`                | 결측치 아닌 값 개수 집계       | `df.notna().sum()` |

---

## 2. 결측치 제거 (`dropna()`)

| 매개변수                | 설명                                        | 예시                             |
| ------------------- | ----------------------------------------- | ------------------------------ |
| `axis=0/1`          | 0: 행 제거, 1: 열 제거                          | `df.dropna(axis=1)`            |
| `how='any'/'all'`   | any: 하나라도 NaN 있으면 제거 / all: 전부 NaN일 때만 제거 | `df.dropna(how='all')`         |
| `thresh=n`          | NaN 아닌 값이 최소 `n`개 이상 있어야 남김               | `df.dropna(thresh=2)`          |
| `subset=[...]`      | 특정 컬럼만 기준으로 결측 판단                         | `df.dropna(subset=['age'])`    |
| `inplace=True`      | 원본 수정                                     | `df.dropna(inplace=True)`      |
| `ignore_index=True` | 반환 시 인덱스 0..N-1로 재배열                      | `df.dropna(ignore_index=True)` |

---

## 3. 결측치 대치 (`fillna()`)

| 매개변수           | 설명                              | 예시                                        |
| -------------- | ------------------------------- | ----------------------------------------- |
| `value`        | 스칼라/딕셔너리 값으로 대치                 | `df.fillna(-1)`<br>`df.fillna({"age":0})` |
| `method`       | ffill: 이전 값 채움 / bfill: 다음 값 채움 | `df.fillna(method='ffill')`               |
| `axis=0/1`     | 0: 행 기준(기본), 1: 열 기준            | `df.fillna(method='ffill', axis=0)`       |
| `limit`        | 몇 개까지만 채울지 제한                   | `df.fillna(method='ffill', limit=1)`      |
| `inplace=True` | 원본 수정                           | `df.fillna(0, inplace=True)`              |
| `downcast`     | 더 낮은 dtype으로 캐스팅                | `df.fillna(0, downcast='infer')`          |

---

## 4. 실무 활용 패턴

| 상황      | 권장 방법                                                |                                                                        |
| ------- | ---------------------------------------------------- | ---------------------------------------------------------------------- |
| 수치형 변수  | 평균/중앙값으로 대치 → `df['col'].fillna(df['col'].median())` |                                                                        |
| 범주형 변수  | 최빈값/Unknown으로 대치 → `df['cat'].fillna('Unknown')`     |                                                                        |
| 시계열 데이터 | 정렬 후 ffill/bfill                                     | `df.sort_values('date')['y'].fillna(method='ffill')`                   |
| 그룹별 대치  | 그룹 평균/중앙값 활용                                         | `df.groupby('group')['age'].transform(lambda s: s.fillna(s.median()))` |

---

✅ 이렇게 정리하면 깃허브 리드미나 노션에 그대로 붙여넣어도 보기 좋아요.

---

