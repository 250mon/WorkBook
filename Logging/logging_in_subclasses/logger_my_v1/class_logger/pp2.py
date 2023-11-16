import os
from common.log_util import Logs
from class_logger.oo import OO

# logger = Logs().get_logger(os.path.basename(__file__))
logger = Logs().get_logger('cl')


class PP2(OO):

    def __init__(self):
        logger.debug("Debug PP2")

    def run_pp2(self):
        logger.debug("Debug Running PP2")
        # logger.info("Info Running PP2")

        self.run_aa()


if __name__ == '__main__':
    pp2 = PP2()
    pp2.run_aa()
    pp2.run_pp2()
