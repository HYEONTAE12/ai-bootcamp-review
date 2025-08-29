
---

# 📊 데이터 분석 정리

---

## 📌 기초 통계량

### `mode()` — 최빈값

* **정의**: 데이터에서 가장 많이 등장하는 값
* **특징**: 데이터 분포에서 대표값으로 활용됨

---

### `median()` — 중앙값

* **정의**: 데이터를 크기순으로 정렬했을 때 가운데 있는 값
* **특징**:

  * 평균과 달리 **이상치(Outlier)에 덜 민감**
  * 데이터가 치우쳐 있어도 중심 경향을 잘 표현

---

### `rank()` — 순위 매기기

```python
df['rank'] = df['score'].rank(method='average')
```

* **정의**: 데이터의 순위를 매기는 메서드
* **주요 매개변수**:

  * `method` (str, 기본값=`'average'`)

    * `'average'`: 동점 시 순위 평균 부여 (예: 1.5등)
    * `'min'`: 동점 시 **가장 작은 순위** 부여
    * `'max'`: 동점 시 **가장 큰 순위** 부여
    * `'first'`: 동점 시 **먼저 등장한 값**이 우선순위

---

## 📌 데이터 타입 분리 처리

### `select_dtypes()` — 특정 타입 선택

```python
df.select_dtypes(include="number").columns
```

* **정의**: DataFrame에서 특정 데이터 타입만 선택
* **주요 매개변수**:

  * `include`: 포함할 타입 지정

    * `"number"` → 숫자형(int, float 등)
  * `exclude`: 제외할 타입 지정

    * `"number"` → 숫자형 제외 → 문자, bool, datetime, category 등

👉 **활용 예시**: 수치형 / 범주형 변수를 나눠서 일괄 처리할 때 사용

---

## 📌 데이터 조건 검색 및 가공

### 1. 리스트 내포 방식

```python
main_origin['IsAlone'] = [1 if x == 1 else 0 for x in main_origin['FamilySize']]
```

* **설명**: `FamilySize` 값이 1이면 1, 아니면 0 반환
* **장점**: 직관적이고 파이썬 기본 문법만으로 구현 가능

---

### 2. `np.where` 방식

```python
main_origin['A'] = np.where(main_origin['FamilySize'] == 1, 1, 0)
```

* **설명**: 조건문(`FamilySize == 1`)이 참이면 1, 거짓이면 0

* **장점**: 벡터화 연산으로 **빠름**

* **매개변수**:

  * `condition`: 조건식 (True/False 결과 반환)
  * `x`: 조건이 참일 때 값
  * `y`: 조건이 거짓일 때 값

---

### 3. 벡터 연산 + 형 변환

```python
main_origin['B'] = (main_origin['FamilySize'] == 1).astype(int)
```

* **설명**: 조건식 자체가 True/False → `.astype(int)`로 1/0 변환
* **장점**: 가장 간결하고 연산 속도 빠름

---

## 📌 피벗 테이블 (Pivot Table)

### 예제 코드

```python
pclass_ratio = (
    train.pivot_table(
        index="Sex", 
        columns="Pclass", 
        values="Survived", 
        aggfunc="mean"
    ).reset_index()
)

pclass_ratio.columns = ["Sex", "pclass1_ratio", "pclass2_ratio", "pclass3_ratio"]
```

* **정의**: 데이터를 그룹화하여 **요약된 형태**로 재구조화

* **매개변수**:

  * `index`: 행 그룹 기준
  * `columns`: 열 그룹 기준
  * `values`: 집계할 대상 컬럼
  * `aggfunc`: 집계 함수 (기본값=`'mean'`)

    * `'mean'`: 평균
    * `'sum'`: 합계
    * `'count'`: 개수
    * 사용자 정의 함수도 가능 (`np.median`, `lambda x: ...`)

* **활용**: 성별(`Sex`) + 객실등급(`Pclass`)별 생존률(`Survived`) 평균 계산

---

# ✅ 정리 요약

* **mode / median** → 대표값 확인 (평균만 보지 말고 같이 참고)
* **rank(method)** → 순위 매기기 (평균, min, max, first 옵션)
* **select\_dtypes** → 수치형/범주형 변수 자동 분리
* **조건 처리 방식**

  * 리스트 내포: 직관적
  * np.where: 빠름, numpy 기반
  * 벡터 연산: 가장 깔끔하고 효율적
* **피벗 테이블** → 그룹별 집계, 구조 변환, 요약 통계

---

