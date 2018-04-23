import unittest

from briscas.main import main

import mock


class MainTest(unittest.TestCase):
    def test_main(self):
        print_mock = mock.Mock()
        input_mock = mock.Mock(return_value='1')
        main(print_fn=print_mock, input_fn=input_mock)


if __name__ == '__main__':
    unittest.main()
