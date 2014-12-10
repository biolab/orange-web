import os
import urllib.request
from bs4 import BeautifulSoup


base_url = 'http://orange.biolab.si/forum/'
base_dir = os.path.dirname(__file__)
queue = ['']
processed = {''}

def extract_links(soup):
    for link in soup.find_all('a'):
        href = link.get('href')

        if not href:
            continue

        if href.startswith('http'):
            yield href
        if href.startswith('/'):
            if href.startswith('/forum/'):
                href = href[7:]
            else:
                href = '#'
        if href.startswith('./'):
            href = href[2:]
        try:
            sid_idx = href.index('sid=')
            href = href[:sid_idx-1]
        except ValueError:
            pass
        if href == 'index.php':
            href = ''
        if href.startswith('search.php'):
            href = '#'
        if href.startswith('ucp.php'):
            href = '#'
        if href.startswith('posting.php'):
            href = '#'
        if href.startswith('mailto:'):
            href = '#'
        if href != '#':
            if '#' in href:
                href = href[:href.index('#')]
            yield href
        link['href'] = href.replace('?', '_qm_')


while queue:
    filename = queue.pop()
    url = base_url + filename
    print(url)
    path = os.path.join(base_dir, filename.replace('?', '_qm_') or 'index.php')

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
