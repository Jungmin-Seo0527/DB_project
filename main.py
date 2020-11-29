# -*- coding: euc-kr -*-
from flask import Flask, render_template, request, redirect, url_for
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

    sql = f'select title from movies where platform_id=?'
    google_movies = db.execute(sql, (1,)).fetchall()
    naver_movies = db.execute(sql, (2,)).fetchall()
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

    sql = 'select * from movies where platform_id=? and title=?'
    movie = db.execute(sql, (platform, title)).fetchall()

    sql = 'select * from myList where title=?'
    myComment = db.execute(sql, (title,)).fetchall()

    db.close()
    return render_template("showAboutMovie.html", movie=movie, platform=platform, myComment=myComment)


@app.route("/search/", methods=['GET', 'POST'])
def search():
    db = sqlite3.connect('movie.db')
    db.row_factory = sqlite3.Row

    # post
    if request.method == 'POST':
        title = request.form['movie_title']
        sql = f'select * from movies where platform_id=? and (replace(title, " ", "") like replace("%{title}%", " ", ""))'

        google_movies = db.execute(sql, (1, )).fetchall()
        naver_movies = db.execute(sql, (2, )).fetchall()

        return render_template("showSearchedMovies.html", google_movies=google_movies, naver_movies=naver_movies)

    # get
    else:
        return render_template("searchMovie.html")

# plus my list


@app.route("/<int:platform><string:title>/editList/", methods=['GET', 'POST'])
def editMyList(title, platform):
    db = sqlite3.connect('movie.db')
    db.row_factory = sqlite3.Row

    if request.method == 'POST':
        sql = "insert into myList values (?, ?, ?, ?, ?)"
        db.execute(sql, (request.form['id'], request.form['platform'],
                         request.form['title'], request.form['myRate'], request.form['comment']))

        sql = "update movies set list_id=? where title=?"
        db.execute(sql, (request.form['id'],request.form['title']))

        db.commit()
        db.close()
        return redirect(url_for('showAboutMovie', platform=platform, title=title))
    else:
        # myList(id) ++
        sql = "select max(id) as m from myList"
        id = db.execute(sql).fetchall()
        id = id[0]['m']+1
        return render_template('editMyList.html', title=title, platform=platform, id=id)

# show and edit myList


@app.route("/<int:platform><string:title>EditMyList/", methods=['GET', 'POST'])
def editList(title, platform):
    db = sqlite3.connect('movie.db')
    db.row_factory = sqlite3.Row

    if request.method == 'POST':
        sql = 'update myList set id=?, platform=?, title=?, myRate=?, comment=? where title=? and platform=?'
        db.execute(sql, (request.form['id'], request.form['platform'], request.form['title'],
                         request.form['myRate'], request.form['comment'], title, platform,))
        db.commit()
        db.close()
        return redirect(url_for('showAboutMovie', platform=platform, title=title))
    else:
        sql = 'select * from myList where title=? and platform=?'
        editItem = db.execute(sql, (title, platform,)).fetchall()
        db.close()
        return render_template('editList.html', Item=editItem, platform=platform, title=title)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)
