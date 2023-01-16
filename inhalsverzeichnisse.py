import requests
from pathlib import Path
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

with open('./links.txt') as f:
    lines = f.readlines()

def extract(el):
    el = el.replace("./", "").replace("\n", "")
    sanitized = el.replace("/index.html", "")

    Path(f"./out/{sanitized}").mkdir(parents=True, exist_ok=True)

    url = f"https://www.gesetze-im-internet.de/{el}"
    r = requests.get(url)

    print(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    headline = soup.find('h1', attrs={'class': 'headline'})
    if headline == None:
        exit()
    table = soup.find('table')
    if table == None:
        exit()

    fetched_full_file = False
    for link in table.find_all('a', href=True): 
        # href: str = link.get('href')
        href: str = link['href']
        if '#' in href:
            continue
        uurl = f"https://www.gesetze-im-internet.de/{sanitized}/{href}"
        print(uurl)
        rr = requests.get(uurl)
        sause = BeautifulSoup(rr.text, 'html.parser')
        title = sause.find('h1')
        body = sause.find('div', attrs={'class': 'jnhtml'})

        with open(f"./out/{sanitized}/{href.replace('__', '').replace('html', 'astro')}", 'w') as f:
            f.write(f"""---
import Laws from "layouts/Laws.astro";
---
<Laws title="{sanitized}">
{str(title)}{str(body)}
</Laws>""")

    with open(f"./out/{el.replace('html', 'astro')}", 'w') as f:
        f.write(f"""---
import Laws from "layouts/Laws.astro";
---
<Laws title="{sanitized}">
<h1>{headline.text}</h1>{str(table).replace('__', '')}
</Laws>""")

    # evt. kuerzel extrachieren

# extract("aabgebv/index.html")
pool = ThreadPool(8)

pool.map(extract, lines[0:10])
