from global_logger.cc import CC
from class_logger.qq import QQ


def main():
    cc = CC()
    cc.run_cc()

    qq = QQ()
    qq.run_qq()


if __name__ == '__main__':
    main()
