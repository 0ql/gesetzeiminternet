from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
import requests
import re

with open("./links.txt") as f:
    lines = f.readlines()

def get(route):
    route = route.replace('\n', '')
    url = f"https://www.gesetze-im-internet.de/{route.replace('./', '')}"
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    h2 = soup.find('h2', attrs={'class': 'headline'})
    a = h2.find_all('a', href=True)[0];
    href = a.get('href')
    uurl = f"https://www.gesetze-im-internet.de/{route.replace('./', '').replace('index.html', '')}{href}"
    print(uurl)
    rr = requests.get(uurl)
    souse = BeautifulSoup(rr.text, 'html.parser')
    div = souse.find('div', attrs={'id': 'paddingLR12'})
    div = str(div)
    div = re.sub('<a href=".*">Nichtamtliches Inhaltsverzeichnis</a>', '', div)
    with open(f"./htmls/{route.replace('./', '').replace('/index.html','')}.html", "w") as f:
        f.write(div)

# get(lines[0])
pool = ThreadPool(8)

pool.map(get, lines)
