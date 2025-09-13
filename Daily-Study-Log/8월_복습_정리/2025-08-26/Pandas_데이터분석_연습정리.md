
---

# 📊 Pandas 데이터 분석 정리

## 1. 문자열 필터링 (`str.contains`)

```python
dt[dt['title'].str.contains('love', case=False, na=False)]
```

* **case=False** : 대소문자 무시
* **na=False** : 결측치(NaN)는 False로 처리 → 오류 방지

---

## 2. 조건 필터링 (`query`)

```python
dt.query('release_year >= 2020 and type == "Movie"')
```

* **가독성**이 좋고, **조건 결합**에 편리함 (`&`, `|` 대신 `and`, `or` 사용 가능)

---

## 3. 범위 필터링 (`between`)

```python
dt[dt['release_year'].between(2015, 2020, inclusive='both')]
```

* `inclusive`: 경계값 포함 여부

  * `'both'` : 양쪽 다 포함
  * `'neither'` : 둘 다 제외
  * `'left'` : 왼쪽만 포함
  * `'right'` : 오른쪽만 포함

---

## 4. 행 개수 세기

* **len 사용**

```python
len(dt[dt['type'] == 'Movie'])
```

* **shape 사용**

```python
dt[dt['title'].str.contains('love', case=False, na=False)].shape[0]
```

* `.shape[0]` = 행 개수

---

## 5. 유형별 작품 수

```python
dt['type'].value_counts()
```

* 카테고리별 데이터 개수를 자동 집계

---

## 6. 국가별 작품 수 Top 10

```python
dt.groupby('country')['show_id'].count().sort_values(ascending=False).head(10)
```

> 🔹 오타 수정: `sort_valuse` → `sort_values`

---

## 7. 연도별 작품 수

```python
year_count = pd.DataFrame(dt.groupby('release_year')["show_id"].count()).reset_index()
year_count.columns = ['year', 'count']
```

* 오름차순 정렬

```python
year_count = year_count.sort_values('year')
```

* 작품 수 기준 정렬

```python
year_count = year_count.sort_values('count', ascending=False)
```

---

## 8. Rating별 작품 수

```python
valid_ratings = ['TV-MA','TV-14','TV-PG','R','PG-13',
                 'TV-Y7','TV-Y','PG','TV-G','NR',
                 'G','TV-Y7-FV','NC-17','UR']

dt = dt[dt['rating'].isin(valid_ratings)]
dt['rating'].value_counts()
```

* **`isin()`**: 특정 값들만 필터링

---

## 9. Duration 처리 (영화 vs TV Show)

```python
num = dt['duration'].str.extract(r'(\d+)')[0].astype('Int64')

dt['minutes'] = np.where(dt['type'].eq('Movie'), num, pd.NA)
dt['seasons'] = np.where(dt['type'].eq('TV Show'), num, pd.NA)
```

* **`.str.extract(r'(\d+)')`** : 문자열에서 숫자 추출
* **`.astype("Int64")`** : `pd.NA`와 호환되는 정수형
* **`np.where`** : 조건 기반 값 할당
* **`.eq('Movie')`** : `== 'Movie'`와 같지만 결측치 처리에 안정적

👉 대안 (pandas식):

```python
dt['minutes'] = num.where(dt['type'].eq('Movie'), other=pd.NA)
dt['seasons'] = num.where(dt['type'].eq('TV Show'), other=pd.NA)
```

---

## 10. 결측치 처리

```python
dt['director'].fillna('Unknown')   # 결측치 채우기
dt.dropna(subset=['director'], how='all', inplace=True)   # 결측치 행 삭제
```

---

## 11. 날짜 변환

```python
dt['date_added'] = pd.to_datetime(dt['date_added'], format='%B %d, %Y', errors='coerce')
```

* `%B`: 영어 월 이름 (예: January, February)
* `%d`: 일(day)
* `%Y`: 연도(4자리)
* **errors='coerce'** : 변환 불가 값 → NaT 처리

---

## 12. 시각화 (연도별 작품 수)

```python
release_year = pd.DataFrame(dt.groupby('release_year')['show_id'].count()).reset_index()
release_year.columns = ['year', 'count'] 

sns.lineplot(data=release_year, x='year', y='count')
```

---

## 13. 시각화 (Rating별 작품 수)

```python
rating = dt.groupby('rating')['show_id'].count().reset_index()
rating.columns = ['rating', 'count']

plt.figure(figsize=(10,6))
plt.rc('font', family='Malgun Gothic')

sns.barplot(data=rating, x='rating', y='count', color='red')
plt.title("rating별 작품 수", fontsize=16, fontweight='bold')
plt.xlabel("rating")
plt.ylabel("count")
plt.xticks(rotation=45)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()
```

---

## 14. 시각화 (국가별 작품 수 Top 10)

```python
countries = dt['country'].dropna().str.split(',').explode().str.strip()

top10 = countries.value_counts().head(10).reset_index()
top10.columns = ['country', 'count']

plt.figure(figsize=(10,6))
sns.barplot(data=top10, y='country', x='count', color='green')
plt.title("국가별 작품 수 Top 10", fontsize=16, fontweight='bold')
plt.xlabel("작품 수")
plt.ylabel("국가")
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
```

---

# ✅ 추가로 알면 좋은 내용

### 1) `groupby` + `agg`

* 여러 통계를 동시에 구할 수 있음

```python
dt.groupby('type').agg(
    작품수=('show_id', 'count'),
    평균_연도=('release_year', 'mean')
)
```

### 2) `value_counts(normalize=True)`

* 비율 확인 가능

```python
dt['type'].value_counts(normalize=True)
```

### 3) `nlargest / nsmallest`

* 빠르게 상위/하위 n개 뽑기

```python
dt['release_year'].value_counts().nlargest(5)
```

### 4) `crosstab`

* 교차분석 (예: type과 rating 관계)

```python
pd.crosstab(dt['type'], dt['rating'])
```

---

