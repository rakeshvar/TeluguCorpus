import re
from bs4 import BeautifulSoup
import os

def unhtml(html):
    """Remove HTML from the text."""
    html = re.sub(r'(?i)&nbsp;', ' ', html)
    html = re.sub(r'(?i)&amp;', '&', html)
    html = re.sub(r'(?i)&gt;', '>', html)
    html = re.sub(r'(?i)&lt;', '<', html)
    html = re.sub(r'(?i)&quot;', '"', html)
    html = re.sub(r'&#8220;', '“', html)
    html = re.sub(r'&#8221;', '”', html)
    html = re.sub(r'&#8216;', '‘', html)
    html = re.sub(r'&#8217;', '’', html)
    html = re.sub(r'(?i)<br[ /]*>', '\n', html)
    html = re.sub(r'(?s)<!--.*?--\s*>', ' ', html)
    html = re.sub(r'(?i)<ref[^>]*>[^>]*</ ?ref>', ' ', html)
    html = re.sub(r'(?s)<.[^<]*?>', ' ', html)
    return html


def extract_content(html_content):
    """Extract entry-content and ALL comments, clean and return text."""
    soup = BeautifulSoup(html_content, 'lxml')

    # Extract entry-content
    entry_content = soup.find('div', class_='entry-content')
    entry_text = ""
    if entry_content:
        entry_html = str(entry_content)
        entry_text = unhtml(entry_html)

    # Extract ALL comments
    comment_contents = soup.find_all('section', class_='comment__content')
    all_comments = []

    for i, comment_content in enumerate(comment_contents, 1):
        comment_html = str(comment_content)
        comment_text = unhtml(comment_html)
        all_comments.append(f"\n\n{comment_text}")

    # Combine with separator
    comments_section = '\n\n'.join(all_comments)
    final_text = f"{entry_text}\n\n{comments_section}"

    return final_text

# Usage in loop:
os.makedirs('texts', exist_ok=True)

def convert_file(filename):
    if not filename.endswith('.html'):
        return

    with open(f'articles/{filename}', 'r', encoding='utf-8') as f:
        html_content = f.read()

    clean_text = extract_content(html_content)
    txt_filename = filename.replace('.html', '.txt')
    with open(f'texts/{txt_filename}', 'w', encoding='utf-8') as f:
        f.write(clean_text)

    print(f"Converted: {filename} -> texts/{txt_filename}")

for file in os.listdir('articles'):
    convert_file(file)


#-------------------------------------------
# Dump all of them into one
#-------------------------------------------
from pathlib import Path
import sys

indir = Path("texts")
out_file_name = "eemaata.txt" if len(sys.argv) == 1 else sys.argv[1]

with open(out_file_name, 'w', encoding='utf-8') as fout:
    for file in indir.glob("*.txt"):
        fout.write(file.read_text(encoding='utf-8'))
        fout.write('\x1e')     # Record Seperator
