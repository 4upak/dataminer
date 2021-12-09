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
                    get_all_base()
                elif currentValue == "test":
                    check_proxy()
                elif currentValue == "update":
                    from autoria import update_base
                    update_base()
                elif currentValue == "telegram":
                    from ftelethon import create_telegram_accounts
                    acc_num = create_telegram_accounts()
                    print(f"{acc_num} accounts created")



    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

# Press the green button in thepython  gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
