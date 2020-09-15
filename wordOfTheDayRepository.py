from datetime import datetime, timedelta
import requests
from wotd import Wotd
import xmltodict

class WordOfTheDayRepository():
    def __init__(
        self,
        cacheTimeDelta = timedelta(hours = 1)
    ):
        self.__cacheTimeDelta = cacheTimeDelta
        self.__cacheTimes = dict()
        self.__wotds = dict()

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

        if lang in self.__wotds and lang in self.__cacheTimes:
            cacheTime = self.__cacheTimes[lang] + self.__cacheTimeDelta

            if cacheTime > datetime.now():
                return self.__wotds[lang]

        print(f'Refreshing \"{lang}\" word of the day...')

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
            print(f'Failed to fetch \"{lang}\" word of the day')

        if wotd == None:
            del self.__wotds[lang]
            del self.__cacheTimes[lang]
        else:
            self.__wotds[lang] = wotd
            self.__cacheTimes[lang] = datetime.now()

        return wotd
