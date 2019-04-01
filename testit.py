import sqlite3
import config
import random


def cocktail():

    spirits = (
        'Jaloviinaa*',
        'Jaloviinaa**',
        'Jaloviinaa***',
        'Vergiä',
        'vodkaa',
        'tequilaa',
        'giniä',
        'Bacardia',
        'martinia',
        'absinttia',
        'punaviiniä',
        'valkoviiniä',
        'Jägermeisteria',
        'viskiä',
        'salmiakkikossua',
        'rommia',
        'konjakkia',
        'Baileys',
        'Gambinaa',
        'Carilloa',
        'Valdemaria',
        '???'
    )

    mixers = (
        'olutta',
        'kiljua',
        'glögiä',
        'vettä',
        'Coca-Colaa',
        'energiajuomaa',
        'lonkeroa',
        'Spriteä',
        'maitoa',
        'kahvia',
        'kuohuviiniä',
        'shamppanjaa',
        'pontikkaa',
        'simaa',
        'sangriaa',
        'tonic-vettä',
        'siideriä',
        'roséviiniä',
        'bensaa',
        'kirsikkamehua',
        'ananasmehua',
        'appelsiinimehua',
        'omenamehua',
        'mitä tahansa',
        'piimää',
        'Muumi-limpparia',
        'extra virgin -oliiviöljyä'
    )
    conn = sqlite3.connect(config.DB_FILE)
    c = conn.cursor()
    sql = '''SELECT * FROM adjektiivit ORDER BY RANDOM() LIMIT 1'''
    c.execute(sql)
    adj = c.fetchall()[0][0].capitalize()  # fetchall returns tuple in list

    sql = '''SELECT * FROM substantiivit ORDER BY RANDOM() LIMIT 1'''
    c.execute(sql)
    sub = c.fetchall()[0][0]

    conn.close()

    # generate cocktail name
    msg = str(adj) + " " + str(sub) + ":\n"

    floor = random.randint(0, 1)

    # generate spirit(s)
    used = []

    for i in range(floor, 3):
        index = random.randint(0, len(spirits) - 1)
        while index in used:
            index = random.randint(0, len(spirits)-1)
        used.append(index)
        rnd = spirits[index]
        vol = str(random.randrange(2, 8, 2))
        msg += "-" + vol + (3 - len(str(vol))) * " " + "cl " + rnd + "\n"

    # generate mixer(s)
    used = []

    if floor == 0:
        # in case of no spirits, lift the floor to 1
        # so recipe contains at least one mixer
        floor += 1

    for i in range(random.randint(floor, 3)):
        index = random.randint(0, len(spirits) - 1)
        while index in used:
            index = random.randint(0, len(spirits) - 1)
        used.append(index)
        rnd = mixers[index]
        vol = str(random.randrange(5, 20, 5))
        msg += "-" + vol + (3 - len(str(vol))) * " " + "cl " + rnd + "\n"

    print(msg)


for h in range(100):
    cocktail()
