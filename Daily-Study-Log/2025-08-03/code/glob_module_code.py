import glob
# glob
# 패턴을 이용하여 파일을 검색할 때 사용하는 모듈


# txt파일 찾기 현재 경로
for filename in glob.glob("*.txt"):
    print(filename)

# txt파일 찾기 하위 경로까지
for filename in glob.glob("**/*.txt"):
    print(filename)

#  txt파일 찾기 현재와 하위 경로 모두 포함
for filename in glob.glob("**/*.txt", recursive=True):
    print(filename)

# 글자수 4
for filename in glob.glob("????.*", recursive=True):
    print(filename)

# 글자수 10
for filename in glob.glob("??????????.*", recursive=True):
    print(filename)

## 문자열 포함 파일명 찾기
# 소문자 4글자가 들어간 파일 찾기 확장자 상관없음
for filename in glob.glob("**/[a-z][a-z][a-z][a-z]*", recursive=True):
    print(filename)
# 첫글자가 새파일 뒷 글자와 확장자는 상관없음    
for filename in glob.glob("**/새파일*.*", recursive=True):
    print(filename)
# 중간에 프로젝트가 포함되고 첫글자와 뒷글자 확장자는 상관없음
for filename in glob.glob("**/*프로젝트*.*", recursive=True):
    print(filename)


#fnmatch
# glob 모듈과 동일하게 특정한 패턴으로 파일을 찾는 모듈
# 파일명 매칭 여부를 bool 값으로 반환해, os.listdir() 함수와 사용하는 것이 특징
import fnmatch
import os

for filename in os.listdir('./sample'):
    if fnmatch.fnmatch(filename, '새??[0-9].txt'):
        print(filename)







 import shutil
# 기본 파일 복사
shutil.copy("./sample/새 텍스트 문저1.txt", "./sample/새파일1_복사본.txt")

# 파일 메타 복사: 고유한 속성 수정된 시간 같이 고유한 속성까지 복사
shutil.copy2("./sample/새 텍스트 문저1.txt", "./sample/새파일1_복사본.txt")

# 확장자 바꾸기
shutil.move("./sample/새파일1_복사본.txt", "./sample/새파일1_복사본.py")
shutil.move("./sample/새파일1_복사본.py", "./sample/새파일1_복사본.txt")

# 파일 이동하기
shutil.move("./sample/새파일1_복사본.txt", "새파일1_복사본.txt")

