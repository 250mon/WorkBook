from mypackage.mymathlib import *
import unittest

math_obj = 0

def setUpModule():
    print("\nIn setUpModule()...")
    global math_obj
    math_obj = MyMathLib()

def tearDownModule():
    print("\nIn tearDownModule()...")
    global math_obj
    del math_obj


class TestClass10(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nIn setUpClass()...")
    def setUp(cls):
        print("\nIn setUp()...")

    def test_case01(self):
        print("\nIn test_case01()")
        self.assertEqual(math_obj.add(2, 5), 7)

    def test_case02(self):
        print("\nIn test_case02()")

    def tearDown(self):
        print("\nIn tearDown()...")

    @classmethod
    def tearDownClass(cls):
        print("\nIn tearDownClass()...")
