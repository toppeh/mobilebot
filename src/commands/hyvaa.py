from telegram.ext import CallbackContext
from telegram import Update

def hyvaajoulua(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                            text=f'Kiitos :) ! Hyvää joulua myös sinulle {update.message.from_user.first_name}!')

def hyvaajussia(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                            text=f'Kiitos :) ! Hyvää jussia myös sinulle {update.message.from_user.first_name}!')