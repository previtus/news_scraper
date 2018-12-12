import math
from newsapi import NewsApiClient
import datetime

from scraper_functions import download_list_of_urls, fileName

search_term = '(artificial intelligence) OR (machine learning)'
directory = 'aiORml_OCT_12.11.-30.11._Top1000WithRelevance'

LIMIT_DONWLOADS = 1000 #< Daily limit is 1000!
SKIP_FIRST = 0 # skip if you are running the same search again

# downloaded
# 11.11. - 11.16.
from_date = "2018-11-12"
to_date = "2018-11-30"

""" # optionally select x last days
last_x_days = 1
LAST_X_DAYS = False
if LAST_X_DAYS:
    # We look from "yesterday" to x days before that
    now=datetime.datetime.now()
    to_date = '%s-%s-%s' % (now.year, str(now.month).zfill(2), str(now.day - 1).zfill(2))
    from_date = '%s-%s-%s' % (now.year, str(now.month).zfill(2), str(now.day - 1 - last_x_days).zfill(2))
"""

print("Looking at period:", from_date, to_date)

# Init
API = ""
with open('API.txt', 'r') as apifile:
    API=apifile.read().replace('\n', '')
newsapi = NewsApiClient(api_key=API)

# SOURCES:
# All english sources:
# >> "Using  1157 sources."
sources = newsapi.get_sources(language='en')

all_sources = ""
for source in sources["sources"]:
    all_sources += source["id"]+","
all_sources = all_sources[0:-1]
print("Using ", len(all_sources), "sources.")

# ARTICLE SEARCH:
#https://newsapi.org/docs/endpoints/everything
all_articles_counter = newsapi.get_everything(q=search_term,
                                      sources=all_sources,
                                      from_param=from_date,
                                      to=to_date,
                                      language='en',
                                      sort_by='relevancy')

n_articles = all_articles_counter["totalResults"]
print("Found in total", n_articles)

if n_articles < LIMIT_DONWLOADS:
    LIMIT_DONWLOADS = n_articles

PER_PAGE=100
n_calls = math.ceil(LIMIT_DONWLOADS / PER_PAGE)



articles = []
url_list = []
total_i = 0 + SKIP_FIRST
skip_pages = math.floor(SKIP_FIRST / PER_PAGE)

for i in range(0,n_calls):
    print("[ page #",i+1+skip_pages, "/", n_calls,"]")
    batch_articles = newsapi.get_everything(q=search_term,
                                            sources=all_sources,
                                            from_param=from_date,
                                            to=to_date,
                                            language='en',
                                            sort_by='relevancy',
                                            page_size=PER_PAGE,
                                            page=(i+1+skip_pages))


    # ['source', 'author', 'title', 'description', 'url', 'urlToImage', 'publishedAt', 'content']
    for j in range(0,len(batch_articles["articles"])):

        print("\n",total_i)
        total_i += 1
        article = batch_articles["articles"][j]

        #print(article.keys())
        articles.append(article)
        url_list.append(article["url"]) #still sorted by relevance

        print(article["title"], "at:", article["url"])
        #print("img:", article["urlToImage"])
        #print("description:", article["description"])
        #print("content:", article["content"])

        #author = article["author"]
        #title = article["title"]
        #date = article["publishedAt"]
        #filename = fileName(author, title, date)


print("Finally we have ", len(url_list), " article URLs.")
print("====== Downloading now ======")

download_list_of_urls(url_list, directory)
