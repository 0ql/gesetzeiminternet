from multiprocessing.dummy import Pool as ThreadPool
import requests
import zipfile
import io

with open("./links.txt") as f:
    lines = f.readlines()

def get(route):
    route = route.replace('\n', '')
    url = f"https://www.gesetze-im-internet.de/{route.replace('./', '').replace('index.html','xml.zip')}"
    print(url)
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("./out")

pool = ThreadPool(8)

pool.map(get, lines)
