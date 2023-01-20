from telegram.ext import CallbackContext
from telegram import Update
from random import randint
from get import getNewestXkcdNum, getXkcd

def xkcd(update: Update, context: CallbackContext):
    max = getNewestXkcdNum()
    rnd = randint(1, max)
    imgUrl = getXkcd(rnd)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=imgUrl)