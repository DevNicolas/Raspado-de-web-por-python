from flask import request, redirect, render_template, url_for
from app import app
import requests
from bs4 import BeautifulSoup

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/result', methods=["POST"])
def result_search():
    query = request.form['search']
    query_search = query.replace(" ","%20")
    url = requests.get("https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&q={}&btnG=&oq=".format(query_search))
    sou = BeautifulSoup(url.content, "html.parser")
    lists = sou.find_all("div", class_="gs_scl")
    articles = []
    for list in lists:
        title = list.find("h3", {'class': 'gs_rt'}).getText()
        try:
            content = list.find("div", {'class': 'gs_rs'}).getText()
        except:
            content = "None content"
        cite = list.find("div", {'class': 'gs_fl'}).getText()
        url_article = list.find("a", href=True).attrs['href']
        article = title + "$" + content + "$" + cite + "$" + url_article
        articles.append(article)
    return render_template('result_search.html', lists= articles, query=query)
