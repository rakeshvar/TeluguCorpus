import json
import os
import sys

import requests
from collections import Counter

headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

# Load the article_issue_lookup dictionary
with open("arxiv/article_issue_lookup.json", 'r') as f:
    article_issue_dict = json.load(f)

article_ids = sorted(article_issue_dict, key=lambda a: (article_issue_dict[a], a))

# Count articles in each issue
c = Counter()
for k, v in article_issue_dict.items():
    c[v] += 1

filelist = os.listdir("articles")

def getlink(iss_id, art_id):
    return f"https://eemaata.com/em/issues/{iss_id}/{art_id}.html"

# The main function to get every nth article
# n instances of this fn are launched in nthreads for download speed
def onethreadfn(nthreads, ithread):
    for i in range(ithread, len(article_ids), nthreads):
        article_id = article_ids[i]
        issue = article_issue_dict[article_id]
        if article_id+'.html' in filelist:
            print(f"{ithread}:Skipping article {article_id:4} from issue {issue}")
            continue

        try:
            url = getlink(issue, article_id)
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            text = response.text
            l = len(text)
            print(f"{ithread}) {issue}/{article_id:4} : ({l:6d}) : ", repr(text[::l // 50]))

        except requests.exceptions.HTTPError as e:
            print(f"{ithread}) {issue}/{article_id:4} : ERROR: ", e)

        else:
            with open("articles/"+article_id+".html", "w", encoding='utf-8') as f:
                f.write(text)


# Launch n threads each getting 1/n of the pages
from threading import Thread
try:
    nthreads = int(sys.argv[1])
except:
    nthreads = 8

for ithread in range(nthreads):
    th = Thread(target=onethreadfn, args=(nthreads, ithread))
    th.start()

