from telegram.ext import CallbackContext
from telegram import Update
from get import getJoke

def joke(update: Update, context: CallbackContext):
    joke = getJoke()
    if joke is None:
        context.bot.send_message(chat_id=update.message.chat_id, text="Tapahtui virhe")
    else:
        msg = f'{joke["setup"]}\n{joke["punchline"]}'
        context.bot.send_message(chat_id=update.message.chat_id, text=msg, disable_notification=True)