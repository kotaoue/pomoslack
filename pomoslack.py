# coding=utf8
import json
import argparse
import requests


def get_args():
    parser = argparse.ArgumentParser(
        description='post pomodoro message to slack. by kotaoue')
    parser.add_argument(
        '-m', '--min', help='Min to set a reminder.')
    parser.add_argument(
        '-t', '--text', help='Reminder message.')
    return parser.parse_args()


def main():
    args = get_args()

    text = '/remind me ":tomato:" in 25 min'
    webhook_url = 'hoge'
    payload = {'text': text}
    requests.post(webhook_url, data=json.dumps(payload))


if __name__ == '__main__':
    main()
