import requests
from bs4 import BeautifulSoup

links = ""

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789":
    r = requests.get("https://www.gesetze-im-internet.de/Teilliste_" + letter + ".html")

    soup = BeautifulSoup(r.text, 'html.parser')

    div = soup.find('div', attrs={'id': 'paddingLR12'}).find_all('p')

    for p in div:
        links += p.a.get('href') + '\n'

with open('links.txt', 'w') as f:
    f.write(links)
