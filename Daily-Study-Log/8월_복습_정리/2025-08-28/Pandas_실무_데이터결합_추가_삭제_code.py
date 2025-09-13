
---

# 📌 데이터 결합/추가/삭제 실습 코드 (Cheat Sheet → Python Script)

```python
import pandas as pd

# 샘플 데이터 준비
data1 = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["민준", "서연", "서준"],
    "score": [85, 90, 95]
})

data2 = pd.DataFrame({
    "id": [2, 3, 4],
    "subject": ["수학", "영어", "과학"],
    "score": [88, 92, 77]
})

print("=== data1 ===")
print(data1)
print("=== data2 ===")
print(data2)

# -------------------------------------------------
# 1. 데이터 결합 (merge)
# -------------------------------------------------

# 1) inner join (교집합)
inner = pd.merge(data1, data2, on="id", how="inner")
print("\n[merge: inner join]")
print(inner)

# 2) full outer join (합집합, 없는 값은 NaN)
outer = pd.merge(data1, data2, on="id", how="outer")
print("\n[merge: outer join]")
print(outer)

# 3) left outer join
left = pd.merge(data1, data2, on="id", how="left")
print("\n[merge: left join]")
print(left)

# 4) right outer join
right = pd.merge(data1, data2, on="id", how="right")
print("\n[merge: right join]")
print(right)

# 5) 컬럼명이 다를 때 (left_on / right_on)
data3 = data2.rename(columns={"id": "student_id"})
merge_diff = pd.merge(data1, data3, left_on="id", right_on="student_id", how="left")
print("\n[merge: left_on vs right_on]")
print(merge_diff)

# -------------------------------------------------
# 2. 행/열 결합 (concat)
# -------------------------------------------------

# 1) 행 추가 (axis=0)
row_concat = pd.concat([data1, data1], axis=0, ignore_index=True)
print("\n[concat: 행 추가]")
print(row_concat)

# 2) 열 추가 (axis=1)
col_concat = pd.concat([data1, data2], axis=1)
print("\n[concat: 열 추가]")
print(col_concat)

# 3) 공통 컬럼만 유지 (join='inner')
inner_concat = pd.concat([data1, data2], axis=0, join="inner", ignore_index=True)
print("\n[concat: join='inner']")
print(inner_concat)

# -------------------------------------------------
# 3. 행/열 추가/삭제 (인덱스 다루기)
# -------------------------------------------------

df = data1.copy()

# 1) set_index
df_indexed = df.set_index("name")
print("\n[set_index: 'name'을 인덱스로]")
print(df_indexed)

# 2) reset_index 기본
df_reset = df_indexed.reset_index()
print("\n[reset_index: 기본]")
print(df_reset)

# 3) reset_index(drop=True)
df_reset_drop = df_indexed.reset_index(drop=True)
print("\n[reset_index: drop=True]")
print(df_reset_drop)

# 4) MultiIndex 예시 + level 지정
multi = df.set_index(["id", "name"])
print("\n[MultiIndex]")
print(multi)
multi_reset = multi.reset_index(level=1)
print("\n[reset_index(level=1)]")
print(multi_reset)

# -------------------------------------------------
# 4. 행/열 제거 (drop)
# -------------------------------------------------

df = data1.copy()

# 1) 행 제거 (axis=0)
drop_row = df.drop([0, 1], axis=0)
print("\n[drop: 행 제거]")
print(drop_row)

# 2) 열 제거 (axis=1)
drop_col = df.drop(["score"], axis=1)
print("\n[drop: 열 제거]")
print(drop_col)

# 3) index/columns 인자로 제거
drop_idx = df.drop(index=[0])
drop_cols = df.drop(columns=["name"])
print("\n[drop: index/columns 사용]")
print(drop_idx)
print(drop_cols)

# 4) errors 옵션 (없는 컬럼 제거 시 에러 무시)
drop_err = df.drop(columns=["not_exist"], errors="ignore")
print("\n[drop: errors='ignore']")
print(drop_err)

# -------------------------------------------------
# 5. 중복 제거 (drop_duplicates / duplicated)
# -------------------------------------------------

df_dup = pd.DataFrame({
    "id": [1, 2, 2, 3, 3, 3],
    "name": ["민준", "서연", "서연", "서준", "서준", "서준"],
    "score": [85, 90, 90, 95, 95, 95]
})

print("\n=== 중복 포함 데이터 ===")
print(df_dup)

# 1) 전체 중복 제거
dedup_all = df_dup.drop_duplicates()
print("\n[drop_duplicates: 전체 중복 제거]")
print(dedup_all)

# 2) 특정 컬럼 기준 중복 제거 (subset)
dedup_subset = df_dup.drop_duplicates(subset=["name"], keep="last")
print("\n[drop_duplicates: subset='name', keep='last']")
print(dedup_subset)

# 3) 중복 여부 확인 (duplicated)
dup_mask = df_dup.duplicated(subset=["name"], keep=False)
print("\n[duplicated: subset='name']")
print(df_dup[dup_mask])
```

---

