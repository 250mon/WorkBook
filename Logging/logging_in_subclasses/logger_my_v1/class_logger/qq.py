import os
from common.log_util import Logs
from class_logger.pp1 import PP1
from class_logger.pp2 import PP2


# logger = Logs().get_logger(os.path.basename(__file__))
logger = Logs().get_logger('cl')


class QQ:
    def __init__(self):
        logger.debug("Debug CC")

    def run_qq(self):
        logger.debug("Debug Running QQ")
        # logger.info("Info Running QQ")

        pp1 = PP1()
        pp1.run_pp1()

        pp2 = PP2()
        pp2.run_pp2()


if __name__ == '__main__':
    qq = QQ()
    qq.run_qq()
