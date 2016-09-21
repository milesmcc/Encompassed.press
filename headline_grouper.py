"""
Find the most encompassing story

PROCESS:

Stem each headline, remove stop words
    (only deal with top 5 articles from each news source)
Extract words each one

Add each word to a list

Give each article a relevance score, defined as
    article["relevance"] = matched / len(article["relevant"]) * \
        (100 - (100 - article["reputability"] / 2.0) / 100)

Return article with highest relevance score
"""

from nltk.stem.porter import PorterStemmer
from nltk.tokenize.simple import SpaceTokenizer
from nltk.corpus import stopwords
import string
import time
from urlparse import urlparse
import re

stemmer = PorterStemmer()
tokenizer = SpaceTokenizer()

def tokenize(text):
    text = "".join(c for c in text if c not in string.punctuation)
    return tokenizer.tokenize(text)

def remove_stopwords(text):
    filtered_words = [word for word in text if word not in stopwords.words('english')]
    return filtered_words

def get_most_relevant_article(articles):
    words = []
    articles = [article for article in articles if article["index"] < 6]
    for article in articles:
        article["relevant"] = remove_stopwords(tokenize(article["title"]))
        words.extend(article["relevant"])
    for article in articles:
        matched = 0
        for word in words:
            if word in article["relevant"]:
                matched += 1
        article["relevance"] = matched / len(article["relevant"]) * \
            ((100 - (article["reputability"] / 2.0))/ 100)
    highest = None
    for article in articles:
        if highest is None or highest["relevance"] < article["relevance"]:
            highest = article
    highest["processed_description"] = re.sub('<[^<]+?>', '', highest["description"])
    highest["time"] = time.strftime("%d/%m/%Y") + " at " + time.strftime("%H:%M:%S")
    parsed_uri = urlparse(highest["url"])
    highest["tld"] = '{uri.netloc}'.format(uri=parsed_uri)
    return highest
