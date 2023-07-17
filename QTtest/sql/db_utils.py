from logger import Logs, logging
from operator import methodcaller

logger = Logs().get_logger('db_utils')
logger.setLevel(logging.DEBUG)


class DbConfig:
    def __init__(self, config_file):
        options = self.get_options(config_file)
        self.host = options['host']
        self.port = options['port']
        self.user = options['user']
        self.database = options['database']
        self.passwd = options['password']

    def get_options(self, file_path="config"):
        try:
            with open(file_path, 'r') as fd:
                # strip lines
                lines = map(methodcaller("strip"), fd.readlines())
                # filtering lines starting with '#' or blank lines
                lines_filtered = filter(lambda l: l and not l.startswith("#"), lines)
                # parsing
                words_iter = map(methodcaller("split", "="), lines_filtered)
                # converting map obj to dict
                options = {k.strip(): v.strip() for k, v in words_iter}

        except Exception as e:
            print(e)
            exit(0)

        return options