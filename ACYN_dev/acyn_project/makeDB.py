#크롤링
import requests
from bs4 import BeautifulSoup
#데이터처리
import os
import re
import json
from urllib.parse import urlparse
#db에 저장
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "acyn_project.settings")
import django
django.setup()
#model import
from webCrawlApp.models import NaverWebtoon, NaverWebnovel, DaumWebtoon, Netflix

#네이버 웹툰
def fetch_naver_webtoon_latest_data():
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
        #thumbnail
        nwt_thumb = detail_soup.select_one('#content > div.comicinfo > div.thumb > a > img')
        nwt_thumb = nwt_thumb['src']
        
        naver_wt_intro.append(nwt_intros)
        naver_wt_url.append(detail_url)
        naver_wt_genre.append(nwt_genre)
        naver_wt_thumbnail.append(nwt_thumb)


    naver_webtoon = {}

    for i in range(len(naver_wt_titles)):
        naver_webtoon[naver_wt_titles[i]] = {
            'intro' : naver_wt_intro[i],
            'url' : naver_wt_url[i],
            'genre' : naver_wt_genre[i],
            'thumbnail' : naver_wt_thumbnail[i]
        }

    return naver_webtoon
    
#다음 웹툰
def fetch_daum_webtoon_latest_data():
    daum_wt_url = 'http://webtoon.daum.net/'
    daum_response = requests.get(daum_wt_url)
    # print(daum_response)

    soup = BeautifulSoup(daum_response.text, 'html.parser')
    # print(soup.select('ul[id=dayListTab]'))

    cookies = {
        '_TI_NID': 'iok9mjEFfnWoNqMjDA5hhW8k8kKH0Wiv8TYB6cQK/PKjTcLbEABjYteWe2L9+Sj6X0L25eis8QV+IXJuAbaCWQ==',
        '__T_': '1',
        '_fbp': 'fb.1.1598431157982.2053593330',
        'VOTE': 'MTAuMTk%3D',
        'MY': 'MTAuMTk%3D',
        'ORDER': 'MTAuMTk%3D',
        'TIARA': '4GrXQNB3I4eNj4AL_shwBbHRF5Gi_VgqD.Tm_v6ks1f.mI.PhtF-cQcKlL9XRlE6P21aOk2QXgar-GKtYlYX-vIcfxLO7SBB',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://webtoon.daum.net/',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('timeStamp', '1598517670442'),
    )

    day_all = ['mon', 'tue', 'wed','thu','fri','sat','sun']

    daum_webtoon = {}

    for day in day_all : 
        daum_wt_response = requests.get('http://webtoon.daum.net/data/pc/webtoon/list_serialized/'+day, headers=headers, params=params, cookies=cookies,verify=False)
        daum_dict = json.loads(daum_wt_response.text)
        # print(daum_dict)
        for i in range(len(daum_dict['data'])):
            daum_webtoon[daum_dict['data'][i]['title']] = {
                'intro': daum_dict['data'][i]['introduction'],
                'url' : 'http://webtoon.daum.net/webtoon/view/'+ daum_dict['data'][i]['nickname'],
                # 'genre': daum_dict['data'][i]['cartoon']['genres'],
                'genre' : list(item['name'] for item in daum_dict['data'][i]['cartoon']['genres']),
                'thumbnail' : daum_dict['data'][i]['thumbnailImage2']['url']
            }

    return daum_webtoon

#네이버 웹소설
def fetch_naver_webnovel_latest_data():
    genre_id = ['101', '109', '102', '110', '103', '104']
    #[로맨스, 로판, 판타지, 현판, 무협, 미스터리]
    # 106 = 완결작품

    all_nvl_ids  = []

    for genre in genre_id:
        naver_nvl_URL = 'https://novel.naver.com/webnovel/ranking.nhn?genre='+genre+'&periodType=DAILY#'

        naver_response = requests.get(naver_nvl_URL)

        soup = BeautifulSoup(naver_response.text,'html.parser')

        naver_nvls = soup.select('#content > div.section_ranking > div.ranking_lst > div.ranking_wrap_left > ul > li')

        for naver_nvl in naver_nvls:
            nvl_id = naver_nvl.select_one('a')['href'].split('=')[-1]
            all_nvl_ids.append(nvl_id)

    all_nvl_title = []
    all_nvl_intro = []
    all_nvl_url = []
    all_nvl_genre = []
    all_nvl_thumbnail = []

    for nvl_ids in all_nvl_ids:
        detail_nvl_URL = 'https://novel.naver.com/webnovel/list.nhn?novelId='+nvl_ids
        detail_response = requests.get(detail_nvl_URL)
        soup = BeautifulSoup(detail_response.text, 'html.parser')

        detail_intro = soup.select_one('#content > div.section_area_info > p.dsc').text
        detail_title = soup.select_one('#content > h2').text
        detail_genre = soup.select_one('#content > div.section_area_info > p.info_book > span.genre').text
        detail_thumbnail = soup.select_one('#content > div.section_area_info > a.pic.NPI\=a\:illust > img')['src']
        
        
        all_nvl_intro.append(detail_intro)
        all_nvl_title.append(detail_title)
        all_nvl_url.append(detail_nvl_URL)
        all_nvl_genre.append(detail_genre)
        all_nvl_thumbnail.append(detail_thumbnail)


    naver_novel = {}

    for i in range(len(all_nvl_title)):
        naver_novel[all_nvl_title[i]] = {
            'intro' : all_nvl_intro[i],
            'url' : all_nvl_url[i],
            'genre' : all_nvl_genre[i],
            'thumbnail' : all_nvl_thumbnail[i]
        }

    return naver_novel

#넷플릭스
def fetch_netflix_latest_data():
    netflix_title = []
    netflix_intro = []
    netflix_genre = []
    netflix_url = []
    # netflix_thumbnail =[]
    for num in range(1,8000):
        url = "https://www.4flix.co.kr/board/netflix/" + str(num)
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
                # thumbnail = ''
                # print(intro)
                
                netflix_title.append(title)
                netflix_genre.append(genre)
                netflix_intro.append(intro)
                netflix_url.append(url)
                # print(netflix_title) 
    
            except:
                # print("except",num)
                pass #3039는 글 지워짐

    netflix_content = {}

    for i in range(len(netflix_title)):
        netflix_content[netflix_title[i]] = {
            'intro' : netflix_intro[i],
            'url' : netflix_url[i],
            'genre' : netflix_genre[i]
            # 'thumbnail' : naver_wt_thumbnail[i]
        }
    return netflix_content

if __name__ == '__main__':
    naver_webtoon_dict = fetch_naver_webtoon_latest_data()
    for i in naver_webtoon_dict.keys():
        NaverWebtoon(
            title=i, 
            intro= naver_webtoon_dict[i]['intro'], 
            genre=naver_webtoon_dict[i]['genre'],
            url=naver_webtoon_dict[i]['url'],
            thumbnail=naver_webtoon_dict[i]['thumbnail']
            ).save()

    daum_webtoon_dict = fetch_daum_webtoon_latest_data()
    for i in daum_webtoon_dict.keys():
        DaumWebtoon(
            title=i, 
            intro= daum_webtoon_dict[i]['intro'], 
            genre=daum_webtoon_dict[i]['genre'],
            url=daum_webtoon_dict[i]['url'],
            thumbnail=daum_webtoon_dict[i]['thumbnail']
            ).save()


    naver_webnovel_dict = fetch_naver_webnovel_latest_data()
    for i in naver_webnovel_dict.keys():
        NaverWebnovel(
            title=i, 
            intro= naver_webnovel_dict[i]['intro'], 
            genre=naver_webnovel_dict[i]['genre'],
            url=naver_webnovel_dict[i]['url'],
            thumbnail=naver_webnovel_dict[i]['thumbnail']
            ).save()


    netflix_dict = fetch_netflix_latest_data()
    for i in netflix_dict.keys():
        Netflix(
            title=i, 
            intro= netflix_dict[i]['intro'], 
            genre=netflix_dict[i]['genre'],
            url=netflix_dict[i]['url'],
            thumbnail=netflix_dict[i]['thumbnail']
            ).save()