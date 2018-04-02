import os, json, re
from sys import argv
from flask import url_for
from newsapi import NewsApiClient

# Environment variable on heroku
NEWS_API_KEY = os.environ['NEWS_API_KEY']

# Init with API_KEY
NewsAPI = NewsApiClient(api_key = NEWS_API_KEY)

# Getting trending news based on user's keyword
def getTopHeadlines(keyword):
    print('KEYWORD: ' + keyword)
    top_headlines = NewsAPI.get_top_headlines(q = keyword, language = 'en')
    articles = top_headlines['articles']
    filter_articles = [article if isImageAvailable(article['urlToImage']) else updateArticleImage(article) for article in articles]
    return filter_articles

# Setting article's image to default
def updateArticleImage(article):
    article['urlToImage'] = url_for('static', filename='assets/img/image_not_available.jpg', _external=True)
    return article

# Checking if article's image is available
def isImageAvailable(url):
    urlRegex = "(http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?(.png|.jpg|.jpeg|.gif)"
    img = re.search(urlRegex, url)
    if img == None:
        return False
    return True
