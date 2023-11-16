import logging, logging.config
import yaml


class LogMixin:
    __loggerConfigured = False

    @property
    def logger(self):
        if not self.__loggerConfigured:
            with open('log_config.yaml', 'rt') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                logging.config.dictConfig(config)
                print("logging config applied")
            self.__loggerConfigured = True
        name = '.'.join([self.__class__.__name__])
        return logging.getLogger(name)
