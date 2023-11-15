import logging, os, sys


def _init_logger():
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s')
    handler.setFormatter(formatter)
    handler.addFilter(lambda record: record.version > 5 or record.levelno >= logging.ERROR)

    logger.addHandler(handler)


_init_logger()
_logger = logging.LoggerAdapter(logging.getLogger('app'), {'version': 6})
_logger.info('App started in %s', os.getcwd())
