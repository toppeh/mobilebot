from telegram.ext import CallbackContext
from telegram import Update
from get import dbQuery

def viisaus(update: Update, context: CallbackContext):
        wisenings = dbQuery("SELECT * FROM sananlaskut ORDER BY RANDOM() LIMIT 1")
        context.bot.send_message(chat_id=update.message.chat_id, text=wisenings[0][0])
