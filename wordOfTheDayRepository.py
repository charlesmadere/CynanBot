from datetime import datetime, timedelta
from jpWord import JpWord
import requests
import xmltodict

class WordOfTheDayRepository():
    def __init__(self):
        self.__jpWord = None
        self.__jpCacheTime = datetime.now() - timedelta(days = 1)

    def fetchJpWord(self):
        now = datetime.now()
        delta = now - timedelta(minutes = 30)

        if delta > self.__jpCacheTime or self.__jpWord == None:
            self.__jpCacheTime = now
            self.__jpWord = self.__refreshJpWord()

        return self.__jpWord

    def __refreshJpWord(self):
        rawResponse = requests.get('https://wotd.transparent.com/rss/ja-widget.xml?t=0')
        xmlTree = xmltodict.parse(rawResponse.content)['xml']['words']

        word = None
        if 'word' in xmlTree:
            word = xmlTree['word']

        translation = None
        if 'translation' in xmlTree:
            translation = xmlTree['translation']

        transliteration = None
        if 'wotd:transliteratedWord' in xmlTree:
            transliteration = xmlTree['wotd:transliteratedWord']

        if word == None or len(word) == 0 or word.isspace():
            return None
        elif translation == None or len(translation) == 0 or translation.isspace():
            return None
        elif transliteration == None or len(transliteration) == 0 or transliteration.isspace():
            return None

        return JpWord(
            word = word,
            definition = translation,
            romaji = transliteration
        )
