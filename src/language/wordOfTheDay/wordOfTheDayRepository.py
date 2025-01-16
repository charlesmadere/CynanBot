import traceback
from datetime import timedelta

from .wordOfTheDayRepositoryInterface import WordOfTheDayRepositoryInterface
from .wordOfTheDayResponse import WordOfTheDayResponse
from ..languageEntry import LanguageEntry
from ..romaji import to_romaji
from ...misc import utils as utils
from ...misc.timedDict import TimedDict
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface
from ...transparent.transparentApiServiceInterface import TransparentApiServiceInterface


class WordOfTheDayRepository(WordOfTheDayRepositoryInterface):

    def __init__(
        self,
        timber: TimberInterface,
        transparentApiService: TransparentApiServiceInterface,
        cacheTimeDelta: timedelta = timedelta(hours = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(transparentApiService, TransparentApiServiceInterface):
            raise TypeError(f'transparentApiService argument is malformed: \"{transparentApiService}\"')
        elif not isinstance(cacheTimeDelta, timedelta):
            raise TypeError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__timber: TimberInterface = timber
        self.__transparentApiService: TransparentApiServiceInterface = transparentApiService
        self.__cache: TimedDict[WordOfTheDayResponse] = TimedDict(cacheTimeDelta)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('WordOfTheDayRepository', 'Caches cleared')

    async def fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        if not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')
        elif not utils.isValidStr(languageEntry.wotdApiCode):
            raise ValueError(f'languageEntry argument is not supported for Word Of The Day: ({languageEntry=})')

        cacheValue = self.__cache[languageEntry.name.casefold()]
        if cacheValue is not None:
            return cacheValue

        wotd = await self.__fetchWotd(languageEntry)
        self.__cache[languageEntry.name.casefold()] = wotd

        return wotd

    async def __fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        if not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')
        elif not utils.isValidStr(languageEntry.wotdApiCode):
            raise ValueError(f'languageEntry argument is not supported for Word Of The Day: ({languageEntry=})')

        self.__timber.log('WordOfTheDayRepository', f'Fetching Word Of The Day... ({languageEntry=})')

        try:
            transparentResponse = await self.__transparentApiService.fetchWordOfTheDay(languageEntry)
        except GenericNetworkException as e:
            self.__timber.log('WordOfTheDayRepository', f'Encountered network error when fetching Word Of The Day ({languageEntry=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'Encountered network error when fetching Word Of The Day ({languageEntry=}): {e}')

        romaji: str | None = None
        if languageEntry.wotdApiCode == 'ja':
            romaji = to_romaji(transparentResponse.transliteratedWord)

        return WordOfTheDayResponse(
            languageEntry = languageEntry,
            romaji = romaji,
            transparentResponse = transparentResponse
        )
