import os
import re
import urllib.request
from bs4 import BeautifulSoup


base_url = 'http://orange.biolab.si/forum/'
base_dir = os.path.dirname(__file__)

forum_url = re.compile('^/forum/|^./')
sid = re.compile('[\?\&]sid=[a-zA-Z0-9]+')
skip_urls = re.compile(
    '^search.php|^ucp.php|^posting.php|^mailto:|^/|^memberlist.php')


def escape_question_marks(s):
    return s.replace('?', '_qm_')


def extract_links(soup):
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href:
            continue

        if href.startswith('http'):
            yield href

        href = forum_url.sub('', href)
        href = sid.sub('', href)

        if skip_urls.match(href):
            href = '#'

        if href != '#':
            if '#' in href:
                href = href[:href.index('#')]
            yield href
        link['href'] = escape_question_marks(href)

queue = ['']
processed = {''}
while queue:
    filename = queue.pop()
    url = base_url + filename
    print(url)
    path = os.path.join(base_dir,
                        escape_question_marks(filename) or 'index.php')

    urllib.request.urlretrieve(url, path)

    with open(path) as f:
        soup = BeautifulSoup(f.read())

    for link in extract_links(soup):
        if link not in processed and not link.startswith('http'):
            queue.append(link)
            processed.add(link)

    with open(path, 'w') as f:
        f.write(str(soup))

stylesheet = os.path.join(base_dir, 'stylesheet.css')
urllib.request.urlretrieve(base_url + 'stylesheet.css', stylesheet)
with open(stylesheet, 'a') as f:
    f.write("""

#footer {
  display: None
}

form {
display: None
}
""")
