
---

# 📌 판다스 정렬 & 함수 적용 요약 (GitHub/Notion 용)

---

## 1️⃣ 정렬: `DataFrame.sort_values`

| 매개변수           | 설명                                                                     | 예시                                                          |
| -------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------- |
| `by`           | 정렬 기준 컬럼/리스트                                                           | `df.sort_values('score')`                                   |
| `axis`         | 0: 행(기본), 1: 열                                                         | `df.sort_values(axis=1, by=['colB','colA'])`                |
| `ascending`    | True=오름차순, False=내림차순 <br> (리스트 지정 가능)                                 | `df.sort_values(['dept','score'], ascending=[True, False])` |
| `inplace`      | True면 원본 수정                                                            | `df.sort_values('score', inplace=True)`                     |
| `kind`         | 정렬 알고리즘 <br>`'quicksort'`, `'mergesort'`(안정), `'heapsort'`, `'stable'` | `df.sort_values('score', kind='mergesort')`                 |
| `na_position`  | `'last'`(기본), `'first'`: NaN 먼저 배치                                     | `df.sort_values('score', na_position='first')`              |
| `ignore_index` | True면 인덱스 0..N-1로 리셋                                                   | `df.sort_values('score', ignore_index=True)`                |
| `key`          | 정렬 키 함수                                                                | `df.sort_values('name', key=lambda s: s.str.lower())`       |

**실무 포인트**

* 랭킹, Top-N 뽑기 전에 필수
* 다중 기준 정렬 자주 씀
* 문자열 정렬 시 `key` 옵션 활용
* 인덱스 꼬임 방지 → `ignore_index=True`

---

## 2️⃣ 함수 적용: `apply`

### 🔹 `Series.apply`

| 매개변수               | 설명                    | 예시                          |
| ------------------ | --------------------- | --------------------------- |
| `func`             | 각 원소에 적용할 함수          | `s.apply(lambda x: x**2)`   |
| `convert_dtype`    | 반환 타입 변환 시도 (기본=True) |                             |
| `args`, `**kwargs` | 추가 인자 전달              | `s.apply(myfunc, arg1=...)` |

---

### 🔹 `DataFrame.apply`

| 매개변수               | 설명                                                                                                                 | 예시                                                  |
| ------------------ | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| `func`             | 축 단위로 적용할 함수                                                                                                       | `df.apply(np.mean, axis=0)`                         |
| `axis`             | 0: 열 단위(기본), 1: 행 단위                                                                                               | `df.apply(lambda r: r['x']+r['y'], axis=1)`         |
| `raw`              | True: ndarray 전달 → 속도↑ <br> False: Series 전달(기본)                                                                   | `df.apply(lambda a: a.max()-a.min(), raw=True)`     |
| `result_type`      | 행 단위(`axis=1`)일 때 결과 모양 제어 <br> - `'expand'`: 여러 열로 확장 <br> - `'reduce'`: 차원 축소 <br> - `'broadcast'`: 원래 DF 크기에 맞춤 | `df.apply(stats_row, axis=1, result_type='expand')` |
| `args`, `**kwargs` | 함수에 인자 전달                                                                                                          |                                                     |

---

### 🔹 관련 메서드 비교

| 메서드                  | 적용 대상              | 설명               |
| -------------------- | ------------------ | ---------------- |
| `Series.map`         | Series 원소 단위       | 가장 가볍고 빠름        |
| `DataFrame.applymap` | DataFrame 모든 원소 단위 | 원소 단위 연산         |
| `DataFrame.apply`    | 행/열 단위             | 집계·피처 생성 시 자주 사용 |

---

**실무 포인트**

* 컬럼 조합해서 새로운 피처 만들 때 (`axis=1`)
* 집계 통계치 생성 (min\~max 차이 등)
* `apply`는 느릴 수 있으니 **가능하면 벡터화 연산/전용 접근자 사용**

---

