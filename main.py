import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from database import Base,session,engine
from models.autoria_item import Autoria_item, Phone, Car
import re
from multiprocessing import Pool



def create_db(engine):
    Base.metadata.create_all(engine)

def get_source_html(url):
    '''try:
        driver.get(url)
        driver.implicitly_wait(20)
        #driver.find_element_by_css_selector("a.phone_show_link").click()
        source = driver.page_source
    except Exception as ex:
        return False

    else:
        return source'''

    headers = {
        'Host': 'auto.ria.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:93.0) Gecko/20100101 Firefox/93.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec - Fetch - User': '?1',
        'Te': 'trailers'
    }
    r = requests.get(url, headers=headers, verify=True)
    return r.text

def get_soup_object(url):
    try:
        sourse = get_source_html(url)
        soup = BeautifulSoup(sourse, "lxml")
    except Exception as ex:
        print("Soup object creation failed")
        return False

    else:
        return soup

def get_seller_info(source):
    response = {}
    try:
        soup = BeautifulSoup(source, "lxml")
        item = soup.find("span", "phone bold")
        phone = re.sub('\D', '', item.attrs['data-phone-number'])
        phone = f"38{phone}"

        try:
            name = soup.find("h4", "seller_info_name bold").text.strip()
        except Exception as ex:
            name = "-"
        try:
            price = soup.find("div", "price_value").find("strong").text.strip()
            price = int(re.sub('\D', '', price))
        except Exception as ex:
            price = "0"
        try:
            car = soup.find("h3", "auto-content_title").text.strip()
        except Exception as ex:
            car = "-"
        try:
            temp = str(soup.find("span", "state-num")).split('<')
            temp = temp[1].split('>')
            number = temp[1]

        except Exception as ex:
            number = "-"
        try:
            vin = soup.find("span", "label-vin").text.strip()
        except Exception as ex:
            vin = "-"

        try:
            #km = int(soup.find_all("div", "technical-info")[2].find("span", "argument").text.split(" ")[0])*1000
            km = int(soup.find("div", "base-information bold").find("span", "size18").text.strip())
            km *= 1000
        except Exception as ex:
            km = 0

        try:
            city = soup.find('div', 'breadcrumbs size13').find_all('div','item')[2].text.strip()
        except Exception as ex:
            city = "-"



        response = {
            'name': name,
            'phone': phone,
            'price' : price,
            'car': car,
            'regnum':number,
            'vin':vin,
            'km':km,
            'city':city
        }


    except Exception as ex:
        return False

    finally:
        return response

def get_brand_numbered_list(url, max_page_num):
    soup = get_soup_object(url)
    items = soup.find_all("a", "item-brands")
    brand_urls = []
    for item in items:
        brand_urls.append(item.attrs['href'].strip())

    print(f"{len(brand_urls)} brands finded")
    brand_urls_numbered = {}
    for url in tqdm(brand_urls):
        soup = get_soup_object(url)
        try:
            pager_len = soup.find("span", "page-item mhide text-c").find_next().find("a", "page-link").text
        except Exception as ex:
            pager_len = 3
        if(int(pager_len)>int(max_page_num)):
            pager_len=max_page_num
        brand_urls_numbered[url] = pager_len

    return brand_urls_numbered

def get_car_link_list(source):
    link_list = []
    try:
        soup = BeautifulSoup(source, "lxml")
        items = soup.find_all("a", "address")
        for item in items:
            link_list.append(item.attrs['href'])

    except Exception as ex:
        print(ex)
        return False
    else:
        return link_list

def filter_links(links):

    filtered_links = []
    item_ids = []
    for link in links:
        link_data = link.split("_")
        item_ids.append(link_data[len(link_data) - 1].replace('.html', ''))

    exist_ids = session.query(Autoria_item.item_id).filter(Autoria_item.item_id.in_(item_ids)).all()

    item_ids = set(item_ids)
    exist_ids = set(exist_ids)

    filtered_ids = list(item_ids.difference(exist_ids))

    for link in links:
        link_data = link.split("_")
        link_item_id = link_data[len(link_data) - 1].replace('.html', '')

        if not re.search('newauto', link) and link_item_id in(filtered_ids):
            filtered_links.append(link)

    return filtered_links

def insert_phone_to_db(phone):


    res = session.query(Phone.phone_id).filter(Phone.phone_id == phone).one()
    print(res)

    if len(res['rows'])>0:
        res = res['rows'][0].get('id')

    else:
        sql = f"INSERT INTO tel(id,tel) VALUES(NULL,'{phone}')"
        print(sql)
        db.executeSQL(sql)
        res = db.lastInsertId()
        return res
    return res

def insert_car_to_db(car):

def get_seller(link):
    sourse = get_source_html(link)
    if sourse:
        seller = get_seller_info(sourse)
        if len(seller) > 0 and seller.get('phone'):
            link_data = link.split("_")
            item_id = link_data[len(link_data)-1].replace('.html','')
            seller['tel_id'] = insert_phone_to_db(seller.get('phone'))
            seller['item_url'] = link
            seller['item_id'] = item_id
            return seller
        else:
            return False
    else:
        return False

def get_seller_multiprocess(link):
    seller = get_seller(link)
    print(seller)
    if seller:
        insert_seller_info_to_db(seller)

def get_seller_info_by_brand(brand_url,page_num):
    print(f"Start parsing {brand_url}, {page_num} pages")

    for i in tqdm(range(1, int(page_num) + 1)):
        if i == 1:
            brand_current_url = brand_url
        else:
            brand_current_url = brand_url + '?page=' + str(i)
        sourse = get_source_html(brand_current_url)
        links = get_car_link_list(sourse)


        filtered_links = filter_links(links)
        if len(filtered_links)>0:
            p = Pool(processes=len(filtered_links))
            try:
                p.map(get_seller_multiprocess,filtered_links)
            except Exception as ex:
                print(ex)
                print("Multiprocessing error, remaking Pool")
            p.terminate()
        else:
            continue

    return True

def test_function():
    phone = Phone()

def main():
    create_db(engine)
    url = "https://auto.ria.com/uk/car/"
    max_page_num = 20
    #brand_list = get_brand_numbered_list(url,max_page_num)

    #get_seller_info_by_brand('https://auto.ria.com/uk/car/volkswagen/',1)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("work")
    main()
