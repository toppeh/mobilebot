from telegram.ext import CallbackContext
from telegram import Update
from get import dbQuery

def quote(update: Update, context: CallbackContext):
    space = update.message.text.find(' ')
    if space == -1:
        quotes = dbQuery("SELECT * FROM quotes WHERE groupID=? ORDER BY RANDOM() LIMIT 1", (update.message.chat_id,))
        if len(quotes) == 0:
            context.bot.send_message(chat_id=update.message.chat_id, text='Yhtään sitaattia ei ole lisätty.')
            return
    else:
        name = update.message.text[space + 1:]
        quotes = dbQuery("""SELECT * FROM quotes WHERE LOWER(quotee)=? AND groupID=? ORDER BY RANDOM() LIMIT 1""",
                    (name.lower(),
                    update.message.chat_id))
        if len(quotes) == 0:
            context.bot.send_message(chat_id=update.message.chat_id, text='Ei löydy')
            return
    context.bot.send_message(chat_id=update.message.chat_id, text=f'"{quotes[0][2]}" -{quotes[0][1]}')
