# coding=utf8
import unittest
from unittest.mock import patch

import aggregator


class TestRemindList(unittest.TestCase):
    def test_exits_zero_when_no_reminders_key(self):
        with patch('aggregator.do_list_api', return_value={}):
            with self.assertRaises(SystemExit) as cm:
                aggregator.remind_list()
            self.assertEqual(cm.exception.code, 0)

    def test_exits_zero_when_reminders_list_is_empty(self):
        with patch('aggregator.do_list_api', return_value={'reminders': []}):
            with self.assertRaises(SystemExit) as cm:
                aggregator.remind_list()
            self.assertEqual(cm.exception.code, 0)

    def test_calls_print_table_with_formatted_reminders(self):
        reminders = [
            {
                'id': 'Rm001',
                'time': 1587042000,
                'complete_ts': 0,
                'text': ':tomato:'
            }
        ]
        with patch('aggregator.do_list_api', return_value={'reminders': reminders}):
            with patch('aggregator.clitable.print_table') as mock_print:
                with self.assertRaises(SystemExit):
                    aggregator.remind_list()
                mock_print.assert_called_once()
                result = mock_print.call_args[0][0]
                self.assertEqual(result[0]['id'], 'Rm001')
                self.assertEqual(result[0]['text'], ':tomato:')

    def test_marks_complete_yes_when_complete_ts_nonzero(self):
        reminders = [
            {
                'id': 'Rm001',
                'time': 1587042000,
                'complete_ts': 1587042100,
                'text': ':tomato:'
            }
        ]
        with patch('aggregator.do_list_api', return_value={'reminders': reminders}):
            with patch('aggregator.clitable.print_table') as mock_print:
                with self.assertRaises(SystemExit):
                    aggregator.remind_list()
                result = mock_print.call_args[0][0]
                self.assertEqual(result[0]['complete'], 'yes')

    def test_marks_complete_no_when_complete_ts_zero(self):
        reminders = [
            {
                'id': 'Rm001',
                'time': 1587042000,
                'complete_ts': 0,
                'text': ':tomato:'
            }
        ]
        with patch('aggregator.do_list_api', return_value={'reminders': reminders}):
            with patch('aggregator.clitable.print_table') as mock_print:
                with self.assertRaises(SystemExit):
                    aggregator.remind_list()
                result = mock_print.call_args[0][0]
                self.assertEqual(result[0]['complete'], 'no')

    def test_reminders_are_sorted_by_time(self):
        reminders = [
            {'id': 'Rm002', 'time': 1587042100, 'complete_ts': 0, 'text': 'second'},
            {'id': 'Rm001', 'time': 1587042000, 'complete_ts': 0, 'text': 'first'},
        ]
        with patch('aggregator.do_list_api', return_value={'reminders': reminders}):
            with patch('aggregator.clitable.print_table') as mock_print:
                with self.assertRaises(SystemExit):
                    aggregator.remind_list()
                result = mock_print.call_args[0][0]
                self.assertEqual(result[0]['text'], 'first')
                self.assertEqual(result[1]['text'], 'second')


class TestAggregate(unittest.TestCase):
    def test_exits_zero_when_no_reminders_key(self):
        with patch('aggregator.do_list_api', return_value={}):
            with self.assertRaises(SystemExit) as cm:
                aggregator.aggregate()
            self.assertEqual(cm.exception.code, 0)

    def test_exits_zero_when_reminders_list_is_empty(self):
        with patch('aggregator.do_list_api', return_value={'reminders': []}):
            with self.assertRaises(SystemExit) as cm:
                aggregator.aggregate()
            self.assertEqual(cm.exception.code, 0)

    def test_counts_reminders_by_date_and_text(self):
        reminders = [
            {'id': 'Rm001', 'time': 1587042000, 'recurring': False, 'text': ':tomato:'},
            {'id': 'Rm002', 'time': 1587042060, 'recurring': False, 'text': ':tomato:'},
            {'id': 'Rm003', 'time': 1587042120, 'recurring': False, 'text': 'test'},
        ]
        with patch('aggregator.do_list_api', return_value={'reminders': reminders}):
            with patch('aggregator.clitable.print_table') as mock_print:
                with self.assertRaises(SystemExit):
                    aggregator.aggregate()
                result = mock_print.call_args[0][0]
                tomato = next(r for r in result if r['text'] == ':tomato:')
                test_entry = next(r for r in result if r['text'] == 'test')
                self.assertEqual(tomato['count'], 2)
                self.assertEqual(test_entry['count'], 1)

    def test_skips_recurring_reminders(self):
        reminders = [
            {'id': 'Rm001', 'time': 1587042000, 'recurring': True, 'text': ':tomato:'},
        ]
        with patch('aggregator.do_list_api', return_value={'reminders': reminders}):
            with patch('aggregator.clitable.print_table') as mock_print:
                with self.assertRaises(SystemExit):
                    aggregator.aggregate()
                result = mock_print.call_args[0][0]
                self.assertEqual(result, [])

    def test_aggregates_reminders_across_dates(self):
        reminders = [
            {'id': 'Rm001', 'time': 1587042000, 'recurring': False, 'text': ':tomato:'},
            {'id': 'Rm002', 'time': 1587128400, 'recurring': False, 'text': ':tomato:'},
        ]
        with patch('aggregator.do_list_api', return_value={'reminders': reminders}):
            with patch('aggregator.clitable.print_table') as mock_print:
                with self.assertRaises(SystemExit):
                    aggregator.aggregate()
                result = mock_print.call_args[0][0]
                dates = {r['date'] for r in result}
                self.assertEqual(len(dates), 2)

    def test_result_contains_date_text_and_count_keys(self):
        reminders = [
            {'id': 'Rm001', 'time': 1587042000, 'recurring': False, 'text': ':tomato:'},
        ]
        with patch('aggregator.do_list_api', return_value={'reminders': reminders}):
            with patch('aggregator.clitable.print_table') as mock_print:
                with self.assertRaises(SystemExit):
                    aggregator.aggregate()
                result = mock_print.call_args[0][0]
                self.assertIn('date', result[0])
                self.assertIn('text', result[0])
                self.assertIn('count', result[0])


if __name__ == '__main__':
    unittest.main()
