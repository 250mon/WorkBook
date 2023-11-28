import unittest
from typing import List
from mypackage.mymathlib import *
from lib import read_file

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

    def setUp(self):
        print("\nIn setUp()...")

    def test_case01(self):
        print("\nIn test_case01()")
        self.assertEqual(math_obj.add(2, 5), 7)

    def test_case02(self):
        self.assertIsInstance(read_file.read_main_config(), List)
        print("\nIn test_case02()")

    def test_case03(self):
        self.assertIsInstance(read_file.read_config(), List)
        print("\nIn test_case03()")

    def tearDown(self):
        print("\nIn tearDown()...")

    @classmethod
    def tearDownClass(cls):
        print("\nIn tearDownClass()...")
