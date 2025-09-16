

---

# 🐍 Python 코드 규칙 (PEP-8) 핵심 키워드 정리

## 📑 Import 규칙

* **순서**

  1. **Built-in 라이브러리** (표준 모듈: `os`, `sys`, `math` 등)
  2. **외부 라이브러리** (pip로 설치한 모듈: `numpy`, `pandas`, `dotenv` 등)
  3. **커스텀 패키지** (내가 만든 모듈: `from src.utils import utils`)

* **그룹 간 줄바꿈** → 각 그룹 사이에 한 줄 띄우기

* **별칭(alias) 사용** → 관례적으로 사용하는 축약 사용 (`import numpy as np`, `import pandas as pd`)

---

## 📝 코드 스타일 기본 원칙

* **들여쓰기**: 스페이스 4칸 사용
* **줄 길이**: 최대 79자 권장
* **함수/클래스 이름**

  * 함수, 변수: `snake_case` (예: `get_user_info`)
  * 클래스: `PascalCase` (예: `UserProfile`)
* **상수**: `UPPER_CASE` (예: `MAX_RETRY = 3`)
* **주석**

  * 한 줄 주석: `# 설명`
  * 여러 줄 주석은 `""" Docstring """` 활용

---

## ✅ Import 예시

```python
# 1. Built-in
import os
import sys
import math

# 2. 외부 라이브러리
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# 3. 커스텀 패키지
from src.utils import utils
```

---


