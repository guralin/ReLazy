#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect("word.db")

sql = """CREATE TABLE words(id integer primary key,
jpn_word text,
eng_word text
);
"""
conn.execute(sql)
conn.close()
