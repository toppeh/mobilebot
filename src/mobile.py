# -*- coding: utf-8 -*-
import regex
import logging
import sqlite3
from datetime import datetime
import config
import stuff
import get
import quiz
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, PrefixHandler, CallbackContext, PollAnswerHandler
from telegram import TelegramError, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Poll
import random
from time import time
from commands.weather import weather
from sys import maxsize
from commands.wabu import wabu 
from commands.kiitos import kiitos
from commands.voivoi import voivoi
from commands.viisaus import viisaus
from commands.kuka import kuka
from commands.sekseli import sekseli
from commands.insv import insv
from commands.poyta import poyta
from commands.kick import kick
from commands.cocktail import cocktail
from commands.leffa import leffa, leffaReply
from commands.viikonloppu import viikonloppu, arki
from commands.quote import quote, quoteadd
from commands.hyvaa import hyvaajoulua, hyvaajussia
from commands.joke import joke
from commands.xkcd import xkcd
from commands.fiilis import fiilis

# TODO: fix quoteadd ja fiili -> self.regex!!!
class TelegramBot:
    def __init__(self):
        logging.basicConfig(filename='mobile.log', format='%(asctime)s - %(name)s - %(levelname)s - '
                            '%(message)s', filemode='w', level=logging.WARNING)

        updater = Updater(token=config.TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        
        self.commands = {'wabu': wabu,
                         'kiitos': kiitos,
                         'sekseli': sekseli,
                         'poyta': poyta,
                         'insv': insv,
                         'quoteadd': quoteadd,
                         'addquote': quoteadd,
                         'addq': quoteadd,
                         'quote': quote,
                         'viisaus': viisaus,
                         'saa': weather,
                         'kuka': kuka,
                         'value_of_content': self.voc,
                         'voc': self.voc,
                         'cocktail': cocktail,
                         'kick': kick,
                         'leffa': leffa,
                         'voivoi': voivoi,
                         'fiilis': fiilis,
                         'arki': arki,
                         'viikonloppu': viikonloppu,
                         'rudelf': self.rudelf,
                         'skalja': self.credit,
                         'skredit': self.credit,
                         'hyvaajouluaturvemestari': hyvaajoulua,
                         'hyvaajuhannusta': hyvaajussia,
                         'kissa': self.kissa,
                         'joke': joke,
                         'xkcd': xkcd,
                         'visa': self.visa,
                         'quiz': self.visa,
                         'visastats': self.visastats
                         }

        for cmd, callback in self.commands.items():
            dispatcher.add_handler(PrefixHandler(['!', '.', '/'], cmd, callback))
            dispatcher.add_handler(CommandHandler(cmd, callback)) # ÄLÄ POISTA TAI KOMMENTOI
        
        dispatcher.add_handler(MessageHandler(Filters.photo, fiilis))
        dispatcher.add_handler(MessageHandler(Filters.text, self.huuto))
        dispatcher.add_handler(PollAnswerHandler(self.visaAnswer))

        # TODO: Tee textHandler niminen funktio mikä on sama kuin commandsHandler mutta tekstille
        # TODO: Ota voc_add pois huuto():sta :DDD
        # TODO: Tee filtterit niin, että gifit ja kuvat kasvattaa self.voc_msg:eä

        self.kissaCache = []
        dispatcher.job_queue.run_repeating(self.voc_check, interval=60, first=5)
        dispatcher.job_queue.run_repeating(self.refreshCache, interval=60, first=5)

        self.noCooldown = (quoteadd, leffa, kick)
        self.users = {}  # user_id : unix timestamp
        self.voc_cmd = list()
        self.voc_msg = list()
        self.visas = dict()  # poll_id : correct answer
        get.create_tables()
        updater.start_polling()
        # updater.idle()
        logging.info('Botti käynnistetty')

    def refreshCache(self, update: Update):
        while len(self.kissaCache) < 10:
            url = get.cat()
            self.kissaCache.append(url)

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


    def huuto(self, update: Update, context: CallbackContext):
        rng = random.randint(0, 99)
        #self.voc_add(update)
        leffaReply(update, context)
        if rng >= len(stuff.message) or not stuff.regexes["huuto"].match(update.message.text):
            return
        context.bot.send_message(chat_id=update.message.chat_id, text=stuff.message[rng], disable_notification=True)

    def rudelf(self, update: Update, context: CallbackContext):
        if update.message.reply_to_message is False or update.message.reply_to_message.text is None:
            return
        # Capitalize
        msg = update.message.reply_to_message.text[0].upper() + update.message.reply_to_message.text[1:]
        for key, val in stuff.regexes["rudismit"].items():
            msg = regex.sub(key, val, msg)
        if random.randint(0,9) < 3:
            msg = msg + " 😅"
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=msg, disable_notification=True)

    def credit(self, update: Update, context: CallbackContext):
        m = stuff.regexes["credit"].match(update.message.text)
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

    def kissa(self, update: Update, context: CallbackContext):
        if len(self.kissaCache) > 0:
            kissa_url = self.kissaCache[0]
            self.kissaCache = self.kissaCache[1:]
        else:
            kissa_url = get.cat()

        context.bot.send_animation(chat_id=update.message.chat_id, animation=kissa_url)
    
    def visa(self, update: Update, context: CallbackContext):
        visa = quiz.getQuizQuestion()
        msg = context.bot.send_poll(chat_id=update.message.chat_id, question=visa['question'], options=visa['all_answers'],
                              correct_option_id=visa['correct_answer_index'], type=Poll.QUIZ, is_anonymous=False)
        if msg:
            self.visas[msg.poll.id] = visa['correct_answer_index']
            context.job_queue.run_once(self.endVisa, 86400, context=[msg.chat.id, msg.message_id, msg.poll.id])

    def endVisa(self, context: CallbackContext):
        del self.visas[context.job.context[2]]
        poll = context.bot.stop_poll(chat_id=context.job.context[0], message_id=context.job.context[1])

    def visaAnswer(self, update: Update, context: CallbackContext):
        if update.poll_answer.poll_id in self.visas:
            if update.poll_answer.option_ids[0] == self.visas[update.poll_answer.poll_id]:
                quiz.answer(update.poll_answer.user.id, True)
            else:
                quiz.answer(update.poll_answer.user.id, False)

    def visastats(self, update: Update, context: CallbackContext):
        stats = quiz.stats(update.message.from_user.id)
        if not stats:
            context.bot.send_message(chat_id=update.message.chat_id, text="Et ole vielä vastannut yhteenkään kysymykseen :/")
        stats = f"{update.message.from_user.first_name}" + stats
        context.bot.send_message(chat_id=update.message.chat_id, text=stats)

if __name__ == '__main__':
    TelegramBot()
