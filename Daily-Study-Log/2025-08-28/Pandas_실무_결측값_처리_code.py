
---

# 📌 결측값 처리 실습 코드 (Cheat Sheet → Python Script)

```python
import pandas as pd
import numpy as np

# 샘플 데이터 생성
df = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "name": ["민준", np.nan, "서연", "서준"],
    "age": [15, 30, np.nan, np.nan],
    "sales": [100, np.nan, 200, np.nan]
})

print("=== 원본 데이터 ===")
print(df)

# -------------------------------------------------
# 1. 결측값 탐색
# -------------------------------------------------

# 1) 결측 여부 (True/False)
print("\n[isna()]")
print(df.isna())  # == df.isnull()

# 2) 컬럼별 결측 개수
print("\n[isna().sum()]")
print(df.isna().sum())

# 3) 결측 아님 여부 (True/False)
print("\n[notna()]")
print(df.notna())  # == df.notnull()

# 4) 컬럼별 결측 아님 개수
print("\n[notna().sum()]")
print(df.notna().sum())

# -------------------------------------------------
# 2. 결측값 제거 (dropna)
# -------------------------------------------------

# 1) 결측치가 하나라도 있는 행 제거
df1 = df.dropna()
print("\n[dropna: 결측 있는 행 제거]")
print(df1)

# 2) 결측치가 있는 열 제거
df2 = df.dropna(axis=1)
print("\n[dropna: 결측 있는 열 제거]")
print(df2)

# 3) 모든 값이 NaN인 행만 제거
df3 = df.dropna(how="all")
print("\n[dropna: 모든 값이 NaN인 행만 제거]")
print(df3)

# 4) 최소 비-NaN 값 개수 기준(thresh)
df4 = df.dropna(thresh=2)  # 최소 2개 이상 값이 있어야 유지
print("\n[dropna: thresh=2]")
print(df4)

# 5) 특정 컬럼만 기준으로 결측 판단
df5 = df.dropna(subset=["name"])
print("\n[dropna: subset='name']")
print(df5)

# -------------------------------------------------
# 3. 결측값 대치 (fillna)
# -------------------------------------------------

# 1) 모든 NaN을 같은 값으로
df_a = df.fillna(-1)
print("\n[fillna: -1로 채우기]")
print(df_a)

# 2) 컬럼별 다른 값으로
df_b = df.fillna({"name": "Unknown", "age": 0})
print("\n[fillna: 컬럼별 다른 값 채우기]")
print(df_b)

# 3) 이전 값/다음 값으로 채우기 (ffill, bfill)
df_ffill = df.fillna(method="ffill")
df_bfill = df.fillna(method="bfill")
print("\n[fillna: ffill]")
print(df_ffill)
print("\n[fillna: bfill]")
print(df_bfill)

# 4) ffill + limit (연속된 NaN 일부만 채우기)
df_lim = df.fillna(method="ffill", limit=1)
print("\n[fillna: ffill + limit=1]")
print(df_lim)

# 5) 반환 대신 원본 수정
df_copy = df.copy()
df_copy.fillna({"age": 0}, inplace=True)
print("\n[fillna: inplace=True]")
print(df_copy)

# 6) downcast 옵션
df_num = pd.DataFrame({"x": [1.0, np.nan, 3.0]})
df_num = df_num.fillna(0, downcast="infer")
print("\n[fillna: downcast]")
print(df_num, df_num.dtypes)

# -------------------------------------------------
# 4. 실무에서 자주 쓰는 패턴
# -------------------------------------------------

# A) 그룹 평균/최빈값으로 채우기
df_group = df.copy()
df_group["age"] = df_group.groupby("name")["age"].transform(lambda s: s.fillna(s.mean()))
print("\n[그룹별 평균으로 age 채우기]")
print(df_group)

# B) 수치/범주 나눠서 일괄 처리
df_split = df.copy()
num_cols = df_split.select_dtypes(include="number").columns
cat_cols = df_split.select_dtypes(exclude="number").columns

df_split[num_cols] = df_split[num_cols].fillna(df_split[num_cols].median())
df_split[cat_cols] = df_split[cat_cols].fillna("Unknown")
print("\n[수치=중앙값, 범주=Unknown으로 대치]")
print(df_split)

# C) 시계열: 정렬 후 ffill/bfill
df_time = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=4),
    "sales": [100, np.nan, 200, np.nan]
}).sort_values("date")

df_time["sales"] = df_time["sales"].fillna(method="ffill").fillna(0)
print("\n[시계열: ffill 후 남은 NaN은 0]")
print(df_time)

# -------------------------------------------------
# 5. 마스크 연산 (조건부 대치)
# -------------------------------------------------

df_mask = df.copy()
mask = df_mask["age"].isna() & (df_mask["name"] == "민준")
df_mask.loc[mask, "age"] = 20
print("\n[마스크 연산: 조건부 age 대치]")
print(df_mask)

# -------------------------------------------------
# 6. replace 활용 (비표준 결측 기호를 NaN으로 변환)
# -------------------------------------------------

df_replace = pd.DataFrame({"age": ["N/A", -1, 25, np.nan]})
df_replace = df_replace.replace({"age": {"N/A": np.nan, -1: np.nan}})
df_replace = df_replace.fillna(0)
print("\n[replace: 비표준 결측 기호 처리 후 fillna]")
print(df_replace)

# -------------------------------------------------
# 7. 상황별 전략 요약 (코드 조각)
# -------------------------------------------------

# 1) 간단히 행 날리기
df_clean = df.dropna()

# 2) 특정 컬럼 기준으로만 행 날리기
df_clean2 = df.dropna(subset=["age", "name"])

# 3) 수치=중앙값 / 범주=Unknown
df3 = df.copy()
df3[num_cols] = df3[num_cols].fillna(df3[num_cols].median())
df3[cat_cols] = df3[cat_cols].fillna("Unknown")

# 4) 시계열 ffill/bfill
df_time["sales"] = df_time["sales"].fillna(method="ffill", limit=2).fillna(method="bfill")

# 5) 그룹 통계 기반 대치
df["age"] = df.groupby("name")["age"].transform(lambda s: s.fillna(s.median()))
```

---

