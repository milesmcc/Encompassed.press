"""This isn't actually used anywhere."""

class NewsSource:
    def __init__(self, reputability, name, articles):
        self.reputability = reputability
        self.name = name
        self.articles = articles

def load_news_collection_from_file(file_location):
    data = open(file_location, "r").readlines

class NewsCollection:
    def __init__(self, sources):
        self.sources = sources


class Story:
    """
    A class to represent a story, a "topic" with a collection of stories.
    """
    def __init__(self, articles):
        self.articles = articles

    def get_appended_headlines(self):
        appended = ""
        for article in self.articles:
            appended = appended + article.headline + " "
        return appended


class Article:
    """
    A class to represent an article.

    Has a title, description, url, index, and max_index
    """

    def __init__(self, title, description, url, index, max_index):
        self.title = title
        self.description = description
        self.url = url
        self.index = index
        self.max_index = max_index

    def displacement_from_top(self):
        """
        Get the "importance".

        calculated as (self.max_index - self.index) / self.max_index
        """
        return (self.max_index - self.index) / self.max_index
