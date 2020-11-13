import requests
import xml.etree.ElementTree as ET
from telegram import KeyboardButton
import regex
import random
from stuff import feels, ssHeaders, emotions
import sqlite3
from config import DB_FILE


def generateKeyboard():
    events = "https://www.finnkino.fi/xml/Events/?listType=ComingSoon&includeVideos=false"
    s = requests.Session()
    res = s.get(events)
    root = ET.fromstring(res.text)
    keyboard = []
    for child in root:
        for i in child:
            if i.tag == "Title":
                keyboard.append(KeyboardButton(i.text))
    return keyboard


def getMovie(name):
    events = "https://www.finnkino.fi/xml/Events/?listType=ComingSoon&includeVideos=false"
    s = requests.Session()
    res = s.get(events)
    root = ET.fromstring(res.text)
    movieFound = False
    for child in root:
        for i in child:
            if i.tag == "Title" and i.text == name:
                movieFound = True
            if i.tag == "dtLocalRelease" and movieFound:
                return i.text
    return "Ensi-iltaa ei löytynyt"


def getImage():
    rng = random.randint(0,1)
    if rng == 0:
        feeling = random.choice(feels) + "+" + random.choice(["man", "men", "woman", "women", "boy", "boys", "girl", "girls"])
        url = "https://www.shutterstock.com/fi/search/"+feeling
    else:
        url = "https://www.shutterstock.com/fi/search/" + random.choice(emotions)
    res = requests.get(url, headers=ssHeaders, timeout=3)
    re = regex.compile(r'src="(https://image.shutterstock.com/image-[(?:photo)(?:vector)]+/.+?)"')
    imageList = re.findall(res.text)
    if imageList:
        imgUrl = random.choice(imageList)
        return imgUrl
    else:
        return ""


def dbQuery(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    if len(params) == 0:
        cur.execute(query)
    else:
        cur.execute(query, params)
    res = cur.fetchall()
    conn.close()
    return res


def dbInsertUpdate(sql, params):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    conn.close()


def create_tables():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS substantiivit ("sub" text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS pinned ("date" text, "name" text, "text" text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sananlaskut ("teksti" text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS adjektiivit ("adj" text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS quotes (
        "date" TEXT DEFAULT CURRENT_TIMESTAMP,
        "quotee" TEXT,
        "quote" TEXT,
        "adder" TEXT,
        "groupID" INT,
        PRIMARY KEY(quotee, quote, groupID)
        )
        ''')
    c.execute('''CREATE TABLE IF NOT EXISTS credits(
        "treasury" TEXT,
        "id" TEXT,
        "username" TEXT,
        "amount" INT,
        PRIMARY KEY(treasury, id)
        );
        ''')
    conn.close()


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def centsToEuroStr(amount: int):
    if amount >= 0:
        euros = amount // 100
        cents = amount - euros * 100
        ret = f"{euros},{cents}"
        return ret
    else:
        euros = (-1 * amount) // 100
        cents = (-1 * amount) - euros * 100
        ret = f"-{euros},{cents}"
        return ret
