# -*- coding: utf-8 -*-

import logging
import sqlite3
from datetime import date, timedelta, datetime
import config
#from config import TOKEN, TOKEN_KB, DB_FILE, PINNED_TABLE
from telegram.ext import Updater, MessageHandler, Filters


class TelegramBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                                   '%(message)s', level=logging.INFO)

        updater = Updater(token=config.TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.command, self.commandsHandler))
        dispatcher.add_handler(MessageHandler(Filters.status_update.pinned_message, self.pinned))

        self.commands = {'wabu': self.wabu,
                         'kiitos': self.kiitos,
                         'sekseli': self.sekseli,
                         'pöytä': self.pöytä,
                         'insv': self.insv,
                         }

        self.viim_kom = {command: [] for command in self.commands.keys()}

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

    def viimeKomentoTarkistus(self, komento, update, sekunnit=5):
        for msg in self.viim_kom[komento]:
            if msg.message.chat_id == update.message.chat_id:
                if datetime.today() - msg.message.date > timedelta(0, sekunnit):
                    self.viim_kom[komento].remove(msg)
                    self.viim_kom[komento].append(update)
                    return True
                else:
                    return False
        self.viim_kom[komento].append(update)
        return True

    def commandsHandler(self, bot, update):
        if not self.aikaTarkistus(update.message.date):
            return
        command = self.commandParser(update.message.text)
        if command not in self.commands:
            return
        if self.viimeKomentoTarkistus(command, update):
            self.commands[command](bot, update)

    @staticmethod
    def commandParser(teksti):
        command = ''
        for i in teksti:
            if i == ' ' or i == '@':
                break
            elif i != '/':
                command += i
        return command.lower()

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

    def create_tables(self):
        conn = sqlite3.connect(config.DB_FILE)
        c = conn.cursor()
        try:
            c.execute('select * from pinned')
        except sqlite3.OperationalError:    # taulua ei ollut olemassa
            c.execute(config.PINNED_TABLE)  # TODO: tähän sais varmaanki helposti useamman tablen for-looppiin
        conn.close()

if __name__ == '__main__':
    TelegramBot()
