import os
from common.log_util import Logs

# logger = Logs().get_logger(os.path.basename(__file__))
logger = Logs().get_logger('aa')


class AA:
    def __init__(self):
        logger.debug("Debug AA")

    def run_aa(self):
        logger.debug("Debug Running AA")
        # logger.info("Info Running AA")


if __name__ == '__main__':
    aa = AA()
    aa.run_aa()
