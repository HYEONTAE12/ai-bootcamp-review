
---

# 📚 오늘 정리한 라이브러리 & 코드

## 1. **Pandas (`pd`)**

데이터 분석의 핵심 도구. CSV 불러오기, 가공, 집계, 시각화 보조에 자주 쓰임.

### 주요 기능

```python
pd.date_range('2025-08-27', periods=4, freq='10S')  
# 2025-08-27부터 시작해 10초 간격으로 4개의 시계열 생성

df.resample('5S').mean()  
# 시계열 데이터를 5초 단위로 리샘플링해 평균 계산

df.interpolate()  
# 결측값을 선형 보간으로 채움

pd.concat([df_target,
           pd.DataFrame([{'bysm' : 'total'}])],
          ignore_index=True)
# 행을 합쳐서 새로운 DataFrame 생성

groupby('a', as_index=False)['b'].sum()
# 그룹화 후 합계 집계
```

👉 **언제 쓰면 좋나?**

* 시계열 데이터 분석
* 결측값 처리
* 여러 DataFrame을 합칠 때
* 고객/상품/경기별 집계

---

## 2. **NumPy (`np`)**

수치 연산, 배열 처리에 최적화된 라이브러리.

### 사용 예

```python
mask = np.triu(np.ones_like(df_clean.corr(), dtype=bool))
# 상삼각행렬 mask 생성 (히트맵 대칭 부분 제거용)
```

👉 **언제 쓰면 좋나?**

* 행렬/벡터 연산
* 마스크(mask) 만들어서 조건 필터링할 때
* 수치 시뮬레이션

---

## 3. **Matplotlib (`plt`)**

기본 시각화 라이브러리. 세밀한 제어 가능.

### 사용 예

```python
%matplotlib inline     # 주피터 노트북에서 그래프 바로 보이게
plt.figure(figsize=(16, 12))  
plt.show()             # 그래프 출력
```

👉 **언제 쓰면 좋나?**

* 그래프 크기, 축, 레이블, 제목 등 세밀한 제어가 필요할 때

---

## 4. **Seaborn (`sns`)**

Matplotlib 기반의 고급 시각화 라이브러리. 코드 간결.

### 사용 예

```python
sns.set_style('darkgrid')  

sns.heatmap(df_clean.drop('blueWins', axis=1).corr(),
            cmap='YlGnBu', annot=True, fmt='.2f', vmin=0, mask=mask)

g = sns.pairplot(data=df_clean,
                 vars=['blueKills','blueWardsPlaced','blueAssists','blueTotalGold'],
                 hue='blueWins', size=3, palette='Set1')
g.map_diag(plt.hist)          # 대각선 → 히스토그램
g.map_offdiag(plt.scatter)    # 비대각선 → 산점도
g.add_legend()                # 범례 추가
```

👉 **언제 쓰면 좋나?**

* 상관관계 시각화
* 그룹별 분포 비교
* 탐색적 데이터 분석(EDA)

---

## 5. **imblearn (imbalanced-learn)**

불균형 데이터 처리용 라이브러리.

### 사용 예

```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)
```

👉 **언제 쓰면 좋나?**

* 타겟 데이터 불균형일 때 (예: 승률 데이터 90:10 → 50:50 맞추기)

---

## 6. **Scikit-Learn (`sklearn`)**

머신러닝의 대표 라이브러리. 데이터 전처리, 분할, 모델링, 평가까지 가능.

### (1) 데이터 전처리

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(X)            # 최소값, 최대값 학습
X_scaled = scaler.transform(X)  # 0~1 범위로 정규화
```

👉 **언제 쓰면 좋나?**

* 변수 스케일 차이가 클 때 (킬 수=10, 골드=20000)

---

### (2) 데이터 분할

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
```

👉 **언제 쓰면 좋나?**

* 학습용/테스트용 데이터 분리해서 과적합 방지할 때

---

### (3) 모델링

```python
from sklearn.naive_bayes import GaussianNB
clf_nb = GaussianNB()
clf_nb.fit(X_train, y_train)          # 모델 학습
pred_nb = clf_nb.predict(X_test)      # 예측
```

* **GaussianNB**: 조건부 확률 기반 분류 (단순, 빠름)

```python
from sklearn import tree
from sklearn.model_selection import GridSearchCV

dt = tree.DecisionTreeClassifier()
grid = {'min_samples_split': [5,10,20,50,100]}
clf_tree = GridSearchCV(dt, grid, cv=5)
clf_tree.fit(X_train, y_train)
pred_tree = clf_tree.predict(X_test)
```

* **DecisionTreeClassifier**: 규칙 기반 분류, 해석 용이
* **GridSearchCV**: 하이퍼파라미터 자동 탐색

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier()
grid = {'n_estimators': [100,200,300,400,500],
        'max_depth': [2,5,10]}
clf_rf = GridSearchCV(rf, grid, cv=5)
clf_rf.fit(X_train, y_train)
pred_rf = clf_rf.predict(X_test)
```

* **RandomForestClassifier**: 앙상블(트리 여러 개) → 정확도↑, 과적합↓

---

### (4) 성능 평가

```python
from sklearn.metrics import accuracy_score

acc = accuracy_score(y_test, pred_rf)
print(acc)
```
**accuracy_score**: 정확도 평가

**다른 지표**: confusion_matrix, classification_report, roc_auc_score

👉 **언제 쓰면 좋나?**

* 모델 성능 비교 및 최적 모델 선택

## ✅ 오늘 배운 흐름

* Pandas/NumPy → 데이터 준비, 집계, 결측 처리

* Matplotlib/Seaborn → 분포·승률·상관관계 시각화

* SMOTE → 불균형 데이터 보정

* Scikit-Learn → 스케일링 → 데이터 분할 → 다양한 모델 학습 → 성능 비교
