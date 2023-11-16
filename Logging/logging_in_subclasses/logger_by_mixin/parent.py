from base import Base


class Parent(Base):
    def __init__(self):
        self.logger.debug("Debug Parent")

    def run_parent(self):
        self.logger.debug("Debug Running Parent")
        self.logger.info("Info Running Parent")


if __name__ == '__main__':
    my_parent = Parent()
    my_parent.run_base()
    my_parent.run_parent()