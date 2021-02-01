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
#model import
# from webCrawlApp.models import TestData


def fetch_netflix_latest_data():
    netflix_title = []
    netflix_intro = []
    netflix_genre = []
    netflix_url = []
    netflix_thumbnail =[]
    for num in range(1,8000):
        # url = "https://www.4flix.co.kr/board/netflix/" + str(num)
        url = "https://www.4flix.co.kr/board/netflix/811"

        with requests.get(url) as url_response:
            try:
                doc = url_response.text
                soup = BeautifulSoup(doc, "html.parser")
                # print(soup)
                title_year = soup.find_all("h1")[2].text.strip() # 제목(연도) 
                title = title_year[:-6] #제목만
                genre = soup.find_all("h3")[1].text.strip()
                intro = soup.select_one("#card > div.text-block > p").text.strip()
                url = soup.select_one("#bo_v_link > ul > button > a")['title']
                thumbnail = soup.select_one('#card')
                print(thumbnail)
                
                netflix_title.append(title)
                netflix_genre.append(genre)
                netflix_intro.append(intro)
                netflix_url.append(url)
                netflix_thumbnail.append(thumbnail)
                # print(netflix_thumbnail) 
                # print(num)
            except:
                print("except",num)
                pass #3039는 글 지워짐

    netflix_content = {}

    for i in range(len(netflix_title)):
        netflix_content[netflix_title[i]] = {
            'intro' : netflix_intro[i],
            'url' : netflix_url[i],
            'genre' : netflix_genre[i],
            'thumbnail' : naver_wt_thumbnail[i]
        }
    return netflix_content


if __name__ == '__main__':
    test_dict = fetch_netflix_latest_data()
    # for t in test_dict.keys():
    #     TestData(
    #         title=t, 
    #         intro= test_dict[t]['intro'], 
    #         genre=test_dict[t]['genre'],
    #         url=test_dict[t]['url'],
    #         thumbnail=test_dict[t]['thumbnail']
    #         ).save()
