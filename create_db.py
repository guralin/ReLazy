#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect("word.db")

# todo:Unixタイムで保存するか、文字列型で保存するか迷っている
# この世界線では文字列で実装してみる

sql = """CREATE TABLE words(id integer primary key,
timestamp text,
jpn_word text,
eng_word text
);
"""
conn.execute(sql)
conn.close()
