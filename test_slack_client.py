# coding=utf8
import configparser
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import slack_client


class TestGetIniPath(unittest.TestCase):
    def test_returns_path_ending_with_config_ini(self):
        path = slack_client.get_ini_path()
        self.assertTrue(path.endswith('config.ini'))

    def test_returns_absolute_path(self):
        path = slack_client.get_ini_path()
        self.assertTrue(os.path.isabs(path))


class TestExistsIni(unittest.TestCase):
    def test_returns_false_when_file_does_not_exist(self):
        with patch('slack_client.get_ini_path', return_value='/nonexistent/config.ini'):
            self.assertFalse(slack_client.exists_ini())

    def test_returns_true_when_file_exists(self):
        with tempfile.NamedTemporaryFile() as f:
            with patch('slack_client.get_ini_path', return_value=f.name):
                self.assertTrue(slack_client.exists_ini())


class TestGetToken(unittest.TestCase):
    def test_returns_empty_string_when_no_config(self):
        with patch('slack_client.exists_ini', return_value=False):
            self.assertEqual(slack_client.get_token(), '')

    def test_returns_bearer_token_when_config_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, 'config.ini')
            config = configparser.ConfigParser()
            config.add_section('slack')
            config.set('slack', 'token', 'xoxp-test-token')
            config.set('slack', 'message', ':tomato:')
            with open(tmpfile, 'w') as f:
                config.write(f)
            with patch('slack_client.exists_ini', return_value=True):
                with patch('slack_client.get_ini_path', return_value=tmpfile):
                    self.assertEqual(slack_client.get_token(), 'Bearer xoxp-test-token')


class TestGetMessage(unittest.TestCase):
    def test_returns_default_message_when_no_config(self):
        with patch('slack_client.exists_ini', return_value=False):
            self.assertEqual(slack_client.get_message(), ':tomato:')

    def test_returns_message_from_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, 'config.ini')
            config = configparser.ConfigParser()
            config.add_section('slack')
            config.set('slack', 'token', 'xoxp-test-token')
            config.set('slack', 'message', 'custom message')
            with open(tmpfile, 'w') as f:
                config.write(f)
            with patch('slack_client.exists_ini', return_value=True):
                with patch('slack_client.get_ini_path', return_value=tmpfile):
                    self.assertEqual(slack_client.get_message(), 'custom message')


class TestInit(unittest.TestCase):
    def test_valid_token_creates_config_and_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, 'config.ini')
            with patch('slack_client.get_ini_path', return_value=tmpfile):
                with patch('builtins.input', side_effect=['xoxp-valid-token', ':tomato:']):
                    with self.assertRaises(SystemExit) as cm:
                        slack_client.init()
                    self.assertEqual(cm.exception.code, 0)
                self.assertTrue(os.path.exists(tmpfile))

    def test_empty_message_defaults_to_tomato(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, 'config.ini')
            with patch('slack_client.get_ini_path', return_value=tmpfile):
                with patch('builtins.input', side_effect=['xoxp-valid-token', '']):
                    with self.assertRaises(SystemExit):
                        slack_client.init()
                config = configparser.ConfigParser()
                config.read(tmpfile)
                self.assertEqual(config.get('slack', 'message'), ':tomato:')

    def test_invalid_token_exits_with_code_one(self):
        with patch('builtins.input', side_effect=['invalid-token', '']):
            with self.assertRaises(SystemExit) as cm:
                slack_client.init()
            self.assertEqual(cm.exception.code, 1)


class TestDoListApi(unittest.TestCase):
    def test_returns_response_on_success(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {'ok': True, 'reminders': []}
        with patch('slack_client.requests.post', return_value=mock_response):
            with patch('slack_client.get_token', return_value='Bearer test-token'):
                result = slack_client.do_list_api()
                self.assertEqual(result, {'ok': True, 'reminders': []})

    def test_returns_empty_dict_on_api_failure(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {'ok': False, 'error': 'not_authed'}
        with patch('slack_client.requests.post', return_value=mock_response):
            with patch('slack_client.get_token', return_value=''):
                result = slack_client.do_list_api()
                self.assertEqual(result, {})


class TestRemindSet(unittest.TestCase):
    def test_prints_remind_time_and_exits_zero_on_success(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'ok': True,
            'reminder': {
                'id': 'Rm123',
                'time': 1000000,
                'text': ':tomato:'
            }
        }
        with patch('slack_client.requests.post', return_value=mock_response):
            with patch('slack_client.get_token', return_value='Bearer test-token'):
                with self.assertRaises(SystemExit) as cm:
                    slack_client.remind_set(1500, ':tomato:')
                self.assertEqual(cm.exception.code, 0)

    def test_exits_with_code_one_on_api_failure(self):
        mock_response = MagicMock()
        mock_response.json.return_value = {'ok': False, 'error': 'not_authed'}
        with patch('slack_client.requests.post', return_value=mock_response):
            with patch('slack_client.get_token', return_value=''):
                with self.assertRaises(SystemExit) as cm:
                    slack_client.remind_set(1500, ':tomato:')
                self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
