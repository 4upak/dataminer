import tqdm

def checking_proxy(proxy):
    import requests
    result = False
    if proxy['type'] == 'socks5':
        try:
            requests.get('https://google.com',proxies=dict(
                    https=f'{proxy["type"]}://{proxy["login"]}:{proxy["pass"]}@{proxy["ip"]}:{proxy["port"]}',
                    http=f'{proxy["type"]}://{proxy["login"]}:{proxy["pass"]}@{proxy["ip"]}:{proxy["port"]}'
                ),verify=True, timeout=5)
            result = True
        except Exception as ex:
            result = False
    return result


def check_proxy():
    f = open("proxy.txt", "r+")
    lines = f.readlines()
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
    f.seek(0)
    for proxy in proxy_list:
        if checking_proxy(proxy) == True:
            final_proxi_list.append(proxy)
            text = f"{proxy['type']}:{proxy['ip']}:{proxy['port']}:{proxy['login']}:{proxy['pass']}\n"
            f.write(text)
        else:
            print(f"{proxy['ip']} is not valid and deleted")
    f.truncate()
    f.close()
    f.close()

    return final_proxi_list


def read_proxy():
    f = open("proxy.txt", "r+")
    lines = f.readlines()
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
    f.close()
    return proxy_list