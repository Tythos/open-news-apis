"""
According to https://open-platform.theguardian.com/access/ :
* Up to 12 calls per second
* Up to 5,000 calls per day (1 call / 17.28 seconds)
* We round up to sleep and request once every 30 seconds
* For surge/testing purposes, this can be overridden with the RATE_LIMIT_RPS env var
"""

import os
import json
import time
import pprint
import hashlib
import requests

MOD_PATH, _ = os.path.split(os.path.abspath(__file__))
SECTION_ID = os.getenv("SECTION_NAME", "world")
BASE_URL = "https://content.guardianapis.com"
RATE_LIMIT_RPS = int(os.getenv("RATE_LIMIT_RPS", "30"))

def poke():
    """
    """
    with open(MOD_PATH + "/api.key", 'r') as f:
        apiKey = f.read().strip()
    params = {}
    params["api-key"] = apiKey
    params["section"] =  SECTION_ID
    params["page-size"] = 1
    params["show-fields"] = "trailText"
    res = requests.get(BASE_URL + "/search", params=params)
    response = json.loads(res.content)
    articles = response["response"]["results"]
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
        "uuid": getHashUuid4(article["webUrl"]),
        "title": article["webTitle"],
        "url": article["webUrl"],
        "timestamp": article["webPublicationDate"],
        "summary": article["fields"]["trailText"],
        "category": article["sectionName"]
    }

def getArticleIdentifier(article):
    """
    """
    return article["webUrl"]

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
