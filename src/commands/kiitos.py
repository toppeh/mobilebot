from telegram.ext import CallbackContext
from telegram import Update
from get import kiitosCounter

def kiitos(update: Update, context: CallbackContext):
    if update.message.reply_to_message is not None:
        count = kiitosCounter(update.message.reply_to_message.from_user.id)
        context.bot.send_message(chat_id=update.message.chat_id,
                                    text=f'Kiitos {update.message.reply_to_message.from_user.first_name}!\n'
                                    f'{update.message.reply_to_message.from_user.first_name} on saanut kiitoksen jo {count} kertaa!',
                                    disable_notification=True)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='Kiitos Jori!', disable_notification=True)