import requests
import re
from bs4 import BeautifulSoup
import sqlite3
from selenium import webdriver
import time

# tite, price, rate, url


def getNaverMovieList():

    # db 만들기
    filepath = "naver_movies.db"
    conn = sqlite3.connect(filepath)
    cur = conn.cursor()
    conn.executescript("""drop table if exists google_movies;
    create table google_movies(title text, genre text, rate text, price text, url text);
    """)

    conn.commit()

    for page in range(1, 6):
        url = "https://serieson.naver.com/movie/top100List.nhn?page={}&rankingTypeCode=PC_D".format(
            page)
        res = requests.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "lxml")
        movies = soup.find_all("li")
        for movie in movies:

            # title
            title = movie.find("a", attrs={"class": "NPI=a:dcontent"})
            if title:
                title = title["title"]
            else:
                continue

            # price
            # 어짜피 p태그는 동일 자매들중에 한개만 있음 따로 클래스 명으로 찾을 필요 없음
            price = movie.find("p")
            if price:
                price = price.find("span").get_text()
            else:
                continue

            # rate
            rate = movie.find("em", attrs={"class": "score_num"})
            if rate:
                rate = rate.get_text()
            else:
                continue

            # link
            link = movie.find("a", attrs={"class": "NPI=a:dcontent"})["href"]
            link_head = "https://serieson.naver.com/"

            # genre
            # 19세는 url을 타고 들어가면 19게 인증을 해야 하기 때문에
            # 일괄적으로 19라고 표기
            genre_url = link_head+link
            genre_res = requests.get(genre_url)
            genre_res.raise_for_status()
            genre_soup = BeautifulSoup(genre_res.text, "lxml")

            genre = genre_soup.find("li", attrs={"class": "info_lst"})
            if genre:
                genre = genre.find("a").get_text()
            else:
                genre = "19"

            conn.execute("insert into google_movies values (?, ?, ?, ?, ?)",
                         (title, genre, rate, price, link))

            # print(
            #     f"title: {title} / price: {price} / rate: {rate} / link : {link_head+link} / genre : {genre}")
    print("naver_movie_list->DB done!!!")
    conn.commit()
    conn.close()
