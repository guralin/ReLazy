#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import requests
import click
from bs4 import BeautifulSoup

@click.command()
@click.option('-l','--list','list_number', default=0, help="print last words")
def mainThread(list_number):
    m = model()
    if list_number != 0:
        m.show_newest_words(list_number)
    else:    
        input_eng_word_in_loop()

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
    m = model()
    while True:
        word = input('検索したい英単語を入力してください >')
        if word == 'exit()':
            break
        ans  = search_weblio_dictionary(word)
        if ans == -1:
            print("検索された英単語は存在しませんでした")
        else:
            print(ans)
            m.add_word_to_sqlite3(word,ans)
            

class model():
    def __init__(self):
        self.connect_database = 'word.db'
    def add_word_to_sqlite3(self,jpn_word,eng_word):
        conn = sqlite3.connect(self.connect_database)
        curs = conn.cursor()
        ins = 'INSERT INTO words(jpn_word, eng_word) VALUES(?, ?)' 
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
            print('{0:12} | {1}'.format(row[0],row[1]))
            print("--------------------------------------")
        conn.close()
    


if __name__ == "__main__":
    mainThread()
