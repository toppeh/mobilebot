from telegram.ext import CallbackContext
from telegram import Update
from datetime import datetime

def wabu(update: Update, context: CallbackContext):
    wabu = datetime(2023, 4, 13, 13)
    tanaan = datetime.now()
    erotus = wabu - tanaan
    hours = erotus.seconds // 3600
    minutes = (erotus.seconds - hours*3600) // 60
    seconds = erotus.seconds - hours * 3600 - minutes * 60
    
    context.bot.send_message(chat_id=update.message.chat_id,
                                text=f'Wabun alkuun on {erotus.days} päivää, {hours} tuntia, {minutes} minuuttia ja'
                                    f' {seconds} sekuntia',
                                disable_notification=True)
    '''    
    context.bot.send_message(chat_id=update.message.chat_id,
                                text=f'Wappu on joskus',
                                disable_notification=True)
    '''