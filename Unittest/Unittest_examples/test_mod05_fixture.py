import unittest


def setUpModule():
    """called once, before anything else in this module"""
    print("\nIn setUpModule()...")

def tearDownModule():
    """called once, after everything else in this module"""
    print("\nIn tearDownModule()...")


class TestClass06(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """called once, before any test"""
        print("\nIn setUpClass()...")

    @classmethod
    def tearDownClass(cls):
        """called once, after all tests, if setUpClass successful"""
        print("\nIn tearDownClass()...")

    def setUp(self):
        """called multiple times, before every test method"""
        print("\nIn setUp()...")

    def tearDown(self):
        """called multiple times, after every test method"""
        print("\nIn tearDown()...")

    def test_case01(self):
        self.assertTrue("PYTHON".isupper())
        print("\nIn test_case01()")

    def test_case02(self):
        self.assertTrue("python".islower())
        print("\nIn test_case02()")


if __name__ == '__main__':
    unittest.main()
