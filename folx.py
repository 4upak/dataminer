import requests
from bs4 import BeautifulSoup
import lxml
import time
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm
from database import Base,session,engine
s = requests.Session()



headers = {
    #':authority': 'www.amazon.com',
    #':method': 'GET',
    #':path': '/s?k=coloring+book+for+kids&i=stripbooks&crid=WWQM0O8Q5990&sprefix=coloring+book+for+kids%2Cstripbooks%2C159&ref=nb_sb_noss',
    #':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,de;q=0.7,uk;q=0.6,ar;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': 'aws-target-data=%7B%22support%22%3A%221%22%7D; regStatus=pre-register; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C18958%7CMCMID%7C73494010306973363482678376048385614495%7CMCAAMLH-1638536359%7C6%7CMCAAMB-1638536359%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1637938760s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; aws-target-visitor-id=1637931560074-887674.37_0; session-id=132-7793712-0990708; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=134-2645104-6346019; session-token=Pswbl6QvDExjP7BQeoCUU5M9/kP6hvQpJP358iaz1cKrRXLDpXOGqQEQCa6qL1P3erxruTbb1GRG1bv4udpn/xaqjOirAo7LjbJKJSy4Iiw1lVJ1EEqBgt15cbulIfgNNan92OCe8NeRq+k8ouJYTkVMY6gqYLcAs5yH1bVFmIxqrqHo2E+0kODYHls+FHEt; skin=noskin; csm-hit=tb:s-GF1QW8H17FDSGNV63WGG|1640085425944&t:1640085429037&adb:adblk_no',
    'downlink': '10',
    'ect': '4g',
    'rtt': '50',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

url = "https://www.amazon.com/s?k=paint+for+painting+kids&crid=37W43PBWST8IN&sprefix=paint+for+painting+kids%2Caps%2C182&ref=nb_sb_noss"



parsed_url = urlparse(url)
file_name = parsed_url.query.split('&')[3].split('=')[1]

source = s.get(url,headers=headers, verify=True)
#print(source.text)
soup = BeautifulSoup(source.text, "lxml")
page_count = soup.find("span", "s-pagination-item s-pagination-disabled").text.strip()
print(page_count)
bsrs = soup.find_all('div', {'data-component-type': 's-search-result'})

lines = []

for elem in bsrs:
    lines.append(elem.get('data-asin') + "\n")

new_url = "https://www.amazon.com"+soup.find("a", "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator").get('href')

for i in range(2,int(page_count)):
    print(new_url)
    source = s.get(new_url, headers=headers, verify=True)
    soup = BeautifulSoup(source.text, "lxml")
    new_url = "https://www.amazon.com" + soup.find("a","s-pagination-item s-pagination-next s-pagination-button s-pagination-separator").get('href')
    bsrs = soup.find_all('div', {'data-component-type': 's-search-result'})
    for elem in bsrs:
        lines.append(elem.get('data-asin') + "\n")
    set_data = set(lines)
    print(len(set_data))



    time.sleep(3)
file = open(f"amazon.txt", "w+")
for line in lines:
    file.write(line+"\n")
file.close()

