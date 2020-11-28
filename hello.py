# -*- coding: euc-kr -*-
# 검색
from flask import Flask, render_template
import requests
from bs4 import BeautifulStoneSoup
import sqlite3
from selenium import webdriver
import time

from crawlingpkg.googleMovie import getGoogleMovieList
from crawlingpkg.naverMovie import getNaverMovieList
from crawlingpkg.test import ggg


db = sqlite3.connect('movie.db')
db.row_factory = sqlite3.Row
google_movies = db.execute(
    'select title from google_movies'
).fetchall()

temp_title = "해리포터"

# 띄어쓰기 배제하고
#sql=f'select title from naver_movies where (replace(title, " ", "") like "%{temp_title}%")'

sql = f'select * from google_movies where (replace(title, " ", "") like replace("%{temp_title}%", " ", ""))'

f = db.execute(sql).fetchall()
for m in f:
    print(m['title'])
    print(m['rate'][10]+m['rate'][11]+m['rate'][12])
    temp=m['rate'][10]+m['rate'][11]+m['rate'][12]
    temp=float(temp)*2
    print(type(temp))
    print(temp)

db.close()
