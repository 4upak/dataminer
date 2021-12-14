import sys
import getopt
from fglobal import check_proxy, read_proxy

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
                    from fglobal import read_proxy
                    check_proxy()

                elif currentValue == "update":
                    from autoria import update_base
                    from fglobal import check_proxy
                    check_proxy()
                    update_base()

                elif currentValue == "check_proxy":
                    from fglobal import check_proxy
                    check_proxy()

                elif currentValue == "telegram":
                    from ftelethon import get_account_from_db, get_client,update_account_id,create_telegram_accounts_in_db, autorespond
                    create_telegram_accounts_in_db()
                    account_from_db = get_account_from_db()
                    account = account_from_db[0]
                    client = get_client(account)
                    me = client.get_me()

                    update_account_id(me,account)

                    autorespond(client)





    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

# Press the green button in thepython  gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
