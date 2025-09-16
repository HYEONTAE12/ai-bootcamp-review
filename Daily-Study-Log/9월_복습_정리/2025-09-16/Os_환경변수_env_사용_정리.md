

---

# 🔑 환경변수 관리 (.env & dotenv) 핵심 키워드 정리

## 📂 구조

* **.env 파일** → 민감한 정보(API Key, 비밀번호, DB 주소 등) 저장
* **dotenv 라이브러리** → 파이썬에서 `.env` 파일 불러오기
* **os.getenv()** → 환경변수 값 가져오기

---

## 🛡️ 왜 필요한가?

* 코드에 **직접 비밀번호/API Key**를 쓰면 보안 위험
* `.env`를 사용하면 **환경별 설정 관리 가능** (개발/테스트/운영)
* `.gitignore`에 `.env` 추가 → 깃허브에 올리지 않도록 필수 설정

---

## 📝 .env 파일 예시

```
API_KEY=my_secret_api_key
DB_URL=mysql://user:password@localhost:3306/mydb
```

---

## 🐍 Python에서 불러오기

```python
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경변수 사용
api_key = os.getenv("API_KEY")
db_url = os.getenv("DB_URL")

print(api_key)  # my_secret_api_key
```

---

## ⚠️ 주의할 점

* `.env`는 **절대 깃허브에 올리지 말 것**
* 팀 프로젝트 시에는 `.env.example` 파일을 만들어 **형식만 공유**

  ```env
  API_KEY=your_api_key_here
  DB_URL=your_db_url_here
  ```

---

