import json
from os import walk
from models.autoria_item import Autoria_item, Phone, Car
from models.telegram_account import Telegram_account
from database import session

def get_account_info(account):
    try:
        f = open(f"taccounts/{account}.json", "r")
        with f as read_file:
            return json.load(read_file)
    except Exception as ex:
        print(ex)
        return False

def save_account_info(accont):
    try:
        f = open(f"taccounts/{accont}.json", "r")
        with f as read_file:
            return json.load(read_file)
    except Exception as ex:
        print(ex)
        return False


def get_telergam_accounts():
    dir_name = 'taccounts'
    sessions = []
    for (dirpath, dirnames, filenames) in walk(dir_name):
        for file in filenames:
            file_data = file.split('.')
            if file_data[1]=='session':
                sessions.append(file_data[0])
    return sessions

def create_telegram_accounts():
    accounts = get_telergam_accounts()
    i = 0
    for account in accounts:
        data = get_account_info(account)
        data['telegram_user_id'] = 0
        tg = Telegram_account(account)
        session.add(tg)
        i+=1

    session.commit()
    if i==0:
        return false
    else:
        return i








