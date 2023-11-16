import os
from common.log_util import Logs

# logger = Logs().get_logger(os.path.basename(__file__))
logger = Logs().get_logger('cl')


class OO:
    def __init__(self):
        logger.debug("Debug OO")

    def run_aa(self):
        logger.debug("Debug Running OO")
        # logger.info("Info Running OO")


if __name__ == '__main__':
    oo = OO()
    oo.run_aa()
