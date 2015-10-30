import os
from bs4 import BeautifulSoup
import sys

path = sys.argv[1]
outfile = sys.argv[2]
webdocprefix = sys.argv[3]

with open(os.path.join(path, 'index.html'), 'r') as f:
    index = f.read()


def get_icon_path(file_path):
    with open(os.path.join(path,file_path), 'r') as f:
        widget_html = f.read()
    widget_soup = BeautifulSoup(widget_html, "html.parser")
    widget_icon = widget_soup.find("img")
    return os.path.normpath(os.path.join(os.path.dirname(file_path),
                                         widget_icon.get('src')))

soup = BeautifulSoup(index, "html.parser")
div = soup.find("div", {"id": "widgets"})

import json

ret = []

for li in div.find_all():
    if li.name == "h2":
        cat = li.text.strip("¶").strip()
        ret.append((cat, []))
    if li.name == "li":
        a = li.find("a")
        imglink = webdocprefix + get_icon_path(a.get("href"))
        doclink = webdocprefix + a.get('href')
        text = a.string
        ret[-1][1].append({"img": imglink, "doc": doclink, "text": text })
    
with open(outfile, 'wt') as f:
    f.write(json.dumps(ret))

