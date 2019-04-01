# -*- coding: utf-8 -*-
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
from time import sleep


S = requests.Session()
last_adj = 'öölantilainen'
last = ''

URL = "https://fi.wiktionary.org/w/api.php"
URL = "https://fi.wiktionary.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Luokka:Suomen_kielen_substantiivit&cmprop=title&cmlimit=500&"
url_sub = "https://fi.wiktionary.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Luokka:Suomen_kielen_substantiivit&cmprop=title&cmlimit=500"
url_adj = "https://fi.wiktionary.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Luokka:Suomen_kielen_adjektiivit&cmprop=title&cmlimit=500"
url = url_adj #replace this
PARAMS = {
    'action': "parse",
    'pageid': 55732,
    'prop': "categories",
    'format': "json"
}

PARAMS2 = {
    'action':"query",
    'cmpageid': 55732,
}
TITLE = "Luokka:Suomen kielen adjektiivit"
haut = 0
subs = []
while True:
    R = S.get(url=url)
    DATA = R.json()
    data = DATA['query']['categorymembers']
    for i in data:
        n = 0
        if i not in subs:
            subs.append(i['title'])
            if i['title'] == "öölantilainen": #adjektiiveille korvaa tama "!kung" :lla
                break
    n = len(data)-1
    print(data[n])
    index = len(subs) - 1
    if 'continue' in DATA:
        url = url + "&cmcontinue=" + DATA['continue']['cmcontinue']
        haut += 1
        print(haut)
        print(url)
        sleep(0.5)
    else:
        break
# 55732

''' sananlaskuparseri osioo
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
'''
conn = sqlite3.connect('mobile.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS adjektiivit (adj text)''')
c.execute('''CREATE TABLE IF NOT EXISTS substantiivit (sub text)''')
sql = "INSERT INTO adjektiivit VALUES (?)"  # TÄÄ ON MYÖS TÄRKEÄ
for i in subs:
    c.execute(sql, (i,))

conn.commit()
conn.close()
print("Kaikki vissiin onnistu")
