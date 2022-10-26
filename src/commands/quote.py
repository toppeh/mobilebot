from telegram.ext import CallbackContext
from telegram import Update
from datetime import datetime
from get import dbQuery, dbInsertUpdate
import config

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

def quoteadd(update: Update, context: CallbackContext):
    match = self.regex["quoteadd"].match(update.message.text)
    if match:
        temp = (match[1], match[2], update.message.chat_id)
        # tarkasta onko sitaatti jo lisätty joskus aiemmin
        result = dbQuery("SELECT * FROM quotes WHERE quotee=? AND quote=? AND groupID=?", temp)
        if len(result) != 0:
            context.bot.send_message(chat_id=update.message.chat_id, text="Toi on jo niin kuultu...",
                                        disable_notification=True)
            return
        quote = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), match[1],
                match[2], update.message.from_user.username, update.message.chat_id)
        '''conn = sqlite3.connect(config.DB_FILE)
        cur = conn.cursor()
        sql_insert = "INSERT INTO quotes VALUES (?,?,?,?,?)"
        cur.execute(sql_insert, quote)
        conn.commit()
        conn.close()'''
        sql_insert = "INSERT INTO quotes VALUES (?,?,?,?,?)"
        dbInsertUpdate(sql_insert, quote)
        context.bot.send_message(chat_id=update.message.chat_id, text="Sitaatti suhahti")
    else:
        context.bot.send_message(chat_id=update.message.chat_id,
                                    text="Opi käyttämään komentoja pliide bliis!! (/quoteadd"
                                        " <nimi> <sitaatti>)")
