# -*- coding: euc-kr -*-
from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulStoneSoup
import sqlite3
from selenium import webdriver
import time

from crawlingpkg.googleMovie import getGoogleMovieList
from crawlingpkg.naverMovie import getNaverMovieList
from crawlingpkg.test import ggg

app = Flask(__name__)
app.debug = True


@app.route("/")
def mainpage():
    # getGoogleMovieList()
    db = sqlite3.connect('movie.db')
    db.row_factory = sqlite3.Row
    table = ''

    table = 'google_movies'
    sql = f'select title from {table}'
    google_movies = db.execute(sql).fetchall()

    table = 'naver_movies'
    naver_movies = db.execute(sql).fetchall()
    db.close()

    return render_template('mainPage_test.html', google_movies=google_movies, naver_movies=naver_movies)


@app.route("/<int:platform>_reset")
def reset(platform):
    if platform == 1:
        getGoogleMovieList()
    else:
        getNaverMovieList()
    return render_template("resetPage.html")


# platform -> 1=google, 2=naver
@app.route("/<int:platform>/<string:title>")
def showAboutMovie(platform, title):
    db = sqlite3.connect("movie.db")
    db.row_factory = sqlite3.Row
    sql = ''

    sql = 'select title from platform where id=?'
    table = db.execute(sql, (platform,)).fetchall()[0]['title']

    sql = f'select * from {table} where title=?'
    movie = db.execute(sql, (title,)).fetchall()

    db.close()
    return render_template("showAboutMovie.html", movie=movie)


@app.route("/search/", methods=['GET', 'POST'])
def search():
    db = sqlite3.connect('movie.db')
    db.row_factory = sqlite3.Row

    # post
    if request.method == 'POST':
        title = request.form['movie_title']
        sql = f'select * from naver_movies where (replace(title, " ", "") like replace("%{title}%", " ", ""))'
        movies = db.execute(sql).fetchall()
        for movie in movies:
            print(movie["title"])
            print(movie["price"])
        return render_template("showAboutMovie.html", movie=movies)

    # get
    else:
        return render_template("searchMovie.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)
