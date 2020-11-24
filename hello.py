# -*- coding: euc-kr -*-
# �˻�
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

temp_title = "�ظ�����"

# ���� �����ϰ�
#sql=f'select title from naver_movies where (replace(title, " ", "") like "%{temp_title}%")'

sql = f'select title from naver_movies, google_movies where (replace(title, " ", "") like replace("%{temp_title}%", " ", ""))'

f = db.execute(sql).fetchall()
for m in f:
    print(m['title'])

db.close()
