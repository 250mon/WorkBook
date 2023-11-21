import unittest
from unittest.mock import patch
import inspect
from employee import Employee


class TestEmployee(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print('\nsetUpClass')

    @classmethod
    def tearDownClass(cls) -> None:
        print('tearDownClass')

    def setUp(self):
        print('\nsetUp')
        self.emp_1 = Employee('Corey', 'Schafer', 50000)
        self.emp_2 = Employee('Sue', 'Smith', 60000)
        pass

    def tearDown(self):
        print('tearDown')
        pass

    def test_email(self):
        print('Running ' + inspect.stack()[0][3])
        self.assertEqual(self.emp_1.email, 'Corey.Schafer@email.com')
        self.assertEqual(self.emp_2.email, 'Sue.Smith@email.com')

    def test_fullname(self):
        print('Running ' + inspect.stack()[0][3])
        self.assertEqual(self.emp_1.fullname, 'Corey Schafer')
        self.assertEqual(self.emp_2.fullname, 'Sue Smith')

        self.emp_1.first = 'John'
        self.emp_2.first = 'Jane'

        self.assertEqual(self.emp_1.fullname, 'John Schafer')
        self.assertEqual(self.emp_2.fullname, 'Jane Smith')

    def test_apply_raise(self):
        print('Running ' + inspect.stack()[0][3])
        self.emp_1.apply_raise()
        self.emp_2.apply_raise()

        self.assertEqual(self.emp_1.pay, 52500)
        self.assertEqual(self.emp_2.pay, 63000)

    def test_monthly_schedule(self):
        with patch('employee.requests.get') as mocked_get:
            # True scenario
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = 'Success'

            schedule = self.emp_1.monthly_schedule('May')
            mocked_get.assert_called_with('http://company.com/Schafer/May')
            self.assertEqual(schedule, 'Success')

            # False scenario
            mocked_get.return_value.ok = False

            schedule = self.emp_2.monthly_schedule('June')
            mocked_get.assert_called_with('http://company.com/Smith/June')
            self.assertEqual(schedule, 'Bad Response!')


if __name__ == "__main__":
    unittest.main()