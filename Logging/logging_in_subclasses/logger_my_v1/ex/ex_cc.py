import sys
import pathlib
from global_logger.cc import CC


sys.path.append(pathlib.Path(__file__).parents[1])


def ex_cc():
    cc = CC()
    cc.run_cc()


if __name__ == '__main__':
    ex_cc()
