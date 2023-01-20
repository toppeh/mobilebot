import regex

spirits = ('Jaloviinaa*', 'Jaloviinaa**', 'Jaloviinaa***', 'Vergiä', 'vodkaa', 'tequilaa', 'giniä', 'Bacardia',
           'martinia', 'absinttia', 'punaviiniä', 'valkoviiniä', 'Jägermeisteria', 'viskiä', 'salmiakkikossua',
           'rommia', 'konjakkia', 'Baileys', 'Gambinaa', 'Carilloa', 'Valdemaria', '???')
mixers = ('olutta', 'kiljua', 'glögiä', 'vettä', 'Coca-Colaa', 'energiajuomaa', 'lonkeroa', 'Spriteä', 'maitoa',
          'kahvia', 'kuohuviiniä', 'shamppanjaa', 'pontikkaa', 'simaa', 'sangriaa', 'tonic-vettä', 'siideriä',
          'roséviiniä', 'bensaa', 'kirsikkamehua', 'ananasmehua', 'appelsiinimehua', 'omenamehua', 'mitä tahansa',
          'piimää', 'Muumi-limpparia', 'extra virgin -oliiviöljyä')
message = ["MITÄ??", "EIKU OLIN NUKKUMASSA", "OLITKOs VIELÄ NUKKUMASSA?", "MISSÄ??", "KUULUU HELVETIN HUONOSTI",
           "EI OLE EIKÄ TULE"]

feels = ["scared", "angry", "sad", "happy", "disgusted", "suprised", "trustful", "anticipating", "joyful", "anxious"]

emotions = ['Absorbed', 'Antsy', 'Bonhomie', 'Abhorrence', 'Anxiety', 'Boredom', 'Acceptance', 'Apathetic', 'Bothered', 'Admiration', 'Apologetic', 'Bouncy', 'Adoration', 'Appalled', 'Brave', 'Adrift',
            'Appreciative', 'Breathless', 'Aching', 'Apprehensive', 'Brooding', 'Affection', 'Ardor', 'Bubbly', 'Afraid', 'Arousal', 'Buoyant', 'Agitated', 'Astonishment', 'Burning', 'Agony', 'Astounded',
            'Calm', 'Aggravated', 'Attachment', 'Captivated', 'Alarm', 'Attraction', 'Carefree', 'Alert', 'Aversion', 'Caring', 'Alienated', 'Awe', 'Cautious', 'Alive', 'Awkward', 'Certain', 'Alone', 'Baffled',
            'Chagrin', 'Amazed', 'Bashful', 'Challenged', 'Amused', 'Befuddled', 'Chary', 'Anger', 'Bemused', 'Cheerful', 'Angst', 'Betrayed', 'Choked', 'Animated', 'Bewildered', 'Choleric', 'Animosity', 'Bitter',
            'Clueless', 'Animus', 'Blessed', 'Cocky', 'Annoyed', 'Bliss', 'Cold', 'Antagonistic', 'Blithe', 'Collected', 'Anticipation', 'Blue', 'Comfortable', 'Antipathy', 'Bold', 'Commiseration', 'Committed', 'Defeated',
            'Doleful', 'Compassionate', 'Dejection', 'Dopey', 'Complacent', 'Delectation', 'Doubtful', 'Complaisance', 'Delighted', 'Down', 'Composed', 'Delirious', 'Downcast', 'Compunction', 'Denial', 'Drained', 'Confused',
            'Derisive', 'Dread', 'Courage', 'Desire', 'Dubious', 'Concerned', 'Desolation', 'Dumbfounded', 'Confident', 'Despair', 'Eager', 'Conflicted', 'Despondent', 'Earnest', 'Consternation', 'Detached', 'Ease', 'Contemplative',
            'Determined', 'Ebullient', 'Contempt', 'Detestation', 'Ecstatic', 'Contentment', 'Devastated', 'Edgy', 'Contrition', 'Devotion', 'Elated', 'Cordial', 'Disappointed', 'Embarrassment', 'Cowardly', 'Disbelief',
            'Empathic', 'Crafty', 'Disdain', 'Empty', 'Cranky', 'Disgruntled', 'Enchantment', 'Craving', 'Disgust', 'Energetic', 'Crestfallen',
            'Disillusioned', 'Engrossed', 'Cross', 'Disinterested', 'Enjoyment', 'Cruel', 'Dismay', 'Enlightenment', 'Crummy', 'Distaste', 'Enmity', 'Crushed', 'Distracted', 'Entertainment', 'Curious',
            'Distress', 'Enthralled', 'Cynical', 'Disturbed', 'Enthusiasm', 'Envy', 'Genial', 'Hostile', 'Euphoria', 'Giddy', 'Humiliated', 'Exasperated', 'Glad', 'Humored', 'Excitement', 'Gleeful', 'Hurt',
            'Excluded', 'Gloomy', 'Hyper', 'Exhausted', 'Goofy', 'Hysterical', 'Exhilaration', 'Gratified', 'Impatient', 'Expectant', 'Grateful', 'Incensed', 'Exuberant', 'Greedy', 'Indifferent', 'Fanatical',
            'Grief', 'Indignant', 'Fascinated', 'Groggy', 'Infatuated', 'Fatigued', 'Grudging', 'Inferior', 'Feisty', 'Guarded', 'Inspired', 'Felicitous', 'Guilt', 'Intense', 'Fervor', 'Gung-ho', 'Interested',
            'Flabbergasted', 'Gusto', 'Intimacy', 'Floored', 'Hankering', 'Intimidated', 'Fondness', 'Happy', 'Intoxicated', 'Foolish', 'Harassed', 'Intrigued', 'Foreboding', 'Hatred', 'Introspective', 'Fortunate',
            'Heartache', 'Invigorated', 'Frazzled', 'Heartbroken', 'Irascible', 'Free', 'Helpless', 'Ire', 'Fretful', 'Hesitant', 'Irritated', 'Frightened', 'Hollow', 'Isolated', 'Frustrated', 'Homesick', 'Jaded',
            'Fulfilled', 'Hopeful', 'Jealous', 'Furious', 'Horrified', 'Jittery', 'Peaceful', 'Jocund', 'Mischievous', 'Peevish', 'Jolly', 'Miserable', 'Pensive', 'Jovial', 'Mollified', 'Perky', 'Joy', 'Mortified',
            'Perplexed', 'Jubilant', 'Motivated', 'Perturbed', 'Jumpy', 'Mournful', 'Pessimistic', 'Keen', 'Moved', 'Petrified', 'Lazy', 'Mystified', 'Petty', 'Left out', 'Nasty', 'Petulant', 'Lethargic', 'Nauseous',
            'Phlegmatic', 'Liberation', 'Needy', 'Pity', 'Lighthearted', 'Nervous', 'Playful', 'Liking', 'Neutral', 'Pleasure', 'Listless', 'Nonplussed', 'Positive', 'Lively', 'Nostalgic', 'Possessive', 'Lonely', 'Numb',
            'Powerful', 'Longing', 'Obsessed', 'Powerless', 'Lost', 'Offended', 'Preoccupied', 'Love', 'Optimistic', 'Protective', 'Lucky', 'Outrage', 'Proud', 'Lust', 'Overwhelmed', 'Psyched', 'Mad', 'Pacified', 'Pumped',
            'Meditative', 'Pain', 'Puzzled', 'Melancholic', 'Panic', 'Quizzical', 'Mellow', 'Paranoid', 'Rage', 'Merry', 'Passion', 'Rapture', 'Miffed', 'Pathetic', 'Rattled', 'Reassured', 'Satisfied', 'Sorry', 'Receptive',
            'Scandalized', 'Sour', 'Reflective', 'Scorn', 'Speechless', 'Regret', 'Secure', 'Spiteful', 'Relaxed', 'Self-', 'Conscious', 'Sprightly', 'Relief', 'Selfish', 'Stirred', 'Relish', 'Sensual', 'Stressed', 'Reluctance',
            'Sensitive', 'Strong', 'Remorse', 'Serendipitous', 'Stung', 'Repugnance', 'Serene', 'Stunned', 'Resentment', 'Settled', 'Stupefied', 'Resignation', 'Shaken', 'Submissive', 'Restless', 'Shame', 'Succor', 'Revolted',
            'Sheepish', 'Suffering', 'Sad', 'Shock', 'Suffocated', 'Sanguine', 'Shy', 'Sullen', 'Satisfied', 'Sick', 'Sunny', 'Scandalized', 'Silly', 'Superior', 'Scorn', 'Sincere', 'Sure', 'Secure', 'Skeptical', 'Surprised',
            'Self-', 'Conscious', 'Sluggish', 'Startled', 'Selfish', 'Smug', 'Sympathy', 'Sensual', 'Snappy', 'Tenderness', 'Sensitive', 'Solemn', 'Tense', 'Serendipitous', 'Solicitous', 'Terror', 'Serene', 'Somber', 'Testy',
            'Sad', 'Sore', 'Tetchy', 'Sanguine', 'Sorrow', 'Thankful', 'Thirst', 'Woe', 'Thoughtful', 'Wonder', 'Thrill', 'Woozy', 'Timid', 'Worry', 'Tired', 'Wrath', 'Titillation', 'Wretched', 'Tormented', 'Yearning', 'Zeal',
            'Torture', 'Zest', 'Touched', 'Uptight', 'Traumatized', 'Vehement', 'Tranquil', 'Vexation', 'Trepidation', 'Vigilant', 'Triumphant', 'Vindication', 'Troubled', 'Vindictive', 'Trust', 'Warmth', 'Twitchy', 'Wary', 'Upbeat',
            'Weak', 'Upset']

ssHeaders = {"Host": "www.shutterstock.com",
             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
             "Accept-Language": "en-GB,en;q=0.5",
             "Accept-Encoding": "gzip, deflate",
             "DNT": "1",
             "Upgrade-Insecure-Requests": "1"}

rudismit = {"[hH]ai": "🦈",
            "\?": "? 🤔",
            "[kK]akka": "💩",
            "[pP]aska": "💩",
            "tus": "tussu",
            "tys": "tyssy",
            "ksaa": "G",
            "kalja": "🍺",
            "kuu": "Q",
            "ku": "Q",
            "pee": "B",
            "pe": "B",
            "k": "G",
            "b": "🅱",
            }
            
regexes = dict()
regexes["huuto"] = regex.compile(r"^(?![\W])[^[:lower:]]+$")
regexes["quoteadd"] = regex.compile(r'(?:\/quoteadd|\/addquote|\/addq) (.[^\s]+) (.+)')
regexes["huuto"] = regex.compile(r"^(?![\W])[^[:lower:]]+$")
regexes["credit"] = regex.compile(r"\/(skalja|skredit) *(([\+-])? ?(\d+[\.,]?\d{0,2}))?")
regexes["fiilis"] = regex.compile(r'"(https:\/\/image.shutterstock.com\/image-[(?:photo)(?:vector)]+/.+?.jpg)"')
regexes['fiilis2'] = regex.compile(r'href="(\/fi\/image-[(?:photo)(?:vector)]+\/.+?)"')
regexes["rudismit"] = dict()
for key, val in rudismit.items():
    regexes["rudismit"][regex.compile(key)] = val