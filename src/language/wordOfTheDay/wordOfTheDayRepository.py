import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final

from .wordOfTheDayRepositoryInterface import WordOfTheDayRepositoryInterface
from .wordOfTheDayResponse import WordOfTheDayResponse
from ..exceptions import WordOfTheDayHasBadContentException
from ..languageEntry import LanguageEntry
from ..romaji import to_romaji
from ...contentScanner.contentCode import ContentCode
from ...contentScanner.contentScannerInterface import ContentScannerInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface
from ...transparent.transparentApiServiceInterface import TransparentApiServiceInterface
from ...transparent.transparentResponse import TransparentResponse


class WordOfTheDayRepository(WordOfTheDayRepositoryInterface):

    @dataclass(frozen = True, slots = True)
    class Entry:
        fetchDateTime: datetime
        languageEntry: LanguageEntry
        wordOfTheDayResponse: WordOfTheDayResponse

    def __init__(
        self,
        contentScanner: ContentScannerInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        transparentApiService: TransparentApiServiceInterface,
        cacheTimeToLive: timedelta = timedelta(minutes = 30),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(transparentApiService, TransparentApiServiceInterface):
            raise TypeError(f'transparentApiService argument is malformed: \"{transparentApiService}\"')
        elif not isinstance(cacheTimeToLive, timedelta):
            raise TypeError(f'cacheTimeToLive argument is malformed: \"{cacheTimeToLive}\"')

        self.__contentScanner: Final[ContentScannerInterface] = contentScanner
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__transparentApiService: Final[TransparentApiServiceInterface] = transparentApiService
        self.__cacheTimeToLive: Final[timedelta] = cacheTimeToLive

        self.__cache: Final[dict[LanguageEntry, WordOfTheDayRepository.Entry | None]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('WordOfTheDayRepository', 'Caches cleared')

    async def fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        if not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')
        elif not utils.isValidStr(languageEntry.wotdApiCode):
            raise ValueError(f'languageEntry argument is not supported for Word Of The Day: ({languageEntry=})')

        cachedValue = self.__cache.get(languageEntry, None)

        if cachedValue is not None:
            now = datetime.now(self.__timeZoneRepository.getDefault())

            if cachedValue.fetchDateTime + self.__cacheTimeToLive >= now:
                return cachedValue.wordOfTheDayResponse

        wordOfTheDayResponse = await self.__fetchWotd(
            languageEntry = languageEntry,
        )

        self.__cache[languageEntry] = WordOfTheDayRepository.Entry(
            fetchDateTime = datetime.now(self.__timeZoneRepository.getDefault()),
            languageEntry = languageEntry,
            wordOfTheDayResponse = wordOfTheDayResponse,
        )

        return wordOfTheDayResponse

    async def __fetchWotd(self, languageEntry: LanguageEntry) -> WordOfTheDayResponse:
        if not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')
        elif not utils.isValidStr(languageEntry.wotdApiCode):
            raise ValueError(f'languageEntry argument is not supported for Word Of The Day: ({languageEntry=})')

        self.__timber.log('WordOfTheDayRepository', f'Fetching Word Of The Day... ({languageEntry=})')

        try:
            transparentResponse = await self.__transparentApiService.fetchWordOfTheDay(
                targetLanguage = languageEntry,
            )
        except GenericNetworkException as e:
            self.__timber.log('WordOfTheDayRepository', f'Encountered network error when fetching Word Of The Day ({languageEntry=})', e, traceback.format_exc())
            raise GenericNetworkException(f'Encountered network error when fetching Word Of The Day ({languageEntry=}): {e}')

        await self.__verifyWotdContent(
            languageEntry = languageEntry,
            transparentResponse = transparentResponse,
        )

        romaji: str | None = None
        if languageEntry is LanguageEntry.JAPANESE:
            romaji = to_romaji(transparentResponse.transliteratedWord)

        return WordOfTheDayResponse(
            languageEntry = languageEntry,
            romaji = romaji,
            transparentResponse = transparentResponse,
        )

    async def __verifyWotdContent(
        self,
        languageEntry: LanguageEntry,
        transparentResponse: TransparentResponse,
    ):
        fnPhraseContentCode = await self.__contentScanner.scan(transparentResponse.fnPhrase)
        enPhraseContentCode = await self.__contentScanner.scan(transparentResponse.enPhrase)
        translationContentCode = await self.__contentScanner.scan(transparentResponse.translation)
        wordContentCode = await self.__contentScanner.scan(transparentResponse.word)

        contentCodes: frozenset[ContentCode] = frozenset({
            fnPhraseContentCode,
            enPhraseContentCode,
            translationContentCode,
            wordContentCode,
        })

        if ContentCode.CONTAINS_BANNED_CONTENT in contentCodes or ContentCode.CONTAINS_URL in contentCodes:
            raise WordOfTheDayHasBadContentException(
                contentCodes = contentCodes,
                languageEntry = languageEntry,
                transparentResponse = transparentResponse,
            )
