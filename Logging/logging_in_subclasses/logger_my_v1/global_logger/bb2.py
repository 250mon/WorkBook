import os
from common.log_util import Logs
from global_logger.aa import AA

# logger = Logs().get_logger(os.path.basename(__file__))
logger = Logs().get_logger('aa')


class BB2(AA):

    def __init__(self):
        logger.debug("Debug BB2")

    def run_bb2(self):
        logger.debug("Debug Running BB2")
        # logger.info("Info Running BB2")

        self.run_aa()


if __name__ == '__main__':
    bb2 = BB2()
    bb2.run_aa()
    bb2.run_bb2()
