##웹 크롤링 & 파이썬 라이브러리 기초 정리##
#HTML & BeautifulSoup
-**HTML이란?**
웹사이트를 구성하는 언어

웹사이트에서 사용하는 파일은 .html 확장자를 가짐

BeautifulSoup 주요 메소드
find: 태그가 처음 등장하는 부분만 추출

find_all: 해당 태그가 사용된 모든 부분 추출

text: 태그 내 텍스트만 추출

read: 파일 읽기 (파이썬 내장, BeautifulSoup용 아님)

HTML 표 태그 설명
table: 표 전체를 감싸는 태그

border: 표의 테두리 속성

caption: 표 제목

tr: 표의 행(row)

th: 표의 헤더(제목 칸)

td: 표의 셀(내용 칸)

크롤링 전 주의사항
크롤링을 하기 전 robots.txt로 크롤링 허용 여부 반드시 확인

모든 사이트는 /robots.txt로 크롤링 지침을 안내

robots.txt란?
웹사이트 루트에 위치한 약속된 파일

크롤러(로봇)에게 접근 허용/금지 경로, 크롤링 간격 등 지침 제공

robots.txt 주요 항목
User-agent: 적용할 크롤러 지정

Disallow: 접근 금지 경로

Allow: 접근 허용 경로

Sitemap: 사이트 구조 안내 파일 위치

Crawl-delay: 크롤링 요청 간격

크롤링 라이브러리 비교
requests: 현업 표준, 인코딩 자동, 매우 편리

urllib: 파이썬 내장, 인코딩 수동, 주로 교육용/단순 작업

selenium: 동적(자바스크립트 렌더링) 페이지 크롤링에 필수

scrapy: 대규모/자동화 전문 크롤링 프레임워크

정적 페이지 vs 동적 페이지
정적 페이지: 누구나 같은 내용, BeautifulSoup만으로 크롤링 가능

동적 페이지: 접속 환경/사용자에 따라 다르게 보임, selenium 필요

개발자 도구 vs 페이지 소스
개발자 도구: 브라우저가 최종 렌더링한 결과물(F12, 검사 기능)

페이지 소스: 웹 서버에서 받아온 원본 HTML(Ctrl+U, 페이지 소스 보기)

Selenium 크롬드라이버 기본 설명
크롬 브라우저를 자동 제어하는 객체(driver) 생성

웹 페이지에서 요소를 찾을 때 최대 n초까지 기다릴 수 있음

headless 옵션 사용 시 브라우저 창 없이(백그라운드) 크롤링 가능

base64란?
이진 데이터를 텍스트(문자열)로 변환하는 인코딩 방식

이메일, 웹 API, JSON 등 텍스트만 허용하는 곳에서 이미지, 파일 등 전송 시 사용

base64는 bytes만 처리 가능하므로, 문자열을 먼저 'ascii' 또는 'utf-8'로 인코딩 필요

base64 인코딩 시 데이터 크기가 약 33% 증가

텍스트 처리 유용 함수(textwrap)
shorten: 길이 제한, 잘린 부분 표시 가능

wrap: 지정한 글자 수마다 리스트로 나눔

fill: 지정한 글자 수마다 줄 바꿈 적용

외부 라이브러리 관리(pip)
설치: pip install 패키지명

삭제: pip uninstall 패키지명

특정 버전 설치: pip install 패키지명==버전

업그레이드: pip install --upgrade 패키지명

설치 목록 확인: pip list

패키지 목록 저장: pip list --format=freeze > requirements.txt

목록에서 일괄 설치: pip install -r requirements.txt

타입 어노테이션
변수나 함수 선언 시 타입을 명시적으로 지정

코드 가독성, 협업 효율성, 버그 방지에 유리

str() vs repr()
str(): 사람이 읽기 쉬운 형태로 출력 (비공식적)

repr(): 컴퓨터가 이해하기 쉬운 형태, eval로 원복 가능 (공식적)

과제
크롤링하고 싶은 사이트 직접 선정

robots.txt로 크롤링 가능 여부 확인

관심 분야 위주로 연습 사이트 선정


