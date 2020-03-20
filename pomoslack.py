# coding=utf8
# cf. https://api.slack.com/web
# cf. https://api.slack.com/methods/reminders.add

import argparse
import configparser
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


def exists_ini() -> (bool):
    return os.path.exists(CONFIG_FILE_NAME)


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

        with open(CONFIG_FILE_NAME, 'w') as file:
            config_ini.write(file)
    else:
        print("It's invalid token.")
        sys.exit(1)


def get_token() -> (str):
    if exists_ini():
        config_ini = configparser.ConfigParser()
        config_ini.read(CONFIG_FILE_NAME)
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
        for value in res['reminders']:
            pprint.pprint(value)
        sys.exit(0)
    else:
        print('error occurred')
        sys.exit(1)


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
