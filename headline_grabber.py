"""For grabbing the headlines from general RSS feeds for news."""

import io
import json
import feedparser
import headline_grouper
import urllib2
from bs4 import BeautifulSoup


def get_relevant_image_url(webpage):
    """Get the URL of the og:image meta tag. Works well in most use cases."""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]  # for authentic response
    soup = BeautifulSoup(opener.open(webpage), "html.parser")  # yum
    img_src = None
    try:
        img_src = soup.find('meta', {"property": 'og:image'})["content"]  # grab the url of the image mentioned in the og:image meta tag.
    except Exception:  # if there is no og:image...
        pass
    if img_src is None:
        img_src = "https://i.imgur.com/v15Q02n.gif"  # a filler. Would host locally, but would require significantly more from the webserver. And I trust imgur as a CDN. Should I?
    return img_src

pool = True  # whether or not to refresh the headline data

url_file = open("urls.txt", "r") # urls stored in file, 1 per line, url first, then space, then reputability (integer {1..100})
output_file_path = "news.json"  # the relative path to the file to store the headlines, if pool == True
most_relevant_file_path = "top.json"  # the relative path to the file to store the top headline
urls = url_file.readlines()
parsed = {}  # the headline object, a dictionary with lots of unneccessary structure
parsed["sources"] = {}
parsed["headlines"] = []
if pool:
    for url_reputability in urls:  # poorly named variable
        (url, reputability) = str.strip(url_reputability).split()
        reputability = int(reputability)
        print("Parsing " + url + "...")
        data = feedparser.parse(url)
        title = data.feed.title
        parsed["sources"][title] = {"reputability": reputability}
        i = 0
        while i < len(data.entries):
            try:
                parsed["headlines"].append({
                    "index": i,
                    "url": data.entries[i].link,
                    "title": data.entries[i].title,
                    "description": data.entries[i].summary,
                    "source": title,
                    "reputability": reputability
                })
                print("    " + title + ": " + data.entries[i].title)
            except Exception as ex:
                print("Error: " + str(ex))
            i += 1

    print("Writing to " + output_file_path + "...")
    with io.open(output_file_path, 'w+', encoding="utf-8") as outfile:
        outfile.write(unicode(json.dumps(parsed, ensure_ascii=False)))
    print("...done.")
else:
    with open(output_file_path) as data_file:
        parsed = json.load(data_file)

print("Finding most relevant...")
relevant = headline_grouper.get_most_relevant_article(parsed["headlines"])
relevant["image"] = get_relevant_image_url(relevant["url"])
print("...done. Writing to file...")
with io.open(most_relevant_file_path, 'w+', encoding="utf-8") as outfile:
    outfile.write(unicode(json.dumps(relevant, ensure_ascii=False)))
print("...done.")
print(relevant)
