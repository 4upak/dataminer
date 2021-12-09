import json
from os import walk

def get_account_info(accont):
    try:
        f = open(f"taccounts/{accont}.json", "r")
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


def get_telergam_account():
    dir_name = 'taccounts'
    sessions = []
    for (dirpath, dirnames, filenames) in walk(dir_name):
        for file in filenames:
            file_data = file.split('.')
            if file_data[1]=='session':
                sessions.append(file_data[0])
    return sessions


