# coding=utf8
# cf. https://api.slack.com/web
# cf. https://api.slack.com/methods/reminders.add

import argparse
import configparser
from datetime import datetime
import json
import os
import pprint
import requests
import sys
import time

CONFIG_FILE_NAME: str = 'config.ini'
CONFIG_FILE_SECTION: str = 'slack'


def get_args() -> (argparse.Namespace):
    parser = argparse.ArgumentParser(
        description='post pomodoro message to slack. by kotaoue')
    parser.add_argument(
        '-i', '--init', help='Reset and input ini file.', action='store_true')
    parser.add_argument(
        '-l', '--list', help='Show remider list.', action='store_true')
    parser.add_argument(
        '-s', '--sec', help='Sec to set a reminder.', type=int, default=0)
    parser.add_argument(
        '-m', '--min', help='Min to set a reminder.', type=int, default=25)
    parser.add_argument(
        '-t', '--text', help='Reminder message.', type=str, default=':tomato:')
    return parser.parse_args()


def get_ini_path() -> (str):
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    return os.path.join(base_dir, CONFIG_FILE_NAME)


def exists_ini() -> (bool):
    return os.path.exists(get_ini_path())


def init():
    print('Please input your OAuth Access Token.')
    print("We need two permissions for 'reminders:read' and 'reminders:write'.")
    print('cf. https://api.slack.com/apps -> OAuth & Permissions')
    token = input('>> ')

    if token.find('xoxp') == 0:
        config_ini = configparser.ConfigParser()
        section = CONFIG_FILE_SECTION
        config_ini.add_section(section)
        config_ini.set(section, 'token', token)

        with open(get_ini_path(), 'w') as file:
            config_ini.write(file)
        sys.exit(0)
    else:
        print("It's invalid token.")
        sys.exit(1)


def get_token() -> (str):
    if exists_ini():
        config_ini = configparser.ConfigParser()
        config_ini.read(get_ini_path())
        return 'Bearer ' + config_ini.get(CONFIG_FILE_SECTION, 'token')
    else:
        return ''


def list():
    api_url = 'https://slack.com/api/reminders.list'
    headers = {
        'content-type': 'application/json; charset=UTF-8',
        'Authorization': get_token()
    }

    res = requests.post(api_url, headers=headers).json()
    if 'ok' in res and res['ok']:
        if 'reminders' in res and len(res['reminders']) > 0:
            res['reminders'].sort(key=lambda x: x.get('time', 0))

            id_len = len('id')
            time_len = len('2000-01-01 00:00:00')
            complete_len = len('complete')
            text_len = len('text')
            margin = 1
            peifix_len = len('|')

            for value in res['reminders']:
                if len(value['id']) > id_len:
                    id_len = len(value['id'])
                if len(value['text']) > text_len:
                    text_len = len(value['text'])

            line = '+'
            line += ('-' * (id_len + (margin * 2) + peifix_len)) + '+'
            line += ('-' * (time_len + (margin * 2) + peifix_len)) + '+'
            line += ('-' * (complete_len + (margin * 2) + peifix_len)) + '+'
            line += ('-' * (text_len + (margin * 2) + peifix_len)) + '+'
            print(line)
            title = ''
            title += _format_list_str('id', id_len, margin)
            title += _format_list_str('time', time_len, margin)
            title += _format_list_str('complete', complete_len, margin)
            title += _format_list_str('text', text_len, margin)
            title += '|'
            print(title)
            print(line)
            for value in res['reminders']:
                if not value['recurring']:
                    id_str = _format_list_str(value['id'], id_len, margin)
                    print(id_str, end='')

                    dt = datetime.fromtimestamp(value['time'])
                    dtstr = dt.strftime('%Y-%m-%d %H:%M:%S')
                    time_str = _format_list_str(dtstr, time_len, margin)
                    print(time_str, end='')

                    complete_value = 'no'
                    if value['complete_ts'] > 0:
                        complete_value = 'yes'
                    complete_str = _format_list_str(
                        complete_value, complete_len, margin)
                    print(complete_str, end='')

                    text_str = _format_list_str(
                        value['text'], text_len, margin)
                    print(text_str, end='')

                    print('|')
            print(line)
        sys.exit(0)
    else:
        print('error occurred')
        sys.exit(1)


def _format_list_str(text: str, max_len: int, margin: int, prefix: str = '|') -> (str):
    return (prefix + (' ' * (len(prefix) + margin)) + text + (' ' * (max_len - len(text) + margin)))


def set(sec: int, text: str):
    api_url = 'https://slack.com/api/reminders.add'
    headers = {
        'content-type': 'application/json; charset=UTF-8',
        'Authorization': get_token()
    }

    payload = {}
    payload['text'] = text
    payload['time'] = int(time.time()) + sec

    res = requests.post(api_url, data=json.dumps(payload), headers=headers)
    pprint.pprint(res.json())
    sys.exit(0)


def main():
    if not exists_ini():
        print('please initialize.')
        init()

    args = get_args()
    if args.init:
        init()

    if args.list:
        list()

    sec = args.min * 60
    if args.sec > 0:
        sec = args.sec
    text = args.text
    print(sec)
    print(text)
    set(sec, text)

    exit(0)


if __name__ == '__main__':
    main()
