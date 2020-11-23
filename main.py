from flask import Flask, render_template
import requests
from bs4 import BeautifulStoneSoup
import sqlite3
from selenium import webdriver
import time

from hello import hello
from crawlingpkg.googleMovie import getGoogleMovieList
from crawlingpkg.naverMovie import getNaverMovieList

app = Flask(__name__)
app.debug = True


@app.route("/")
def mainpage():
    # getGoogleMovieList()
    db = sqlite3.connect('movie.db')
    db.row_factory = sqlite3.Row
    google_movies = db.execute(
        'select title from google_movies'
    ).fetchall()
    naver_movies = db.execute(
        'select title from naver_movies'
    ).fetchall()
    db.close()
    return render_template('mainPage_test.html', google_movies=google_movies, naver_movies=naver_movies)


# platform -> 1=google, 2=naver
@app.route("/<int:platform>/<string:title>")
def showAboutMovie(platform, title):
    if platform == 1:
        table = "google_movies"
    else:
        table = "naver_movies"

    db = sqlite3.connect("movie.db")
    db.row_factory = sqlite3.Row

    movie = db.execute(
        f'select * from {table} where title=?', (title,)
    ).fetchall()
    db.close()
    return render_template("showAboutMovie.html", movie=movie)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)
