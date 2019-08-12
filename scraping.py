#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import sys
import os

import sqlite3
import click
from bs4 import BeautifulSoup

ERROR_STATUS = -1
EXIT_STATUS = -2

DATABASE_PATH = os.path.dirname(__file__) + "/word.db"

def mainThread():
    args = sys.argv
    # 引数の最初がハイフンなら、オプションだと判断する
    # 最初に引数の数を評価させることでIndexErrorを防ぐ
    if  len(args) > 1 and args[1][0] == '-':
        cmd()

    elif len(args) == 1:
        input_eng_word_in_loop()

    elif len(args) == 2:
        word = args[1]
        input_eng_word(word)

@click.command()
@click.option('-l','--list','list_number', default=0, help="print N pieces words")
@click.option('-d','--days','days_ago', default=0, help="print N days ago")
def cmd(list_number,days_ago):
    m = sqlite3_model()
    if list_number:
        m.show_newest_words(list_number)
    if days_ago:
        m.show_words_days_ago(days_ago)

def input_eng_word(word):
    result = save_existing_word(word)

    if   result == EXIT_STATUS:
        print('bye')
        sys.exit(0)

    elif result == ERROR_STATUS:
        print("検索された英単語は存在しませんでした")

    else:
        print(result)

def input_eng_word_in_loop():
    while True:
        try:
            word = input('検索したい英単語を入力してください >')
        except KeyboardInterrupt:
            print('\nbye')
            sys.exit(0)
        input_eng_word(word)


def search_weblio_dictionary(word):
    r = requests.get('https://ejje.weblio.jp/content/' + word)
    soup = BeautifulSoup(r.content , 'html.parser')
    main = soup.find('td', class_='content-explanation ej')
    try:
        ans = main.string
        return ans
# 検索した英単語が見つからない場合
    except AttributeError:
        return ERROR_STATUS


def save_existing_word(word):
    m = sqlite3_model()

    if word == 'exit()':
        return EXIT_STATUS

    ans  = search_weblio_dictionary(word)
    if ans == ERROR_STATUS:
        return ERROR_STATUS
    else:
        m.add_word(word,ans)
        return ans

class sqlite3_model():
    def __init__(self):
        self.connect_database = DATABASE_PATH

    def add_word(self,jpn_word,eng_word):
        conn = sqlite3.connect(self.connect_database)
        curs = conn.cursor()
        datetime_now = datetime.datetime.now()
        ins = 'INSERT INTO words(timestamp,jpn_word, eng_word) VALUES(CURRENT_TIMESTAMP, ?, ?)'
        curs.execute(ins, (jpn_word,eng_word))
        conn.commit()
        conn.close()

    def show_newest_words(self,list_number):
        conn = sqlite3.connect(self.connect_database)
        curs = conn.cursor()
        show = 'SELECT jpn_word,eng_word FROM words ORDER BY id DESC LIMIT (?)'
        curs.execute(show, (list_number,))
        result = curs.fetchall()
        for row in result:
            print('{0:10} | {1}'.format(row[0],row[1]))
            print("--------------------------------------")
        conn.close()

    def show_words_days_ago(self,period_days):
        conn = sqlite3.connect(self.connect_database)
        curs = conn.cursor()
        period_days =  str(0 - period_days)
        period_days_for_sql = period_days + ' days'
        show = "SELECT timestamp,jpn_word,eng_word FROM words WHERE timestamp > datetime('now',?) ORDER BY id DESC"
        curs.execute(show,(period_days_for_sql,))
        result = curs.fetchall()
        for row in result:
            #print('{0:12} | {1} | {2}'.format(row[0],row[1],row[2]))
            print('{0:10} | {1}'.format(row[1],row[2]))
            print("--------------------------------------")
        conn.close()

if __name__ == "__main__":
    mainThread()
