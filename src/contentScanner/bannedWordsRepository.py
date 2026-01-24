import re
import traceback
from typing import Final, Pattern

from .absBannedWord import AbsBannedWord
from .bannedPhrase import BannedPhrase
from .bannedWord import BannedWord
from .bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from ..misc import utils as utils
from ..storage.linesReaderInterface import LinesReaderInterface
from ..timber.timberInterface import TimberInterface


class BannedWordsRepository(BannedWordsRepositoryInterface):

    def __init__(
        self,
        bannedWordsLinesReader: LinesReaderInterface,
        timber: TimberInterface,
    ):
        if not isinstance(bannedWordsLinesReader, LinesReaderInterface):
            raise TypeError(f'bannedWordsLinesReader argument is malformed: \"{bannedWordsLinesReader}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__bannedWordsLinesReader: Final[LinesReaderInterface] = bannedWordsLinesReader
        self.__timber: Final[TimberInterface] = timber

        self.__exactWordRegEx: Final[Pattern] = re.compile(r'^\"(.+)\"$', re.IGNORECASE)
        self.__cache: frozenset[AbsBannedWord] | None = None

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('BannedWordsRepository', 'Caches cleared')

    def __createCleanedBannedWordsSetFromLines(
        self,
        lines: list[str] | None,
    ) -> frozenset[AbsBannedWord]:
        if lines is not None and not isinstance(lines, list):
            raise TypeError(f'lines argument is malformed: \"{lines}\"')

        if lines is None or len(lines) == 0:
            return frozenset()

        cleanedBannedWords: set[AbsBannedWord] = set()

        for line in lines:
            bannedWord = self.__processLine(line)

            if bannedWord is not None:
                cleanedBannedWords.add(bannedWord)

        return frozenset(cleanedBannedWords)

    def __fetchBannedWords(self) -> frozenset[AbsBannedWord]:
        lines: list[str] | None = None

        try:
            lines = self.__bannedWordsLinesReader.readLines()
        except FileNotFoundError as e:
            self.__timber.log('BannedWordsRepository', f'Banned words file not found when trying to synchronously read from banned words file ({self.__bannedWordsLinesReader=})', e, traceback.format_exc())
            raise FileNotFoundError(f'Banned words file not found when trying to synchronously read from banned words file ({self.__bannedWordsLinesReader=})')

        return self.__createCleanedBannedWordsSetFromLines(lines)

    async def __fetchBannedWordsAsync(self) -> frozenset[AbsBannedWord]:
        lines: list[str] | None = None

        try:
            lines = await self.__bannedWordsLinesReader.readLinesAsync()
        except FileNotFoundError as e:
            self.__timber.log('BannedWordsRepository', f'Banned words file not found when trying to asynchronously read from banned words file ({self.__bannedWordsLinesReader=})', e, traceback.format_exc())
            raise FileNotFoundError(f'Banned words file not found when trying to asynchronously read from banned words file ({self.__bannedWordsLinesReader=})')

        return self.__createCleanedBannedWordsSetFromLines(lines)

    def getBannedWords(self) -> frozenset[AbsBannedWord]:
        cache = self.__cache
        if cache is not None:
            return cache

        bannedWords = self.__fetchBannedWords()
        self.__cache = bannedWords
        self.__timber.log('BannedWordsRepository', f'Synchronously read in {len(bannedWords)} banned word(s)')

        return bannedWords

    async def getBannedWordsAsync(self) -> frozenset[AbsBannedWord]:
        cache = self.__cache
        if cache is not None:
            return cache

        bannedWords = await self.__fetchBannedWordsAsync()
        self.__cache = bannedWords
        self.__timber.log('BannedWordsRepository', f'Asynchronously read in {len(bannedWords)} banned word(s)')

        return bannedWords

    def __processLine(self, line: str | None) -> AbsBannedWord | None:
        if line is not None and not isinstance(line, str):
            raise TypeError(f'line argument is malformed: \"{line}\"')

        if not utils.isValidStr(line):
            return None

        line = line.strip().casefold()

        if not utils.isValidStr(line):
            return None

        exactWordMatch = self.__exactWordRegEx.fullmatch(line)
        exactWord: str | None = None

        if exactWordMatch is not None:
            exactWord = exactWordMatch.group(1)

        if utils.isValidStr(exactWord):
            return BannedWord(exactWord.casefold())
        else:
            return BannedPhrase(line.casefold())
