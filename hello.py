# -*- coding: euc-kr -*-
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

temp_title="검객"

sql='select title from google_movies where title=?'

f=db.execute(sql, (temp_title, )).fetchall()
print(type(f[0]))
print(f[0]['title'])

db.close()
