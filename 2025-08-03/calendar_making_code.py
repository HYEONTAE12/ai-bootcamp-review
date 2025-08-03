def isleap(year):
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

def lastday(year, month):
    m = [31,28,31,30,31,30,31,31,30,31,30,31]

    if isleap(year):
        m[1] = 29

    return m[month - 1]

def totalday(year, month, day):
    total = (year - 1) * 365 + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400
    
    for i in range(1, month):
        total += lastday(year, i) 

    return total + day


def weekday(year, month, day):
    return totalday(year, month, day) % 7

if  __name__ == "__main__":
    year, month = map(int, input("년 월 을 입력해주세요. (예: 2025 9) 입력: ").split())
    print("=" * 28)
    print("       {0:4d}년  {1:2d}월 ".format(year, month))
    print("=" * 28)
    print("  일  월  화  수  목  금  토 ")
    print("=" * 28)
    for i in range(weekday(year, month, 1)):
        print("    ", end="")
    for i in range(1, lastday(year, month)+1):
        print("  {0:2d}".format(i), end="")

        if weekday(year, month, i) == 6:
            print()
    print("\n" + "=" * 28)


