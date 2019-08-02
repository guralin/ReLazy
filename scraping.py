#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import requests
import datetime

import click
import sys

from bs4 import BeautifulSoup

    
def mainThread():
    args = sys.argv
    if len(args) == 1:
        input_eng_word_in_loop()
    else:
        cmd()

@click.command()
@click.option('-l','--list','list_number', default=0, help="print last words")
def cmd(list_number):
    m = sqlite3_model()
    m.show_newest_words(list_number)


def search_weblio_dictionary(word):
    r = requests.get('https://ejje.weblio.jp/content/' + word)
    soup = BeautifulSoup(r.content , 'html.parser')
    main = soup.find('td', class_='content-explanation ej')
    try:
        ans = main.string
        return ans
# 検索した英単語が見つからない場合
    except AttributeError:
        return -1
def input_eng_word_in_loop():
    m = sqlite3_model()
    while True:
        word = input('検索したい英単語を入力してください >')
        if word == 'exit()':
            break
        ans  = search_weblio_dictionary(word)
        if ans == -1:
            print("検索された英単語は存在しませんでした")
        else:
            print(ans)
            m.add_word(word,ans)

            
class sqlite3_model():
    def __init__(self):
        self.connect_database = 'word.db'
    def add_word(self,jpn_word,eng_word):
        conn = sqlite3.connect(self.connect_database)
        curs = conn.cursor()
        datetime_now = datetime.datetime.now()
        ins = 'INSERT INTO words(timestamp,jpn_word, eng_word) VALUES(?, ?, ?)'
        curs.execute(ins, (datetime_now,jpn_word,eng_word))
        conn.commit()
        conn.close()
        
    def show_newest_words(self,list_number):
        conn = sqlite3.connect(self.connect_database)
        curs = conn.cursor()
        show = 'SELECT jpn_word,eng_word FROM words ORDER BY id DESC LIMIT (?)'
        curs.execute(show, (list_number,))
        result = curs.fetchall()
        for row in result:
            print('{0:12} | {1}'.format(row[0],row[1]))
            print("--------------------------------------")
        conn.close()


if __name__ == "__main__":
    mainThread()
