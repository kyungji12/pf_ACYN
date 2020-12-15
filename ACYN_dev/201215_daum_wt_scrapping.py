import requests
from bs4 import BeautifulSoup
import csv
import re
import json

# daum_wt_url = 'http://webtoon.daum.net/'
# daum_response = requests.get(daum_wt_url)
# # print(daum_response)

# soup = BeautifulSoup(daum_response.text, 'html.parser')
# # print(soup.select('ul[id=dayListTab]'))

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
        for i in range(len(daum_dict['data'])):
            daum_webtoon[daum_dict['data'][i]['title']] = {
                'intro': daum_dict['data'][i]['introduction'],
                'url' : 'http://webtoon.daum.net/webtoon/view/'+ daum_dict['data'][i]['nickname']
            }

with open('daum_webtoon.csv', 'w', newline='',encoding='utf-8-sig') as file:
  writer = csv.DictWriter(file, fieldnames = ['title', 'intro', 'url'])
  for key in daum_webtoon.keys():
      writer.writerow({'title' : key, 'intro' : daum_webtoon[key]['intro'], 'url': daum_webtoon[key]['url']})
