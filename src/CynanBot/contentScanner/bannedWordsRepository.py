import re
import traceback
from typing import List, Optional, Pattern, Set

import misc.utils as utils
from contentScanner.absBannedWord import AbsBannedWord
from contentScanner.bannedPhrase import BannedPhrase
from contentScanner.bannedWord import BannedWord
from contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from storage.linesReaderInterface import LinesReaderInterface
from timber.timberInterface import TimberInterface


class BannedWordsRepository(BannedWordsRepositoryInterface):

    def __init__(
        self,
        bannedWordsLinesReader: LinesReaderInterface,
        timber: TimberInterface
    ):
        if not isinstance(bannedWordsLinesReader, LinesReaderInterface):
            raise ValueError(f'bannedWordsLinesReader argument is malformed: \"{bannedWordsLinesReader}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__bannedWordsLinesReader: LinesReaderInterface = bannedWordsLinesReader
        self.__timber: TimberInterface = timber

        self.__exactWordRegEx: Pattern = re.compile(r'^\"(.+)\"$', re.IGNORECASE)
        self.__cache: Optional[Set[BannedWord]] = None

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('BannedWordsRepository', 'Caches cleared')

    def __createCleanedBannedWordsSetFromLines(
        self,
        lines: Optional[List[Optional[str]]]
    ) -> Set[AbsBannedWord]:
        cleanedBannedWords: Set[AbsBannedWord] = set()

        if not utils.hasItems(lines):
            return cleanedBannedWords

        for line in lines:
            bannedWord = self.__processLine(line)

            if bannedWord is not None:
                cleanedBannedWords.add(bannedWord)

        return cleanedBannedWords

    def __fetchBannedWords(self) -> Set[AbsBannedWord]:
        lines: Optional[List[Optional[str]]] = None

        try:
            lines = self.__bannedWordsLinesReader.readLines()
        except FileNotFoundError as e:
            self.__timber.log('BannedWordsRepository', f'Banned words file not found when trying to synchronously read from banned words file', e, traceback.format_exc())
            raise FileNotFoundError('Banned words file not found when trying to synchronously read from banned words file')

        return self.__createCleanedBannedWordsSetFromLines(lines)

    async def __fetchBannedWordsAsync(self) -> Set[AbsBannedWord]:
        lines: Optional[List[Optional[str]]] = None

        try:
            lines = await self.__bannedWordsLinesReader.readLinesAsync()
        except FileNotFoundError as e:
            self.__timber.log('BannedWordsRepository', 'Banned words file not found when trying to asynchronously read from banned words file', e, traceback.format_exc())
            raise FileNotFoundError('Banned words file not found when trying to asynchronously read from banned words file')

        return self.__createCleanedBannedWordsSetFromLines(lines)

    def getBannedWords(self) -> Set[AbsBannedWord]:
        if self.__cache is not None:
            return self.__cache

        bannedWords = self.__fetchBannedWords()
        self.__cache = bannedWords
        self.__timber.log('BannedWordsRepository', f'Synchronously read in {len(bannedWords)} banned word(s)')

        return bannedWords

    async def getBannedWordsAsync(self) -> Set[AbsBannedWord]:
        if self.__cache is not None:
            return self.__cache

        bannedWords = await self.__fetchBannedWordsAsync()
        self.__cache = bannedWords
        self.__timber.log('BannedWordsRepository', f'Asynchronously read in {len(bannedWords)} banned word(s)')

        return bannedWords

    def __processLine(self, line: Optional[str]) -> Optional[AbsBannedWord]:
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
