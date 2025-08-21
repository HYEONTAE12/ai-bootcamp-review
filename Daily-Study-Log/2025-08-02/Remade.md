# Naver Finance Stock Crawler

네이버 금융에서 주식 종목들의 회사명, 현재가, 거래량, 시가총액을 크롤링하여 엑셀 파일로 저장합니다.

## 사용 라이브러리
- BeautifulSoup4
- requests
- pandas
- openpyxl

## 출력 예시
| 회사명 | 현재가 | 거래량 | 시가총액 |
|--------|--------|--------|-----------|
| 삼성전자 | 75,000 | 13,123,000 | 500조 |

## 파일 저장
- 저장 형식: `Stock_YYYY-MM-DD.xlsx`
