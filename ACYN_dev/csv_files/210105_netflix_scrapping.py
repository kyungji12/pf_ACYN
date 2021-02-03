import requests
from bs4 import BeautifulSoup

#scrapping
netflix_title = []
netflix_intro = []
netflix_genre = []
netflix_url = []
# netflix_thumbnail =[]
for num in range(1,3): #8000
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
# print(netflix_content)

