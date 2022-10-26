from telegram.ext import CallbackContext
from telegram import Update
from random import randint
import config

def kuka(update: Update, context: CallbackContext):
    index = randint(0, len(config.MEMBERS)-1)
    context.bot.send_message(chat_id=update.message.chat_id, text=config.MEMBERS[index])