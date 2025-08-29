
---

# 🧩 실무용 예제 데이터 구성

```python
import numpy as np
import pandas as pd

# 예제 데이터 (실무에서도 흔한 형태로 구성)
df = pd.DataFrame({
    "customer_id": [101, 102, 103, 104, 105, 106],
    "score":       [100, 100, 95, 80, 80, np.nan],
    "age":         [29, 33, 41, 23, 35, 30],
    "gender":      ["M", "F", "F", "M", "F", "M"],
    "FamilySize":  [1, 2, 1, 3, 1, 2],
    "Pclass":      [1, 1, 2, 3, 2, 3],
    "Survived":    [1, 0, 1, 0, 1, 0]
})
df["gender"] = df["gender"].astype("category")  # 범주형 예시
df
```

---

## 1) 기초 통계: `mode`, `median`, `rank`

```python
# --- mode() : 최빈값 ---
# dropna=True(기본) → NaN 제거 후 최빈값 계산, 여러 최빈값이면 모두 반환(Series)
mode_vals = df["score"].mode(dropna=True)
print("[mode] score 최빈값(들):", list(mode_vals))

# --- median() : 중앙값 ---
# skipna=True(기본) → NaN 무시하고 계산
median_val = df["score"].median(skipna=True)
print("[median] score 중앙값:", median_val)

# --- rank() : 순위 매기기 ---
# method 매개변수:
#  - 'average' (기본): 동점 순위 평균
#  - 'min' : 동점에 가장 작은 순위
#  - 'max' : 동점에 가장 큰 순위
#  - 'first': 먼저 나온 것이 더 높은 순위
df["rank_avg"]  = df["score"].rank(method="average", ascending=False)  # 높은 점수가 1등 되게 하려면 ascending=False
df["rank_min"]  = df["score"].rank(method="min",     ascending=False)
df["rank_max"]  = df["score"].rank(method="max",     ascending=False)
df["rank_first"]= df["score"].rank(method="first",   ascending=False)
# pct=True → 백분위 순위(0~1)
df["rank_pct"]  = df["score"].rank(method="average", ascending=True, pct=True)
df[["customer_id","score","rank_avg","rank_min","rank_max","rank_first","rank_pct"]]
```

---

## 2) 수치/범주 일괄 처리: `select_dtypes()`

```python
# include / exclude 로 타입 필터링
num_cols  = df.select_dtypes(include="number").columns     # 숫자형만
cat_cols  = df.select_dtypes(exclude="number").columns     # 숫자형 제외(문자, bool, datetime, category 등)

print("[select_dtypes] 숫자형 컬럼:", list(num_cols))
print("[select_dtypes] 비숫자 컬럼:", list(cat_cols))

# (실무 패턴) 수치형/범주형 전처리를 나눠 적용
# 예: 수치형 결측치 중앙값 대체, 범주형 결측치 최빈값 대체
df_num = df[num_cols].copy()
df_cat = df[cat_cols].copy()

df_num = df_num.fillna(df_num.median(numeric_only=True))  # 중앙값 대체
for c in df_cat.columns:
    if df_cat[c].isna().any():
        df_cat[c] = df_cat[c].fillna(df_cat[c].mode(dropna=True).iloc[0])

df_preprocessed = pd.concat([df_num, df_cat], axis=1)
df_preprocessed
```

---

## 3) 조건 가공 3가지 방식: 리스트내포 / `np.where` / 벡터연산

```python
# 1) 리스트 내포 : 직관적
df["IsAlone_lc"] = [1 if x == 1 else 0 for x in df["FamilySize"]]

# 2) np.where : 벡터화, 빠름
df["IsAlone_np"] = np.where(df["FamilySize"] == 1, 1, 0)

# 3) 벡터연산 + astype(int) : 가장 간결, 매우 빠름
df["IsAlone_vec"] = (df["FamilySize"] == 1).astype(int)

df[["customer_id","FamilySize","IsAlone_lc","IsAlone_np","IsAlone_vec"]]
```

---

## 4) 피벗 테이블: 그룹 요약 + 파라미터 설명

```python
# 성별(gender) × 객실등급(Pclass)별 생존률 평균
# pivot_table 주요 매개변수:
#  - index: 행 그룹 기준
#  - columns: 열 그룹 기준
#  - values: 집계 대상 컬럼
#  - aggfunc: 집계 함수 ('mean','sum','count', np.median, 사용자 정의 등)
#  - fill_value: 결측 집계값 대체
#  - margins=True, margins_name="All" → 전체 합계/평균 행·열 추가
pclass_ratio = (
    df.pivot_table(
        index="gender",
        columns="Pclass",
        values="Survived",
        aggfunc="mean",
        fill_value=0.0,
        margins=True,
        margins_name="All"
    )
    .reset_index()
)

# 실무에서 바로 쓰기 좋게 컬럼명 정리
# Pclass가 1,2,3,All 일 때의 평균 → 의미 있는 이름으로 리네임
new_cols = ["gender"] + [f"pclass{c}_ratio" if c != "All" else "overall_ratio" for c in pclass_ratio.columns[1:]]
pclass_ratio.columns = new_cols
pclass_ratio
```

---

## 5) “실무형” 전처리 파이프라인 함수 (재사용)

```python
def build_features(table: pd.DataFrame) -> pd.DataFrame:
    """
    실무 재사용을 위한 전처리/특징 엔지니어링 파이프라인 예시
    - 결측치 처리(숫자: 중앙값, 범주: 최빈값)
    - 파생변수 생성(IsAlone)
    - 기본 통계 컬럼 추가(예: score의 순위)
    - 피벗 결과를 조인해 요약 피처로 활용
    """
    df = table.copy()

    # 타입 분리
    num_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(exclude="number").columns

    # 결측치 처리
    df[num_cols] = df[num_cols].fillna(df[num_cols].median(numeric_only=True))
    for c in cat_cols:
        if df[c].isna().any():
            df[c] = df[c].fillna(df[c].mode(dropna=True).iloc[0])

    # 파생 변수: IsAlone (가장 간결한 벡터 방식)
    if "FamilySize" in df.columns:
        df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

    # 순위 파생: 높은 score가 1등이 되도록(동점 평균)
    if "score" in df.columns:
        df["score_rank"] = df["score"].rank(method="average", ascending=False)

    # 피벗 결과를 고객 레벨에 조인해 요약 피처로 사용 (예시)
    if set(["gender","Pclass","Survived"]).issubset(df.columns):
        pivot = (
            df.pivot_table(
                index="gender",
                columns="Pclass",
                values="Survived",
                aggfunc="mean",
                fill_value=0.0
            )
            .reset_index()
        )
        # 컬럼명 리네임
        pivot.columns = ["gender"] + [f"pclass{c}_ratio" for c in pivot.columns[1:]]
        df = df.merge(pivot, on="gender", how="left")

    return df

df_feat = build_features(df)
df_feat.head()
```

---

## 6) (옵션) 빠른 EDA 유틸: 대표값/이상치 민감도 비교

```python
# 평균 vs 중앙값 비교(이상치 민감도 체크)
summary = pd.DataFrame({
    "mean_score": [df["score"].mean(skipna=True)],
    "median_score": [df["score"].median(skipna=True)],
    "mode_score": [df["score"].mode(dropna=True).iloc[0] if not df["score"].mode(dropna=True).empty else np.nan]
})
summary
```

---

### 이렇게 쓰면 좋아

* 노트북/스크립트에서 **위 블록들을 그대로 복붙** → 즉시 실행/응용
* 전처리 템플릿 `build_features()`를 **프로젝트 공용 유틸**로 두고 재사용
* `pivot_table` 결과를 **요약 피처로 조인**하는 패턴은 실제 모델 성능 개선에 자주 도움 됨
* `select_dtypes`로 **수치/범주 분리 후 일괄 처리**는 실무 정석 패턴

