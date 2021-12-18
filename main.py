import sys
import getopt
from fglobal import check_proxy, read_proxy
import time


def update_proxy_list():
    print('Checking proxies')
    check_proxy()
    print(f'We have {len(read_proxy())} valid proxies in proxy list')

def main(argumentList):
    options = "a:h:"
    long_options = []

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-a", "-action", "-act"):
                if currentValue == "base":
                    from autoria import get_all_base
                    from fglobal import check_proxy
                    check_proxy()
                    get_all_base()

                elif currentValue == "test":
                    from database import Base, session, engine
                    from models.autoria_item import Autoria_item, Phone, Car
                    from models.telegram_account import Telegram_account
                    acc = session.query(Telegram_account).filter(Telegram_account.telegram_user_id == 2046141639).first()

                    print(acc.restricted)


                elif currentValue == "update":
                    from autoria import update_base
                    from fglobal import check_proxy
                    check_proxy()
                    update_base()

                elif currentValue == "check_proxy":
                    from fglobal import check_proxy
                    check_proxy()

                elif currentValue == "telegram":
                    from ftelethon import get_account_from_db, get_client,update_account_id,create_telegram_accounts_in_db, autorespond, leave_all_chats
                    create_telegram_accounts_in_db()
                    account_from_db = get_account_from_db()

                    account = account_from_db
                    client = get_client(account)
                    leave_all_chats(client)
                    me = client.get_me()

                    update_account_id(me,account)

                    autorespond(client)

                elif currentValue == "accounts":
                    from ftelethon import get_account_from_db, get_client, update_account_id, create_telegram_accounts_in_db, autorespond, leave_all_chats

                elif currentValue == "create_base":
                    from models.autoria_item import Autoria_item
                    from models.phone import Phone
                    from models.car import Car
                    from models.dialog import Telegram_dialog
                    from models.proxy import Proxy
                    from models.telegram_account import Telegram_account
                    from database import Base, session, engine
                    Base.metadata.create_all(engine)




    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

# Press the green button in thepython  gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
