# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import date, timedelta, datetime
import logging
from config import TOKEN


class TelegramBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                                   '%(message)s', level=logging.INFO)

        updater = Updater(token=TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('kiitos', self.kiitos))
        dispatcher.add_handler(CommandHandler('wabu', self.vappu))
        dispatcher.add_handler(CommandHandler('sekseli', self.sekseli))

        self.viim_kom = {'vappu': [], 'kiitos': [], 'sekseli': []}

        updater.start_polling()
        updater.idle()

    def vappu(self, bot, update):
        if not self.aikaTarkistus(update.message.date):
            return
        if not self.viimeKomentoTarkistus('vappu', update):
            return
        wabu = date(2019, 4, 15)
        tanaan = date.today()
        erotus = wabu - tanaan
        bot.send_message(chat_id=update.message.chat_id,
                         text='Wabun alkuun on {} päivää'.format(erotus.days))

    def kiitos(self, bot, update):
        if not self.aikaTarkistus(update.message.date):
            return
        if not self.viimeKomentoTarkistus('kiitos', update):
            return
        bot.send_message(chat_id=update.message.chat_id, text='Kiitos Jori')

    def sekseli(self, bot, update):
        if not self.aikaTarkistus(update.message.date):
            return
        if not self.viimeKomentoTarkistus('sekseli', update):
            return
        bot.send_message(chat_id=update.message.chat_id, text='Akseli sekseli guu nu kaijakka niko toivio sitä r el'
                                                                  'sa')

    def aikaTarkistus(self, viesti_aika):
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


if __name__ == '__main__':
    TelegramBot()

