# -*- coding: utf-8 -*-

import logging
import sqlite3
from datetime import date, timedelta, datetime
import config
from telegram.ext import Updater, MessageHandler, Filters
import random
from time import time


class TelegramBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                                   '%(message)s', level=logging.INFO)

        updater = Updater(token=config.TOKEN_KB)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.command, self.commandsHandler))
        dispatcher.add_handler(MessageHandler(Filters.status_update.pinned_message, self.pinned))

        self.commands = {'wabu': self.wabu,
                         'kiitos': self.kiitos,
                         'sekseli': self.sekseli,
                         'pöytä': self.pöytä,
                         'insv': self.insv,
                         'quoteadd': self.quoteadd,
                         'quote': self.quote,
                         'viisaus': self.viisaus
                         }

        self.viim_kom = {command: [] for command in self.commands.keys()}
        self.users = {}  # user_id : unix timestamp

        self.create_tables()

        updater.start_polling()
        updater.idle()

    @staticmethod
    def wabu(bot, update):
        wabu = date(2019, 4, 15)
        tanaan = date.today()
        erotus = wabu - tanaan
        bot.send_message(chat_id=update.message.chat_id,
                         text=f'Wabun alkuun on {erotus.days} päivää', disable_notification=True)

    @staticmethod
    def kiitos(bot, update):
        if update.message.reply_to_message is not None:
            bot.send_message(chat_id=update.message.chat_id, text=f'Kiitos {update.message.reply_to_message.from_user.first_name}!',
                             disable_notifications=True)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Kiitos Jori!', disable_notification=True)

    @staticmethod
    def sekseli(bot, update):
        text = 'Akseli sekseli guu nu kaijakka niko toivio sitä r elsa'
        bot.send_message(chat_id=update.message.chat_id, text=text, disable_notification=True)

    @staticmethod
    def pöytä(bot, update):
        xd = 'CgADBAADyAQAAgq36FKsK7BL1PNfZQI'
        bot.send_animation(chat_id=update.message.chat_id, animation=xd, disable_notification=True)

    @staticmethod
    def insv(bot, update):
        file_id = "CAADBAADqgADsnJvGjljGk2zOaJJAg"
        bot.send_sticker(chat_id=update.message.chat_id, sticker=file_id, disable_notification=True)

    @staticmethod
    def aikaTarkistus(viesti_aika):
        if datetime.today() - viesti_aika < timedelta(0, 30):
            return True
        else:
            return False

    def cooldownFilter(self, update):

        cooldown = 15

        if not update.message.from_user.id:
            # Some updates are not from any user -- ie when bot is added to a group
            return True

        id = update.message.from_user.id

        if id not in self.users.keys():
            # new user, add id to users
            self.users[id] = time()
            return True

        elif id in self.users.keys():
            # old user
            if time() - self.users[id] < cooldown:
                # caught in spam filter
                return False
            else:
                # passed the spam filter.
                self.users[id] = time()
                return True

    def commandsHandler(self, bot, update):
        if not self.aikaTarkistus(update.message.date):
            return
        if update.message.entities is None:
            return
        commands = self.commandParser(update.message)
        for command in commands:
            if command in self.commands:
                if self.cooldownFilter(update):
                    self.commands[command](bot, update)

    @staticmethod
    def commandParser(msg):
        commands = list()
        for i in msg.entities:
            if i.type == 'bot_command':
                command = msg.text[i.offset + 1: i.offset + i.length].lower()
                temp = command.split('@')
                commands.append(temp[0])

        is_desk = msg.text.find('pöytä')
        if is_desk != -1:
            commands.append(msg.text[is_desk:is_desk+5])
        return commands

    def pinned(self, bot, update):
        try:
            if update.message.pinned_message:
                if update.message.chat_id == config.MOBILE_ID:
                    sql = "INSERT INTO pinned VALUES (?,?,?)"
                    pinned = (update.message.date.isoformat(), update.message.pinned_message.from_user.username,
                              update.message.pinned_message.text)
                    conn = sqlite3.connect(config.DB_FILE)
                    cur = conn.cursor()
                    cur.execute(sql, pinned)
                    conn.commit()
                    conn.close()

        except KeyError:
            return False

    def quoteadd(self, bot, update):
        text = update.message.text
        first_space = 9
        try:
            second_space = text.find(' ', first_space + 1)
        except IndexError:
            bot.send_message(chat_id=update.message.chat_id, text="Opi käyttämään komentoja pliide bliis!!")
            return

        if second_space != -1:
            quote = (text[10:second_space].lower(), text[second_space + 1:])
            conn = sqlite3.connect(config.DB_FILE)
            cur = conn.cursor()
            sql = "INSERT INTO quotes VALUES (?,?)"
            cur.execute(sql, quote)
            conn.commit()
            conn.close()
            bot.send_message(chat_id=update.message.chat_id, text="Sitaatti lisätty")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Opi käyttämään komentoja pliide bliis!!")

    def quote(self, bot, update):
        space = update.message.text.find(' ')
        conn = sqlite3.connect(config.DB_FILE)
        c = conn.cursor()
        if space == -1:
            c.execute("SELECT * FROM quotes")
            quotes = c.fetchall()
            i = self.random_select(len(quotes)-1)
        else:
            name = update.message.text[space + 1 :]
            c.execute("SELECT * FROM quotes WHERE name=?", (name.lower(),))
            quotes = c.fetchall()
            if len(quotes) == 0:
                bot.send_message(chat_id=update.message.chat_id, text='Ei löydy')
                return
            i = self.random_select(len(quotes)-1)
        bot.send_message(chat_id=update.message.chat_id, text=f'"{quotes[i][1]}" -{quotes[i][0].capitalize()}')

    def viisaus(self, bot, update):
        conn = sqlite3.connect(config.DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM sananlaskut")
        wisenings = c.fetchall()
        i = self.random_select(len(wisenings)-1)
        bot.send_message(chat_id=update.message.chat_id, text=wisenings[i][0])

    @staticmethod
    def random_select(max):
        rand_int = random.randint(0, max)
        return rand_int

    def create_tables(self):
        conn = sqlite3.connect(config.DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS pinned (date text, name text, text text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS quotes (name text, quote text unique)''')
        c.execute('''CREATE TABLE IF NOT EXISTS sananlaskut (teksti text)''')
        conn.close()

if __name__ == '__main__':
    TelegramBot()
