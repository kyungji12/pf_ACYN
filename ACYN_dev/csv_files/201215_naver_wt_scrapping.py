"""
2020.12.15
1. 크롤링을 하기위해 가상환경을 만들기 -> 여러 프로젝트 별로 다른 버전의 패키지 사용
    이 프로젝트에서는 pipenv를 사용함 (입장 : pipenv shell, 퇴장 : exit)
cd ACYN_dev
pipenv shell    
pipenv install requests bs4

** 필요한 정보들 
[웹툰] 제목, 작가, 소개, 장르, 이용, 썸네일, 요일

"""
import requests
from bs4 import BeautifulSoup
import csv
import re

naver_wt_url = 'https://comic.naver.com/webtoon/weekday.nhn'
naver_response = requests.get(naver_wt_url)
# print(naver_response) <Response [200]>

soup = BeautifulSoup(naver_response.text, 'html.parser')
# print(soup)

naver_wts = soup.select('#content > div.list_area.daily_all > div.col')

naver_wt_titles = [] #제목
naver_wt_days = [] #요일
naver_wt_ids = [] #고유 아이디

for naver_wt in naver_wts:
    naver_wt_id = naver_wt.select('div.col_inner > ul > li > a')
    for info in naver_wt_id:
        naver_wt_ids.append(info['href'].split('&')[-2].split('=')[-1])
        naver_wt_days.append(info['href'].split('=')[-1])
        naver_wt_titles.append(info.text)
# print(naver_wt_titles)

naver_wt_intro = []
naver_wt_url = []
# naver_wt_genre = []

for wt_i in range(len(naver_wt_titles)):
    naver_wt_id = naver_wt_ids[wt_i]
    naver_wt_day = naver_wt_days[wt_i]
    
    detail_url = 'https://comic.naver.com/webtoon/list.nhn?titleId='+naver_wt_id+'&weekday='+naver_wt_day
    
    detail_response = requests.get(detail_url)
    #print(detail_response)

    detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
    
    nwt_intros = detail_soup.select('#content > div.comicinfo > div.detail > p:nth-child(2)')
    nwt_intros = re.sub("<.*?>", " ", str(nwt_intros))
    nwt_intros = nwt_intros.replace('[', ' ').replace(']', ' ').strip()
    
    naver_wt_intro.append(nwt_intros)
    naver_wt_url.append(detail_url)


naver_webtoon = {}

for i in range(len(naver_wt_titles)):
    naver_webtoon[naver_wt_titles[i]] = {
        'intro' : naver_wt_intro[i],
        'url' : naver_wt_url[i]
    }

with open('naver_webtoon.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames = ['tilte', 'intro', 'url'])
    for key in naver_webtoon.keys():
        writer.writerow({
            'tilte':key, 
            'intro': naver_webtoon[key]['intro'],
            'url': naver_webtoon[key]['url']
        })