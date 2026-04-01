# coding=utf8
# cf. https://api.slack.com/web
# cf. https://api.slack.com/methods/reminders.add

import configparser
import json
import os
import sys
import time
from datetime import datetime

import requests

CONFIG_FILE_NAME: str = 'config.ini'
CONFIG_FILE_SECTION: str = 'slack'


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
    print('Please input reminder message.')
    print('When not input message becames message is ":tomato:".')
    message = input('>> ')
    if token.find('xoxp') == 0:
        config_ini = configparser.ConfigParser()
        section = CONFIG_FILE_SECTION
        config_ini.add_section(section)
        config_ini.set(section, 'token', token)
        config_ini.set(
            section, 'message',
            (lambda message: message if message else ':tomato:')(message)
        )

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


def get_message() -> (str):
    if exists_ini():
        config_ini = configparser.ConfigParser()
        config_ini.read(get_ini_path())
        return config_ini.get(CONFIG_FILE_SECTION, 'message')
    else:
        return ':tomato:'


def do_list_api() -> (dict):
    api_url = 'https://slack.com/api/reminders.list'
    headers = {
        'content-type': 'application/json; charset=UTF-8',
        'Authorization': get_token()
    }

    res = requests.post(api_url, headers=headers).json()
    if res.get('ok', False):
        return res
    else:
        print('error occurred')
        return {}


def remind_set(sec: int, text: str):
    api_url = 'https://slack.com/api/reminders.add'
    headers = {
        'content-type': 'application/json; charset=UTF-8',
        'Authorization': get_token()
    }

    payload = {}
    payload['text'] = text
    payload['time'] = int(time.time()) + sec

    res = requests.post(
        api_url,
        data=json.dumps(payload),
        headers=headers).json()
    if 'ok' in res and res['ok']:
        if len(res.get('reminder')) > 0:
            dt = datetime.fromtimestamp(res['reminder']['time'])
            dtstr = dt.strftime('%Y-%m-%d %H:%M:%S')
            print('remind at ' + dtstr)
        sys.exit(0)
    else:
        print('error occurred')
        sys.exit(1)
