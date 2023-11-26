import pytest

from CynanBot.contentScanner.bannedPhrase import BannedPhrase
from CynanBot.contentScanner.bannedWord import BannedWord
from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.storage.linesReaderInterface import LinesReaderInterface
from CynanBot.storage.linesStaticReader import LinesStaticReader
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestBannedWordsRepository():

    timber: TimberInterface = TimberStub()

    bannedWordsLinesReader: LinesReaderInterface = LinesStaticReader(
        lines = [ 'Hello', 'WORLD', '"QAnon"', 'world' ]
    )

    emptyBannedWordsLinesReader: LinesReaderInterface = LinesStaticReader(
        lines = None
    )

    def test_getBannedWords(self):
        bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
            bannedWordsLinesReader = self.bannedWordsLinesReader,
            timber = self.timber
        )

        bannedWords = bannedWordsRepository.getBannedWords()
        assert len(bannedWords) == 3

        assert BannedPhrase('hello') in bannedWords
        assert BannedPhrase('world') in bannedWords
        assert BannedWord('qanon') in bannedWords

    @pytest.mark.asyncio
    async def test_getBannedWordsAsync(self):
        bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
            bannedWordsLinesReader = self.bannedWordsLinesReader,
            timber = self.timber
        )

        bannedWords = await bannedWordsRepository.getBannedWordsAsync()
        assert len(bannedWords) == 3

        assert BannedPhrase('hello') in bannedWords
        assert BannedPhrase('world') in bannedWords
        assert BannedWord('qanon') in bannedWords

    def test_getBannedWords_withEmptyBannedWordsLinesReader(self):
        bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
            bannedWordsLinesReader = self.emptyBannedWordsLinesReader,
            timber = self.timber
        )

        bannedWords = bannedWordsRepository.getBannedWords()
        assert len(bannedWords) == 0

    @pytest.mark.asyncio
    async def test_getBannedWordsAsync_withEmptyBannedWordsLinesReader(self):
        bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
            bannedWordsLinesReader = self.emptyBannedWordsLinesReader,
            timber = self.timber
        )

        bannedWords = await bannedWordsRepository.getBannedWordsAsync()
        assert len(bannedWords) == 0
