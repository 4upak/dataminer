import sys
import getopt
from fglobal import check_proxy, read_proxy


def main(argumentList):
    options = "a:h:"
    print('Checking proxies')
    check_proxy()
    print(f'We have {len(read_proxy())} valid proxies in proxy list')

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
                    from ftelethon import get_telergam_account
                    print(get_telergam_account())


    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

# Press the green button in thepython  gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
