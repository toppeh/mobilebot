from telegram.ext import CallbackContext
from telegram import Update
from get import getFiilis
from stuff import regexes

def fiilis(update: Update, context: CallbackContext):
    if (update.message.photo and not update.message.caption):
        return
    elif update.message.photo and 'fiilis' not in update.message.caption:
        return
    imgUrl = getFiilis(regexes["fiilis2"])
    if imgUrl != "":
        context.bot.send_message(chat_id=update.message.chat_id, text=imgUrl)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Ei fiilistä")