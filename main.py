import sys
import getopt
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
                    test_function()
                elif currentValue == "update":
                    from autoria import update_base
                    update_base()


    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

# Press the green button in thepython  gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
