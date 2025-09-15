

---

# 환경 관리툴 정리

## 정의

* **환경 관리툴**은 프로젝트마다 다른 **파이썬/라이브러리/시스템 의존성**을 분리·관리해 주는 도구다.
* 목적은 **충돌 방지, 재현성 보장, 배포 용이성**이다. “어제 되던 코드가 오늘 안 되는” 상황을 줄인다.

## 주요 기능

* **환경 격리:** 프로젝트별로 독립 가상환경을 만들어 라이브러리 버전 충돌을 막는다.
* **종속성 관리:** 필요한 패키지 목록과 정확한 버전을 잠근다(락 파일/환경 파일).
* **환경 재현성:** 다른 PC/서버에서도 동일한 환경을 **파일 한 장**으로 똑같이 만든다.
* **버전 호환성:** 파이썬/패키지/하위 C라이브러리(예: CUDA, MKL)까지 버전 호환을 맞춘다.

## 종류

* **conda**: 파이썬뿐 아니라 R, C/포트란 기반 라이브러리까지 다루는 **범용 패키지+환경 관리자**.
* **virtualenv / venv**: 파이썬 표준/경량 가상환경. 패키지 설치는 **pip**로 수행.
* **pipenv**: `Pipfile`/`Pipfile.lock`으로 **의존성 잠금 + 가상환경**을 한 번에.
* **container 기술(Docker 등)**: 애플리케이션+런타임+OS라이브러리까지 **컨테이너 이미지**로 묶어 재현성을 극대화.

---

# Conda란?

## 정의

* **언어/플랫폼 독립적**인 패키지·환경 관리자. `conda`는 가상환경 생성과 바이너리 패키지 설치를 함께 처리한다.
* `conda-forge`, `defaults` 같은 **채널**에서 미리 빌드된 패키지를 받아온다(컴파일 스트레스 ↓).

## 주요 특징

* **언어 독립적:** Python, R, Julia 등 다양한 언어 패키지를 다룬다.
* **크로스 플랫폼:** Windows / macOS / Linux 모두 동일한 UX.
* **환경 관리:** `conda create / activate / env export`로 생성·전환·내보내기.
* **다양한 패키지:** CUDA, MKL, GDAL 같은 **C 기반 의존성**도 손쉽게 설치.

## 활용

* **패키지 설치:**

  ```bash
  conda install numpy pandas
  # or 채널 지정
  conda install -c conda-forge xgboost
  ```
* **환경 관리:**

  ```bash
  conda create -n myenv python=3.11
  conda activate myenv
  conda remove -n myenv --all
  ```
* **버전 관리(환경 파일):**

  ```bash
  conda env export > environment.yml
  conda env create -f environment.yml
  ```

  > 팁: 팀 협업 시 **conda-forge 단일 채널**을 권장. 환경 파일 맨 위에 `channels:`로 명시해 두면 재현성이 좋아진다.

## 장점

* **패키지 호환성:** 미리 빌드된 바이너리라 복잡한 컴파일 없이 설치 성공률이 높다.
* **재현성:** `environment.yml` 하나로 서버/동료 PC에 동일 환경 복제.
* **효율성:** 하나의 명령으로 환경+패키지 동시 관리(파이썬 외 의존성까지).

---

# Virtualenv란?

## 정의

* 파이썬만 대상으로 하는 **경량 가상환경**. Python 3 표준 모듈은 `venv`, 별도 패키지는 `virtualenv`.
* 패키지 설치는 **pip**로 한다.

## 주요 특징

* **환경 격리:** 프로젝트별 site-packages 분리.
* **간편한 사용:** 표준 `venv`는 추가 설치 불필요.
* **패키지 관리:** `pip`, `requirements.txt`와 궁합이 좋다.

**예시**

```bash
# venv 생성/활성화
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 패키지 동결/복원
pip freeze > requirements.txt
pip install -r requirements.txt
```

---

# Pipenv 란?

## 정의

* **의존성 해석기 + 가상환경**을 통합한 툴. `Pipfile`과 `Pipfile.lock`으로 버전 잠금.

## 주요 특징

* **종속성 관리:** 충돌 없는 버전 조합을 자동 탐색해 `Pipfile.lock`에 고정.
* **가상환경 통합:** 프로젝트 폴더 기준 자동 가상환경(경로를 신경 쓸 일이 적다).
* **보안 강화:** `pipenv check`로 알려진 취약 패키지 점검.

**예시**

```bash
pipenv install requests
pipenv run python app.py
pipenv lock
pipenv check
```

---

# 컨테이너(Docker 등)와의 관계 한 줄 정리

* **가상환경(Conda/venv/pipenv)**: “**파이썬 레벨**”에서 격리. 가볍고 빠름.
* **컨테이너(Docker)**: OS 라이브러리까지 포함한 “**시스템 레벨**” 격리. 재현성 최강, 배포 친화.

---

# Conda 사용 명령 모음 (요청하신 라인 보강)

> 아래는 오타 수정 포함: `enviroment_my.yml`/`envirment_my.yml` → **`environment_my.yml`** (정식 철자)

## 가상환경 만들기

```bash
conda create --name hyoentae python=3.11
```

* Python 버전을 함께 명시하면 **의존성 충돌**을 크게 줄인다.

## 가상환경 입장

```bash
conda activate hyoentae
```

## 가상환경 나가기

```bash
conda deactivate
```

## 패키지 리스트를 `environment_my.yml`에 저장

```bash
conda env export > environment_my.yml
```

* 팀 공유용으로는 **채널·핵심 패키지 위주**만 남기는 걸 권장.
  (필요 시 `--from-history` 옵션으로 **직접 설치한 패키지**만 내보낼 수 있음)

  ```bash
  conda env export --from-history > environment_my.yml
  ```

## 파일 보기

```bash
cat environment_my.yml
```

> 오타 주의: `envir**o**nment_my.yml`

## 가상환경 생성과 동시에 패키지 설치

```bash
# 환경 파일의 name을 그대로 쓰려면:
conda env create -f environment_my.yml

# 다른 이름으로 만들고 싶다면:
conda env create --name new -f environment_my.yml
```

* `environment_my.yml` 안에 `name:`이 이미 있을 수 있다.
  `--name new`로 **덮어쓰기 이름**을 지정하거나, 파일의 `name:`을 수정해 충돌을 피한다.

---

## `environment.yml` 예시(추천 레이아웃)

```yaml
name: hyoentae
channels:
  - conda-forge
dependencies:
  - python=3.11
  - numpy=2.1.*
  - pandas=2.2.*
  - scikit-learn=1.5.*
  - pip
  - pip:
      - lightgbm==4.5.0
      - shap==0.46.0
```

* **규칙**: conda 패키지 먼저, `pip:`는 마지막에. (충돌 ↓)
* GPU 사용 시 `cudatoolkit` 등도 conda에서 정합성 있게 잡는 게 편하다.

---

## 언제 무엇을 쓰면 좋은가? (짧은 판단표)

| 상황                                      | 추천                         |
| --------------------------------------- | -------------------------- |
| 데이터/AI 패키지, CUDA/MKL 등 **복잡한 네이티브 의존성** | **Conda**                  |
| 순수 파이썬 앱, 간단/경량, 표준만 쓰고 싶음              | **venv(virtualenv) + pip** |
| 의존성 락과 가상환경을 한툴로, 앱 중심                  | **Pipenv**                 |
| 배포/운영, 팀 단위 완전 재현성, OS 레벨 격리            | **Docker(컨테이너)**           |

---

## 실전 팁

* **단일 채널 전략**: 팀 전체가 `conda-forge`를 쓰면 충돌과 “버전 지옥”이 줄어든다.
* **mamba** 사용: conda의 느린 의존성 해석을 빠르게 하고 싶으면 `mamba` 설치 후 같은 명령으로 사용.

  ```bash
  conda install -n base -c conda-forge mamba
  mamba env create -f environment.yml
  ```
* **혼합 설치 최소화**: 가능하면 한 환경에서 **conda 또는 pip 중 하나를 우선**. 불가피하면 conda → pip 순서.
* **프로젝트마다 가상환경 1개**: 재현성과 충돌 방지의 최솟값.

---

