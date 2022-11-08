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

MOD_PATH, _ = os.path.split(os.path.abspath(__file__))
BASE_URL = "https://api.nytimes.com"
RATE_LIMIT_RPS = int(os.getenv("RATE_LIMIT_RPS", "60"))

def poke():
    """
    """
    with open(MOD_PATH + "/api.key", 'r') as f:
        apiKey = f.read().strip()
    params = {}
    params["api-key"] = apiKey
    params["limit"] = 20
    params["offset"] = 0
    res = requests.get(BASE_URL + "/svc/news/v3/content/all/all.json", params)
    articles = json.loads(res.content)["results"]
    return articles[0]
    #pprint.pprint(articles[0])

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
        "timestamp": article["published_date"],
        "summary": article["abstract"],
        "category": article["section"]
    }

def main():
    """
    """
    mostRecentUrl = None
    isRunning = True
    while isRunning:
        article = poke()
        if mostRecentUrl is None or mostRecentUrl != article["url"]:
            mostRecentUrl = article["url"]
            pprint.pprint(summarize(article))
        else:
            print(" ( ( ( no new articles ) ) )")
        time.sleep(RATE_LIMIT_RPS)

if __name__ == "__main__":
    main()
