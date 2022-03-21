# -*- coding: utf-8 -*-

import regex
import logging
import sqlite3

from datetime import datetime
import config
import stuff
import get
import quiz
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, PrefixHandler, CallbackContext
from telegram import TelegramError, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Poll
import random
from time import time
from weather import WeatherGod
from sys import maxsize


# TODO: fix leffa, cocktail, joulu, jussi, kick (bot.kick_chat_member -> bot.ban_chat_member)
class TelegramBot:
    def __init__(self):
        logging.basicConfig(filename='mobile.log', format='%(asctime)s - %(name)s - %(levelname)s - '
                            '%(message)s', filemode='w', level=logging.WARNING)

        updater = Updater(token=config.TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        
        self.commands = {'wabu': self.wabu,
                         'kiitos': self.kiitos,
                         'sekseli': self.sekseli,
                         'poyta': self.poyta,
                         #'pöytä': self.poyta,
                         'insv': self.insv,
                         'quoteadd': self.quoteadd,
                         'addquote': self.quoteadd,
                         'quote': self.quote,
                         'viisaus': self.viisaus,
                         'saa': self.weather,
                         #'sää': self.weather,
                         'kuka': self.kuka,
                         'value_of_content': self.voc,
                         'voc': self.voc,
                         'cocktail': self.cocktail,
                         'episode_ix': self.episode_ix,
                         'kick': self.kick,
                         'leffa': self.leffa,
                         'voivoi': self.voivoi,
                         'fiilis': self.getFiilis,
                         'arki': self.arki,
                         'viikonloppu': self.viikonloppu,
                         'rudelf': self.rudelf,
                         'skalja': self.credit,
                         'skredit': self.credit,
                         'hyvaajouluaturvemestari': self.hyvaajoulua,
                         'hyvaajuhannusta': self.hyvaajussia,
                         'kissa': self.kissa,
                         'joke': self.joke,
                         'xkcd': self.xkcd,
                         'visa': self.visa
                         }

        for cmd, callback in self.commands.items():
            dispatcher.add_handler(PrefixHandler(['!', '.', '/'], cmd, callback))
            dispatcher.add_handler(CommandHandler(cmd, callback)) # ÄLÄ POISTA TAI KOMMENTOI
        
        dispatcher.add_handler(MessageHandler(Filters.photo, self.getFiilis))
        dispatcher.add_handler(MessageHandler(Filters.status_update.pinned_message, self.pinned))
        dispatcher.add_handler(MessageHandler(Filters.text, self.huuto))

        # TODO: Tee textHandler niminen funktio mikä on sama kuin commandsHandler mutta tekstille
        # TODO: Ota voc_add pois huuto():sta :DDD
        # TODO: Tee filtterit niin, että gifit ja kuvat kasvattaa self.voc_msg:eä

        self.kissaCache = []
        dispatcher.job_queue.run_repeating(self.voc_check, interval=60, first=5)
        dispatcher.job_queue.run_repeating(self.refreshCache, interval=60, first=5)

        self.noCooldown = (self.quoteadd, self.leffa, self.kick)
        self.users = {}  # user_id : unix timestamp
        self.voc_cmd = list()
        self.voc_msg = list()
        self.regex = dict()
        self.regexInit()
        get.create_tables()
        updater.start_polling()
        # updater.idle()
        logging.info('Botti käynnistetty')

    def refreshCache(self, update: Update):
        while len(self.kissaCache) < 10:
            url = get.cat()
            self.kissaCache.append(url)


    @staticmethod
    def wabu(update: Update, context: CallbackContext):
        wabu = datetime(2021, 4, 15, 13)
        tanaan = datetime.now()
        erotus = wabu - tanaan
        hours = erotus.seconds // 3600
        minutes = (erotus.seconds - hours*3600) // 60
        seconds = erotus.seconds - hours * 3600 - minutes * 60
        """
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f'Wabun alkuun on {erotus.days} päivää, {hours} tuntia, {minutes} minuuttia ja'
                                      f' {seconds} sekuntia',
                                 disable_notification=True)
        """
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f'Wappu on joskus',
                                 disable_notification=True)

    @staticmethod
    def episode_ix(update: Update, context: CallbackContext):
        wabu = datetime(2019, 12, 20)
        tanaan = datetime.now()
        erotus = wabu - tanaan
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f'Ensi-iltaan on mennyt jo kauan sitten.', disable_notification=True)

    @staticmethod
    def kiitos(update: Update, context: CallbackContext):
        if update.message.reply_to_message is not None:
            count = get.kiitosCounter(update.message.reply_to_message.from_user.id)
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f'Kiitos {update.message.reply_to_message.from_user.first_name}!\n'
                                     f'{update.message.reply_to_message.from_user.first_name} on saanut kiitoksen jo {count} kertaa!',
                                     disable_notifications=True)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='Kiitos Jori!', disable_notification=True)

    @staticmethod
    def voivoi(update: Update, context: CallbackContext):
        if update.message.reply_to_message is not None:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f'voi voi {update.message.reply_to_message.from_user.first_name}😩😩😩',
                                     disable_notifications=True)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='voi voi Nuutti😩😩😩', disable_notification=True)

    @staticmethod
    def sekseli(update: Update, context: CallbackContext):
        if update.message.chat_id == config.MOBILE_ID:
            context.bot.forward_message(chat_id=update.message.chat_id, from_chat_id=config.MOBILE_ID,
                                        message_id=316362, disable_notification=True)

    @staticmethod
    def poyta(update: Update, context: CallbackContext):
        context.bot.send_animation(chat_id=update.message.chat_id, animation=config.desk, disable_notification=True)

    @staticmethod
    def insv(update: Update, context: CallbackContext):
        context.bot.send_sticker(chat_id=update.message.chat_id, sticker=config.insv, disable_notification=True)

    @staticmethod
    def pinned(update: Update, context: CallbackContext):
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

    def quoteadd(self, update: Update, context: CallbackContext):
        match = self.regex["quoteadd"].match(update.message.text)
        if match:
            temp = (match[1], match[2], update.message.chat_id)
            # tarkasta onko sitaatti jo lisätty joskus aiemmin
            result = get.dbQuery("SELECT * FROM quotes WHERE quotee=? AND quote=? AND groupID=?", temp)
            if len(result) != 0:
                context.bot.send_message(chat_id=update.message.chat_id, text="Toi on jo niin kuultu...",
                                         disable_notification=True)
                return
            quote = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), match[1],
                     match[2], update.message.from_user.username, update.message.chat_id)
            conn = sqlite3.connect(config.DB_FILE)
            cur = conn.cursor()
            sql_insert = "INSERT INTO quotes VALUES (?,?,?,?,?)"
            cur.execute(sql_insert, quote)
            conn.commit()
            conn.close()
            context.bot.send_message(chat_id=update.message.chat_id, text="Sitaatti suhahti")
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Opi käyttämään komentoja pliide bliis!! (/quoteadd"
                                          " <nimi> <sitaatti>)")

    @staticmethod
    def quote(update: Update, context: CallbackContext):
        space = update.message.text.find(' ')
        if space == -1:
            quotes = get.dbQuery("SELECT * FROM quotes WHERE groupID=? ORDER BY RANDOM() LIMIT 1", (update.message.chat_id,))
            if len(quotes) == 0:
                context.bot.send_message(chat_id=update.message.chat_id, text='Yhtään sitaattia ei ole lisätty.')
                return
        else:
            name = update.message.text[space + 1:]
            quotes = get.dbQuery("""SELECT * FROM quotes WHERE LOWER(quotee)=? AND groupID=? ORDER BY RANDOM() LIMIT 1""",
                      (name.lower(),
                       update.message.chat_id))
            if len(quotes) == 0:
                context.bot.send_message(chat_id=update.message.chat_id, text='Ei löydy')
                return
        context.bot.send_message(chat_id=update.message.chat_id, text=f'"{quotes[0][2]}" -{quotes[0][1]}')

    @staticmethod
    def viisaus(update: Update, context: CallbackContext):
        wisenings = get.dbQuery("SELECT * FROM sananlaskut ORDER BY RANDOM() LIMIT 1")
        context.bot.send_message(chat_id=update.message.chat_id, text=wisenings[0][0])

    @staticmethod
    def kuka(update: Update, context: CallbackContext):
        index = random.randint(0, len(config.MEMBERS)-1)
        context.bot.send_message(chat_id=update.message.chat_id, text=config.MEMBERS[index])


    @staticmethod
    def weather(update: Update, context: CallbackContext):
        try:
            city = update.message.text[5:]
            weather = WeatherGod()
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=weather.generateWeatherReport(city))
        except AttributeError:
            context.bot.send_message(chat_id=update.message.chat_id,
                             text="Komento vaatii parametrin >KAUPUNKI< \n"
                                  "Esim: /saa Hervanta ")
            return

    @staticmethod
    def kick(update: Update, context: CallbackContext):
        try:
            context.bot.banChatMember(chat_id=update.message.chat.id, user_id=update.message.from_user.id, until_date=time()+60, revoke_messages=False)
            link = context.bot.createChatInviteLink(chat_id=update.message.chat_id, expire_date=time()+7200, member_limit=1)
            if link:
                invite = lambda context : context.bot.send_message(chat_id=context.job.context[0], text=f"{context.job.context[1]}, linkki vanhenee kahden tunnin päästä BEEP BOOP.")
                context.job_queue.run_once(invite, 60, context=[update.message.from_user.id, link['invite_link']])
        except TelegramError:
            context.bot.send_message(chat_id=update.message.chat_id, text="Vielä joku päivä...")

    def voc(self, update: Update, context: CallbackContext):
        if self.voc_calc():
            context.bot.send_message(chat_id=update.message.chat_id, text="Value of content: Laskussa")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Value of content: Nousussa")

    def voc_check(self, update: Update):
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

    def voc_add(self, update: Update):
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
    def cocktail(update: Update, context: CallbackContext):
        adj = get.dbQuery('''SELECT * FROM adjektiivit ORDER BY RANDOM() LIMIT 1''')[0][0].capitalize() # fetchall returns tuple in list
        sub = get.dbQuery('''SELECT * FROM substantiivit ORDER BY RANDOM() LIMIT 1''')[0][0]

        if update.message.text[0:12] == '/cocktail -n':
            context.bot.send_message(chat_id=update.message.chat_id, text=f'{adj} {sub}', disable_notification=True)
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

        context.bot.send_message(chat_id=update.message.chat_id, text=msg)

    def huuto(self, update: Update, context: CallbackContext):
        rng = random.randint(0, 99)
        #self.voc_add(update)
        self.leffaReply(update, context)
        if rng >= len(stuff.message) or not self.regex["huuto"].match(update.message.text):
            return

        context.bot.send_message(chat_id=update.message.chat_id, text=stuff.message[rng], disable_notification=True)

    @staticmethod
    def leffa(update: Update, context: CallbackContext):
        custom_keyboard = get.generateKeyboard()
        reply_markup = ReplyKeyboardMarkup(get.build_menu(custom_keyboard, n_cols=2))
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Leffoja",
                                 reply_markup=reply_markup)

    @staticmethod
    def leffaReply(update: Update, context: CallbackContext):
        if update.message.reply_to_message is None:
            return
        if update.message.reply_to_message.text != "Leffoja":
            return
        premiere = get.getMovie(update.message.text)
        reply_markup = ReplyKeyboardRemove()
        context.bot.send_message(chat_id=update.message.chat_id, text=f'Ensi-ilta on {premiere}', reply_markup=reply_markup)

    def getFiilis(self, update: Update, context: CallbackContext):
        if (update.message.photo and not update.message.caption):
            return
        elif update.message.photo and 'fiilis' not in update.message.caption:
            return
        imgUrl = get.getImage(self.regex["fiilis"])
        if imgUrl != "":
            context.bot.send_message(chat_id=update.message.chat_id, text=imgUrl)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Ei fiilistä")

    @staticmethod
    def viikonloppu(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f'On viiiiiikonloppu! https://youtu.be/vkVidHRkF88',
                                 disable_notifications=True)

    @staticmethod
    def arki(update: Update, context: CallbackContext):
      context.bot.send_message(chat_id=update.message.chat_id,
                               text=f'https://open.spotify.com/track/6V2XKKilzsIcGAIsDhwEhF?si=eabb43bae9c446aa')

    def rudelf(self, update: Update, context: CallbackContext):
        if update.message.reply_to_message is False or update.message.reply_to_message.text is None:
            return
        # Capitalize
        msg = update.message.reply_to_message.text[0].upper() + update.message.reply_to_message.text[1:]
        for key, val in self.regex["rudismit"].items():
            msg = regex.sub(key, val, msg)
        if random.randint(0,9) < 3:
            msg = msg + " 😅"
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=msg, disable_notification=True)

    def credit(self, update: Update, context: CallbackContext):
        m = self.regex["credit"].match(update.message.text)
        treasury = m.group(1)
        params = (treasury, update.message.from_user.id)        
        res = get.dbQuery("SELECT username, amount FROM credits WHERE treasury=? AND id=?", params)
        # Kerro käyttäjän saldo
        if m.group(2) is None and len(res) != 0:
            context.bot.send_message(text=f"{res[0][0]}: {get.centsToEuroStr(res[0][1])}€", chat_id=update.message.chat_id)
            return
        # Kannasta ei löytynyt käyttäjää
        elif m.group(2) is None and len(res) == 0:
            context.bot.send_message(text=f'Ei löydy. Kannattaa lisätä krediittejä komennolla /{treasury} {{määrä}} =)', chat_id=update.message.chat_id)
            return

        input = m.group(2)
        # Korjaa kirjoitusvirhe
        if " " in m.group(2):
            parted = m.group(2).partition(" ")
            input = parted[0] + parted[2]

        # Päivitä uuteen saldoon
        if len(res) != 0:
            try:
                diff = int(float(input.replace(",", "."))*100)
            except ValueError:
                diff = int(float(input.replace(",", ".").partition(".")[0]) * 100)

            if abs(res[0][1] + diff) > maxsize:
                context.bot.send_message(text="Ei onnistu, lopputulos on liian iso/pieni luku", chat_id=update.message.chat_id)
                return
            params = (res[0][1]+diff, treasury, update.message.from_user.id,)
            sql = f"UPDATE credits SET amount=? WHERE treasury=? AND id=?"
            get.dbInsertUpdate(sql, params)
            context.bot.send_message(text=f"Uusi tasapaino:\n{res[0][0]}: {get.centsToEuroStr(res[0][1]+diff)}€", chat_id=update.message.chat_id)
        # Lisää uusi käyttäjä ja saldo
        else:
            amount = int(float(input.replace(",", "."))*100)
            params = (treasury, update.message.from_user.id, update.message.from_user.username,
                      amount)
            sql = f"INSERT INTO credits VALUES (?,?,?,?)"
            get.dbInsertUpdate(sql, params)
            context.bot.send_message(text=f"Uusi tasapaino:\n{update.message.from_user.username}: {get.centsToEuroStr(amount)}€",
                                     chat_id=update.message.chat_id)
            return


    def hyvaajoulua(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.message.chat_id,
                                    text=f'Kiitos :) ! Hyvää joulua myös sinulle {update.message.from_user.first_name}!',
                                    disable_notifications=True)

    def hyvaajussia(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.message.chat_id,
                                    text=f'Kiitos :) ! Hyvää jussia myös sinulle {update.message.from_user.first_name}!',
                                    disable_notifications=True)


    def kissa(self, update: Update, context: CallbackContext):
        if len(self.kissaCache) > 0:
            kissa_url = self.kissaCache[0]
            self.kissaCache = self.kissaCache[1:]
        else:
            kissa_url = get.cat()

        context.bot.send_animation(chat_id=update.message.chat_id, animation=kissa_url)

    def regexInit(self):
        self.regex["quoteadd"] = regex.compile(r'\/quoteadd (.[^\s]+) (.+)')
        self.regex["huuto"] = regex.compile(r"^(?![\W])[^[:lower:]]+$")
        self.regex["credit"] = regex.compile(r"\/(skalja|skredit) *(([\+-])? ?(\d+[\.,]?\d{0,2}))?")
        self.regex["fiilis"] = regex.compile(r'url":"(https:\/\/image.shutterstock.com\/image-[(?:photo)(?:vector)]+/.+?.jpg)"')
        self.regex["rudismit"] = dict()
        for key, val in stuff.rudismit.items():
            self.regex["rudismit"][regex.compile(key)] = val

    def joke(self, update: Update, context: CallbackContext):
        joke = get.joke()
        if joke is None:
            context.bot.send_message(chat_id=update.message.chat_id, text="Tapahtui virhe")
        else:
            msg = f'{joke["setup"]}\n{joke["punchline"]}'
            context.bot.send_message(chat_id=update.message.chat_id, text=msg, disable_notification=True)

    def xkcd(self, update: Update, context: CallbackContext):
      max = get.getNewestXkcd()
      rnd = random.randint(1, max)
      imgUrl = get.getXkcd(rnd)
      context.bot.send_photo(chat_id=update.message.chat_id, photo=imgUrl)
    
    def visa(self, update: Update, context: CallbackContext):
        visa = quiz.getQuizQuestion()
        context.bot.send_poll(chat_id=update.message.chat_id, question=visa['question'], options=visa['all_answers'],
                              correct_option_id=visa['correct_answer_index'], type=Poll.QUIZ, is_anonymous=False, open_period=600)
            
if __name__ == '__main__':
    TelegramBot()
