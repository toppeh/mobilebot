from telegram.ext import CallbackContext
from telegram import Update
from random import randint, randrange
from get import dbQuery
from stuff import spirits, mixers

def cocktail(update: Update, context: CallbackContext):
    adj = dbQuery('''SELECT * FROM adjektiivit ORDER BY RANDOM() LIMIT 1''')[0][0].capitalize() # fetchall returns tuple in list
    sub = dbQuery('''SELECT * FROM substantiivit ORDER BY RANDOM() LIMIT 1''')[0][0]
    if update.message.text[0:12] == '/cocktail -n':
        context.bot.send_message(chat_id=update.message.chat_id, text=f'{adj} {sub}', disable_notification=True)
        return

    # generate cocktail name
    msg = str(adj) + " " + str(sub) + ":\n"

    floor = randint(0, 1)

    # generate spirit(s)
    used = []

    for i in range(randint(0, 3) * floor):
        index = randint(0, len(spirits) - 1)
        while index in used:
            index = randint(0, len(spirits) - 1)
        used.append(index)
        rnd = spirits[index]
        vol = str(randrange(2, 8, 2))
        msg += "-" + vol + " " + "cl " + rnd + "\n"

    # generate mixer(s)
    used = []

    if floor == 0:
        # in case of no spirits, lift the floor to 1
        # so recipe contains at least one mixer
        floor = 1

    for i in range(randint(floor, 3)):
        index = randint(0, len(spirits) - 1)
        while index in used:
            index = randint(0, len(spirits) - 1)
        used.append(index)
        rnd = mixers[index]
        vol = str(randrange(5, 20, 5))
        msg += "-" + vol + " " + "cl " + rnd + "\n"

    context.bot.send_message(chat_id=update.message.chat_id, text=msg)