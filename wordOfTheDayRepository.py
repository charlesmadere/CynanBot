from datetime import timedelta

import requests
import xmltodict

from timedDict import TimedDict
from wotd import Wotd


class WordOfTheDayRepository():

    def __init__(
        self,
        cacheTimeDelta = timedelta(hours = 1)
    ):
        if cacheTimeDelta == None:
            raise ValueError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__cache = TimedDict(timeDelta = cacheTimeDelta)

    def fetchDeWotd(self):
        return self.__fetchWotd('de')

    def fetchEnEsWotd(self):
        return self.__fetchWotd('en-es')

    def fetchEnPtWotd(self):
        return self.__fetchWotd('en-pt')

    def fetchEsWotd(self):
        return self.__fetchWotd('es')

    def fetchFrWotd(self):
        return self.__fetchWotd('fr')

    def fetchItWotd(self):
        return self.__fetchWotd('it')

    def fetchJaWotd(self):
        return self.__fetchWotd('ja')

    def fetchKoWotd(self):
        return self.__fetchWotd('korean')

    def fetchNoWotd(self):
        return self.__fetchWotd('norwegian')

    def fetchPtWotd(self):
        return self.__fetchWotd('pt')

    def fetchRuWotd(self):
        return self.__fetchWotd('ru')

    def fetchSvWotd(self):
        return self.__fetchWotd('swedish')

    def fetchZhWotd(self):
        return self.__fetchWotd('zh')

    def __fetchWotd(self, lang: str):
        if lang == None or len(lang) == 0 or lang.isspace():
            raise ValueError(f'lang argument is malformed: \"{lang}\"')

        cacheValue = self.__cache[lang]

        if cacheValue != None:
            return cacheValue

        print(f'Refreshing word of the day for \"{lang}\"...')

        ##############################################################################
        # retrieve word of the day from https://www.transparent.com/word-of-the-day/ #
        ##############################################################################

        rawResponse = requests.get(f'https://wotd.transparent.com/rss/{lang}-widget.xml?t=0')
        xmlTree = xmltodict.parse(rawResponse.content)['xml']['words']

        if xmlTree == None:
            print(f'xmlTree for \"{lang}\" is malformed: \"{xmlTree}\"')
            return None
        elif len(xmlTree) == 0:
            print(f'xmlTree for \"{lang}\" is empty: \"{xmlTree}\"')
            return None

        word = xmlTree.get('word')
        definition = xmlTree.get('translation')
        englishExample = xmlTree.get('enphrase')
        foreignExample = xmlTree.get('fnphrase')
        language = xmlTree.get('langname')
        transliteration = xmlTree.get('wotd:transliteratedWord')

        wotd = None

        try:
            wotd = Wotd(
                word = word,
                definition = definition,
                englishExample = englishExample,
                language = language,
                foreignExample = foreignExample,
                transliteration = transliteration
            )
        except ValueError:
            print(f'Word Of The Day for \"{lang}\" has a data error')

        if wotd == None:
            del self.__cache[lang]
        else:
            self.__cache[lang] = wotd

        return wotd
