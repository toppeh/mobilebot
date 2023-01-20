from telegram.ext import CallbackContext
from telegram import Update
import config

def insv(update: Update, context: CallbackContext):
    context.bot.send_sticker(chat_id=update.message.chat_id, sticker=config.insv, disable_notification=True)