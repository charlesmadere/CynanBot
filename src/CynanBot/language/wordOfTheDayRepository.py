import traceback
from datetime import timedelta
from typing import Any, Dict

import xmltodict

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.wordOfTheDayRepositoryInterface import \
    WordOfTheDayRepositoryInterface
from CynanBot.language.wordOfTheDayResponse import WordOfTheDayResponse
from CynanBot.misc.timedDict import TimedDict
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface


class WordOfTheDayRepository(WordOfTheDayRepositoryInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        cacheTimeDelta: timedelta = timedelta(hours = 1)
    ):
        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(cacheTimeDelta, timedelta), f"malformed {cacheTimeDelta=}"

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__cache: TimedDict = TimedDict(cacheTimeDelta)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('WordOfTheDayRepository', 'Caches cleared')

    async def fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        assert isinstance(languageEntry, LanguageEntry), f"malformed {languageEntry=}"
        if not languageEntry.hasWotdApiCode():
            raise ValueError(f'the given languageEntry is not supported for Word Of The Day: \"{languageEntry.getName()}\"')

        cacheValue = self.__cache[languageEntry.getName()]
        if cacheValue is not None:
            return cacheValue

        wotd = await self.__fetchWotd(languageEntry)
        self.__cache[languageEntry.getName()] = wotd

        return wotd

    async def __fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        assert isinstance(languageEntry, LanguageEntry), f"malformed {languageEntry=}"
        if not languageEntry.hasWotdApiCode():
            raise ValueError(f'the given languageEntry is not supported for Word Of The Day: \"{languageEntry.getName()}\"')

        self.__timber.log('WordOfTheDayRepository', f'Fetching Word Of The Day for \"{languageEntry.getName()}\" ({languageEntry.getWotdApiCode()})...')
        clientSession = await self.__networkClientProvider.get()

        ##############################################################################
        # retrieve word of the day from https://www.transparent.com/word-of-the-day/ #
        ##############################################################################

        try:
            response = await clientSession.get(f'https://wotd.transparent.com/rss/{languageEntry.requireWotdApiCode()}-widget.xml?t=0')
        except GenericNetworkException as e:
            self.__timber.log('WordOfTheDayRepository', f'Encountered network error when fetching Word Of The Day for \"{languageEntry.getName()}\": {e}', e, traceback.format_exc())
            raise RuntimeError(f'Encountered network error when fetching Word Of The Day for \"{languageEntry.getName()}\": {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('WordOfTheDayRepository', f'Encountered non-200 HTTP status code when fetching Word Of The Day for \"{languageEntry.getName()}\" ({languageEntry.getWotdApiCode()}): {response.getStatusCode()}')
            raise RuntimeError(f'Encountered non-200 HTTP status code when fetching Word Of The Day for \"{languageEntry.getName()}\" ({languageEntry.getWotdApiCode()}): {response.getStatusCode()}')

        xmlTree = xmltodict.parse(await response.read())
        await response.close()

        if not utils.hasItems(xmlTree):
            self.__timber.log('WordOfTheDayRepository', f'xmlTree for \"{languageEntry.getName()}\" is malformed: {xmlTree}')
            raise RuntimeError(f'xmlTree for \"{languageEntry.getName()}\" is malformed: {xmlTree}')

        wordsTree: Dict[str, Any] = xmlTree['xml']['words']
        word = utils.getStrFromDict(wordsTree, 'word', clean = True)
        definition = utils.getStrFromDict(wordsTree, 'translation', clean = True)
        englishExample = utils.getStrFromDict(wordsTree, 'enphrase', fallback = '', clean = True)
        foreignExample = utils.getStrFromDict(wordsTree, 'fnphrase', fallback = '', clean = True)
        transliteration = utils.getStrFromDict(wordsTree, 'wotd:transliteratedWord', fallback = '', clean = True)

        return WordOfTheDayResponse(
            languageEntry = languageEntry,
            word = word,
            definition = definition,
            englishExample = englishExample,
            foreignExample = foreignExample,
            transliteration = transliteration
        )
