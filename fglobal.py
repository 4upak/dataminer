import tqdm
from database import Base,session,engine
from models.proxy import Proxy
import random

def checking_proxy(proxy):
    import requests
    result = False
    if proxy['type'] == 'socks5':
        try:
            requests.get('https://google.com',proxies=dict(
                    https=f'{proxy["type"]}://{proxy["login"]}:{proxy["pass"]}@{proxy["ip"]}:{proxy["port"]}',
                    http=f'{proxy["type"]}://{proxy["login"]}:{proxy["pass"]}@{proxy["ip"]}:{proxy["port"]}'
                ),verify=True, timeout=20)
            result = True
        except Exception as ex:
            result = False
    return result

def check_proxy():
    f = open("proxy.txt", "r+")
    lines = f.readlines()
    f.close()
    proxy_list = []
    for line in lines:
        proxy_data = line.strip().split(':')
        proxy = dict()
        proxy['type'] = proxy_data[0]
        proxy['ip'] = proxy_data[1]
        proxy['port'] = proxy_data[2]
        proxy['login'] = proxy_data[3]
        proxy['pass'] = proxy_data[4]
        proxy_list.append(proxy)
    final_proxi_list = []


    for proxy in proxy_list:
        if checking_proxy(proxy) == True:
            final_proxi_list.append(proxy)

    session.query(Proxy).delete()
    session.commit()
    for proxy in final_proxi_list:
        text = f"{proxy['type']}:{proxy['ip']}:{proxy['port']}:{proxy['login']}:{proxy['pass']}\n"
        proxy_class = Proxy(text)
        session.add(proxy_class)
        session.flush()
    session.commit()

    return final_proxi_list

def read_proxy():
    proxy_list = session.query(Proxy).all()
    return proxy_list

def get_one_proxy():

    proxies = read_proxy()
    if len(proxies)>0:
        proxy = proxies[random.randint(0, len(proxies) - 1)]
        return proxy
    else:
        return False



