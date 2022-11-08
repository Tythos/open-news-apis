"""
According to https://newsapi.org/pricing (Developer tier):
* Limit is 100 requests/day (864 seconds)
* We round up to sleep and request once every 15 minutes (900 seconds)
* For surge/testing purposes this can be overridden with the RATE_LIMIT_RPS env var
"""

import os
import json
import time
import pprint
import hashlib
import requests

MOD_PATH, _ = os.path.split(os.path.abspath(__file__))
BASE_URL = "https://newsapi.org"
RATE_LIMIT_RPS = int(os.getenv("RATE_LIMIT_RPS", "900"))

def poke():
    """
    """
    with open(MOD_PATH + "/api.key", 'r') as f:
        apiKey = f.read().strip()
    params = {}
    params["country"] = "us"
    params["apiKey"] = apiKey
    params["pageSize"] = 1
    res = requests.get(BASE_URL + "/v2/top-headlines", params=params)
    articles = json.loads(res.content)["articles"]
    return articles[0]

def getHashUuid4(identifier):
    """
    """
    hash = hashlib.md5(identifier.encode())
    hex = hash.hexdigest()
    return "%s-%s-4%s-%s-%s" % (hex[0:8], hex[8:12], hex[13:16], hex[16:20], hex[20:32])

def summarize(article):
    """
    """
    return {
        "uuid": getHashUuid4(article["url"]),
        "title": article["title"],
        "url": article["url"],
        "timestamp": article["publishedAt"],
        "summary": article["description"],
        "category": article["source"]["name"]
    }

def getArticleIdentifier(article):
    """
    """
    return article["url"]

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
