import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from database import Base,session,engine
from models.autoria_item import Autoria_item, Phone, Car
import re
from multiprocessing import Pool
from sqlalchemy.sql import func
import sys, getopt
import json


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
            'regnum':number.strip(),
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

def get_id_from_item_url(url):
    try:
        regxp = re.compile('_')
        if regxp.search(url):
            link_data = url.split("_")
            return int(link_data[len(link_data) - 1].replace('.html', ''))
        else:
            link_data = url.split("-")
            return int(link_data[len(link_data) - 1].replace('.html', ''))
    except Exception as ex:
        print(ex)
        return 0

def filter_links(links):
    filtered_links = []
    item_ids = []
    for link in links:
            item_ids.append(get_id_from_item_url(link))

    rows = session.query(Autoria_item.item_id).filter(Autoria_item.item_id.in_(item_ids)).all()
    exist_ids = []
    for row in rows:
        exist_ids.append(int(row.item_id))

    item_ids = set(item_ids)
    #print("\nitem_ids")
    #print(item_ids)


    exist_ids = set(exist_ids)
    #print("\nexist_ids")
    #print(exist_ids)


    filtered_ids = list(item_ids.difference(exist_ids))
    #print("\nfiltered_ids")
    #print(filtered_ids)

    for link in links:

        link_item_id = get_id_from_item_url(link)

        if not re.search('newauto', link) and link_item_id in(filtered_ids):
            filtered_links.append(link)

    result_list = []

    for link in filtered_links:
        if link not in result_list:
            result_list.append(link)


    return result_list

def get_phone_info(tel):
    pass

def insert_phone_to_db(tel):
    phone = Phone(tel)
    row = session.query(Phone.phone_id).filter(Phone.tel == tel).first()
    if row:
        phone.phone_id = row.phone_id
    else:
        try:
            session.add(phone)
            session.flush()
        except Exception as ex:
            print(ex)
    return phone.phone_id

def insert_car_to_db(vin,name,regnum):
    car = Car(vin,name,regnum)
    session.add(car)
    session.flush()
    return car.car_id

def get_seller(link):
    try:
        sourse = get_source_html(link)
        if sourse:
            seller = get_seller_info(sourse)
            if len(seller) > 0 and seller.get('phone'):
                link_data = link.split("_")
                item_id = link_data[len(link_data)-1].replace('.html','')
                seller['tel_id'] = insert_phone_to_db(seller.get('phone'))
                seller['car_id'] = insert_car_to_db(seller['vin'],seller['car'],seller['regnum'])
                seller['item_url'] = link
                seller['item_id'] = item_id

                autoria_item = Autoria_item(
                    link,
                    seller['item_id'],
                    seller['tel_id'],
                    seller['name'],
                    seller['price'],
                    seller['car_id'],
                    seller['km'],
                    seller['city'],
                    0
                )
                autoria_item.update_date = func.now()
                autoria_item.creation_date = func.now()
                session.add(autoria_item)
                session.commit()
                return True
            else:
                return False
        else:
            return False
    except Exception as ex:
        #print(ex)
        return False

def get_seller_multiprocess(link):
    try:
        get_seller(link)
    except Exception as ex:
        print(ex)

def get_seller_info_by_brand(brand_url,page_num):
    print(f"Start parsing {brand_url}, {page_num} pages")
    for i in tqdm(range(1, int(page_num) + 1)):
        if i == 1:
            brand_current_url = brand_url
        else:
            brand_current_url = brand_url + '?page=' + str(i)
        try:
            sourse = get_source_html(brand_current_url)
            links = get_car_link_list(sourse)
        except Exception as ex:
            print(ex)
            continue


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
    phone = 380939675735
    phone = '+'+str('+380939675735')
    pn = phonenumbers.parse(phone)
    print(pn)
    geo = region_code_for_number(pn)
    print(geo)

    operator = carrier.name_for_number(pn,geo)
    print(operator)

def get_all_base():
    create_db(engine)
    url = "https://auto.ria.com/uk/car/"
    max_page_num = 1000
    print('Creating brand_list')
    brand_list = get_brand_numbered_list(url, max_page_num)
    while 1:
        for (brand_url, page_num) in brand_list.items():
            get_seller_info_by_brand(brand_url, page_num)
        print('Parsing finished, reloading')

def get_statistic(item_id):
    data = {}
    try:
        views_url = f"https://auto.ria.com/bu/final_page/views/{item_id}"
        data['views'] = int(get_source_html(views_url).strip())
    except Exception as ex:
        print(ex)
        data['views'] = 0

    try:
        notepad_url = f"https://auto.ria.com/uk/demo/bu/notepad/auto/statistic/{item_id}/"
        json_data = json.loads(get_source_html(notepad_url))
        data['saved'] = json_data['addCount']
    except Exception as ex:
        data['saved'] = 0


    return data

def udpade_multiprocess(item):
    soup = get_soup_object(item.item_url)
    if soup.find("div", "sold-out"):
        item.sold = 1

    elif soup.find("div", id='autoDeletedTopBlock'):
        item.sold = 2

    stats = get_statistic(item.item_id)
    item.views = stats.get('views')
    item.saved = stats.get('saved')

    try:
        price = soup.find("div", "price_value").find("strong").text.strip()
        item.price = int(re.sub('\D', '', price))
    except Exception as ex:
        item.price = "0"


    session.add(item)
    session.commit()


def update_base():
    count = session.query(Autoria_item).count()
    print(f"{count} items finded")
    while 1:
        for i in tqdm(range(0,count,10)):
            items = session.query(Autoria_item).offset(i).limit(10).all()

            p = Pool(processes=len(items))
            try:
                 p.map(udpade_multiprocess, items)
            except Exception as ex:
                p.terminate()
        print("Base update finished, reload after 3600 seconds")
        time.sleep(3600)





