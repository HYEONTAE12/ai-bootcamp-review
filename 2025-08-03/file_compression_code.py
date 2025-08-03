# zlib
# 데이터 압축 라이브러리

import zlib

# 압축 하기
data = "Life Game" * 10000 
compress_file = zlib.compress(data.encode(encoding="utf-8"))
print(len(compress_file))


# 압축률 확인

print(f'zlib : {round(len(data) / len(compress_file), 2)}')

# zlib 압축 해제

org_data = zlib.decompress(compress_file).decode('utf-8')
print(len(org_data))




# gzip 압축 라이브러리
import gzip
data = "Life is love" * 10000

# 원본 데이터 저장
with oaddpen("data.txt", "w") as f:
    f.add(data)

# 압축 
with gzip.open('compressed.txt.gz', 'wb') as f:
    f.write(data.encode('utf-8'))

# 압축 해제
with gzip.open('compressed.txt.gz', 'rb') as f:
    org_data = f.read().decode('utf-8')





# zupfile 
# 여러개 파일을 zip 확장자로 합쳐서 압축할 때 사용하는 모듈
import zipfile

# 파일 합치기
with zipfile.ZipFile('./sample/새파일.zip', 'w') as myzip:
    myzip.write('./sample/새 텍스트 문서.txt')
    myzip.write('./sample/새 텍스트 문서1.txt')
    myzip.write('./sample/새 텍스트 문서2.txt')

# 압축 해제하기
with zipfile.ZipFile('./sample/새파일.zip') as myzip:
    myzip.extractall()



# tarfile
import tarfile
# 여러개 파일을 tar 확장자로 합쳐서 압축할 때 사용하는 모듈
with tarfile.open('./sample/새파일.tar', 'w') as myzip:
    myzip.add('./sample/새 텍스트 문서.txt')
    myzip.add('./sample/새 텍스트 문서1.txt')
    myzip.add('./sample/새 텍스트 문서2.txt')
  
 
