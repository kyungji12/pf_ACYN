import requests
from bs4 import BeautifulSoup
# import csv
import re
import os
from urllib.parse import urlparse

#db에 저장
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "acyn_project.settings")
import django

django.setup()

from webCrawlApp.models import TestData


def fetch_naver_webtoon_latest_data():

    result = []

    naver_wt_url = 'https://comic.naver.com/webtoon/weekday.nhn'
    naver_response = requests.get(naver_wt_url)
    # print(naver_response) #<Response [200]>

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
    naver_wt_genre = []
    naver_wt_thumbnail = []

    for wt_i in range(len(naver_wt_titles)):
        naver_wt_id = naver_wt_ids[wt_i]
        naver_wt_day = naver_wt_days[wt_i]
        
        detail_url = 'https://comic.naver.com/webtoon/list.nhn?titleId='+naver_wt_id+'&weekday='+naver_wt_day
        
        detail_response = requests.get(detail_url)
        #print(detail_response)

        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        #intro
        nwt_intros = detail_soup.select('#content > div.comicinfo > div.detail > p:nth-child(2)')
        nwt_intros = re.sub("<.*?>", " ", str(nwt_intros))
        nwt_intros = nwt_intros.replace('[', ' ').replace(']', ' ').strip()
        #genre
        nwt_genre = detail_soup.select('#content > div.comicinfo > div.detail > p.detail_info > span.genre')
        nwt_genre = re.sub("<.*?>", " ", str(nwt_genre))
        nwt_genre = nwt_genre.replace('[', ' ').replace(']', ' ').strip()
        # #thumbnail
        # nwt_thumb = detail_soup.select('#content > div.comicinfo > div.thumb > a > img')
        # nwt_thumb = nwt_thumb.find('src')
        
        naver_wt_intro.append(nwt_intros)
        naver_wt_url.append(detail_url)
        naver_wt_genre.append(nwt_genre)
        # naver_wt_thumbnail.append()

        # print(nwt_thumb)


    naver_webtoon = {}

    for i in range(len(naver_wt_titles)):
        naver_webtoon[naver_wt_titles[i]] = {
            'intro' : naver_wt_intro[i],
            'url' : naver_wt_url[i],
            'genre' : naver_wt_genre[i]
            # 'thumbnail' : naver_wt_thumbnail[i]
        }
        result.append(naver_webtoon)

    # print(result)
    # return result
    return naver_webtoon

if __name__ == '__main__':
    test_dict = fetch_naver_webtoon_latest_data()
    for t in test_dict.keys():
        TestData(title=t, intro= test_dict[t]['intro'], genre=test_dict[t]['genre'], url=test_dict[t]['url']).save()

# with open('naver_webtoon.csv', 'w', newline='', encoding='utf-8-sig') as file:
#     writer = csv.DictWriter(file, fieldnames = ['tilte', 'intro', 'url'])
#     for key in naver_webtoon.keys():
#         writer.writerow({
#             'tilte':key, 
#             'intro': naver_webtoon[key]['intro'],
#             'url': naver_webtoon[key]['url']
#         })