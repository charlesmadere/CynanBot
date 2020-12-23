from datetime import timedelta
from typing import List

import requests
import xmltodict

import utils
from timedDict import TimedDict


class WordOfTheDayRepository():

    def __init__(
        self,
        cacheTimeDelta=timedelta(hours=1)
    ):
        if cacheTimeDelta is None:
            raise ValueError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__cache = TimedDict(timeDelta=cacheTimeDelta)
        self.__languageList = self.__createLanguageList()

    def __createLanguageList(self):
        entries = list()
        entries.append(LanguageEntry(apiName='de', commandName='de'))
        entries.append(LanguageEntry(apiName='en-es', commandName='en-es'))
        entries.append(LanguageEntry(apiName='en-pt', commandName='en-pt'))
        entries.append(LanguageEntry(apiName='es', commandName='es'))
        entries.append(LanguageEntry(apiName='fr', commandName='fr'))
        entries.append(LanguageEntry(apiName='it', commandName='it'))
        entries.append(LanguageEntry(apiName='ja', commandName='ja'))
        entries.append(LanguageEntry(apiName='korean', commandName='ko'))
        entries.append(LanguageEntry(apiName='nl', commandName='nl'))
        entries.append(LanguageEntry(apiName='norwegian', commandName='no'))
        entries.append(LanguageEntry(apiName='polish', commandName='po'))
        entries.append(LanguageEntry(apiName='pt', commandName='pt'))
        entries.append(LanguageEntry(apiName='ru', commandName='ru'))
        entries.append(LanguageEntry(apiName='swedish', commandName='sv'))
        entries.append(LanguageEntry(apiName='zh', commandName='zh'))

        return LanguageList(entries=entries)

    def fetchWotd(self, languageEntry):
        if languageEntry is None:
            raise ValueError(f'languageEntry argument is malformed: \"{languageEntry}\"')

        cacheValue = self.__cache[languageEntry]

        if cacheValue is not None:
            return cacheValue

        print(f'Refreshing word of the day for \"{languageEntry.getCommandName()}\"...')

        ##############################################################################
        # retrieve word of the day from https://www.transparent.com/word-of-the-day/ #
        ##############################################################################

        rawResponse = requests.get(
            f'https://wotd.transparent.com/rss/{languageEntry.getApiName()}-widget.xml?t=0')
        xmlTree = xmltodict.parse(rawResponse.content)['xml']['words']

        if xmlTree is None:
            print(f'xmlTree for \"{languageEntry.getCommandName()}\" is malformed: \"{xmlTree}\"')
            return None
        elif len(xmlTree) == 0:
            print(f'xmlTree for \"{languageEntry.getCommandName()}\" is empty: \"{xmlTree}\"')
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
                word=word,
                definition=definition,
                englishExample=englishExample,
                language=language,
                foreignExample=foreignExample,
                transliteration=transliteration
            )
        except ValueError:
            print(f'Word Of The Day for \"{languageEntry.getCommandName()}\" has a data error')

        if wotd is None:
            del self.__cache[languageEntry]
        else:
            self.__cache[languageEntry] = wotd

        return wotd

    def getLanguageList(self):
        return self.__languageList


class LanguageEntry():

    def __init__(self, apiName: str, commandName: str):
        if not utils.isValidStr(apiName):
            raise ValueError(f'apiName argument is malformed: \"{apiName}\"')
        elif not utils.isValidStr(commandName):
            raise ValueError(f'commandName argument is malformed: \"{commandName}\"')

        self.__apiName = apiName
        self.__commandName = commandName

    def getApiName(self):
        return self.__apiName

    def getCommandName(self):
        return self.__commandName


class LanguageList():

    def __init__(self, entries: List):
        if entries is None or len(entries) == 0:
            raise ValueError(f'entries argument is malformed: \"{entries}\"')

        self.__entries = entries

    def getLanguages(self):
        return self.__entries

    def getLanguageForCommand(self, command: str):
        if not utils.isValidStr(command):
            raise ValueError(f'command argument is malformed: \"{command}\"')

        for entry in self.__entries:
            if command.lower() == entry.getCommandName().lower():
                return entry

        raise RuntimeError(f'Unable to find language for \"{command}\"')

    def toApiNameStr(self, delimiter: str = ', '):
        if delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        apiNames = list()

        for entry in self.__entries:
            apiNames.append(entry.getApiName())

        apiNames.sort()
        return delimiter.join(apiNames)

    def toCommandNameStr(self, delimiter: str = ', '):
        if delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        commandNames = list()

        for entry in self.__entries:
            commandNames.append(entry.getCommandName())

        commandNames.sort()
        return delimiter.join(commandNames)


class Wotd():

    def __init__(
        self,
        definition: str,
        englishExample: str,
        foreignExample: str,
        language: str,
        transliteration: str,
        word: str
    ):
        if not utils.isValidStr(definition):
            raise ValueError(f'definition argument is malformed: \"{definition}\"')
        elif not utils.isValidStr(language):
            raise ValueError(f'language argument is malformed: \"{language}\"')
        elif not utils.isValidStr(word):
            raise ValueError(f'word argument is malformed: \"{word}\"')

        self.__definition = definition
        self.__englishExample = englishExample
        self.__foreignExample = foreignExample
        self.__language = language
        self.__transliteration = transliteration
        self.__word = word

    def getDefinition(self):
        return self.__definition

    def getEnglishExample(self):
        return self.__englishExample

    def getForeignExample(self):
        return self.__foreignExample

    def getLanguage(self):
        return self.__language

    def getTransliteration(self):
        return self.__transliteration

    def getWord(self):
        return self.__word

    def hasExamples(self):
        return utils.isValidStr(self.__englishExample) and utils.isValidStr(self.__foreignExample)

    def hasTransliteration(self):
        return utils.isValidStr(self.__transliteration)

    def toStr(self):
        if self.hasExamples():
            if self.hasTransliteration():
                return f'({self.getLanguage()}) {self.getWord()} ({self.getTransliteration()}) — {self.getDefinition()}. Example: {self.getForeignExample()} {self.getEnglishExample()}'
            else:
                return f'({self.getLanguage()}) {self.getWord()} — {self.getDefinition()}. Example: {self.getForeignExample()} {self.getEnglishExample()}'
        elif self.hasTransliteration():
            return f'({self.getLanguage()}) {self.getWord()} ({self.getTransliteration()}) — {self.getDefinition()}'
        else:
            return f'({self.getLanguage()}) {self.getWord()} — {self.getDefinition()}'
