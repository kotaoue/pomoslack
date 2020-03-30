# pomoslack
![GitHub](https://img.shields.io/github/license/kotaoue/pomoslack)
## Overview
ポモドーロ・テクニックお助け用スクリプト  
コマンドラインからslackにリマインダを登録したり、  
1日の総ポモドーロ数を集計したりする。

## Dependency
### Python
* Python3
* requests
### Slack
* [reminders:read scope](https://api.slack.com/scopes/reminders:read)
* [reminders:write scope](https://api.slack.com/scopes/reminders:write)
#### トークン 習得方法
1. https://api.slack.com/ -> click 'Start Building'
2. Create App
3. Basic Information -> Add features and functionality -> Premissions
4. Scopes -> User Token Scopes -> Add an OAuth Scope

## Setup
```
$ pip3 install -r requirements.txt
```

## Usage
* リマインダの登録
  ```
  $ python3 pomoslack.py 
  remind at 2020-04-16 00:25:00
  ```
* 60分後にリマインダを登録
  ```
  $ python3 pomoslack.py -m 60
  remind at 2020-04-16 01:00:00
  ```
* リマインダ文言と日付毎に集計する
  ```
  $ python3 pomoslack.py -a
  +-------------+-----------+--------+
  |  time       |  text     |  count |
  +-------------+-----------+--------+
  |  2020-04-14 |  test     |  1     |
  |  2020-04-14 |  :tomato: |  10    |
  |  2020-04-15 |  :tomato: |  13    |
  +-------------+-----------+--------+
  ```

## License
MITっす。
