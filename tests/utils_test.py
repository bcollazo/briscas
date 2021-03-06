from __future__ import absolute_import
import unittest

from briscas.util import ask_for_input

import mock


class UtilsTest(unittest.TestCase):
    def test_ask_for_input_until_allows(self):
        d = {'times_called': 0}  # We use dictionary for 2-3 compat.

        def side_effect(arg):
            d['times_called'] += 1
            return 'bad_input' if d['times_called'] < 2 else 'a'

        input_mock = mock.Mock(side_effect=side_effect)
        i = ask_for_input('>>>', ['a', 'b'],
                          input_fn=input_mock)
        self.assertTrue(input_mock.called)
        self.assertEqual('a', i)

    def test_ask_exits(self):
        input_mock = mock.Mock(return_value='exit')
        exit_mock = mock.Mock()
        ask_for_input('>>>', ['a', 'b'],
                      input_fn=input_mock, exit_fn=exit_mock)
        self.assertTrue(exit_mock.called)


if __name__ == '__main__':
    unittest.main()
