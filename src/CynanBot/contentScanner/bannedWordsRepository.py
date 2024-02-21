import re
import traceback
from typing import List, Optional, Pattern, Set

import CynanBot.misc.utils as utils
from CynanBot.contentScanner.absBannedWord import AbsBannedWord
from CynanBot.contentScanner.bannedPhrase import BannedPhrase
from CynanBot.contentScanner.bannedWord import BannedWord
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.storage.linesReaderInterface import LinesReaderInterface
from CynanBot.timber.timberInterface import TimberInterface


class BannedWordsRepository(BannedWordsRepositoryInterface):

    def __init__(
        self,
        bannedWordsLinesReader: LinesReaderInterface,
        timber: TimberInterface
    ):
        assert isinstance(bannedWordsLinesReader, LinesReaderInterface), f"malformed {bannedWordsLinesReader=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__bannedWordsLinesReader: LinesReaderInterface = bannedWordsLinesReader
        self.__timber: TimberInterface = timber

        self.__exactWordRegEx: Pattern = re.compile(r'^\"(.+)\"$', re.IGNORECASE)
        self.__cache: Optional[Set[AbsBannedWord]] = None

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('BannedWordsRepository', 'Caches cleared')

    def __createCleanedBannedWordsSetFromLines(
        self,
        lines: Optional[List[str]]
    ) -> Set[AbsBannedWord]:
        assert lines is None or isinstance(lines, List), f"malformed {lines=}"

        cleanedBannedWords: Set[AbsBannedWord] = set()

        if lines is None or len(lines) == 0:
            return cleanedBannedWords

        for line in lines:
            bannedWord = self.__processLine(line)

            if bannedWord is not None:
                cleanedBannedWords.add(bannedWord)

        return cleanedBannedWords

    def __fetchBannedWords(self) -> Set[AbsBannedWord]:
        lines: Optional[List[str]] = None

        try:
            lines = self.__bannedWordsLinesReader.readLines()
        except FileNotFoundError as e:
            self.__timber.log('BannedWordsRepository', f'Banned words file not found when trying to synchronously read from banned words file ({self.__bannedWordsLinesReader=})', e, traceback.format_exc())
            raise FileNotFoundError(f'Banned words file not found when trying to synchronously read from banned words file ({self.__bannedWordsLinesReader=})')

        return self.__createCleanedBannedWordsSetFromLines(lines)

    async def __fetchBannedWordsAsync(self) -> Set[AbsBannedWord]:
        lines: Optional[List[str]] = None

        try:
            lines = await self.__bannedWordsLinesReader.readLinesAsync()
        except FileNotFoundError as e:
            self.__timber.log('BannedWordsRepository', f'Banned words file not found when trying to asynchronously read from banned words file ({self.__bannedWordsLinesReader=})', e, traceback.format_exc())
            raise FileNotFoundError(f'Banned words file not found when trying to asynchronously read from banned words file ({self.__bannedWordsLinesReader=})')

        return self.__createCleanedBannedWordsSetFromLines(lines)

    def getBannedWords(self) -> Set[AbsBannedWord]:
        cache = self.__cache
        if cache is not None:
            return cache

        bannedWords = self.__fetchBannedWords()
        self.__cache = bannedWords
        self.__timber.log('BannedWordsRepository', f'Synchronously read in {len(bannedWords)} banned word(s)')

        return bannedWords

    async def getBannedWordsAsync(self) -> Set[AbsBannedWord]:
        cache = self.__cache
        if cache is not None:
            return cache

        bannedWords = await self.__fetchBannedWordsAsync()
        self.__cache = bannedWords
        self.__timber.log('BannedWordsRepository', f'Asynchronously read in {len(bannedWords)} banned word(s)')

        return bannedWords

    def __processLine(self, line: Optional[str]) -> Optional[AbsBannedWord]:
        assert line is None or isinstance(line, str), f"malformed {line=}"

        if not utils.isValidStr(line):
            return None

        line = line.strip().lower()

        if not utils.isValidStr(line):
            return None

        exactWordMatch = self.__exactWordRegEx.fullmatch(line)

        if exactWordMatch is not None and utils.isValidStr(exactWordMatch.group(1)):
            return BannedWord(exactWordMatch.group(1))
        else:
            return BannedPhrase(line)
