import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sql
import config
import re
from config import db_host, db_user, db_password, db_name
import pymysql.cursors
from sql import MySQL
from multiprocessing import Pool

db = MySQL(db_host, 3306, db_user, db_password, db_name)


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
            # km = int(soup.find_all("div", "technical-info")[2].find("span", "argument").text.split(" ")[0])*1000
            km = int(soup.find("div", "base-information bold").find("span", "size18").text.strip())
            km *= 1000
        except Exception as ex:
            km = 0

        try:
            city = soup.find('div', 'breadcrumbs size13').find_all('div', 'item')[2].text.strip()
        except Exception as ex:
            city = "-"

        response = {
            'name': name,
            'phone': phone,
            'price': price,
            'car': car,
            'regnum': number,
            'vin': vin,
            'km': km,
            'city': city
        }


    except Exception as ex:
        return False

    finally:
        return response


def get_car_link_list(source):
    link_list = []
    try:
        soup = BeautifulSoup(source, "lxml")
        items = soup.find_all("a", "address")
        for item in items:
            link_list.append(item.attrs['href'])

    except Exception as ex:
        return False
    finally:
        return link_list

def get_source_html(url, driver):
    try:
        driver.get(url)
        driver.implicitly_wait(20)
        # driver.find_element_by_css_selector("a.phone_show_link").click()
        source = driver.page_source
    except Exception as ex:
        return False

    else:
        return source

def get_web_driver_object(driver_path):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.headless = True
        options.add_argument('--disable-gpu')
        #options = Options()
        #options.headless = True

        driver = webdriver.Chrome(
            executable_path=driver_path,
            options=options
        )

        headers = {
            'user - agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'sec-fetch-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            ':scheme': 'https',
            ':path': '/uk/auto_hyundai_sonata_31308146.html',
            ':authority': 'auto.ria.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en-US;q=0.9,en;q=0.8,de;q=0.7,uk;q=0.6,ar;q=0.5',
            'cache-control': 'max-age=0'
        }

    except Exception as ex:
        print("Driver object creation failed")
        print(ex)
        return False

    else:
        return driver

def get_soup_object(url, driver):
    try:
        sourse = get_source_html(url, driver)
        soup = BeautifulSoup(sourse, "lxml")
    except Exception as ex:
        print("Soup object creation failed")
        return False

    else:
        return soup

def get_brand_numbered_list(driver):
    url = "https://auto.ria.com/uk/car/"
    soup = get_soup_object(url, driver)
    items = soup.find_all("a", "item-brands")
    brand_urls = []

    for item in items:
        brand_urls.append(item.attrs['href'].strip())

    print(f"{len(brand_urls)} brands finded")
    brand_urls_numbered = {}
    c=10
    for url in brand_urls:
        soup = get_soup_object(url, driver)
        try:
            pager_len = soup.find("span", "page-item mhide text-c").find_next().find("a", "page-link").text
        except Exception as ex:
            pager_len = 3
        if c>10:
            brand_urls_numbered[url] = pager_len
        c+=1


    print(brand_urls_numbered)
    return brand_urls_numbered

def insert_phone_to_db(phone):
    global db
    sql = f"SELECT id from tel WHERE tel='{phone}'"
    res = db.executeSQL(sql)
    if len(res['rows']) > 0:
        res = res['rows'][0].get('id')
    else:
        sql = f"INSERT INTO tel(id,tel) VALUES('','{phone}')"
        while True:
            if db.is_connected():
                res = db.executeSQL(sql)
                break
            else:
                print("DB died, reconnecting")
                time.sleep(30)
                db = MySQL(db_host, 3306, db_user, db_password, db_name)
        res = db.lastInsertId()
        return res

def insert_seller_info_to_db(seller):
    global db
    sql = f"SELECT id from autoria_item WHERE item_id='{seller['item_id']}'"
    res = db.executeSQL(sql)

    if len(res['rows']) > 0:
        print(f"Item already exist, id:{str(res['rows'])}")
        res = res['rows'][0].get('id')
    else:
        sql = f"INSERT INTO autoria_item(" \
              f"id," \
              f"item_url," \
              f"item_id," \
              f"tel_id," \
              f"name," \
              f"car," \
              f"price," \
              f"vin," \
              f"regnum," \
              f"km," \
              f"city," \
              f"comment" \
              f") " \
              f"VALUES(" \
              f"''," \
              f"'{db.escapeString(seller['item_url'])}'," \
              f"'{db.escapeString(seller['item_id'])}'," \
              f"'{db.escapeString(seller['tel_id'])}'," \
              f"'{db.escapeString(seller['name'])}'," \
              f"'{db.escapeString(seller['car'])}'," \
              f"'{db.escapeString(seller['price'])}'," \
              f"'{db.escapeString(seller['vin'])}'," \
              f"'{db.escapeString(seller['regnum'])}'," \
              f"'{db.escapeString(seller['km'])}'," \
              f"'{db.escapeString(seller['city'])}'," \
              f"'') "
        print(sql)
        while True:
            if db.is_connected():
                res = db.executeSQL(sql)
                break
            else:
                print("DB died, reconnecting")
                time.sleep(30)
                db = MySQL(db_host, 3306, db_user, db_password, db_name)
        res = db.lastInsertId()

        return res

def get_seller(link, driver):
    print(link)
    sourse = get_source_html(link, driver)
    if sourse:
        seller = get_seller_info(sourse)
        if len(seller) > 0 and seller.get('phone'):
            link_data = link.split("_")
            item_id = link_data[len(link_data) - 1].replace('.html', '')
            seller['tel_id'] = insert_phone_to_db(seller.get('phone'))
            seller['item_url'] = link
            seller['item_id'] = item_id
            return seller
        else:
            return False
    else:
        return False

def get_seller_multiprocess(link):
    mdriver = get_web_driver_object("/Users/serg/Desktop/python/chromedriver")
    seller = get_seller(link, mdriver)
    print(seller)
    if seller:
        insert_seller_info_to_db(seller)
    mdriver.close()
    mdriver.quit()

def get_seller_info_by_brand(brand_url, page_num, driver):
    global db
    for i in range(1, int(page_num) + 1):
        if i == 1:
            brand_current_url = brand_url
        else:
            brand_current_url = brand_url + '?page=' + str(i)
        print(brand_current_url)
        sourse = get_source_html(brand_current_url, driver)
        links = get_car_link_list(sourse)

        filtered_links = []
        for link in links:
            link_data = link.split("_")
            item_id = link_data[len(link_data) - 1].replace('.html', '')
            sql = f"SELECT id from autoria_item WHERE item_id='{item_id}'"
            db.conn.ping(reconnect=True)
            res = db.executeSQL(sql)
            if len(res['rows']) > 0:
                print(f"Itemmmm already exist, id:{str(res['rows'])}")
            else:
                filtered_links.append(link)
            time.sleep(1.5)

        print(f"starting multiprocess. Link list lenght: {len(filtered_links)}")

        if len(filtered_links) > 0:
            p = Pool(processes=3)
            try:
                p.map(get_seller_multiprocess, filtered_links)
            except Exception as ex:
                print(ex)
                print("Multiprocessing error, remaking Pool")
            p.terminate()
        else:
            continue

    return True


def main():
    driver = get_web_driver_object("/Users/serg/Desktop/python/chromedriver")

    brand_urls_numbered = get_brand_numbered_list(driver)
    for (brand_url, page_num) in brand_urls_numbered.items():
        brand_seller_list = get_seller_info_by_brand(brand_url, page_num, driver)

    # link = "https://auto.ria.com/uk/auto_volkswagen_touareg_31365937.html"
    # sourse = get_source_html(link, driver)
    # seller = get_seller_info(sourse)
    # print(seller)
    # id = insert_phone_to_db(seller.get('phone'))
    # print(id)

    driver.close()
    driver.quit()


if __name__ == "__main__":
    main()
