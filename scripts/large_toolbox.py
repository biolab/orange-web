import os
from bs4 import BeautifulSoup

path = 'build/html/'

with open(os.path.join(path, 'index.html'), 'r') as f:
    index = f.read()


def get_icon_path(file_path):
    with open(path + file_path, 'r') as f:
        widget_html = f.read()
    widget_soup = BeautifulSoup(widget_html, "html.parser")
    widget_icon = widget_soup.find("img")
    return os.path.normpath(os.path.join(os.path.dirname(file_path),
                                         widget_icon.get('src')))


soup = BeautifulSoup(index, "html.parser")
div = soup.find("div", {"id": "widgets"})
for li in div.find_all("li"):
    a = li.find("a")
    new_tag = soup.new_tag("a", href=a.get('href'))
    new_tag.insert(0, soup.new_tag("img",
                                   src=get_icon_path(a.get("href")),
                                   alt=a.string))
    li.insert(0, new_tag)

h1 = div.find("h1")
h1.decompose()

html = div.prettify("utf-8")
with open(os.path.join(path, 'widgets.html'), 'wb') as f:
    f.write(html)

style = """
#widgets li a {
    color: #F8A842;
    display: block;
}

#widgets img {
    border-radius: 100%;
    box-shadow: 0px 0px 5px #888;
    vertical-align: middle;
    margin: 16px;
    height: 50px;
    width: 50px;
}

#widgets #data img {
    background: transparent radial-gradient(#FFDEB7 0%, #FFDCB5 50%, #FFC178 100%) repeat scroll 0% 0%;
}

#widgets #visualize img {
    background: transparent radial-gradient(#FFC9C5 0%, #FFC9C5 50%, #FF9991 100%) repeat scroll 0% 0%;
}

#widgets #classify img {
    background: transparent radial-gradient(#FAD0E2 0%, #FAD0E2 50%, #FAA8CA 100%) repeat scroll 0% 0%;
}

#widgets #regression img {
    background: transparent radial-gradient(#EBCBFB 0%, #EBCBFB 50%, #DB9FFB 100%) repeat scroll 0% 0%;
}

#widgets #evaluation img {
    background: transparent radial-gradient(#CFF3F3 0%, #CFF3F3 50%, #ADF3F3 100%) repeat scroll 0% 0%;
}

#widgets #unsupervised img {
    background: transparent radial-gradient(#D4E5EF 0%, #D4E5EF 50%, #BBD8E9 100%) repeat scroll 0% 0%;
}

#widgets li.toctree-l1 {
    display: inline-block;
    min-height: 120px;
    min-width: 190px;
    float: left;
    text-align: center;
    vertical-align: bottom;
}

#widgets ul {
    max-width: 760px;
    overflow: auto;
}
"""

with open(os.path.join(path, 'widgets_style.css'), 'w') as f:
    f.write(style)
