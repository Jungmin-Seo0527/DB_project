import requests
from bs4 import BeautifulSoup
import sqlite3
from selenium import webdriver
import time

def getGoogleMovieList():
    # 크롬창의 띄우지 않고 백그라운드로 실행해서 스크롤을 내려 아래에 있는 정보 로딩
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")
    browser = webdriver.Chrome(options=options)
    # browser.maximize_window()

    # 페이지 이동
    url = "https://play.google.com/store/movies/top"
    browser.get(url)

    # 스크롤 내리기
    browser.execute_script("window.scrollTo(0, 1080)")
    interval = 2
    prev_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(interval)  # 스크롤 내리고 로딩 시간 임의로 2초로 함
        cur_height = browser.execute_script("return document.body.scrollHeight")
        if cur_height == prev_height:
            break
        prev_height = cur_height
    print("done")
    browser.get_screenshot_as_file("google_movie_test.png")

    # db 만들기
    filepath = "google_movies.db"
    conn = sqlite3.connect(filepath)
    cur = conn.cursor()

    conn.executescript("""drop table if exists google_movies;
    create table google_movies(title text, genre text, rate text, price text, url text);
    """)

    conn.commit()

    # 스크래핑
    soup = BeautifulSoup(browser.page_source, "lxml")

    movies = soup.find_all("div", attrs={"class": "Vpfmgd"})

    # title, price, rate, genre, url
    for movie in movies:
        title = movie.find("div", attrs={"class": "WsMG1c nnK0zc"}).get_text()
        genre = movie.find("div", attrs={"class": "KoLSrc"})
        # 장르가 표기되지 않은 것이 있음
        if genre:
            genre = genre.get_text()
        else:
            genre = "NULL" 
        # rate 우선 보류
        rate = movie.find("div", attrs={"role": "img"})  # 별점 5개 만점에 4.4개를 받았습니다. -> 4.4만 추출...
        if rate:
            rate = rate["aria-label"]
        else:
            rate = "NULL"
        price = movie.find("span", attrs={"class": "VfPpfd ZdBevf i5DZme"}).get_text()
        link = movie.find("a", attrs={"class": "JC71ub"})["href"]

        conn.execute("insert into google_movies values (?, ?, ?, ?, ?)", (title, genre, rate, price, link))

    conn.commit()
    conn.close()
    print("google movie!!!!!!!!!!!!!!!!!!!!!!")