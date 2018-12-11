# news_scraper
Scrape news article by searched term. Imagine downloading articles you can find searching via https://news.google.com/.

We use two big libraries: 1) News API (https://newsapi.org/) to get direct urls to the articles from a query string. 2) Newspaper3k (https://newspaper.readthedocs.io/en/latest/) to download and parse these urls to extract article bodies, titles and keywords (and optionally perform additional NLP on them).

*PS: News API allows us to search via news.google.com, but also on many more websites (see the [full list](https://newsapi.org/sources)). The current limitations are 1000 requests per day for the News API and individual limitations on targetted websites aimed against automatic scrapers.*

## setup

1. Setup list (for Python 3):
   1. pip install newsapi-python
   1. pip install newspaper3k
   1. pip install requests
1. Get API from https://newsapi.org and fill it to API.txt

## to do

* Manage already downloaded articles, or periods of time. Don't redownload what we already have.
   * Also detect duplicates.
* Clean downloaded text (right now it may contain unicode '\u2019', '\n\n', etc.)


## credits
Code inspired by previously used version of news scraper from https://github.com/heximhotep/fakenews_scraper. We download in the same format (to easily reuse code), but we don't fork from one page to all possible urls - instead we get a list of urls to download via another search library.
We also thank the two big libraries: News API and Newspaper3k
