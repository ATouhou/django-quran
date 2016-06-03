import re

_unicode_to_buckwalter = {
    u"\u0621": "'",  # Hamza
    u"\u0622": "|",  # Alif + MaddahAbove (not used in Tanzil)
    u"\u0623": ">",  # Alif + HamzaAbove
    u"\u0624": "&",  # Waw + HamzaAbove
    u"\u0625": "<",  # Alif + HamzaBelow
    u"\u0626": "}",  # Ya + HamzaAbove
    u"\u0627": "A",  # Alif
    u"\u0628": "b",  # Ba
    u"\u0629": "p",  # TaMarbuta
    u"\u062A": "t",  # Ta
    u"\u062B": "v",  # Tha
    u"\u062C": "j",  # Jeem
    u"\u062D": "H",  # HHa
    u"\u062E": "x",  # Kha
    u"\u062F": "d",  # Dal
    u"\u0630": "*",  # Thal
    u"\u0631": "r",  # Ra
    u"\u0632": "z",  # Zain
    u"\u0633": "s",  # Seen
    u"\u0634": "$",  # Sheen
    u"\u0635": "S",  # Sad
    u"\u0636": "D",  # DDad
    u"\u0637": "T",  # TTa
    u"\u0638": "Z",  # DTha
    u"\u0639": "E",  # Ain
    u"\u063A": "g",  # Ghain
    u"\u0640": "_",  # Tatweel
    u"\u0641": "f",  # Fa
    u"\u0642": "q",  # Qaf
    u"\u0643": "k",  # Kaf
    u"\u0644": "l",  # Lam
    u"\u0645": "m",  # Meem
    u"\u0646": "n",  # Noon
    u"\u0647": "h",  # Ha
    u"\u0648": "w",  # Waw
    u"\u0649": "Y",  # AlifMaksura
    u"\u064A": "y",  # Ya

    u"\u0654": "#",  # HamzaAbove (extended)                        | hamza above horizontal line

    u"\u064B": "F",  # Fathatan
    u"\u064C": "N",  # Dammatan
    u"\u064D": "K",  # Kasratan
    u"\u064E": "a",  # Fatha
    u"\u064F": "u",  # Damma
    u"\u0650": "i",  # Kasra
    u"\u0651": "~",  # Shadda
    u"\u0652": "o",  # Sukun
    u"\u0653": "^",  # Maddah (extended)                            | mad
    u"\u0671": "{",  # Alif + HamzaWasl                             | hamza wasl
    u"\u0670": "`",  # AlifKhanjareeya                              | short elif above
    u"\u06DC": ":",  # SmallHighSeen (extended)                     | 2 places, sad > seen
    u"\u06DF": "@",  # SmallHighRoundedZero (extended)              | cezm above elif
    u"\u06E0": "\"",  # SmallHighUprightRectangularZero (extended)  | mostly above ana's last elif
    u"\u06E2": "[",  # SmallHighMeemIsolatedForm (extended)         | iklaab
    u"\u06E3": ";",  # SmallLowSeen (extended)                      | 1 place, sad > seen
    u"\u06E5": ",",  # SmallWaw (extended)                          | zamir
    u"\u06E6": ".",  # SmallYa (extended)                           | zamir
    u"\u06E8": "!",  # SmallHighNoon (extended)                     | 1 place nu!jiY, sura 21, aya id 2571
    u"\u06EA": "-",  # EmptyCentreLowStop (extended)                | 1 place major-Y`haA, sura 11, aya id 1514
    u"\u06EB": "+",  # EmptyCentreHighStop (extended)               | 1 place ta>oma+n~aA, sura 12, aya id 1607
    u"\u06EC": "%",  # RoundedHighStopWithFilledCentre (extended)   | 1 place 'aA%EojamiY~N, sura 41, aya id 4262
    u"\u06ED": "]",  # SmallLowMeem (extended)                      | 99 places ??
    u" ": " ",

    # not in quran
    u"\u067E": "P",  # Peh (not Quranic)
    u"\u0686": "J",  # Tcheh (not Quranic)
    u"\u06A4": "V",  # Veh (not Quranic)
    u"\u06AF": "G",  # Gaf (not Quranic)
}


_buckwalter_to_unicode = {}
for u, bw in _unicode_to_buckwalter.items():
    _buckwalter_to_unicode[bw] = u



diacritics_latin = 'FNKaui~o^{`:@"[;,.!-+%]'
diacritics_latin_regex = '[FNKaui~o^{`:@"[;,.!-+%\]]'

def remove_diacritics_latin(input_str):
    return re.sub(diacritics_latin_regex, '', input_str)

diacritics_unicode = u'['
for bw in diacritics_latin:
    diacritics_unicode += _buckwalter_to_unicode[bw]
diacritics_unicode += ']'

def remove_diacritics_unicode(input_str):
    return re.sub(diacritics_unicode, '', input_str)



def get_unicode(buckwalter_str):
    """
    >>> get_unicode('yaHoyaY`')
    u'\u064a\u064e\u062d\u0652\u064a\u064e\u0649\u0670'
    """
    result = u""
    for char in buckwalter_str:
        result += _buckwalter_to_unicode[char]
    return result


def get_buckwalter(unicode_str):
    """
    >>> get_buckwalter(u'\u064a\u064e\u062d\u0652\u064a\u064e\u0649\u0670')
    'yaHoyaY`'
    """
    result = ""
    for char in unicode_str:
        result += _unicode_to_buckwalter[char]
    return result
