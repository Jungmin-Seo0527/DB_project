from flask import Flask, render_template
import requests
from bs4 import BeautifulStoneSoup
import sqlite3
from selenium import webdriver
import time

from hello import hello
from crawlingpkg.googleMovie import getGoogleMovieList

app=Flask(__name__)
app.debug=True

@app.route("/")
def mainpage():
    # getGoogleMovieList()
    db=sqlite3.connect('google_movies.db')
    db.row_factory=sqlite3.Row
    movies=db.execute(
        'select title from google_movies'
    ).fetchall()
    db.close()
    return render_template('showMovieList.html', movies=movies)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)