from telegram.ext import CallbackContext
from telegram import Update

def voivoi(update: Update, context: CallbackContext):
    if update.message.reply_to_message is not None:
        context.bot.send_message(chat_id=update.message.chat_id,
                                    text=f'voi voi {update.message.reply_to_message.from_user.first_name}😩😩😩',
                                    disable_notification=True)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='voi voi Nuutti😩😩😩', disable_notification=True)
