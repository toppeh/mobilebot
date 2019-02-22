#!/usr/bin/python3

"""
    parse.py

    MediaWiki Action API Code Samples
    Demo of `Parse` module: Parse content of a page
    MIT license
"""

import sqlite3

import requests
import csv

S = requests.Session()

URL = "https://fi.wikiquote.org/w/api.php"

TITLE = "Suomalaisia sananlaskuja"

PARAMS = {
    'action': "parse",
    'page': TITLE,
    'prop': "wikitext",
    'format': "json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

wikitext = DATA['parse']['wikitext']['*']
lines = wikitext.split('*')
#print(wikitext)
entries = []
for line in lines:
    line = line.strip()
    #line = line.strip("' (KRA)")
    line = line.replace('[', '')
    line = line.replace(']', '')
    index = line.find("'", 2)
    if "''" in line:
        entries.append(line[2:index])

conn = sqlite3.connect('mobile.db')
c = conn.cursor()
sql = "INSERT INTO sananlaskut VALUES (?)"

for i in entries:
    print(i)
    c.execute(sql, (i,))

conn.commit()
conn.close()

