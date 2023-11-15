import os
import sys
import logging


def _init_logger():
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


_init_logger()
_logger = logging.getLogger('app')

_logger.info('App started in %s', os.getcwd())