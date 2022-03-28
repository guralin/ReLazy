#!/usr/bin/env python
# -*- coding: utf-8 -*-

import deepl
import requests
import datetime
import sys
import os

import sqlite3
import click
from bs4 import BeautifulSoup

ERROR_STATUS = -1
EXIT_STATUS  = -2

DATABASE_PATH = os.path.dirname(__file__) + "/word.db"

def mainThread():
    # 最初に引数の数を評価させることでIndexErrorを防ぐ
    args = sys.argv
    # 引数の最初がハイフンなら、オプションだと判断する
    if  len(args) > 1 and args[1][0] == '-':
        cmd()
    # コマンドラインに引数が渡されない場合
    elif len(args) == 1:
        input_eng_word_in_loop()
    # python scraping.py {検索したいワード}
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
    # 引数にマイナスが渡された場合はハンドリングを行う
    result = save_existing_word(word)
    if   result == EXIT_STATUS:
        print('bye')
        sys.exit(0)
    elif result == ERROR_STATUS:
        print("検索された英単語は存在しませんでした")
    else:
        print(result)

def input_eng_word_in_loop():
    # 検索を繰り返し行う関数
    while True:
        try:
            word = input('検索したい英単語を入力してください > ')
        except KeyboardInterrupt:
            print('\nbye')
            sys.exit(0)
        input_eng_word(word)


def search_using_deepl(word):
    # DeepLのAPIを用いて検索を行います。
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(word, target_lang="JA")
    return result.text


def save_existing_word(word):
    # 取り出してきた単語を分けて、保存して、出力する。
    # データが帰ってきた場合:DBに保存
    # データがない場合:ERROR_STATUS
    # 終了する場合:EXIT_STATUS
    m = sqlite3_model()

    if word == 'exit()':
        return EXIT_STATUS
    ans  = search_using_deepl(word)
    print(ans)
    if ans == ERROR_STATUS or ans == "":
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
        # 渡された引数の数字分の単語と訳を新しい順に出力する
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
        # 渡された引数の日付から現在までで検索された単語と訳を出力する。
        conn = sqlite3.connect(self.connect_database)
        curs = conn.cursor()
        period_days =  str(0 - period_days)
        period_days_for_sql = period_days + ' days'
        show = "SELECT timestamp,jpn_word,eng_word FROM words WHERE timestamp > datetime('now',?) ORDER BY id DESC"
        curs.execute(show,(period_days_for_sql,))
        result = curs.fetchall()
        for row in result:
            print('{0:10} | {1}'.format(row[1],row[2]))
            print("--------------------------------------")
        conn.close()

if __name__ == "__main__":
    mainThread()
