from global_logger.cc import CC
from class_logger.qq import QQ
from common.log_util import Logs


def main():
    logger = Logs().get_logger('cl')

    cc = CC()
    cc.run_cc()

    qq = QQ()
    qq.run_qq()

    try:
        a = 1/0
        print(a)
    except Exception as e:
        logger.debug("division error %s", e)



if __name__ == '__main__':
    main()
