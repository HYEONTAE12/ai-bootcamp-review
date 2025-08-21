import os
import pathlib

# 현재 디렉토리 확인
print(os.getcwd())
print()
print(pathlib.Path.cwd())
print()

# 경로 존재 확인  r을 사용시 슬래시를 역슬래시로 사용 가능
dir_file = r"D:/practice.code/practice/"
print(os.path.exists(dir_file))
print()
print(pathlib.Path.exists(pathlib.Path(dir_file)))
print()


# 디렉토리 만들기
dir_file1 = r"D:\practice.code\practice\exercise_book\새폴더"
dir_file2 = pathlib.Path(r"D:\practice.code\practice\exercise_book\새폴더")

# os
if not os.path.exists(dir_file1):
    os.makedirs(dir_file1)
print()

#pathlib
dir_file2.mkdir(parents=True, exist_ok= True)
print()


## 전체 파일 리스트 확인
dir_file1 = r"D:/practice.code/practice/exercise_book/"
print(os.listdir(dir_file1))
print()

# os
# basename: 주어진 경로 문자열에서 파일명 또는 마지막 요소만 반환
print(os.path.basename(dir_file1))
print()

# pathlib
# PurePath: 
# 경로를 문자열로 처리하는 용도, 
# 실제 파일이 존재하는지 여부와 상관없이 경로의 구조만 다룬다.
# 파일 시스템과 연결되어 있지 않음
print(pathlib.PurePath(os.listdir(dir_file1)[0]).name)
print()


## 상위 경로 확인

# os
print(os.path.dirname(dir_file1))
print()

# pathlib
print(pathlib.PurePath(dir_file1).parent)
print()


## 경로 연결

# os
print(os.path.join(dir_file1, "os"))
print()

# pathlib
print(pathlib.PurePath(pathlib.PurePath(dir_file1).parent).joinpath("pathlib"))
print()


## 확장자 분리
file_path = os.path.basename(os.listdir(dir_file1)[0])
print()

# os
print(os.path.splitext(file_path))
print()

# pathlib
print(pathlib.PurePath(file_path).suffix)
print()
