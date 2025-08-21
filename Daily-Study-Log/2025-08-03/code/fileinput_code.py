import fileinput
import glob
import os

# fileinput
# 텍스트 파일을 읽고, 쓰고, 저장하는 기능을 더욱 편리하게 사용할 수 있게 하는 라이브러리
# 여러개의 파일을 읽어서 수정할 수 있음.
# "inplace editing" 기능 사용하면 open, close 보다 더 수정이 간편하고 직관적이다

# 파일 여러개 동시에 읽기
path = "sample/"
txt_files = glob.glob(os.path.join(path, "*.txt"))
print(f"[파일 목록] {txt_files}")

with fileinput.input(files=txt_files, encoding="utf-8") as f:
    for line in f:         
        print(f"{fileinput.filename()}: {line}", end="")  # 파일명도 함께 출력


# inplace editing

txt_files1 = glob.glob(os.path.join(path, "*.txt"))
print(f"[파일 목록] {txt_files1}")

with fileinput.input(txt_files1, inplace= True, encoding="utf-8") as f:
    for line in f:
        if f.isfirstline():
            print('1번째 줄입니다.', end="\n")
        else:
            print(line, end="")

# 검색된 줄 수정
with fileinput.input(txt_files1, inplace= True, encoding="utf-8") as f:
    for line in f:
        if line == "1번째 줄입니다.\n":
            print('첫 번째 줄입니다.', end='\n')
        else:
            print(line, end='')

# 키워드 포함 라인 수정
with fileinput.input(txt_files1, inplace= True, encoding="utf-8") as f:
    for line in f:
        if "10번째" in line:
            print('열 번째 줄입니다.', end='\n')
        else:
            print(line, end='')

# 텍스트 치환
with fileinput.input(txt_files1, inplace= True, encoding="utf-8") as f:
    for line in f:
        if "10번째" in line:
            print(line.replace('열 번째', "10번 째"), end='\n')
        else:
            print(line, end='')
