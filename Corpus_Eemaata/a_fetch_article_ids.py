import json
import re
import requests
from collections import OrderedDict


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8'
}

issue_head = "https://www.eemaata.com/em/category/issues/"


# Load the sorted issues list
with open("arxiv/issues_list.json", 'r') as f:
    valid_issue_ids = json.load(f)

found_ids = set()
article_issue_dict = {}
try_issue_ids = [f"{year:4d}{1 + month:02d}" for year in range(1998, 2026) for month in range(12)]

for issue_id in try_issue_ids:
    url = issue_head+issue_id+"/"
    print(f"Fetching {issue_id} from {url}", end="\t")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for 4xx/5xx errors
    except requests.exceptions.HTTPError as e:
        if issue_id <= "201301":
            if issue_id not in valid_issue_ids:
                print("OK. Not Found.")
            else:
                print(f"NOT OK ###### HTTP Error: {e}")
        else:
            print("No Issue.")

    except requests.exceptions.RequestException as e:
        print(f"!!!!!!!REQUEST FAILED: {e}")

    else:
        found_ids.add(issue_id)
        content = response.content.decode('utf-8')
        pattern = re.compile(issue_id + r"/(\d+)", re.S)
        articles = set()

        for m in pattern.finditer(content):
            article_id = m.group(1)
            article_issue_dict[article_id] = issue_id
            articles.add(article_id)
        print("Articles: ", articles)


print("New Issues: ", sorted(list(found_ids - valid_issue_ids)))
article_issue_dict = OrderedDict(sorted(article_issue_dict.items(), key=lambda kv: (kv[1], kv[0])))
print(article_issue_dict)
with open("arxiv/article_issue_lookup.json", 'w') as f:
    json.dump(article_issue_dict, f, indent=2, ensure_ascii=True)
with open("arxiv/issues_list.json", 'w') as f:
    json.dump(sorted(list(found_ids)), f, indent=2, ensure_ascii=True)

