import newspaper
from newspaper import Article
from newspaper import ArticleException
import nltk
import json
import os
import time

#run once:
#nltk.download('punkt')


def fileName(author, title, date):
    authorName = author
    if (authorName == None):
        authorName = 'NOAUTHOR'
    else:
        authorName = authorName.replace(' ', '_')
        authorName = authorName.replace('?', '')

    titleName = title
    if (titleName == None):
        titleName = 'NOTITLE'
    else:
        titleName = titleName.replace(':', '_')
        titleName = titleName.replace(';', '_')
        titleName = titleName.replace(r'.,', '_')
        titleName = titleName.replace(' ', '_')
        titleName = titleName.replace('?', '')
        titleName = titleName.replace('"', "'")
        titleName = titleName.replace('*', '')
        titleName = titleName.replace('/', '_')
        titleName = titleName.replace('|', '')
        titleName = titleName.replace('$', '')
        titleName = titleName.replace('^', '')
        titleName = titleName.replace('>', '')
        titleName = titleName.replace('<', '')
        titleName = titleName.replace(r'\\\//|<>', '')
    if (date == None):
        dateName = 'NODATE'
    else:
        if (type(date) == str):
            dateName = date
        else:
            dateName = str(date.date())
    delimiter = '$$$$$'
    return authorName + delimiter + titleName + delimiter + dateName + '.json'

def download_list_of_urls(urls, target_dir, delay=0.2):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for sorted_i,url in enumerate(urls):
        print(sorted_i, "] downloading ", url)
        article = Article(url)
        try:
            article.download()
            article.parse()

            article_filename = fileName(None if article.authors == [] else article.authors[0], article.title,
                                       article.publish_date)
            article.nlp()
            features = {"content": {"keywords": [{"keyword": word} for word in article.keywords]}}

            articleJSON = {"features": features, "url": article.url, "date": article.publish_date,
                           "title": article.title, "authors": article.authors, "body": article.text,
                           "relevance_sorted_i": sorted_i}
            with open(target_dir+"/"+article_filename, 'w') as outfile:
                json.dump(articleJSON, outfile, indent=2, default=str)
                print("saved sucessfully to", target_dir+"/"+article_filename)
        except Exception as e:
            print(e)
            continue

        time.sleep(delay)




#
# NOT USING RIGHT NOW
#
def root_from(root_urls, target_dir, delay=0.2):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    # This function is based on https://github.com/heximhotep/fakenews_scraper
    # it starts with a list of root urls
    # for each root url it gets other urls on that page and forks in this way,
    # scraping everything on the road

    # use this for home news server pages, but not for direct news download
    # you will get a lot of articles, but not all necessarily connected with the original search

    visited_urls = set([])
    saved_articles = set([])
    article_lengths = dict([])

    while (True):
        if (len(root_urls) == 0):
            break
        root_url = root_urls[0]
        root_urls = root_urls[1:]
        # print(root_urls)
        if (root_url in visited_urls):
            continue
        else:
            visited_urls.add(root_url)
        root_paper = newspaper.build(root_url)
        print(root_url, 'size:', root_paper.size())
        print('category urls count:', len(root_paper.category_urls()))
        adjacent_urls = root_paper.category_urls()
        for adj_url in adjacent_urls:
            if (adj_url in visited_urls):
                continue
            root_urls.append(adj_url)
            # print(root_urls)
        index = 0
        visited_streak = 0
        for carticle in root_paper.articles:
            if (visited_streak > 26):
                break
            article = Article(carticle.url)
            try:
                article.download()
                article.parse()

                article_name = fileName(None if article.authors == [] else article.authors[0], article.title,
                                           article.publish_date)

                if (article_name in saved_articles and len(article.text) <= article_lengths[article_name]):
                    print('skipping article')
                    visited_streak += 1
                    continue
                visited_streak = 0
                article.nlp()
                saved_articles.add(article_name)
                article_lengths[article_name] = (len(article.text))
                payload = {"url": article.url, "title": article.title, "content": article.text}
                features = {"content": {"keywords": [{"keyword": word} for word in article.keywords]}}

                articleJSON = {"features": features, "url": article.url, "date": article.publish_date,
                               "title": article.title, "authors": article.authors, "body": article.text}
                with open(target_dir+"/"+article_name, 'w') as outfile:
                    json.dump(articleJSON, outfile, indent=2, default=str)
                    print("saved article")
            except ArticleException:
                continue
            except FileNotFoundError:
                continue
            except OSError:
                continue
            except UnicodeError:
                continue
            except Exception:
                continue
            index += 1
        print(index)
    time.sleep(delay)


