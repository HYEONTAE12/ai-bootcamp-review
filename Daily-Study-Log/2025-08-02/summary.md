## 📌 정규 표현식 (Regular Expressions)

# ✅ 1. 패턴 예시
r'(\w)(\w+)(\w)\s(010)-(\d{4})-(\d{4})'

**설명**:

(\w) : 알파벳, 숫자, 밑줄 중 하나 → 이름의 첫 글자 (예: '김')

(\w+) : 알파벳, 숫자, 밑줄 중 1개 이상 → 이름의 가운데 (예: '현')

(\w) : 알파벳, 숫자, 밑줄 중 하나 → 이름의 끝 글자 (예: '태')

\s : 공백 문자 (space)

(010) : 문자열 '010' (휴대폰 앞자리)

- : 하이픈

(\d{4}) : 숫자 4자리 (중간 번호)

- : 하이픈

(\d{4}) : 숫자 4자리 (끝 번호)


# 📌 결론:
이름(3글자) + 공백 + 전화번호(010-xxxx-xxxx) 형식을 탐지하는 정규식

| 메타문자    | 의미                 | 예시                           |     |              |
| ------- | ------------------ | ---------------------------- | --- | ------------ |
| `.`     | 임의의 문자 1개 (줄바꿈 제외) | `a.b` → a와 b 사이 아무 문자 1개     |     |              |
| `^`     | 문자열의 시작            | `^a` → a로 시작                 |     |              |
| `$`     | 문자열의 끝             | `b$` → b로 끝                  |     |              |
| `*`     | 앞 문자가 0개 이상 반복     | `ab*` → a, ab, abb, abbb     |     |              |
| `+`     | 앞 문자가 1개 이상 반복     | `ab+` → ab, abb, abbb (a는 X) |     |              |
| `?`     | 앞 문자가 0개 또는 1개     | `ab?` → a, ab                |     |              |
| `{n}`   | 앞 문자가 n개           | `a{3}` → aaa                 |     |              |
| `{n,}`  | 앞 문자가 n개 이상        | `a{2,}` → aa, aaa, ...       |     |              |
| `{n,m}` | 앞 문자가 n\~m개        | `a{2,4}` → aa, aaa, aaaa     |     |              |
| `[]`    | 문자 집합              | `[abc]` → a, b, c 중 하나       |     |              |
| `[^]`   | not, 괄호 안 문자가 아닌 것 | `[^a]` → a 제외 문자             |     |              |
| '       | '                 |   or 또는                    |  |
| `()`    | 그룹핑 / 캡처           | `(abc)+` → abc, abcabc       |     |              |
| `\`     | 이스케이프 문자           | `\.` → 마침표, `\\` → 역슬래시      |     |              |


# 📌 datetime 모듈
**✅ 날짜형 데이터 다루기**

from datetime import datetime, timedelta
datetime.date(2020, 9, 29) : 날짜 객체 생성

datetime.today() 또는 datetime.now() : 현재 시간 반환

.weekday() : 요일을 숫자로 반환

월:0 ~ 일:6

**✅ 날짜 계산 (timedelta)**
from datetime import timedelta
datetime.today() + timedelta(days=3)  # 3일 뒤

**✅ 날짜 속성 접근**
*.year : 연도*

*.month : 월*

*.day : 일*

*.hour : 시*

*.minute : 분*

*.second : 초*

**✅ 문자열 ↔ 날짜 변환**
strptime() : 문자열 → 날짜 객체로 변환

datetime.strptime("2025-08-02", "%Y-%m-%d")
strftime() : 날짜 객체 → 문자열로 변환

datetime.now().strftime("%Y/%m/%d %H:%M:%S")

# 📌 형식 코드

포맷	의미
*%Y	4자리 연도*
*%m	2자리 월*
*%d	2자리 일*
*%H	시(hour)*
*%M	분(minute)*
*%S	초(second)*

# 📌 calendar 모듈
**✅ 윤년 관련**

import calendar
calendar.isleap(2024)        # True
calendar.leapdays(2000, 2025)  # 2000~2024 사이 윤년 개수

**✅ 요일 계산**
calendar.weekday(2025, 8, 2)  # 해당 날짜의 요일 반환

**✅ 달력 출력**
print(calendar.calendar(2025))
print(calendar.month(2025, 8))  # 2025년 8월

**✅ 요약**
정규표현식은 문자열 패턴을 탐색하거나 변환하는 강력한 도구
datetime, calendar 모듈은 날짜와 시간 관련 작업에 필수

