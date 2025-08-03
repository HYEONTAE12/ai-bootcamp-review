## 📅 날짜 및 시간 관련 파이썬 코드 정리
# 1. dateutil.parser.parse — 문자열을 날짜로 변환
문자열을 datetime 객체로 파싱

fuzzy=True 옵션을 사용하면 날짜가 아닌 불필요한 문자를 무시하고 날짜만 파싱할 수 있음

AM, PM 형식도 인식 가능
from dateutil.parser import parse

date = '2025-08-03'
print(parse(date))

date1 = 'oct 25, 2025 4:5:32 Pm'
print(parse(date1))

date2 = 'INFO 2022-01-01T00:00:01 Happy new year, human.'
print(parse(date2, fuzzy=True))


# 2. time 모듈 — 시간 관련 함수들
# 🔸 time.time()
현재 시간(Unix timestamp)을 반환 (1970년 1월 1일부터 초 단위)

# 🔸 time.ctime()
사람이 읽을 수 있는 문자열 시간 반환

# 🔸 time.sleep(seconds)
특정 초 동안 프로그램 일시 정지 (대기)

# 🔸 경과 시간 측정 예시
import time

*print(time.time())*      # 유닉스 시간
*print(time.ctime())*     # 현재 시간 (가독성 있음)

*print(time.sleep(1))*    # 1초 대기

# 경과 시간 측정
*t = time.time()*

*for i in range(5):*
    *print(f"반복횟수{i}")*
    *time.sleep(1)*

*f = time.time()*
*print(f"경기시간은 {f - t}초 입니다.")*

3. 달력 생성기 — 윤년 계산 및 달력 출력

# 🔹 윤년 판별 함수
*def isleap(year):*
    *return year % 4 == 0 and year % 100 != 0 or year % 400 == 0*
    
# 🔹 각 달의 마지막 날짜 계산
*def lastday(year, month):*
    *m = [31,28,31,30,31,30,31,31,30,31,30,31]*
    *if isleap(year):*
        *m[1] = 29*
    *return m[month - 1]*
    
# 🔹 총 날짜 수 계산
*def totalday(year, month, day):*
    *total = (year - 1) * 365 + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400*
    *for i in range(1, month):*
        *total += lastday(year, i)*
    *return total + day*
    
# 🔹 요일 구하기
*def weekday(year, month, day):*
    *return totalday(year, month, day) % 7*
    
# 4. 달력 출력 실행 코드
*if __name__ == "__main__":*
    *year, month = map(int, input("년 월 을 입력해주세요. (예: 2025 9) 입력: ").split())*
    *print("=" * 28)*
    *print("       {0:4d}년  {1:2d}월 ".format(year, month))*
    *print("=" * 28)*
    *print("  일  월  화  수  목  금  토 ")*
    *print("=" * 28)*

    for i in range(weekday(year, month, 1)):
        print("    ", end="")

    for i in range(1, lastday(year, month)+1):
        print("  {0:2d}".format(i), end="")
        if weekday(year, month, i) == 6:
            print()

    print("\n" + "=" * 28)
## 🧠 오늘의 학습 요약
# 주제	내용
**📆 날짜 파싱**	dateutil.parser.parse로 문자열 날짜 변환 (fuzzy=True 포함)
**⏱ 시간 측정**	time.time, time.sleep, time.ctime
**🗓 달력 출력**	윤년 체크, 날짜 계산, 달력 출력 구현
