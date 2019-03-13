import random


def juoma():

    juomat = ('olutta',
              'Jaloviinaa*',
              'Jaloviinaa**',
              'Jaloviinaa***',
              'Vergiä',
              'vodkaa',
              'kiljua',
              'glögiä',
              'vettä',
              'Coca-Colaa',
              'tequilaa',
              'energiajuomaa',
              'lonkeroa',
              'giniä',
              'Spriteä',
              'Gambinaa',
              'maitoa',
              'kahvia',
              'kuohuviiniä',
              'shamppanjaa',
              'pontikkaa',
              'simaa',
              'sangriaa',
              'martinia',
              'Bacardia',
              'tonic-vettä',
              'siideriä',
              'absinttia',
              'punaviiniä',
              'valkoviiniä',
              'roséviiniä',
              'bensaa',
              )

    resepti = ""
    for i in range(random.randint(2, 5)):
        tilavuus = random.randrange(5, 30, 5)
        resepti += "-" + str(tilavuus) + " cl " + random.choice(juomat) + "\n"

    print(resepti)

juoma()