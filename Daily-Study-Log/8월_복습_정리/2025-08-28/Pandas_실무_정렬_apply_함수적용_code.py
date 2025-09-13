
---

# 📌 정렬 & 함수 적용 실습 코드 (Cheat Sheet → Python Script)

```python
import pandas as pd
import numpy as np

# 샘플 데이터 생성
df = pd.DataFrame({
    "dept": ["A", "B", "A", "B", "C"],
    "name": ["민준", "서연", "서준", "도현", "지윤"],
    "score": [85, 90, 95, np.nan, 88],
    "age": [15, 30, 40, 20, 23]
})

print("=== 원본 데이터 ===")
print(df)

# -------------------------------------------------
# 1. 정렬 (sort_values)
# -------------------------------------------------

# 1) 단일 컬럼 오름차순 (기본값)
asc = df.sort_values("score")
print("\n[sort_values: score 오름차순]")
print(asc)

# 2) 단일 컬럼 내림차순
desc = df.sort_values("score", ascending=False)
print("\n[sort_values: score 내림차순]")
print(desc)

# 3) 다중 컬럼 정렬 (부서 오름차순 → 점수 내림차순)
multi = df.sort_values(["dept", "score"], ascending=[True, False])
print("\n[sort_values: dept 오름차순, score 내림차순]")
print(multi)

# 4) NaN 먼저 배치
nan_first = df.sort_values("score", na_position="first")
print("\n[sort_values: NaN을 먼저 배치]")
print(nan_first)

# 5) 문자열 대소문자 무시 정렬 (key 옵션)
str_sort = df.sort_values("name", key=lambda s: s.str.lower())
print("\n[sort_values: 문자열 대소문자 무시 정렬]")
print(str_sort)

# 6) 안정 정렬 (동일 값일 때 기존 순서 유지)
stable = df.sort_values("dept", kind="mergesort")
print("\n[sort_values: 안정 정렬]")
print(stable)

# -------------------------------------------------
# 2. 함수 적용 (apply)
# -------------------------------------------------

# 1) Series.apply: 각 원소 제곱
squared = df["age"].apply(lambda x: x**2)
print("\n[Series.apply: age 제곱]")
print(squared)

# 2) Series.apply: 추가 인자 전달
def add_then_pow(x, add=0, p=1):
    return (x + add) ** p

series_custom = df["age"].apply(add_then_pow, add=3, p=2)
print("\n[Series.apply: add_then_pow]")
print(series_custom)

# 3) DataFrame.apply: 열 단위 집계 (axis=0, 기본값)
col_mean = df.apply(np.mean, axis=0, numeric_only=True)
print("\n[DataFrame.apply: 열 평균]")
print(col_mean)

# 4) DataFrame.apply: 행 단위 연산 (axis=1)
row_sum = df.apply(lambda row: row["score"] + row["age"], axis=1)
print("\n[DataFrame.apply: 행 단위 (score+age)]")
print(row_sum)

# 5) DataFrame.apply: 여러 값 반환 → expand
def stats_row(row):
    return pd.Series({"sum": row.sum(numeric_only=True), "mean": row.mean(numeric_only=True)})

row_stats = df.apply(stats_row, axis=1)
print("\n[DataFrame.apply: result_type='expand' 동작 예시]")
print(row_stats)

# 6) DataFrame.apply: 브로드캐스트 (원래 모양 유지)
broadcast = df.apply(lambda row: row - row.mean(numeric_only=True), axis=1, result_type="broadcast")
print("\n[DataFrame.apply: result_type='broadcast']")
print(broadcast)

# 7) DataFrame.apply: raw=True (ndarray 전달 → 속도 ↑)
raw_apply = df[["score", "age"]].apply(lambda arr: arr.max() - arr.min(), raw=True)
print("\n[DataFrame.apply: raw=True 예시 (max-min)]")
print(raw_apply)

# -------------------------------------------------
# 3. map / applymap 비교 (참고)
# -------------------------------------------------

# Series.map: Series 원소 단위 적용
mapped = df["name"].map(lambda x: x.upper())
print("\n[Series.map: 이름 대문자 변환]")
print(mapped)

# DataFrame.applymap: DataFrame 원소 단위 적용
applymapped = df[["dept", "name"]].applymap(lambda x: str(x).lower())
print("\n[DataFrame.applymap: 문자열 소문자 변환]")
print(applymapped)
```

---

