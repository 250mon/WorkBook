from log_mixin import LogMixin


class Base(LogMixin):
    def __init__(self):
        self.logger.debug("Debug Base")

    def run_base(self):
        self.logger.debug("Debug Running Base")
        self.logger.info("Info Running Base")


if __name__ == '__main__':
    my_base = Base()
    my_base.run_base()