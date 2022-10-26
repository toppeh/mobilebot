from telegram.ext import CallbackContext
from telegram import Update, TelegramError
from time import time

def kick(update: Update, context: CallbackContext):
    try:
        context.bot.banChatMember(chat_id=update.message.chat.id, user_id=update.message.from_user.id, until_date=time()+60, revoke_messages=False)
        link = context.bot.createChatInviteLink(chat_id=update.message.chat_id, expire_date=time()+7200, member_limit=1)
        if link:
            invite = lambda context : context.bot.send_message(chat_id=context.job.context[0], text=f"{context.job.context[1]}, linkki vanhenee kahden tunnin päästä BEEP BOOP.")
            context.job_queue.run_once(invite, 60, context=[update.message.from_user.id, link['invite_link']])
    except TelegramError:
        context.bot.send_message(chat_id=update.message.chat_id, text="Vielä joku päivä...")