from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import date, timedelta
import logging



updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def kiitos(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Kiitos Jori')


# wabu alkaa 15.4.2019
def vappu(bot, update):
    wabu = date(2019, 4, 15)
    tanaan = date.today()
    erotus = wabu - tanaan
    bot.send_message(chat_id=update.message.chat_id, text='Wabun alkuun on {} paivaa'.format(erotus.days))


dispatcher.add_handler(CommandHandler('kiitos', kiitos))
dispatcher.add_handler(CommandHandler('wabu', vappu))

updater.start_polling()
updater.idle()
