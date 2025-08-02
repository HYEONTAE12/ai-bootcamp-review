from bs4 import BeautifulSoup
import requests
import sys
import io
import re
import pandas as pd
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
class Finance():
    def url_code(self, code): 
        url = f"https://finance.naver.com/item/main.naver?code={code}"
        res = requests.get(url)
        print(res)
        r = res.text
        return r
    
    def company_name(self, code):
        result = []
        for i in code:
            html = self.url_code(i)
            bs_obj = BeautifulSoup(html, "html.parser")
            name_data = bs_obj.find("div" ,{'class':"wrap_company"})
            result.append(name_data.h2.a.text)
        return result
    
    def company_place(self, code):
        result = []
        for i in code:
            html = self.url_code(i)
            bs_obj = BeautifulSoup(html, "html.parser")
            place_data = bs_obj.find("div" ,{'class':"today"})
            place_data1 = place_data.find("em")
            result.append(place_data1.span.text)
        return result

    def company_volume(self, code):
        result = []
        for i in code:
            html = self.url_code(i)
            bs_obj = BeautifulSoup(html, "html.parser")
            volume_data = bs_obj.find("table" ,{'class':"no_info"})
            volume_data1 = volume_data.find_all("td")
            result.append(volume_data1[2].find("span",{'class':"blind"}).text)
        return result
    
    def company_total_value(self, code):
        result = []
        for i in code:
            html = self.url_code(i)
            bs_obj = BeautifulSoup(html, "html.parser")
            value_data = bs_obj.find("table" ,{'summary':"시가총액 정보"})
            value_data1 = value_data.find('td')

            raw_text = value_data1.find("em", {'id':"_market_sum"}).text
            cleaned = re.sub(r'[\n\t]+', '' , raw_text)
            result.append(cleaned)
        return result
    
    def output(self, n, p ,v, t):
        df = pd.DataFrame({
            "회사명" : n,
            "현재가" : p,
            "거래량" : v,
            "시가총액" : t
        })
        print(df)
        return df
    
    def save_excel(self, df):
        today = datetime.today().strftime('%Y-%m-%d')
        df.to_excel(f"Stock_{today}.xlsx", index=False, sheet_name="주식 정보")
        
        

    def company_code_list(self):
        company_list = ["005930","042660","034020","439260","000660",
                        "005380","035420","064350","035720","009830"
                ]
        return company_list
    
    

f = Finance()
r = f.company_code_list()
name = f.company_name(r)
place = f.company_place(r)
volume = f.company_volume(r)
total_value = f.company_total_value(r)

df = f.output(name, place, volume, total_value)
f.save_excel(df)

