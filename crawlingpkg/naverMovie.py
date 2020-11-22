import requests
from bs4 import BeautifulSoup
import sqlite3
from selenium import webdriver
import time

# 우선 장르 보류
# tite, price, rate, url
def getNaverMovieList():
    for page in range(1, 6):
        url = "https://serieson.naver.com/movie/top100List.nhn?page={}&rankingTypeCode=PC_D".format(page)
        res = requests.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "lxml")
        movies=soup.find_all("li")
        for movie in movies:
            title=movie.find("a", attrs={"class":"NPI=a:dcontent"})
            if title:
                title=title["title"]
            else:
                continue

            price=movie.find("p", attrs={"class":"price2_book"})
            if price:
                price=price.find("span")
                if price:
                    price=price.get_text()
                else:
                    continue
            else:
                continue
            

            print(title+"->"+price)

if __name__ == "__main__":
    getNaverMovieList()
