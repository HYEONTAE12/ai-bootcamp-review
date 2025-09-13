from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import requests

url = "https://www.livesport.com/team/ac-milan/8Sa8HInO/"
html = requests.get(url).text
bs = BeautifulSoup(html, "html.parser")
bs1 = bs.find_all("span", {"class" :"wcl-simpleText_Asp-0 wcl-scores-simpleText-01_pV2Wk"})

driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get("https://www.livesport.com/team/ac-milan/8Sa8HInO/")
page = driver.page_source
bs_obj = BeautifulSoup(page, "html.parser")

win = bs_obj.find_all("span", {"class":"wcl-simpleText_Asp-0 wcl-scores-simpleText-01_pV2Wk"})
len(win)

for i in range(0, len(win)):
    print(win[i].text)

result = {"win":0,
          "draw":0,
          "lose":0}

keys = result.keys()
print(keys)

for i in range(0, len(win)):
    if win[i].text == "W":
        result["win"] += 1
    elif win[i].text == "D":
        result["draw"] += 1
    elif win[i].text == "L":
        result["lose"] += 1
    print(result)


import base64
from PIL import Image

string = "life  is too short"

bt = string.encode("ascii")

encoded = base64.b64encode(bt)

print(bt)

decoded = base64.decodebytes(encoded)

dstr = decoded.decode('ascii')
print(dstr)

path = "C:\\Users\\USER\\OneDrive\\Documents\\0005303739_001_20220828154501895.jpg"

img = Image.open(path)
img.show()


with open(path, 'rb') as img:
    image = img.read()
    print(image)


import textwrap
text = ""  # 주소
print(text)

print(textwrap.shorten(text, width=100))
print(textwrap.shorten(text, width=100, placeholder='...[중략]'))
print('\n'.join(textwrap.wrap(text, width=100)))



import re
import collections 
words = re.findall(r'\w', text)
print(collections.Counter(words))


import gensim

model = gensim.models.Word2Vec.load('ko/ko.bin')
model.wv_most


# 클로저와 데코레이터
import time

def elapsed(func):
    def wrapper(a, b):
        print("함수 시작")
        start = time.time()
        result = func(a, b)
        end = time.time()
        print("함수 끝 시간 %f" % (end - start))
        return result
    return wrapper
@elapsed
def func1(a, b):
    var = a + b
    return var

@elapsed
def func2(a, b):
    var = a * b
    return var

coconut = func2(20, 30)

print(coconut)
