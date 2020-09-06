from datetime import datetime, timedelta
import requests
from transliteratableWotd import TransliteratableWotd
from wotd import Wotd
import xmltodict

class WordOfTheDayRepository():
    def __init__(self):
        cacheTime = datetime.now() - timedelta(days = 1)

        self.__esWotd = None
        self.__esCacheTime = cacheTime
        self.__jaWotd = None
        self.__jaCacheTime = cacheTime

    def fetchEsWotd(self):
        now = datetime.now()
        delta = now - timedelta(minutes = 30)

        if delta > self.__esCacheTime or self.__esWotd == None:
            self.__esCacheTime = now
            self.__esWotd = self.__refreshEsWotd()

        return self.__esWotd

    def fetchJaWotd(self):
        now = datetime.now()
        delta = now - timedelta(minutes = 30)

        if delta > self.__jaCacheTime or self.__jaWotd == None:
            self.__jaCacheTime = now
            self.__jaWotd = self.__refreshJaWotd()

        return self.__jaWotd

    def __fetchWotdXml(self, lang: str):
        rawResponse = requests.get(f'https://wotd.transparent.com/rss/{lang}-widget.xml?t=0')
        return xmltodict.parse(rawResponse.content)['xml']['words']

    def __refreshEsWotd(self):
        xmlTree = self.__fetchWotdXml('es')

        word = None
        if 'word' in xmlTree:
            word = xmlTree['word'].strip()

        definition = None
        if 'translation' in xmlTree:
            definition = xmlTree['translation'].strip()

        englishExample = None
        if 'enphrase' in xmlTree:
            englishExample = xmlTree['enphrase'].strip()

        foreignExample = None
        if 'fnphrase' in xmlTree:
            foreignExample = xmlTree['fnphrase'].strip()

        try:
            return Wotd(
                word = word,
                definition = definition,
                englishExample = englishExample,
                foreignExample = foreignExample
            )
        except ValueError:
            print('Spanish word of the day is malformed!')
            return None

    def __refreshJaWotd(self):
        xmlTree = self.__fetchWotdXml('ja')

        word = None
        if 'word' in xmlTree:
            word = xmlTree['word'].strip()

        definition = None
        if 'translation' in xmlTree:
            definition = xmlTree['translation'].strip()

        transliteration = None
        if 'wotd:transliteratedWord' in xmlTree:
            transliteration = xmlTree['wotd:transliteratedWord'].strip()

        englishExample = None
        if 'enphrase' in xmlTree:
            englishExample = xmlTree['enphrase'].strip()

        foreignExample = None
        if 'fnphrase' in xmlTree:
            foreignExample = xmlTree['fnphrase'].strip()

        try:
            return TransliteratableWotd(
                word = word,
                definition = definition,
                englishExample = englishExample,
                foreignExample = foreignExample,
                transliteration = transliteration
            )
        except ValueError:
            print('Japanese word of the day is malformed!')
            return None
