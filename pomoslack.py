# coding=utf8
# cf. https://api.slack.com/web
# cf. https://api.slack.com/methods/reminders.add

import argparse

from aggregator import aggregate, remind_list
from slack_client import exists_ini, get_message, init, remind_set


def get_args() -> (argparse.Namespace):
    parser = argparse.ArgumentParser(
        description='post pomodoro message to slack. by kotaoue')
    parser.add_argument(
        '-i', '--init', help='Reset and input ini file.', action='store_true')
    parser.add_argument(
        '-l', '--list', help='Show remider list.', action='store_true')
    parser.add_argument(
        '-a', '--aggregate', help='Aggregate complete remind.', action='store_true')
    parser.add_argument(
        '-s', '--sec', help='Sec to set a reminder.', type=int, default=0)
    parser.add_argument(
        '-m', '--min', help='Min to set a reminder.', type=int, default=25)
    parser.add_argument(
        '-t', '--text', help='Reminder message.', type=str, default=get_message())
    return parser.parse_args()


def main():
    if not exists_ini():
        init()

    args = get_args()
    if args.init:
        init()

    if args.list:
        remind_list()

    if args.aggregate:
        aggregate()

    sec = args.min * 60 if args.sec == 0 else args.sec
    text = args.text
    remind_set(sec, text)
    exit(0)


if __name__ == '__main__':
    main()
