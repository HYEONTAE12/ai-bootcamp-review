
---

# 📌 `watch_log` 코드 리뷰

## 1. 클래스 초기화

```python
def __init__(self, df, scaler=None, label_encoder=None):
    self.df = df
    self.features = None
    self.labels = None
    self.scaler = scaler
    self.label_encoder = label_encoder
    self.contents_id_map = None
    self._preprocessing()
```

* `WatchLogDataset`을 호출하면서 데이터를 전달하면, 해당 데이터가 생성자에 들어가서 내부 변수가 초기화됨.
* `scaler`, `label_encoder`를 **기본값 None**으로 둔 이유는:

  * 새로운 데이터셋 → 새롭게 학습(fit)
  * 기존 데이터셋 → 이미 학습된 전처리기를 그대로 재사용
* `features`, `labels`, `contents_id_map`은 이후 전처리 과정에서 채워질 변수.
* `_preprocessing()`을 바로 호출하여 생성 시 자동으로 전처리가 실행됨.

---

## 2. 전처리 과정

```python
def _preprocessing(self):
    if self.label_encoder:
        self.df["content_id"] = self.label_encoder.transform(self.df["content_id"])
    else:
        self.label_encoder = LabelEncoder()
        self.df["content_id"] = self.label_encoder.fit_transform(self.df["content_id"])
```

* `label_encoder`가 주어진 경우 → 기존 매핑대로 `content_id`를 정수로 변환.
* 없는 경우 → `LabelEncoder()`를 새로 생성해 `fit_transform`으로 학습 + 변환을 동시에 수행.
* 결과적으로 `self.df["content_id"]`는 정수형 라벨이 됨.

---

```python
self.contents_id_map = dict(enumerate(self.label_encoder.classes_))
```

* **역매핑**을 위한 딕셔너리 생성.
* `label_encoder.classes_`: `fit()` 시 학습한 고유 클래스들의 리스트.
* `enumerate`로 각 클래스에 번호를 붙여 `{정수: 원래 content_id}` 형태로 저장.
* 예측 결과(정수)를 원래 ID 문자열로 되돌릴 때 사용.

---

```python
target_columns = ["rating", "popularity", "watch_seconds"]
self.labels = self.df["content_id"].values
features = self.df[target_columns].values
```

* `target_columns`: 학습에 사용할 feature 컬럼들.
* `self.labels`: `content_id` 정수 라벨.
* `features`: 지정한 feature 컬럼들의 값만 추출.

---

```python
if self.scaler:
    self.features = self.scaler.transform(features)
else:
    self.scaler = StandardScaler()
    self.features = self.scaler.fit_transform(features)
```

* `scaler`가 있으면 학습 없이 **transform**만 수행.
* `scaler`가 없으면 `StandardScaler()`를 새로 생성해 `fit_transform`으로 학습 + 변환.
* 학습된 `scaler`는 저장돼 이후 val/test에도 동일하게 적용.

---

## 3. 유틸리티 메서드

```python
def decode_content_id(self, encoded_id):
    return self.contents_id_map[encoded_id]
```

* 모델 예측값(정수)을 원래 콘텐츠 ID 문자열로 복원.

---

```python
@property
def features_dim(self): 
    return self.features.shape[1]

@property
def num_classes(self): 
    return len(self.label_encoder.classes_)
```

* 모델 생성 시 편의를 위해 제공.
* `features_dim`: 입력 feature 개수
* `num_classes`: 분류 클래스 수

---

```python
def __len__(self): 
    return len(self.labels)

def __getitem__(self, idx): 
    return self.features[idx], self.labels[idx]
```

* `len(dataset)` → 샘플 개수 반환.
* `dataset[i]` → (feature, label) 쌍 반환.
* 파이썬 기본 컨벤션을 따르며, 데이터셋 객체를 iterable하게 사용할 수 있음.

---

## 4. 데이터셋 준비 함수

```python
def read_dataset():
    watch_log_path = os.path.join(project_path(), "dataset", "watch_log.csv")
    return pd.read_csv(watch_log_path)
```

* `watch_log.csv` 파일을 읽어 데이터프레임으로 반환.
* `project_path()`를 통해 상위 디렉토리 경로를 가져와 안전하게 경로 구성.

---

```python
def split_dataset(df):
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df, test_df = train_test_split(train_df, test_size=0.2, random_state=42)
    return train_df, val_df, test_df
```

* 데이터셋을 **train\:val\:test = 6:2:2** 비율로 나눔.
* `random_state` 고정으로 재현성 보장.

---

```python
def get_datasets(scaler=None, label_encoder=None):
    df = read_dataset()
    train_df, val_df, test_df = split_dataset(df)

    train_dataset = WatchLogDataset(train_df, scaler, label_encoder)
    val_dataset = WatchLogDataset(val_df,
                                  scaler=train_dataset.scaler,
                                  label_encoder=train_dataset.label_encoder)
    test_dataset = WatchLogDataset(test_df,
                                   scaler=train_dataset.scaler,
                                   label_encoder=train_dataset.label_encoder)
    return train_dataset, val_dataset, test_dataset
```

* 최종 데이터셋 생성 함수.
* `train_dataset`에서 학습한 `scaler`, `label_encoder`를 그대로 val/test에 전달해 **데이터 누수 방지**.
* 결과: `(train_dataset, val_dataset, test_dataset)` 튜플 반환.

---

# ✅ 요약

* **`WatchLogDataset` 클래스**는 입력 데이터프레임을 받아 **라벨 인코딩, 스케일링, feature/label 분리**까지 자동 수행.
* **`get_datasets` 함수**는 CSV를 읽어 train/val/test로 나누고, 동일 전처리기를 적용해 데이터 누수를 막음.
* 모델 학습/평가 단계에서 바로 쓸 수 있는 형태로 데이터셋을 준비해 주는 구조.

---

