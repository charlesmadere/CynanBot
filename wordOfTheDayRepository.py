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
        self.__frWotd = None
        self.__frCacheTime = cacheTime
        self.__jaWotd = None
        self.__jaCacheTime = cacheTime
        self.__zhWotd = None
        self.__zhCacheTime = cacheTime

    def fetchEsWotd(self):
        now = datetime.now()
        delta = now - timedelta(minutes = 30)

        if delta > self.__esCacheTime or self.__esWotd == None:
            self.__esCacheTime = now
            self.__esWotd = self.__refreshEsWotd()

        return self.__esWotd

    def fetchFrWotd(self):
        now = datetime.now()
        delta = now - timedelta(minutes = 30)

        if delta > self.__frCacheTime or self.__frWotd == None:
            self.__frCacheTime = now
            self.__frWotd = self.__refreshFrWotd()

        return self.__frWotd

    def fetchJaWotd(self):
        now = datetime.now()
        delta = now - timedelta(minutes = 30)

        if delta > self.__jaCacheTime or self.__jaWotd == None:
            self.__jaCacheTime = now
            self.__jaWotd = self.__refreshJaWotd()

        return self.__jaWotd

    def fetchZhWotd(self):
        now = datetime.now()
        delta = now - timedelta(minutes = 30)

        if delta > self.__zhCacheTime or self.__zhWotd == None:
            self.__zhCacheTime = now
            self.__zhWotd = self.__refreshZhWotd()

        return self.__zhWotd

    def __fetchWotdXml(self, lang: str):
        rawResponse = requests.get(f'https://wotd.transparent.com/rss/{lang}-widget.xml?t=0')
        return xmltodict.parse(rawResponse.content)['xml']['words']

    def __refreshEsWotd(self):
        print('Refreshing Spanish (ES) WOTD...')
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

    def __refreshFrWotd(self):
        print('Refreshing French (FR) WOTD...')
        xmlTree = self.__fetchWotdXml('fr')

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
            print('French (FR) word of the day is malformed!')
            return None

    def __refreshJaWotd(self):
        print('Refreshing Japanese (JA) WOTD...')
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

    def __refreshZhWotd(self):
        print('Refreshing Mandarin Chinese (ZH) WOTD...')
        xmlTree = self.__fetchWotdXml('zh')

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
            print('Mandarin Chinese word of the day is malformed!')
            return None
