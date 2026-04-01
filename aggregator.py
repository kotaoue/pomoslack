# coding=utf8

import sys
from datetime import datetime

from modules.clitable import clitable
from slack_client import do_list_api


def remind_list():
    res = do_list_api()

    if 'reminders' in res and len(res['reminders']) > 0:
        res['reminders'].sort(key=lambda x: x.get('time', 0))

        result = []
        for value in res['reminders']:
            remind = {}
            remind['id'] = value['id']

            dt = datetime.fromtimestamp(value['time'])
            remind['time'] = dt.strftime('%Y-%m-%d %H:%M:%S')
            complete_value = 'no'
            if value['complete_ts'] > 0:
                complete_value = 'yes'
            remind['complete'] = complete_value
            remind['text'] = value['text']
            result.append(remind)

        clitable.print_table(result)
    sys.exit(0)


def aggregate():
    res = do_list_api()
    if 'reminders' in res and len(res['reminders']) > 0:
        res['reminders'].sort(key=lambda x: x.get('time', 0))

        aggregate_result = {}
        for value in res['reminders']:
            if not value['recurring']:
                dt = datetime.fromtimestamp(value['time'])
                dtstr = dt.strftime('%Y-%m-%d')

                if dtstr not in aggregate_result:
                    aggregate_result[dtstr] = {}

                text = value['text']
                if text not in aggregate_result[dtstr]:
                    aggregate_result[dtstr][text] = 0

                aggregate_result[dtstr][text] += 1

        result = []
        for date, details in aggregate_result.items():
            for text, count in details.items():
                result.append({'date': date, 'text': text, 'count': count})

        clitable.print_table(result)
    sys.exit(0)
