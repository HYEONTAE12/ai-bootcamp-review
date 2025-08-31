
---

# Matplotlib · Seaborn · Pandas 상관/축·라벨·히트맵·히스토그램 정리

실습 중 자주 쓰는 함수/옵션을 예시 코드와 함께 정리했습니다.

---

## 1) `plt.xticks()` 반환값: `locs`, `labels`

```python
locs, labels = plt.xticks()
```

* **`locs`**: 현재 X축 **눈금 위치(숫자 좌표값)** 배열/리스트
  예) 데이터가 1, 2, 3이면 → `locs = [1.0, 2.0, 3.0]`
* **`labels`**: 각 눈금에 붙은 **`Text` 객체 리스트**
  문자열이 아니라 **텍스트 객체**라서 “글자 내용, 폰트, 회전각, 색상” 같은 **스타일 속성**을 가짐
  예) `[Text(1.0, 0, '1'), Text(2.0, 0, '2'), ...]`

> 문자열만 뽑고 싶다면:
>
> ```python
> texts = [t.get_text() for t in labels]  # ['1','2','3', ...]
> ```

### 사용 팁

* `plt.xticks()` **인자 없이 호출**하면 “현재 상태를 조회”하고 `(locs, labels)`를 **반환**한다.
* 위치/라벨을 **설정**하고 싶다면:

  ```python
  plt.xticks([0,1,2], ['A','B','C'], rotation=45)
  ```

---

## 2) `ax.set_xticklabels(...)`로 라벨 스타일만 수정

```python
ax.set_xticklabels(labels, rotation=45)
```

* `labels`에 **문자열 리스트** 또는 **Text 객체 리스트**를 줄 수 있음.
* 위 코드는 “반환받은 라벨을 그대로 쓰되 **회전만 적용**”하는 예.

> ⚠️ **주의**
> `set_xticklabels`만 바꾸면 **눈금 위치**(`xticks`)와 **라벨 개수**가 어긋나 **경고/오표기**가 날 수 있음.
> 안전하게 하려면 위치와 라벨을 **함께** 지정:
>
> ```python
> ax.set_xticks([0,1,2])
> ax.set_xticklabels(['A','B','C'], rotation=45, ha='right')
> ```

---

## 3) `df.corr(numeric_only=True)` — 상관계수 행렬

```python
corr = df.corr(numeric_only=True)  # 기본: Pearson
```

* **기본 메서드**: 피어슨(Pearson) 상관계수
* **`numeric_only=True`**: 정수/실수/불리언 등 **숫자형 열만** 사용 (문자열, 날짜 등은 자동 제외)
* **`numeric_only=False`**: 숫자형이 아닌 열까지 시도 → 보통 **오류/의미없음**
  (대부분 실무에선 `True` 권장)

> 다른 상관법:
>
> ```python
> df.corr(method='spearman', numeric_only=True)  # 순위 상관
> df.corr(method='kendall',  numeric_only=True)  # Kendall τ
> ```

---

## 4) 히트맵에서 상·하 삼각 마스크 만들기

### 4-1) `np.ones_like` + `np.triu`

```python
mask = np.ones_like(corr, dtype=bool)  # corr와 동일 shape의 True 배열
mask = np.triu(mask)                   # 상삼각(대각선 포함)만 True, 나머지 False
```

* `np.ones_like(corr, dtype=bool)`: **corr와 같은 크기**의 **True** 마스크 생성
* `np.triu(mask)`: **상삼각(Upper Triangle)** 부분을 남김
  → **위쪽을 가릴지/보여줄지**는 `sns.heatmap(..., mask=mask)`에서 해석됨
  (Seaborn은 `True`인 위치를 **가린다**)

> 대각선(자기 자신과의 상관)을 **빼고 싶으면**:
>
> ```python
> mask = np.triu(np.ones_like(corr, dtype=bool), k=1)  # k=1이면 대각선 위만 True
> ```

### 4-2) 하삼각만 보고 싶을 때

* 위처럼 만든 `mask`를 그대로 쓰면 **상삼각이 가려지고** 하삼각만 보임:

  ```python
  sns.heatmap(corr, mask=mask, ...)
  ```

---

## 5) `sns.heatmap(...)` 핵심 옵션

```python
sns.heatmap(
    data=corr,
    annot=True,          # 각 셀에 수치 표시
    fmt='.2f',           # 소수 둘째 자리까지
    mask=mask,           # True인 셀은 가림
    linewidths=.5,       # 셀 경계선 두께
    cmap='RdYlBu_r'      # 컬러맵 (Red–Yellow–Blue 반전)
)
```

### 옵션 설명

* **`data`**: 2D 배열/데이터프레임(여기선 상관행렬)
* **`annot=True`**: 셀에 숫자 표시
* **`fmt='.2f'`**: 표시 형식(소수점 2자리)
* **`mask=mask`**: `True`인 셀 **가림** → 상·하삼각 선택에 사용
* **`linewidths=.5`**: **셀 경계선 두께**
* **`cmap='RdYlBu_r'`**: 색상 맵(파열형). `_r`는 **반전**

  * 보통 상관행렬은 `vmin=-1, vmax=1, center=0`를 함께 주면 해석이 쉬움:

    ```python
    sns.heatmap(corr, vmin=-1, vmax=1, center=0, cmap='RdYlBu_r')
    ```

> 추가 팁
>
> ```python
> plt.figure(figsize=(10, 8))  # 그림 크기 키우기
> sns.heatmap(..., square=True)  # 셀을 정사각형으로
> ```

---

## 6) `sns.histplot(..., kde=True)` — KDE 곡선 함께 그리기

```python
sns.histplot(data=df, x='target_feature', kde=True)
```

* **히스토그램**: 데이터를 구간(bin)으로 나눠 **빈도**를 막대로 표시
* **KDE (커널 밀도 추정)**: 데이터를 **연속 분포 곡선**으로 **부드럽게** 추정
  → `kde=True`이면 히스토그램 위에 곡선이 함께 그려짐

### 자주 쓰는 옵션

```python
sns.histplot(
    data=df,
    x='xcol',
    bins=30,           # 구간 수 (or binwidth=, binrange=)
    stat='count',      # 'count' | 'frequency' | 'density' | 'probability'
    kde=True,          # KDE 곡선 표시
    element='bars',    # 'bars' | 'step' | 'poly'
)
```

* \*\*`stat='density'`\*\*로 바꾸면 **KDE와 스케일(축)이 맞아** 비교가 더 직관적

  ```python
  sns.histplot(df['xcol'], stat='density', kde=True)
  ```

> ⚠️ **주의**
>
> * **이산형/범주형** 데이터에 KDE를 켜면 의미가 약해짐
> * **0 이하 값**에 `log_scale`을 쓰면 오류(로그 불가)
> * 결측치가 많으면 빈 그래프처럼 보일 수 있으니 `dropna()` 혹은 `fillna()` 고려

---

## 7) 종합 예시 코드

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 예시 데이터
rng = np.random.default_rng(42)
df = pd.DataFrame({
    'A': rng.normal(0, 1, 300),
    'B': rng.normal(1, 2, 300),
    'C': rng.normal(-1, 1.5, 300),
    'cat': rng.integers(0, 3, 300).astype(str)  # 범주형
})

# 1) 상관행렬 (숫자형만)
corr = df.corr(numeric_only=True)

# 2) 상삼각 마스크 (대각선 제외)
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

# 3) 히트맵
plt.figure(figsize=(7, 6))
sns.heatmap(
    corr, annot=True, fmt='.2f',
    mask=mask, linewidths=.5,
    vmin=-1, vmax=1, center=0,
    cmap='RdYlBu_r', square=True
)
plt.title('Correlation (Lower Triangle Shown)')
plt.tight_layout()
plt.show()

# 4) 히스토그램 + KDE
plt.figure()
sns.histplot(df['A'], bins=30, stat='density', kde=True)
plt.title('Histogram with KDE (A)')
plt.tight_layout()
plt.show()

# 5) xticks 조회 & 라벨 회전
plt.figure()
ax = sns.countplot(x='cat', data=df)
locs, labels = plt.xticks()                # 현재 눈금/라벨 조회
ax.set_xticklabels(labels, rotation=45)    # 기존 라벨 유지 + 회전만 적용
plt.title('Count by Category')
plt.tight_layout()
plt.show()
```

---

## 8) 빠른 체크리스트

* `plt.xticks()`

  * **인자 없음**: 현재 **위치/라벨을 반환**
  * **인자 있음**: **위치/라벨을 설정**
* `ax.set_xticklabels([...])`

  * 라벨만 교체/회전 등 **스타일 수정** (위치 어긋나지 않게 **set\_xticks**와 병행 권장)
* `df.corr(numeric_only=True)`

  * **숫자형 열만** 사용하여 **피어슨 상관**(기본) 계산
* `mask = np.triu(np.ones_like(corr, dtype=bool), k=1)`

  * **대각선 위**만 `True` → heatmap에서 **가려짐** (하삼각만 표시)
* `sns.heatmap(..., annot=True, fmt='.2f', linewidths=.5, cmap='RdYlBu_r')`

  * 숫자 표기/표현 형식/경계선/컬러맵 설정
* `sns.histplot(..., kde=True, stat='density')`

  * 히스토그램 + KDE, 축 스케일 맞추려면 `stat='density'`

---

