import os
from common.log_util import Logs
from class_logger.oo import OO

# logger = Logs().get_logger(os.path.basename(__file__))
logger = Logs().get_logger('cl')


class PP1(OO):
    def __init__(self):
        logger.debug("Debug PP1")

    def run_pp1(self):
        logger.debug("Debug Running PP1")
        # logger.info("Info Running PP1")

        self.run_aa()


if __name__ == '__main__':
    pp1 = PP1()
    pp1.run_aa()
    pp1.run_pp1()
