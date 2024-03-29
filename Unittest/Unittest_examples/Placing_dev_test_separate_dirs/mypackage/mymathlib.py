from lib import read_file


class MyMathLib:
    def __init__(self):
        """Constructor for this class..."""
        read_file.read_main_config()
        read_file.read_config()
        print("Creating object: " + self.__class__.__name__)

    def add(self, x, y):
        return(x + y)

    def mul(self, x, y):
        return (x * y)

    def sub(self, x, y):
        return (x - y)

    def div(self, x, y):
        return (x / y)

    def __del__(self):
        """Destructor for this class..."""
        print("Destroying object: " + self.__class__.__name__)
