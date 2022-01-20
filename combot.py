import requests
import ast
from bs4 import BeautifulSoup
import json
import lxml
import time
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm
from database import Base,session,engine
s = requests.Session()

offset = 0
lines = []
while True:

    url = f"https://combot.org/api/chart/ru?limit=20&offset={offset}"
    s = requests.Session()
    source = s.get(url,verify=True)
    data = ast.literal_eval(source.text)

    data = json.loads(source.text)
    for row in data:
        lines.append(row['u'])

    offset +=20
    if offset>9600:
        break
    time.sleep(1)
    print(len(lines))

file = open(f"chats.txt", "w+")
for line in lines:
    file.write(line + "\n")
file.close()

