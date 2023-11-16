import os
import sys
from common.log_util import Logs
from global_logger.bb1 import BB1
from global_logger.bb2 import BB2


# logger = Logs().get_logger(os.path.basename(__file__))
logger = Logs().get_logger('aa')


class CC:
    def __init__(self):
        logger.debug("Debug CC")

    def run_cc(self):
        logger.debug("Debug Running CC")
        # logger.info("Info Running CC")

        bb1 = BB1()
        bb1.run_bb1()

        bb2 = BB2()
        bb2.run_bb2()


if __name__ == '__main__':
    cc = CC()
    cc.run_cc()
