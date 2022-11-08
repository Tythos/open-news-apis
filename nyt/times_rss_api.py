"""
According to https://developer.nytimes.com/faq , limits are:
* 4000 req/day ( = 21.6 sec/req )
* 10 req/min ( = 6.0 sec/req )
* 6 sec/req ( sleep suggestion )

We default to 1 req / 60 seconds but this can be adjusted w/ the env "RATE_LIMIT_RPS"
"""

import os
import json
import time
import hashlib
import pprint
import requests
import bs4

MOD_PATH, _ = os.path.split(os.path.abspath(__file__))
BASE_URL = "https://api.nytimes.com"
RATE_LIMIT_RPS = int(os.getenv("RATE_LIMIT_RPS", "60"))
RSS_SECTION = os.getenv("RSS_SECTION", "World")

def poke():
    """
    """
    with open(MOD_PATH + "/api.key", 'r') as f:
        apiKey = f.read().strip()
    params = {}
    params["api-key"] = apiKey
    params["limit"] = 20
    params["offset"] = 0
    res = requests.get(BASE_URL + "/services/xml/rss/nyt/%s.xml" % RSS_SECTION, params)
    soup = bs4.BeautifulSoup(res.content, features="xml")
    articles = soup.find_all("item")
    return articles[0]
    #pprint.pprint(articles[0])

def getHashUuid4(identifier):
    """
    """
    hash = hashlib.md5(identifier.encode())
    hex = hash.hexdigest()
    return "%s-%s-4%s-%s-%s" % (hex[0:8], hex[8:12], hex[13:16], hex[16:20], hex[20:32])

def getArticleIdentifier(article):
    """
    """
    return article.find("link").text

def summarize(article):
    """
    """
    return {
        "uuid": getHashUuid4(getArticleIdentifier(article)),
        "title": article.find("title").text,
        "url": article.find("link").text,
        "timestamp": article.find("pubDate").text,
        "summary": article.find("description").text,
        "category": article.find("credit").text
    }

def main():
    """
    """
    mostRecentIdentifier = None
    isRunning = True
    while isRunning:
        article = poke()
        identifier = getArticleIdentifier(article)
        if mostRecentIdentifier is None or mostRecentIdentifier != identifier:
            mostRecentIdentifier = identifier
            pprint.pprint(summarize(article))
        else:
            print(" ( ( ( no new articles ) ) )")
        time.sleep(RATE_LIMIT_RPS)

if __name__ == "__main__":
    main()
