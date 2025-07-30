import json
with open('./test01.json', 'r') as file:
    data = json.load(file)
print(data)  
#  [{'id': 1,
#   'name': 'Kim Crawl',
#   'age': 28,
#   'hobby': 'Painting',
#   'apply': ['Amazon', 'Microsoft']},
#  {'id': 2,
#   'name': 'Lee Pai',
#   'age': 34,
#   'hobby': 'Music',
#   'apply': ['Meta', 'X', 'Linkedin']}]

    
type(data)   # list

data[0]      # JSON 형식도 인덱싱 가능
data[1]["id"]# 특정 요소 꺼내오기


import pandas as pd   
df = pd.DataFrame(data)  #JSON 형식을 데이터프레임으로 만들기
print(df)


class country01:
  def __init__(self, name, capital, population):
    self.name = name
    self.capital = capital
    self.population = population

  def introduce(self):
    setence = '국가 소개 문장입니다'
    return sentence

c1 = country01("현태", "KOREA", "50,000,000")
c1.name
c1.capital
c1.population
c1.introduce()


# 인코딩, 디코딩

name = '안현태'
nm_encode = name.encode("etf8")      # name 을 인코딩
print(nm_encode)

nm_decode = nm_encode.decode("etf8") # nm_encode 를 디코딩
print(nm_decode)      


import hashlib
name = '안현태'
nm_encode = name.encode("etf8")    # name 을 인코딩

nm_hash = hashlib.sha256(nm_encode)# sha256으로 암호화
print(nm_hash)    

nm_hash_val = nm_hash.hexdigest()  # 16진수변환
print(nm_hash_val)          



from bs4 import BeautifulSoup
html_doc = """
<!doctype html>
<html>
    <head>
        <title> 반갑습니다. </title>
    </head>
    <body> 
        AI 부트캠프 화이팅 현태 할 수 있다.
    </body>
</html>
"""

bs_obj = BeautifulSoup(html_doc, "html.parser")   # 뷰티풀수프 객체를 생성/ 매개변수 1번 째- 분석(파싱)할 html 문자열을 삽입 /매개변수 2번 째 - 사용할 html 파서 종류
head = bs_obj.find("head")    # 제목을 가지고 와줘
print(head)

