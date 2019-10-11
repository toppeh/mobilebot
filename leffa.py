import requests
import xml.etree.ElementTree as ET
from telegram import KeyboardButton


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
            debug = i.tag
            debug2 = i.text
            if i.tag == "Title" and i.text == name:
                movieFound = True
            if i.tag == "dtLocalRelease" and movieFound:
                return i.text
    return "Ensi-iltaa ei löytynyt"

