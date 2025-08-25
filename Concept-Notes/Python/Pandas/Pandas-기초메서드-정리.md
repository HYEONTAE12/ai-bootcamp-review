
---

# 📊 Pandas 데이터 분석 자주 사용하는 메서드 정리

```python
import pandas as pd

data = {
    'Name': ['A', 'B', 'C', 'A', 'B'],
    'Age': [20, 21, 22, 20, 21],
    'Score': [85, 90, 78, 88, 92]
}
df = pd.DataFrame(data)
```

---

## 1. 데이터 확인 관련

### 🔹 `head()` / `tail()`

* 데이터의 앞부분 / 뒷부분 확인

```python
df.head(3)   # 앞 3행
df.tail(2)   # 뒤 2행
```

---

### 🔹 `info()`

* 컬럼별 데이터 타입, 결측치 여부, 전체 행 수 확인

```python
df.info()
```

---

### 🔹 `describe()`

* 수치형 데이터의 요약 통계량 제공 (평균, 표준편차, 최소/최대값 등)

```python
df.describe()
```

---

### 🔹 `shape`

* (행 수, 열 수) 반환

```python
df.shape
# (5, 3)
```

---

## 2. 선택 및 필터링

### 🔹 `[]` (컬럼 선택)

```python
df['Name']       # 단일 컬럼
df[['Name','Age']]  # 여러 컬럼
```

---

### 🔹 `loc` / `iloc`

* `loc`: 인덱스 이름으로 접근
* `iloc`: 정수 인덱스로 접근

```python
df.loc[0, 'Name']    # 인덱스 0, 'Name' 컬럼 값
df.iloc[0, 1]        # 0행 1열 값
```

---

### 🔹 조건 필터링

```python
df[df['Age'] > 20]
```

---

## 3. 결측치 처리

### 🔹 `isna()` / `notna()`

```python
df.isna().sum()
```

### 🔹 `dropna()`

```python
df.dropna(subset=['Score'])
```

### 🔹 `fillna()`

```python
df['Score'].fillna(df['Score'].mean(), inplace=True)
```

---

## 4. 중복 처리

### 🔹 `duplicated()` / `drop_duplicates()`

```python
df.duplicated()
df.drop_duplicates(subset=['Name'])
```

---

## 5. 고유값 & 빈도

### 🔹 `unique()`

```python
df['Name'].unique()
# ['A', 'B', 'C']
```

### 🔹 `nunique()`

```python
df['Name'].nunique()
# 3
```

### 🔹 `value_counts()`

```python
df['Name'].value_counts()
# B 2
# A 2
# C 1
```

---

## 6. 정렬

### 🔹 `sort_values()`

```python
df.sort_values(by='Score', ascending=False)
```

---

## 7. 그룹화

### 🔹 `groupby()`

```python
df.groupby('Name')['Score'].mean()
```

---

## 8. 집계 함수

```python
df['Score'].mean()   # 평균
df['Score'].max()    # 최댓값
df['Score'].min()    # 최솟값
df['Score'].sum()    # 합계
```

---

## 9. 열/행 추가 및 삭제

### 🔹 새로운 컬럼 추가

```python
df['Pass'] = df['Score'] >= 80
```

### 🔹 열 삭제

```python
df.drop(columns=['Age'], inplace=True)
```

### 🔹 행 삭제

```python
df.drop(index=0, inplace=True)  # 인덱스 0 행 삭제
```

---

## 10. 합치기 & 병합

### 🔹 `concat`

```python
df2 = pd.DataFrame({'Name':['D'], 'Age':[23], 'Score':[95]})
pd.concat([df, df2])
```

### 🔹 `merge`

```python
df3 = pd.DataFrame({'Name':['A','B'], 'Team':['Red','Blue']})
df.merge(df3, on='Name')
```

---

# ✅ 요약

* **데이터 구조 확인**: `head`, `info`, `describe`, `shape`
* **결측치 처리**: `isna`, `dropna`, `fillna`
* **중복/고유값**: `duplicated`, `unique`, `nunique`, `value_counts`
* **정렬/그룹화**: `sort_values`, `groupby`
* **추가/삭제/병합**: `drop`, `concat`, `merge`

---

