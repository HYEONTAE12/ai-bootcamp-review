
---

# 📝 선형회귀(Linear Regression) 모델링 방법론 정리

## 1. 실습 개요

* 데이터셋: **당뇨병 진행도 예측 (Diabetes Dataset, sklearn 제공)**
* 목표: 10개의 입력 피처로부터 \*\*1년 후 당뇨병 진행도(target)\*\*를 예측하는 회귀 문제
* 샘플 수: 442개
* 피처: age, sex, bmi, bp, S1\~S6 (혈청 지표)

---

## 2. 데이터 준비와 전처리

```python
from sklearn.datasets import load_diabetes
diabetes = load_diabetes(scaled=False)

data = diabetes["data"]
data = pd.DataFrame(data, columns=diabetes["feature_names"])
```

### Feature 이름

* `diabetes["feature_names"]` → 입력 변수 이름 리스트
* `age, sex, bmi, bp, s1, s2, s3, s4, s5, s6`

### Target 값

* `diabetes["target"]` → 당뇨병 진행 정도 (숫자형 값)

---

## 3. 데이터 표준화 (Standardization)

```python
fts_mean = data.mean(axis=0)
fts_std = data.std(axis=0)
data = (data - fts_mean) / fts_std
```

* 평균을 빼고, 표준편차로 나누어 **평균=0, 표준편차=1**로 변환
* 이렇게 하면 피처 크기 차이를 줄여 학습 안정성↑

👉 왜 평균=0, 표준편차=1이 되는가?

* (x - μ)/σ 계산 → 데이터가 μ를 중심으로 퍼짐 정도가 σ가 됨
* 표준화하면 μ=0, σ=1로 맞춰짐

---

## 4. 학습 데이터 분리

```python
from sklearn.model_selection import train_test_split

train_data, test_data, train_target, test_target = train_test_split(
    data, target, test_size=0.3, random_state=1234
)
```

* 70% → 학습, 30% → 테스트

---

## 5. 선형회귀 모델 학습

### 1) 사이킷런 사용

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(train_data, train_target)
```

* `model.intercept_` → 절편(bias, b)
* `model.coef_` → 각 피처의 기울기(weight, w)

👉 **해석**

* 기울기: 입력값이 1단위 변할 때, target이 얼마나 변하는지
* 절편: 모든 입력이 0일 때의 target 값

---

### 2) 해석적 해법 (정규방정식)

$$
w = (X^TX)^{-1}X^Ty
$$

* `X`: 입력 데이터 행렬
* `y`: target 값
* `w`: 최적의 계수 벡터

👉 np.linalg.solve로 계산:

```python
w = np.linalg.solve(X.T @ X, X.T @ y)
```

---

## 6. 모델 평가

### 평균제곱오차 (MSE)

```python
from sklearn.metrics import mean_squared_error

pred = model.predict(test_data)
mse = mean_squared_error(test_target, pred)
```

* 실제 값과 예측값의 차이를 제곱해서 평균낸 값
* 낮을수록 모델 성능이 좋음

---

## 7. 시각화

### 예측 vs 실제값

```python
plt.scatter(test_target, pred)
plt.xlabel("True Target")
plt.ylabel("Predicted Target")
plt.plot([-2.5, 2.5], [-2.5, 2.5], "r--")
```

* 점: 실제 vs 예측
* 빨간 선: 완벽히 맞을 경우 (y=x)

👉 점들이 빨간 선에 가까울수록 모델 성능이 좋음

---

## 8. 핵심 개념 정리

* **Intercept(b)**: 모든 입력이 0일 때 예측값 (바이어스)
* **Coefficient(w)**: 입력값 변화가 출력에 미치는 영향 (기울기)
* **표준화**: 모든 피처를 평균 0, 표준편차 1로 변환
* **정규방정식**: 선형회귀의 해석적 해법
* **np.linalg.solve(A, b)**: $Ax = b$ 형태의 선형방정식 풀기
* **@ 연산자**: 행렬 곱 (dot product)
* **max\_iter**: 반복 최적화 알고리즘에서 최대 반복 횟수

---

