from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from get import generateKeyboard, build_menu, getMovie

def leffa(update: Update, context: CallbackContext):
    custom_keyboard = generateKeyboard()
    reply_markup = ReplyKeyboardMarkup(build_menu(custom_keyboard, n_cols=2), one_time_keyboard=True, selective=True)
    context.bot.send_message(chat_id=update.message.chat_id,
                                text=f'Leffoja @{update.message.from_user.username}',
                                reply_to_message_id=update.message.message_id,
                                reply_markup=reply_markup)

def leffaReply(update: Update, context: CallbackContext):
    if update.message.reply_to_message is None:
        return
    if "Leffoja" not in update.message.reply_to_message.text:
        return
    premiere = getMovie(update.message.text)
    reply_markup = ReplyKeyboardRemove()
    if premiere == 'Ensi-iltaa ei löytynyt':
        context.bot.send_message(chat_id=update.message.chat_id, text=f'{premiere} :/', reply_markup=reply_markup)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=f'Ensi-ilta on {premiere}', reply_markup=reply_markup)