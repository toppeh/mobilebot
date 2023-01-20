from telegram.ext import CallbackContext
from telegram import Update
import config

def sekseli(update: Update, context: CallbackContext):
    if update.message.chat_id == config.MOBILE_ID:
        context.bot.forward_message(chat_id=update.message.chat_id, from_chat_id=config.MOBILE_ID,
                                    message_id=316362, disable_notification=True)