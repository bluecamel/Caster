from dragonfly import Choice

from castervoice.lib.actions import Key, Text


def caster_alphabet():
    return {
        "(air|arch)":      "a",  # 01
        "(bat|brov)":      "b",  # 02
        "(cap|char)":      "c",  # 03
        "(drum|delta)":    "d",  # 04
        "(each|echo)":     "e",  # 05
        "(fine|foxy)":     "f",  # 06
        "(gust|goof)":     "g",  # 07
        "(harp|hotel)":    "h",  # 08
        "(sit|India)":     "i",  # 09
        "(jury|julia)":    "j",  # 10
        "(krunch|kilo)":   "k",  # 11
        "(look|Lima)":     "l",  # 12
        "(made|Mike)":     "m",  # 13
        "(near|Novakeen)": "n",  # 14
        "(odd|oscar)":     "o",  # 15
        "(pit|prime)":     "p",  # 16
        "(quench|Quebec)": "q",  # 17
        "Romeo":           "r",  # 18
        "(sun|Sierra)":    "s",  # 19
        "(trap|tango)":    "t",  # 20
        "(urge|uniform)":  "u",  # 21
        "(vest|victor)":   "v",  # 22
        "(whale|whiskey)": "w",  # 23
        "(plex|x-ray)":    "x",  # 24
        "(yank|yankee)":   "y",  # 25
        "(zip|Zulu)":      "z"   # 26
    }


def get_alphabet_choice(spec):
    return Choice(spec, caster_alphabet())


def letters(big, dict1, dict2, letter):
    '''used with alphabet.txt'''
    d1 = str(dict1)
    if d1 != "":
        Text(d1).execute()
    if big:
        Key("shift:down").execute()
    letter.execute()
    if big:
        Key("shift:up").execute()
    d2 = str(dict2)
    if d2 != "":
        Text(d2).execute()


def letters2(big, letter):
    if big:
        Key(letter.capitalize()).execute()
    else:
        Key(letter).execute()


'''for fun'''


def elite_text(text):
    elite_map = {
        "a": "@",
        "b": "|3",
        "c": "(",
        "d": "|)",
        "e": "3",
        "f": "|=",
        "g": "6",
        "h": "]-[",
        "i": "|",
        "j": "_|",
        "k": "|{",
        "l": "|_",
        "m": r"|\/|",
        "n": r"|\|",
        "o": "()",
        "p": "|D",
        "q": "(,)",
        "r": "|2",
        "s": "$",
        "t": "']['",
        "u": "|_|",
        "v": r"\/",
        "w": r"\/\/",
        "x": "}{",
        "y": "`/",
        "z": r"(\)"
    }
    text = str(text).lower()
    result = ""
    for c in text:
        if c in elite_map:
            result += elite_map[c]
        else:
            result += c
    Text(result).execute()
