from telegram.ext import CallbackContext
from telegram import Update

def viikonloppu(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                                text=f'On viiiiiikonloppu! https://youtu.be/vkVidHRkF88',
                                disable_notification=True)

def arki(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                            text=f'https://open.spotify.com/track/6V2XKKilzsIcGAIsDhwEhF?si=eabb43bae9c446aa')
