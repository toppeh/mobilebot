from telegram.ext import CallbackContext
from telegram import Update
import config

def poyta(update: Update, context: CallbackContext):
    context.bot.send_animation(chat_id=update.message.chat_id, animation=config.desk, disable_notification=True)