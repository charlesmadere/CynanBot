from datetime import datetime, timedelta
from jpWotd import JpWotd
import requests
import xmltodict

class WordOfTheDayRepository():
    def __init__(self):
        self.__jpWotd = None
        self.__jpCacheTime = datetime.now() - timedelta(days = 1)

    def fetchJpWotd(self):
        now = datetime.now()
        delta = now - timedelta(minutes = 30)

        if delta > self.__jpCacheTime or self.__jpWotd == None:
            self.__jpCacheTime = now
            self.__jpWotd = self.__refreshJpWotd()

        return self.__jpWotd

    def __refreshJpWotd(self):
        rawResponse = requests.get('https://wotd.transparent.com/rss/ja-widget.xml?t=0')
        xmlTree = xmltodict.parse(rawResponse.content)['xml']['words']

        word = None
        if 'word' in xmlTree:
            word = xmlTree['word'].strip()

        definition = None
        if 'translation' in xmlTree:
            definition = xmlTree['translation'].strip()

        romaji = None
        if 'wotd:transliteratedWord' in xmlTree:
            romaji = xmlTree['wotd:transliteratedWord'].strip()

        englishExample = None
        if 'enphrase' in xmlTree:
            englishExample = xmlTree['enphrase'].strip()

        foreignExample = None
        if 'fnphrase' in xmlTree:
            foreignExample = xmlTree['fnphrase'].strip()

        try:
            return JpWotd(
                word = word,
                definition = definition,
                englishExample = englishExample,
                foreignExample = foreignExample,
                romaji = romaji
            )
        except ValueError:
            print('Japanese word of the day is malformed!')
            return None
