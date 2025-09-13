
# 문자열을 데이트타입 객체로 쉽게 반환 시키고 정규화가 되지않은 날짜 형식도 fuzzy= True 입력시 
# 날짜형식으로 변환
# AM, PM도 사용가능
from dateutil.parser import parse

date = '2025-08-03'

print(parse(date))
print()
date1 = 'oct 25, 2025 4:5:32 Pm'

print(parse(date1))


print()

date2 = 'INFO 2022-01-01T00:00:01 Happy new year, human.'

print(parse(date2, fuzzy=True))
print()

# 시간 확인 라이브러리 대부분 프로그램이 진행하는데 걸리는 시간을 확일할 때 많이 사용
import time
# time.time() - 컴퓨터가 알 수 있는 시간으로 반환
print(time.time())
print()
# time.ctime() - 현재 우리가 알고 있는 시간으로 반환
print(time.ctime())
print()
# 대기 시간 생성 
print(time.sleep(1))
print()

# 경과 시간 출력
t = time.time()
for i in range(5):
    print(f"반복횟수{i}")
    time.sleep(1)

f = time.time()
print(f"경기시간은 {f - t}초 입니다. ")


    
