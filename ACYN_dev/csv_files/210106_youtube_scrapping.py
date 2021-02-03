# 0826 윤경지
# 유튜브 제목 크롤링 코드
import csv
import json
import requests
from bs4 import BeautifulSoup as bs

string = map(str, input("검색어: ", ).split())
keyword = '+'.join(string)
# keyword = 'dpr+live'

headers = {
    'authority':
    'www.youtube.com',
    'pragma':
    'no-cache',
    'cache-control':
    'no-cache',
    'upgrade-insecure-requests':
    '1',
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'accept':
    '*/*',
    'sec-fetch-site':
    'same-origin',
    'sec-fetch-mode':
    'cors',
    'sec-fetch-user':
    '?1',
    'sec-fetch-dest':
    'empty',
    'accept-language':
    'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie':
    'VISITOR_INFO1_LIVE=f8RyEXUWXuE; YSC=aKzX5uBh-ZE; GPS=1; PREF=f4=4000000',
    'referer':
    'https://www.youtube.com/results?search_query=' + keyword,
    'origin':
    'https://www.youtube.com',
    'Referer':
    'https://www.youtube.com/',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'x-goog-visitor-id':
    'CgtmOFJ5RVhVV1h1RSiY7576BQ^%^3D^%^3D',
    'content-type':
    'application/json',
    'x-youtube-device':
    'cbr=Chrome^&cbrver=84.0.4147.135^&ceng=WebKit^&cengver=537.36^&cos=Windows^&cosver=10.0',
    'x-youtube-page-label':
    'youtube.ytfe.desktop_20200825_2_RC1',
    'x-youtube-variants-checksum':
    '993e813e08900a61d1bb98b69a5cc013',
    'x-youtube-page-cl':
    '328441518',
    'x-youtube-utc-offset':
    '540',
    'x-youtube-client-name':
    '1',
    'x-youtube-client-version':
    '2.20200826.02.01',
    'x-youtube-time-zone':
    'Asia/Seoul',
    'x-youtube-ad-signals':
    'dt=1598535577990^&flash=0^&frm^&u_tz=540^&u_his=3^&u_java^&u_h=864^&u_w=1536^&u_ah=824^&u_aw=1536^&u_cd=24^&u_nplug=3^&u_nmime=4^&bc=31^&bih=710^&biw=730^&brdim=1^%^2C9^%^2C1^%^2C9^%^2C1536^%^2C0^%^2C1555^%^2C830^%^2C747^%^2C710^&vis=1^&wgl=true^&ca_type=image',
}

params = (
    ('search_query', keyword),
    ('pbj', '1'),
)

response = requests.post('https://www.youtube.com/results',
                         headers=headers,
                         params=params)
result = json.loads(response.text)
# print(result)

contents = result[1]['response']['contents']['twoColumnSearchResultsRenderer'][
    'primaryContents']['sectionListRenderer']['contents'][0][
        'itemSectionRenderer']['contents']
# print(contents)

detail_list = []
for content in contents:
    keys = list(content.keys())

    if 'videoRenderer' in keys:
        tag = content['videoRenderer']

        title = tag['title']['runs'][0].get('text')  #영상 제목
        # print(title)
        ownerText = tag['ownerText']['runs'][0].get('text')  #업로더
        # print(ownerText)
        viewCount = tag['viewCountText']['simpleText'].split("조회수 ")[1]  #조회수
        # print(viewCount)
        publishedTime = tag['publishedTimeText']['simpleText']  #게시일
        # print(publishedTime)
        videoUrl = tag['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'] # url

        # description = tag['descriptionSnippet']['runs'][0].get('text')
        # if description:
        #     print(description)
        # else:
        #     continue

        detail = {
            'title': title,
            'ownerText': ownerText,
            'viewCount': viewCount,
            'publishedTime': publishedTime,
            'videoUrl': "https://www.youtube.com"+videoUrl
        }
        detail_list.append(detail)
    else:
        continue
# print(detail_list[1])

# with open(keyword.split('+')[0] + '_youtube_list.csv',
#           'w',
#           newline='',
#           encoding='utf-8-sig') as file:
#     writer = csv.DictWriter(
#         file, fieldnames=['title', 'ownerText', 'viewCount', 'publishedTime', 'videoUrl'])
#     for item in detail_list:
#         writer.writerow({
#             'title': item['title'],
#             'ownerText': item['ownerText'],
#             'viewCount': item['viewCount'],
#             'publishedTime': item['publishedTime'],
#             'videoUrl' : item['videoUrl']
#         })