# -*- coding: utf-8 -*-

import regex
import logging
import sqlite3

from datetime import timedelta, datetime
import config
import stuff
import leffa
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram import TelegramError, ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
from time import time
from weather import WeatherGod


class TelegramBot:
    def __init__(self):
        logging.basicConfig(filename='mobile.log', format='%(asctime)s - %(name)s - %(levelname)s - '
                            '%(message)s', filemode='w', level=logging.WARNING)

        updater = Updater(token=config.TOKEN_KB)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("kick", self.kick, pass_job_queue=True))
        dispatcher.add_handler(MessageHandler(Filters.command, self.commandsHandler))
        dispatcher.add_handler(MessageHandler(Filters.status_update.pinned_message, self.pinned))
        dispatcher.add_handler(MessageHandler(Filters.text, self.huuto))
        # TODO: Tee textHandler niminen funktio mikä on sama kuin commandsHandler mutta tekstille
        # TODO: Ota voc_add pois huuto():sta :DDD
        # TODO: Tee filtterit niin, että gifit ja kuvat kasvattaa self.voc_msg:eä

        dispatcher.job_queue.run_repeating(self.voc_check, interval=60, first=5)

        self.commands = {'wabu': self.wabu,
                         'kiitos': self.kiitos,
                         'sekseli': self.sekseli,
                         'poyta': self.poyta,
                         'insv': self.insv,
                         'quoteadd': self.quoteadd,
                         'quote': self.quote,
                         'viisaus': self.viisaus,
                         'saa': self.weather,
                         'sää': self.weather,
                         'kuka': self.kuka,
                         'value_of_content': self.voc,
                         'voc': self.voc,
                         'cocktail': self.cocktail,
                         'episode_ix': self.episode_ix,
                         'kick': self.kick,
                         'leffa': self.leffa
                         }
        self.users = {}  # user_id : unix timestamp
        self.voc_cmd = list()
        self.voc_msg = list()
        self.create_tables()
        updater.start_polling()
       # updater.idle()
        logging.info('Botti käynnistetty')


    @staticmethod
    def wabu(bot, update):
        wabu = datetime(2020, 4, 13, 13)
        tanaan = datetime.now()
        erotus = wabu - tanaan
        hours = erotus.seconds // 3600
        minutes = (erotus.seconds - hours*3600) // 60
        seconds = erotus.seconds - hours * 3600 - minutes * 60

        bot.send_message(chat_id=update.message.chat_id,
                         text=f'Wabun alkuun on {erotus.days} päivää, {hours} tuntia, {minutes} minuuttia ja {seconds} '
                         f'sekuntia', disable_notification=True)

    @staticmethod
    def episode_ix(bot, update):
        wabu = datetime(2019, 12, 20)
        tanaan = datetime.now()
        erotus = wabu - tanaan
        bot.send_message(chat_id=update.message.chat_id,
                         text=f'Ensi-iltaan on {erotus.days} päivää.', disable_notification=True)

    @staticmethod
    def kiitos(bot, update):
        if update.message.reply_to_message is not None:
            bot.send_message(chat_id=update.message.chat_id,
                             text=f'Kiitos {update.message.reply_to_message.from_user.first_name}!',
                             disable_notifications=True)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Kiitos Jori!', disable_notification=True)

    @staticmethod
    def sekseli(bot, update):
        if update.message.chat_id == config.MOBILE_ID:
            bot.forward_message(chat_id=update.message.chat_id, from_chat_id=config.MOBILE_ID, message_id=316362,
                                disable_notification=True)

    @staticmethod
    def poyta(bot, update):
        bot.send_animation(chat_id=update.message.chat_id, animation=config.desk, disable_notification=True)

    @staticmethod
    def insv(bot, update):
        bot.send_sticker(chat_id=update.message.chat_id, sticker=config.insv, disable_notification=True)

    def cooldownFilter(self, update):
        cordon = 3600  # time in seconds
        #  cordon = 1  # For testing purposes
        if not update.message.from_user.id:
            # Some updates are not from any user -- ie when bot is added to a group
            return False

        user_id = update.message.from_user.id

        if user_id not in self.users.keys():
            # new user, add id to users
            self.users[user_id] = time()
            return True

        else:
            # old user
            if time() - self.users[user_id] < cordon:
                # caught in spam filter
                return False
            else:
                # passed the spam filter.
                self.users[user_id] = time()
                return True

    def commandsHandler(self, bot, update):
        # Ignore messages older than 30 seconds
        if not datetime.today() - update.message.date < timedelta(0, 30):
            return
        if update.message.entities is None:
            return
        commands = self.commandParser(update.message)
        for command in commands:
            if command in self.commands:
                if self.cooldownFilter(update):
                    self.commands[command](bot, update)
        self.voc_add(bot, update)

    @staticmethod
    def commandParser(msg):
        # Parses commands from the message, changing them to lowercase and removing the slash and bot's name.
        commands = list()
        for i in msg.entities:
            if i.type == 'bot_command':
                command = msg.text[i.offset + 1: i.offset + i.length].lower()
                temp = command.split('@')
                if len(temp) > 1 and temp[1] == "kiitos_jori_bot":
                    commands.append(temp[0])
                elif len(temp) == 1:
                    commands.append(temp[0])
        is_desk = msg.text.find('pöytä')
        if is_desk != -1:
            commands.append(msg.text["poyta"])
        return commands

    @staticmethod
    def pinned(bot, update):
        try:
            if update.message.pinned_message:
                if update.message.chat_id == config.MOBILE_ID:
                    sql = "INSERT INTO pinned VALUES (?,?,?)"
                    pinned = (update.message.date.isoformat(), update.message.pinned_message.from_user.username,
                              update.message.pinned_message.text)
                    conn = sqlite3.connect(config.DB_FILE)
                    cur = conn.cursor()
                    cur.execute(sql, pinned)
                    conn.commit()
                    conn.close()

        except KeyError:
            return False

    @staticmethod
    def quoteadd(bot, update):
        text = update.message.text
        first_space = 9
        if text[first_space] != ' ':
            bot.send_message(chat_id=update.message.chat_id, text="Opi käyttämään komentoja pliide bliis!! (/quoteadd"
                                                                  " <nimi> <sitaatti>)")
            return False
        # try to find the end of the name
        try:
            second_space = text.find(' ', first_space + 1)
        except IndexError:
            bot.send_message(chat_id=update.message.chat_id, text="Opi käyttämään komentoja pliide bliis!! (/quoteadd"
                                                                  " <nimi> <sitaatti>)")
            return

        if second_space != -1:
            temp = (text[10:second_space].lower(), text[second_space + 1:], update.message.chat_id)
            quote = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text[10:second_space].lower(),
                     text[second_space + 1:], update.message.from_user.username, update.message.chat_id)
            conn = sqlite3.connect(config.DB_FILE)
            cur = conn.cursor()
            sql_select = "SELECT * FROM quotes WHERE quotee=? AND quote=? AND groupID=?"
            cur.execute(sql_select, temp)
            result = cur.fetchall()
            if len(result) != 0:
                bot.send_message(chat_id=update.message.chat_id, text="Toi on jo niin kuultu...",
                                 disable_notification=True)
                return
            sql_insert = "INSERT INTO quotes VALUES (?,?,?,?,?)"
            cur.execute(sql_insert, quote)
            conn.commit()
            conn.close()
            bot.send_message(chat_id=update.message.chat_id, text="Sitaatti suhahti")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Opi käyttämään komentoja pliide bliis!! (/quoteadd"
                                                                  " <nimi> <sitaatti>)")
        if update.message.chat_id != config.MOBILE_ID:
            bot.send_message(chat_id=config.MOBILE_ID, text=f'@{update.message.from_user.username}'
                                                            f' lisäsi sitaatin jossain muualla kuin täällä o.O')

    @staticmethod
    def quote(bot, update):
        space = update.message.text.find(' ')
        conn = sqlite3.connect(config.DB_FILE)
        c = conn.cursor()
        if space == -1:
            c.execute("SELECT * FROM quotes WHERE groupID=? ORDER BY RANDOM() LIMIT 1", (update.message.chat_id,))
            quotes = c.fetchall()
            if len(quotes) == 0:
                bot.send_message(chat_id=update.message.chat_id, text='Yhtään sitaattia ei ole lisätty.')

        else:
            name = update.message.text[space + 1:]
            c.execute("""SELECT * FROM quotes WHERE quotee=? AND groupID=? ORDER BY RANDOM() LIMIT 1""",
                      (name.lower(),
                       update.message.chat_id))
            quotes = c.fetchall()
            if len(quotes) == 0:
                bot.send_message(chat_id=update.message.chat_id, text='Ei löydy')
                return
        bot.send_message(chat_id=update.message.chat_id, text=f'"{quotes[0][2]}" -{quotes[0][1].capitalize()}')

    @staticmethod
    def viisaus(bot, update):
        conn = sqlite3.connect(config.DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM sananlaskut ORDER BY RANDOM() LIMIT 1")
        wisenings = c.fetchall()
        bot.send_message(chat_id=update.message.chat_id, text=wisenings[0][0])

    @staticmethod
    def kuka(bot, update):
        index = random.randint(0, len(config.MEMBERS)-1)
        bot.send_message(chat_id=update.message.chat_id, text=config.MEMBERS[index])

    @staticmethod
    def create_tables():
        conn = sqlite3.connect(config.DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS substantiivit ("sub" text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS pinned ("date" text, "name" text, "text" text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS sananlaskut ("teksti" text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS adjektiivit ("adj" text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS quotes (
           "date" TEXT DEFAULT CURRENT_TIMESTAMP,
           "quotee" TEXT,
           "quote" TEXT,
           "adder" TEXT,
           "groupID" INT,
           PRIMARY KEY(quotee, quote, groupID)
           )
           ''')
        conn.close()

    @staticmethod
    def weather(bot, update):
        try:
            city = update.message.text[5:]
            weather = WeatherGod()
            bot.send_message(chat_id=update.message.chat_id,
                             text=weather.generateWeatherReport(city))
        except AttributeError:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Komento vaatii parametrin >KAUPUNKI< \n"
                                  "Esim: /saa Hervanta ")
            return

    @staticmethod
    def kick(bot, update, job_queue):
        try:
            bot.kickChatMember(update.message.chat.id, update.message.from_user.id)
            job_queue.run_once(TelegramBot.invite, 60, context=[update.message.chat_id, update.message.from_user.id])
        except TelegramError:
            bot.send_message(chat_id=update.message.chat_id, text="Vielä joku päivä...")

    @staticmethod
    def invite(bot, job):
        bot.unBanChatMember(chat_id=job.context[0], user_id=job.context[1])

    def voc(self, bot, update):
        if self.voc_calc():
            bot.send_message(chat_id=update.message.chat_id, text="Value of content: Laskussa")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Value of content: Nousussa")

    def voc_check(self, bot, job):
        now = time()
        while len(self.voc_cmd) > 0:
            if now - self.voc_cmd[0] > 7200:
                self.voc_cmd.pop(0)
            else:
                break
        while len(self.voc_msg) > 0:
            if now - self.voc_msg[0] > 7200:
                self.voc_msg.pop(0)
            else:
                return

    def voc_add(self, bot, update):
        if update.message.entities is None:
            self.voc_msg.append(time())
        for i in update.message.entities:
            if i.type == 'bot_command':
                self.voc_cmd.append(time())
            else:
                self.voc_msg.append(time())

    def voc_calc(self):
        now = time()
        cmds = 0
        for i in self.voc_cmd:
            if now - i < 900:
                cmds += 4
            elif 900 < now - i < 1800:
                cmds += 2
            else:
                cmds += 1
        msgs = 2 * len(self.voc_msg)
        # Minus 4 so that we dont count the calling /voc
        return cmds - 4 > msgs

    @staticmethod
    def cocktail(bot, update):
        conn = sqlite3.connect(config.DB_FILE)
        c = conn.cursor()
        sql = '''SELECT * FROM adjektiivit ORDER BY RANDOM() LIMIT 1'''
        c.execute(sql)
        adj = c.fetchall()[0][0].capitalize()  # fetchall returns tuple in list

        sql = '''SELECT * FROM substantiivit ORDER BY RANDOM() LIMIT 1'''
        c.execute(sql)
        sub = c.fetchall()[0][0]

        conn.close()

        if update.message.text[0:12] == '/cocktail -n':
            bot.send_message(chat_id=update.message.chat_id, text=f'{adj} {sub}', disable_notification=True)
            return

        # generate cocktail name
        msg = str(adj) + " " + str(sub) + ":\n"

        floor = random.randint(0, 1)

        # generate spirit(s)
        used = []

        for i in range(random.randint(0, 3) * floor):
            index = random.randint(0, len(stuff.spirits) - 1)
            while index in used:
                index = random.randint(0, len(stuff.spirits) - 1)
            used.append(index)
            rnd = stuff.spirits[index]
            vol = str(random.randrange(2, 8, 2))
            msg += "-" + vol + " " + "cl " + rnd + "\n"

        # generate mixer(s)
        used = []

        if floor == 0:
            # in case of no spirits, lift the floor to 1
            # so recipe contains at least one mixer
            floor = 1

        for i in range(random.randint(floor, 3)):
            index = random.randint(0, len(stuff.spirits) - 1)
            while index in used:
                index = random.randint(0, len(stuff.spirits) - 1)
            used.append(index)
            rnd = stuff.mixers[index]
            vol = str(random.randrange(5, 20, 5))
            msg += "-" + vol + " " + "cl " + rnd + "\n"

        bot.send_message(chat_id=update.message.chat_id, text=msg)

    def huuto(self, bot, update):
        rng = random.randint(0, 99)
        r = regex.compile(r"^(?![\W])[^[:lower:]]+$")
        self.voc_add(bot, update)
        self.leffaReply(bot, update)
        if rng >= len(stuff.message) or not r.match(update.message.text):
            return

        bot.send_message(chat_id=update.message.chat_id, text=stuff.message[rng], disable_notification=True)

    def leffa(self, bot, update):
        custom_keyboard = leffa.generateKeyboard()
        reply_markup = ReplyKeyboardMarkup(build_menu(custom_keyboard, n_cols=2))
        bot.send_message(chat_id=update.message.chat_id,
                         text="Leffoja",
                         reply_markup=reply_markup)

    @staticmethod
    def leffaReply(bot, update):
        if update.message.reply_to_message is None:
            return
        if update.message.reply_to_message.text != "Leffoja":
            return
        premiere = leffa.getMovie(update.message.text)
        reply_markup = ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text=f'Ensi-ilta on {premiere}', reply_markup=reply_markup)


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


if __name__ == '__main__':
    TelegramBot()
