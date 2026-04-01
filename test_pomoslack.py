# coding=utf8
import sys
import unittest
from unittest.mock import patch

import pomoslack


class TestGetArgs(unittest.TestCase):
    def test_default_args(self):
        with patch('sys.argv', ['pomoslack.py']):
            with patch('pomoslack.get_message', return_value=':tomato:'):
                args = pomoslack.get_args()
                self.assertFalse(args.init)
                self.assertFalse(args.list)
                self.assertFalse(args.aggregate)
                self.assertEqual(args.sec, 0)
                self.assertEqual(args.min, 25)
                self.assertEqual(args.text, ':tomato:')

    def test_init_flag(self):
        with patch('sys.argv', ['pomoslack.py', '-i']):
            with patch('pomoslack.get_message', return_value=':tomato:'):
                args = pomoslack.get_args()
                self.assertTrue(args.init)

    def test_list_flag(self):
        with patch('sys.argv', ['pomoslack.py', '-l']):
            with patch('pomoslack.get_message', return_value=':tomato:'):
                args = pomoslack.get_args()
                self.assertTrue(args.list)

    def test_aggregate_flag(self):
        with patch('sys.argv', ['pomoslack.py', '-a']):
            with patch('pomoslack.get_message', return_value=':tomato:'):
                args = pomoslack.get_args()
                self.assertTrue(args.aggregate)

    def test_min_flag(self):
        with patch('sys.argv', ['pomoslack.py', '-m', '60']):
            with patch('pomoslack.get_message', return_value=':tomato:'):
                args = pomoslack.get_args()
                self.assertEqual(args.min, 60)

    def test_sec_flag(self):
        with patch('sys.argv', ['pomoslack.py', '-s', '300']):
            with patch('pomoslack.get_message', return_value=':tomato:'):
                args = pomoslack.get_args()
                self.assertEqual(args.sec, 300)

    def test_text_flag(self):
        with patch('sys.argv', ['pomoslack.py', '-t', 'hello']):
            with patch('pomoslack.get_message', return_value=':tomato:'):
                args = pomoslack.get_args()
                self.assertEqual(args.text, 'hello')

    def test_long_init_flag(self):
        with patch('sys.argv', ['pomoslack.py', '--init']):
            with patch('pomoslack.get_message', return_value=':tomato:'):
                args = pomoslack.get_args()
                self.assertTrue(args.init)

    def test_long_list_flag(self):
        with patch('sys.argv', ['pomoslack.py', '--list']):
            with patch('pomoslack.get_message', return_value=':tomato:'):
                args = pomoslack.get_args()
                self.assertTrue(args.list)

    def test_long_aggregate_flag(self):
        with patch('sys.argv', ['pomoslack.py', '--aggregate']):
            with patch('pomoslack.get_message', return_value=':tomato:'):
                args = pomoslack.get_args()
                self.assertTrue(args.aggregate)


if __name__ == '__main__':
    unittest.main()
