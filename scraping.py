#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import requests
from bs4 import BeautifulSoup

def mainThread():
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
    while True:
        word = input('検索したい英単語を入力してください >')
        if 


        ans  = search_weblio_dictionary(word)
        if ans == -1:
            print("検索された英単語は存在しませんでした")
        else:
            print(ans)
            add_word_to_sqlite3(word,ans)
            
def add_word_to_sqlite3(jpn_word,eng_word):
    conn = sqlite3.connect('scraped_word.db')
    curs = conn.cursor()
    ins = ' INSERT INTO words(jpn_word, eng_word) VALUES(?, ?)' 
    curs.execute(ins, (jpn_word,eng_word))
    #curs.execute('SELECT * FROM words')
    #print(curs.fetchall())
    conn.commit()
    conn.close()
    

if __name__ == "__main__":
    mainThread()
