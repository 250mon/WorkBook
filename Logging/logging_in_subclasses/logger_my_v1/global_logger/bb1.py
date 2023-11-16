import os
from common.log_util import Logs
from global_logger.aa import AA

# logger = Logs().get_logger(os.path.basename(__file__))
logger = Logs().get_logger('aa')


class BB1(AA):
    def __init__(self):
        logger.debug("Debug BB1")

    def run_bb1(self):
        logger.debug("Debug Running BB1")
        # logger.info("Info Running BB1")

        self.run_aa()


if __name__ == '__main__':
    bb1 = BB1()
    bb1.run_aa()
    bb1.run_bb1()
