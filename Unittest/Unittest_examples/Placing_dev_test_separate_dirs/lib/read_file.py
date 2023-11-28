def read_config():
    try:
        with open('lib/config.txt') as fd:
            options = fd.readlines()
            for option in options:
                print(option)
        return options
    except Exception as e:
        return e


def read_main_config():
    try:
        with open('main_config.txt') as fd:
            options = fd.readlines()
            for option in options:
                print(option)
        return options
    except Exception as e:
        return e


if __name__ == "__main__":
    read_config()